#!/usr/bin/env node
// Usage: node scripts/build-reel.mjs <name>
// Reads videos/<name>/edit.json (+ transcript.json) and writes videos/<name>/index.html
// using the shared look in kit/. Re-run it after every change to edit.json.
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const name = process.argv[2];
if (!name) {
  console.error("usage: node scripts/build-reel.mjs <name>");
  process.exit(1);
}
const dir = path.join(root, "videos", name);
const kit = path.join(root, "kit");
const edit = JSON.parse(fs.readFileSync(path.join(dir, "edit.json"), "utf8"));
const transcriptPath = path.join(dir, edit.transcript || "transcript.json");
const words = fs.existsSync(transcriptPath) ? JSON.parse(fs.readFileSync(transcriptPath, "utf8")) : [];

const FPS = edit.fps || 30;
const q = (t) => Math.round(t * FPS) / FPS;
const DUR = q(edit.duration);
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
// ==phrase== in any text becomes a yellow marker highlight
const rich = (s) => esc(s).replace(/==(.+?)==/g, '<span class="mark"><span class="mark-bg"></span>$1</span>');

// ---------- copy kit assets into the project ----------
fs.mkdirSync(path.join(dir, "assets", "fonts"), { recursive: true });
fs.mkdirSync(path.join(dir, "assets", "sfx"), { recursive: true });
fs.mkdirSync(path.join(dir, "assets", "vendor"), { recursive: true });
for (const f of fs.readdirSync(path.join(kit, "fonts"))) fs.copyFileSync(path.join(kit, "fonts", f), path.join(dir, "assets", "fonts", f));
for (const f of fs.readdirSync(path.join(kit, "sfx"))) fs.copyFileSync(path.join(kit, "sfx", f), path.join(dir, "assets", "sfx", f));
fs.copyFileSync(path.join(root, "node_modules", "gsap", "dist", "gsap.min.js"), path.join(dir, "assets", "vendor", "gsap.min.js"));

// ---------- captions ----------
const capCfg = { maxWords: 3, maxChars: 16, ...(edit.captions || {}) };
const norm = (w) => w.toLowerCase().replace(/[^a-z0-9₹%]/g, "");
const hot = new Set((capCfg.hot || []).map(norm));
const groups = [];
let cur = null;
words.forEach((w, i) => {
  const text = w.text.trim();
  if (!text) return;
  const prev = words[i - 1];
  const breakHere =
    !cur ||
    cur.words.length >= capCfg.maxWords ||
    cur.chars + text.length > capCfg.maxChars ||
    (prev && w.start - prev.end > 0.35) ||
    (prev && /[.,?!;:]$/.test(prev.text.trim()));
  if (breakHere) {
    cur = { words: [], chars: 0 };
    groups.push(cur);
  }
  cur.words.push({ text, start: w.start, end: w.end });
  cur.chars += text.length + 1;
});
groups.forEach((g, i) => {
  g.start = q(g.words[0].start);
  const lastEnd = g.words[g.words.length - 1].end;
  const next = groups[i + 1];
  g.end = q(next && next.words[0].start - lastEnd < 0.6 ? next.words[0].start : Math.min(lastEnd + 0.3, DUR));
});
const capsOff = (edit.captions && edit.captions.off) || []; // [[from,to], ...] ranges with no captions
const visibleGroups = capCfg.enabled === false ? [] : groups.filter((g) => !capsOff.some(([a, b]) => g.start >= a && g.start < b));
const captionsHtml = visibleGroups
  .map(
    (g) =>
      `<div class="cap-group" data-gs="${g.start}" data-ge="${g.end}">` +
      g.words
        .map((w) => `<span class="w${hot.has(norm(w.text)) ? " hot" : ""}" data-ws="${q(w.start)}" data-we="${q(w.end)}">${esc(w.text.replace(/[.,;:]$/, ""))}</span>`)
        .join("") +
      `</div>`,
  )
  .join("\n        ");

// ---------- cards ----------
const map = JSON.parse(fs.readFileSync(path.join(kit, "india-map.json"), "utf8"));
const stateName = Object.fromEntries(map.states.map((s) => [s.id, s.name]));
const PAPER_TYPES = new Set(["headline", "stat", "map", "timeline", "term", "compare"]);
const cards = (edit.cards || []).map((c, i) => ({ ...c, id: `card-${String(i + 1).padStart(2, "0")}`, start: q(c.start), end: q(c.end) }));

