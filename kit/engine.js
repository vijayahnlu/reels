// Builds the reel's single paused GSAP timeline from window.REEL (written by
// scripts/build-reel.mjs) plus the static DOM. Inlined into index.html.
(function () {
  const R = window.REEL;
  const tl = gsap.timeline({ paused: true });
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  // Motion feel. Short, decisive entrances that settle hard; quick exits.
  const IN = 0.32;
  const OUT = 0.18;
  const SNAP = "expo.out";
  const LEAVE = "power3.in";
  const MOVE = "expo.inOut";
  const NO = { immediateRender: false };

  // ---------- camera: punch-ins, slow pushes, pull-outs ----------
  let cam = { scale: 1, x: 0, y: 0 };
  gsap.set("#cam", cam);
  R.zooms.forEach((z) => {
    const next = { scale: z.scale, x: z.x || 0, y: z.y || 0 };
    if (z.cut) tl.set("#cam", next, z.at); // jump cut: change framing on the exact frame
    else tl.fromTo("#cam", { ...cam }, { ...next, duration: z.dur, ease: z.ease, ...NO }, z.at);
    cam = next;
  });

  // ---------- paper mode: the video shrinks into a framed window ----------
  const FULL = { clipPath: "inset(0% 0% 0% 0% round 0px)", scale: 1, y: 0 };
  const WINDOW = { clipPath: "inset(18% 6% 30% 6% round 28px)", scale: 0.62, y: -285 };
  const T_WIN = 0.45;
  gsap.set("#cam-wrap", FULL);
  R.paper.forEach((seg) => {
    tl.fromTo("#cam-wrap", FULL, { ...WINDOW, duration: T_WIN, ease: MOVE, ...NO }, seg.in);
    tl.fromTo(".cam-frame", { opacity: 0 }, { opacity: 1, duration: 0.12, ...NO }, seg.in + T_WIN - 0.1);
    tl.fromTo(".vignette", { opacity: 1 }, { opacity: 0, duration: 0.25, ...NO }, seg.in);
    tl.fromTo("#captions", { y: 0, scale: 1 }, { y: 225, scale: 0.88, duration: T_WIN, ease: MOVE, ...NO }, seg.in);
    if (seg.out !== null) {
      tl.fromTo(".cam-frame", { opacity: 1 }, { opacity: 0, duration: 0.08, ...NO }, seg.out);
      tl.fromTo("#cam-wrap", WINDOW, { ...FULL, duration: T_WIN, ease: MOVE, ...NO }, seg.out);
      tl.fromTo(".vignette", { opacity: 0 }, { opacity: 1, duration: 0.25, ...NO }, seg.out + 0.15);
      tl.fromTo("#captions", { y: 225, scale: 0.88 }, { y: 0, scale: 1, duration: T_WIN, ease: MOVE, ...NO }, seg.out);
    }
  });

  // ---------- captions: word-by-word, locked to the transcript ----------
  $$(".cap-group").forEach((g) => {
    const gs = +g.dataset.gs, ge = +g.dataset.ge;
    tl.set(g, { opacity: 1 }, gs);
    tl.fromTo(g, { y: 10, scale: 0.96 }, { y: 0, scale: 1, duration: 0.1, ease: "power2.out", ...NO }, gs);
    tl.set(g, { opacity: 0 }, ge);
    $$(".w", g).forEach((w) => {
      const ws = +w.dataset.ws, we = +w.dataset.we;
      if (w.classList.contains("hot")) {
        tl.fromTo(w, { scale: 1 }, { scale: 1.1, duration: 0.07, ease: "power2.out", yoyo: true, repeat: 1, ...NO }, ws);
      } else {
        tl.set(w, { color: "#ffd31a" }, ws);
        tl.set(w, { color: "#ffffff" }, we);
      }
    });
  });

  // ---------- cards ----------
  const marks = (root, t) => {
    const m = $$(".mark-bg", root);
    if (m.length) tl.fromTo(m, { scaleX: 0 }, { scaleX: 1, duration: 0.28, ease: "power3.inOut", stagger: 0.12, ...NO }, t);
  };
  const fmt = (v, dec) => Number(v).toLocaleString("en-IN", { minimumFractionDigits: dec, maximumFractionDigits: dec });

  R.cards.forEach((c) => {
    const root = document.getElementById(c.id);
    const s = c.start, e = c.end;
    const exitAt = e - OUT;

    if (c.type === "hook") {
      tl.fromTo($(".kicker", root), { y: -24, opacity: 0 }, { y: 0, opacity: 1, duration: IN, ease: SNAP }, s);
      tl.fromTo($(".hook-title", root), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: IN, ease: SNAP }, s + 0.06);
      marks(root, s + 0.3);
      tl.to($(".hook", root), { y: -30, opacity: 0, duration: OUT, ease: LEAVE }, exitAt);
    }

    if (c.type === "keyword") {
      tl.fromTo($$(".kw-bg", root), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: SNAP, stagger: 0.07 }, s);
      tl.fromTo($$(".kw-text", root), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.22, ease: SNAP, stagger: 0.07 }, s + 0.06);
      tl.fromTo($(".kw", root), { scale: 1.08 }, { scale: 1, duration: 0.35, ease: SNAP }, s);
      tl.to($(".kw", root), { y: -24, opacity: 0, duration: OUT, ease: LEAVE }, exitAt);
    }

    if (c.type === "headline") {
      const clip = $(".clipping", root);
      tl.fromTo(clip, { y: 140, rotation: -7, opacity: 0 }, { y: 0, rotation: -2, opacity: 1, duration: 0.42, ease: SNAP }, s);
      marks(root, s + 0.4);
      tl.to(clip, { y: -50, opacity: 0, duration: OUT, ease: LEAVE }, exitAt);
    }

    if (c.type === "stat") {
      const num = $(".stat-val", root);
      const o = { v: c.from };
      tl.fromTo($(".stat", root), { scale: 0.86, opacity: 0 }, { scale: 1, opacity: 1, duration: IN, ease: SNAP }, s);
      tl.to(o, { v: c.value, duration: 0.8, ease: "expo.out", onUpdate: () => { num.textContent = fmt(o.v, c.decimals); } }, s + 0.05);
      tl.fromTo($(".stat-bar", root), { width: 0 }, { width: 420, duration: 0.35, ease: SNAP }, s + 0.25);
      tl.fromTo($$(".stat-label, .stat-src", root), { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.28, ease: SNAP, stagger: 0.08 }, s + 0.3);
      marks(root, s + 0.6);
      tl.to($(".stat", root), { opacity: 0, scale: 0.96, duration: OUT, ease: LEAVE }, exitAt);
    }

    if (c.type === "map") {
      tl.fromTo($(".map-wrap", root), { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: SNAP }, s);
      const hl = $$("path.hl", root);
      tl.to(hl, { fill: "#c22b22", duration: 0.18, stagger: 0.18, ease: "power2.out" }, s + 0.3);
      tl.fromTo(hl, { scale: 1 }, { scale: 1.06, transformOrigin: "50% 50%", duration: 0.1, yoyo: true, repeat: 1, stagger: 0.18, ...NO }, s + 0.3);
      tl.fromTo($$(".map-side > *", root), { x: 36, opacity: 0 }, { x: 0, opacity: 1, duration: 0.28, ease: SNAP, stagger: 0.08 }, s + 0.15);
      marks(root, s + 0.5);
      tl.to($$(".map-wrap, .map-side", root), { opacity: 0, duration: OUT }, exitAt);
    }

    if (c.type === "timeline") {
      tl.fromTo($$(".kicker, .tl-title", root), { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: 0.28, ease: SNAP, stagger: 0.05 }, s);
      marks(root, s + 0.25);
      tl.fromTo($(".tl-line", root), { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: MOVE }, s + 0.1);
      $$(".tl-item", root).forEach((it, i) => {
        const t = c.itemTimes[i];
        tl.fromTo($(".tl-dot", it), { scale: 0 }, { scale: 1, duration: 0.22, ease: "back.out(3)" }, t);
        tl.fromTo($$(".tl-year, .tl-text", it), { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.24, ease: SNAP, stagger: 0.05 }, t + 0.03);
      });
      tl.to($$(".kicker, .tl-title, .tl-line, .tl-item", root), { opacity: 0, duration: OUT }, exitAt);
    }

    if (c.type === "term") {
      tl.fromTo($(".term", root), { x: -90, opacity: 0 }, { x: 0, opacity: 1, duration: 0.38, ease: SNAP }, s);
      tl.fromTo($(".term .kicker", root), { scaleX: 0 }, { scaleX: 1, transformOrigin: "0 50%", duration: 0.22, ease: SNAP }, s + 0.15);
      tl.fromTo($$(".term-body .tw", root), { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.16, stagger: 0.025 }, s + 0.35);
      marks(root, s + 0.35);
      tl.to($(".term", root), { x: 60, opacity: 0, duration: OUT, ease: LEAVE }, exitAt);
    }

    if (c.type === "compare") {
      tl.fromTo($(".cmp-col.a", root), { x: -100, opacity: 0 }, { x: 0, opacity: 1, duration: 0.36, ease: SNAP }, s);
      tl.fromTo($(".cmp-col.b", root), { x: 100, opacity: 0 }, { x: 0, opacity: 1, duration: 0.36, ease: SNAP }, s + 0.08);
      tl.fromTo($$(".cmp-col.a li", root), { x: -16, opacity: 0 }, { x: 0, opacity: 1, duration: 0.22, ease: SNAP, stagger: c.step }, s + 0.3);
      tl.fromTo($$(".cmp-col.b li", root), { x: 16, opacity: 0 }, { x: 0, opacity: 1, duration: 0.22, ease: SNAP, stagger: c.step }, s + 0.3 + c.step * 0.5);
      tl.to($(".cmp", root), { opacity: 0, y: 24, duration: OUT, ease: LEAVE }, exitAt);
    }
  });

  window.__timelines["reel"] = tl;
})();