function cardInner(c) {
  switch (c.type) {
    case "hook":
      return `<div class="hook">${c.kicker ? `<div><span class="kicker">${esc(c.kicker)}</span></div>` : ""}<div><span class="hook-title">${rich(c.title)}</span></div></div>`;
    case "keyword":
      return `<div class="kw">${(c.lines || [c.text])
        .map((l) => `<div class="kw-line"><div class="kw-bg"></div><div class="kw-text">${esc(l)}</div></div>`)
        .join("")}${c.sub ? `<div class="kw-line kw-sub"><div class="kw-bg"></div><div class="kw-text">${esc(c.sub)}</div></div>` : ""}</div>`;
    case "headline":
      return `<div class="slot"><div class="clipping"><div class="clip-mast"><span class="src">${esc(c.source || "The Daily Brief")}</span><span class="date">${esc(c.date || "")}</span></div><h2 class="clip-head">${rich(c.title)}</h2>${c.sub ? `<p class="clip-sub">${rich(c.sub)}</p>` : ""}</div></div>`;
    case "stat":
      return `<div class="slot"><div class="stat"><div class="stat-num">${c.prefix ? `<span class="pre">${esc(c.prefix)}</span>` : ""}<span class="stat-val">${esc(Number(c.from || 0).toLocaleString("en-IN"))}</span>${c.unit ? `<span class="unit">${esc(c.unit)}</span>` : ""}</div><div class="stat-bar"></div><div class="stat-label">${rich(c.label)}</div>${c.source ? `<div class="stat-src">${esc(c.source)}</div>` : ""}</div></div>`;
    case "map": {
      const hl = new Set(c.states || []);
      const paths = map.states.map((s) => `<path id="${c.id}-${s.id}"${hl.has(s.id) ? ' class="hl"' : ""} d="${s.d}"/>`).join("");
      const labels = (c.labels || (c.states || []).map((s) => stateName[s] || s)).map((l) => `<div class="map-item"><span class="sw"></span>${esc(l)}</div>`).join("");
      return `<div class="slot"><div class="map-wrap"><svg viewBox="${map.viewBox}">${paths}</svg></div><div class="map-side">${c.kicker ? `<div><span class="kicker">${esc(c.kicker)}</span></div>` : ""}<div class="map-title">${rich(c.title || "")}</div>${labels}${c.note ? `<div class="map-note">${esc(c.note)}</div>` : ""}</div></div>`;
    }
    case "timeline": {
      const n = c.items.length;
      const items = c.items
        .map((it, i) => `<div class="tl-item" style="left:${n === 1 ? 50 : 12 + (76 * i) / (n - 1)}%"><div class="tl-dot"></div><div class="tl-year">${esc(it.year)}</div><div class="tl-text">${esc(it.text)}</div></div>`)
        .join("");
      return `<div class="slot">${c.kicker ? `<span class="kicker">${esc(c.kicker)}</span>` : ""}<div class="tl-title">${rich(c.title || "")}</div><div class="tl-line"></div>${items}</div>`;
    }
    case "term":
      return `<div class="slot"><div class="term"><span class="kicker">${esc(c.kicker || "Key term")}</span><h2 class="term-title">${rich(c.title)}</h2><p class="term-body">${esc(c.body || "")
        .split(/\s+/)
        .map((w) => `<span class="tw">${w}</span>`)
        .join("")}</p></div></div>`;
    case "compare":
      return `<div class="slot"><div class="cmp">${["a", "b"]
        .map((k) => {
          const col = c[k];
          return `<div class="cmp-col ${k}"><h3>${esc(col.title)}</h3><ul>${col.items.map((t) => `<li>${esc(t)}</li>`).join("")}</ul></div>`;
        })
        .join("")}</div></div>`;
    default:
      throw new Error(`unknown card type "${c.type}" in ${c.id}`);
  }
}

const cardsHtml = cards
  .map((c, i) => `<div id="${c.id}" class="card-host clip" data-start="${c.start}" data-duration="${q(c.end - c.start)}" data-track-index="${3 + (i % 2)}">${cardInner(c)}</div>`)
  .join("\n      ");

// Merge back-to-back paper cards into one "video in a window" stretch.
const paper = [];
cards
  .filter((c) => PAPER_TYPES.has(c.type))
  .forEach((c) => {
    const last = paper[paper.length - 1];
    if (last && c.start - last.end < 1.2) last.end = c.end;
    else paper.push({ start: c.start, end: c.end });
  });
const paperSegs = paper.map((p) => ({ in: q(Math.max(0, p.start - 0.3)), out: p.end >= DUR - 0.2 ? null : q(p.end - 0.1) }));

// ---------- zooms ----------
const zooms = (edit.zooms || []).map((z) => {
  const style = z.style || "punch";
  const preset = { punch: { dur: 0.22, ease: "power3.out" }, push: { dur: 3, ease: "sine.inOut" }, smooth: { dur: 0.7, ease: "power2.inOut" } }[style];
  return { at: q(z.at), scale: z.scale, x: z.x || 0, y: z.y || 0, dur: z.dur || preset.dur, ease: z.ease || preset.ease };
});

// ---------- sound effects ----------
const sfx = [];
const sfxLen = { "whoosh.wav": 0.55, "pop.wav": 0.2, "tick.wav": 0.08 };
const add = (file, at, vol) => at >= 0 && at < DUR - 0.1 && sfx.push({ file, at: q(at), vol });
const sfxOn = edit.sfx !== false;
if (sfxOn) {
  paperSegs.forEach((p) => {
    add("whoosh.wav", p.in, 0.45);
    if (p.out !== null) add("whoosh.wav", p.out, 0.35);
  });
  cards.forEach((c) => {
    const inPaperStart = paperSegs.some((p) => Math.abs(p.in - q(Math.max(0, c.start - 0.3))) < 0.01);
    if (c.type === "keyword" || c.type === "hook" || c.type === "stat") add("pop.wav", c.start, 0.5);
    else if (!inPaperStart) add("whoosh.wav", c.start, 0.3);
    if (c.type === "timeline") {
      c.step = c.step || 0.45;
      c.items.forEach((_, i) => add("tick.wav", c.start + 0.9 + i * c.step, 0.5));
    }
  });
  zooms.filter((z) => z.dur <= 0.3 && z.scale > 1.05).forEach((z) => add("whoosh.wav", z.at - 0.05, 0.15));
}
// give each effect the first audio lane that is free at its start time
const laneEnds = [];
sfx.sort((a, b) => a.at - b.at).forEach((s) => {
  let lane = laneEnds.findIndex((end) => end <= s.at);
  if (lane === -1) lane = laneEnds.push(0) - 1;
  laneEnds[lane] = s.at + sfxLen[s.file] + 0.05;
  s.track = 10 + lane;
});
const sfxHtml = sfx
  .map((s, i) => `<audio id="sfx-${i + 1}" src="assets/sfx/${s.file}" data-start="${s.at}" data-duration="${sfxLen[s.file]}" data-track-index="${s.track}" data-volume="${s.vol}"></audio>`)
  .join("\n      ");

const reel = {
  zooms,
  paper: paperSegs,
  cards: cards.map((c) => ({
    id: c.id,
    type: c.type,
    start: c.start,
    end: c.end,
    value: c.value,
    from: c.from || 0,
    decimals: c.decimals || 0,
    step: c.step || (c.type === "compare" ? 0.3 : 0.45),
  })),
};

const css = fs.readFileSync(path.join(kit, "style.css"), "utf8");
const engine = fs.readFileSync(path.join(kit, "engine.js"), "utf8");
const video = edit.video || "assets/footage.mp4";

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>${esc(edit.title || name)}</title>
    <!-- Generated by scripts/build-reel.mjs from edit.json. Edit edit.json, then rebuild. -->
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
${css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="reel" data-start="0" data-width="1080" data-height="1920" data-duration="${DUR}" data-fps="${FPS}">
      <div class="paper-bg"><div class="rule" style="top: 150px"></div><div class="rule" style="top: 1500px"></div></div>
      <div id="cam-wrap">
        <div id="cam" data-layout-allow-overflow>
          <video id="a-roll" class="clip" src="${esc(video)}" playsinline data-has-audio="true" data-start="0" data-duration="${DUR}" data-track-index="0"></video>
        </div>
        <div class="vignette"></div>
      </div>
      <div class="cam-frame"></div>
      ${cardsHtml}
      <div id="captions">
        ${captionsHtml}
      </div>
      <div class="grain"></div>
      ${sfxHtml}
    </div>
    <script>
      window.REEL = ${JSON.stringify(reel)};
    </script>
    <script>
${engine}
    </script>
  </body>
</html>
`;
fs.writeFileSync(path.join(dir, "index.html"), html);
console.log(`Built videos/${name}/index.html: ${DUR}s, ${visibleGroups.length} caption groups, ${cards.length} cards, ${zooms.length} zooms, ${sfx.length} sfx`);
