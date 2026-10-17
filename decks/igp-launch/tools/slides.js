/* Motion for each slide. B(root, tl, P, L): root is the slide, tl its paused timeline, P(t) marks a hold
   (the deck waits there for a click), L the slide's lights {x, y, r, ry, i} in stage pixels.
   E(root)[i] is the i-th element of that slide in the PPT, in the order model.json lists them. */
function $(r, s) { return r.querySelector(s); }
function $$(r, s) { return [].slice.call(r.querySelectorAll(s)); }
function E(root) { return $$(root, '.e'); }
function W(el, line) { return $$(el, line == null ? '.w' : '.w[data-l="' + line + '"]'); }

// the small orange label, then the heading word by word
function head(tl, e, at, o) {
  o = o || {};
  M.fade(tl, e[0], at, { y: 12, dur: 0.8 });
  return M.fade(tl, W(e[1], o.line), at + 0.25, { stagger: 0.06, dur: 1.0, y: 30 });
}
// any number inside a text box counts up from zero
function num(tl, el, at, dur) {
  $$(el, '.w').forEach(function (w) {
    var m = w.textContent.match(/^(\D*)(\d+)(.*)$/);
    if (!m) return;
    if (!w.querySelector('.n')) w.innerHTML = m[1] + '<span class="n">' + m[2] + '</span>' + m[3];
    M.count(tl, $(w, '.n'), at, +m[2], dur || 1.4);
  });
}
// a screenshot rises and opens from the top
function reveal(tl, el, at, dur) {
  dur = dur || 1.3;
  tl.fromTo(el, { opacity: 0, y: 24, clipPath: 'inset(0% 0% 100% 0%)' }, { opacity: 1, y: 0, clipPath: 'inset(0% 0% 0% 0%)', duration: dur, ease: 'power3.inOut' }, at);
  return at + dur;
}
function rule(tl, el, at, dur) { tl.fromTo(el, { scaleX: 0 }, { scaleX: 1, duration: dur || 1.0, ease: 'expo.out' }, at); return at + (dur || 1.0); }
// an amber box is drawn round a part of a screenshot, then its glow comes up
function box(tl, svg, at, dur) {
  dur = dur || 0.8;
  var st = $(svg, '.stroke'), gl = $(svg, '.glow'), len = st.getTotalLength();
  tl.fromTo(st, { strokeDasharray: len, strokeDashoffset: len, opacity: 0 }, { strokeDashoffset: 0, opacity: 1, duration: dur, ease: 'power2.inOut' }, at);
  tl.fromTo(gl, { opacity: 0 }, { opacity: 1, duration: 0.5 }, at + dur * 0.6);
  return at + dur;
}
function glowPulse(tl, svg, at) { tl.fromTo($(svg, '.glow'), { opacity: 1 }, { opacity: 0.3, duration: 0.45, yoyo: true, repeat: 3, ease: 'sine.inOut', immediateRender: false }, at); }
// the camera inside a screenshot frame: bring point (px, py) of the picture to the middle at scale s
function cam(tl, root, px, py, s, at, dur) {
  var frame = $(root, '.cam'), inner = $(root, '.cami'), w = frame.offsetWidth, h = frame.offsetHeight;
  var x = Math.min(0, Math.max(w - s * w, w / 2 - s * px)), y = Math.min(0, Math.max(h - s * h, h / 2 - s * py));
  tl.to(inner, { x: x, y: y, scale: s, transformOrigin: '0 0', duration: dur || 1.4, ease: 'power3.inOut' }, at);
  return at + (dur || 1.4);
}
function swap(tl, a, b, at) { M.out(tl, a, at, { dur: 0.6 }); tl.fromTo(b, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 1.0, ease: 'power3.out' }, at + 0.4); return at + 1.4; }
// numbered rows (slides 6, 22, 24): number, text, rule; the row's own icon and light come up with it
function rowIn(tl, parts, at, icon, light, prevLight) {
  M.fade(tl, parts[0], at, { y: 16, dur: 0.7 });
  M.fade(tl, W(parts[1]).length ? W(parts[1]) : parts[1], at + 0.12, { y: 16, dur: 0.8, stagger: 0.03 });
  if (parts[2]) rule(tl, parts[2], at + 0.1, 1.1);
  if (icon) M.rise(tl, icon, at + 0.15, { y: 24, dur: 1.2 });
  if (light) M.bloom(tl, light, at + 0.1, { dur: 1.2 });
  if (prevLight) M.light(tl, prevLight, { i: 0.35, duration: 0.9 }, at);
  return at + 1.3;
}
function sheen(tl, el, at) { tl.fromTo(el, { backgroundPosition: '120% 0' }, { backgroundPosition: '-20% 0', duration: 1.4, ease: 'power2.inOut', immediateRender: false }, at); }

/* ---------------- 1 · every year, the highest scorers ---------------- */
function scoreRow(tl, name, score, rl, at, glint, runner) {
  M.fade(tl, W(name), at, { y: 22, dur: 0.9 });
  M.fade(tl, score, at + 0.15, { y: 0, dur: 0.5 });
  num(tl, score, at + 0.15, 1.3);
  tl.fromTo(glint, { i: 0 }, { i: 1.1, duration: 0.6, ease: 'power2.out', immediateRender: false }, at + 0.2);
  tl.to(glint, { i: 0.22, duration: 1.2, ease: 'power2.inOut' }, at + 1.3);
  if (rl) {
    var y = rl.offsetTop + 1;
    rule(tl, rl, at + 0.1, 1.1);
    tl.fromTo(runner, { x: 96, y: y, i: 0.9 }, { x: 1120, duration: 1.1, ease: 'expo.out', immediateRender: false }, at + 0.1);
    tl.to(runner, { i: 0, duration: 0.4 }, at + 1.0);
  }
}
BUILDERS.s01 = function (root, tl, P, L) {
  var e = E(root), crowd = $$(root, '.crowd');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.3, { dur: 2.6 });
  tl.fromTo($(root, '.pod'), { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 2.2, ease: 'power3.out' }, 0.4);
  M.hide(tl, crowd); tl.set($$(e[13], '.c'), { opacity: 0 }, 0);
  var t = 2.65; P(2.6);
  [[2, 3, 4], [5, 6, 7], [8, 9, 10]].forEach(function (r, i) { scoreRow(tl, e[r[0]], e[r[1]], e[r[2]], t + i * 0.75, L[2 + i], L[1]); });
  M.pulse(tl, L[0], 1.05, 1.35, t + 0.3, 0.5);
  P(t + 3.1); t += 3.15;
  [[11, 14], [12, 15]].forEach(function (r, i) { scoreRow(tl, e[r[0]], e[r[1]], null, t + i * 0.75, L[5 + i]); });
  P(t + 2.35); t += 2.4;
  $$(e[13], '.c').forEach(function (c, i) { tl.set(c, { opacity: 1 }, t + i * 0.06); });
  M.bloom(tl, L[7], t + 0.4, { dur: 1.8 });
  crowd.forEach(function (c, i) { tl.fromTo(c, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, t + 0.6 + i * 0.16); });
  M.pulse(tl, L[0], 1.05, 1.3, t + 0.6, 0.6);
};

/* ---------------- 2 · the three on YouTube, one per click ---------------- */
BUILDERS.s02 = function (root, tl, P, L) {
  var e = E(root), rings = $$(root, '.ring'), sh = $(root, '.sheen');
  tl.fromTo(e[0], { opacity: 0 }, { opacity: 1, duration: 1.4, ease: 'power2.out' }, 0);
  [[3, -1], [2, 1], [1, -1]].forEach(function (s, k) {
    var at = [0.4, 3.05, 5.65][k];
    if (k) P(at - 0.05);
    tl.fromTo(e[s[0]], { opacity: 0, x: 260 * -s[1] }, { opacity: 1, x: 0, duration: 1.3, ease: 'expo.out' }, at);
    sheen(tl, sh, at + 0.6);
    M.draw(tl, rings[k], at + 1.1, 0.9);
  });
};

/* ---------------- 3 · the same process produced all three ---------------- */
BUILDERS.s03 = function (root, tl, P, L) {
  var e = E(root), ps = $$(root, '.three');
  M.fade(tl, W(e[0]), 0.2, { stagger: 0.07, dur: 1.0, y: 30 });
  ps.forEach(function (p, i) { M.rise(tl, p, 0.5 + i * 0.35, { dur: 1.4 }); M.bloom(tl, L[i], 0.5 + i * 0.35, { dur: 1.2 }); });
  // the three lights draw together into one
  [0, 1, 2].forEach(function (i) { M.light(tl, L[i], { x: 1530, y: 640, i: 0, duration: 1.6 }, 2.4); });
  M.bloom(tl, L[3], 2.6, { dur: 2.0 });
};

/* ---------------- 4 · you are the syllabus now ---------------- */
BUILDERS.s04 = function (root, tl, P, L) {
  var e = E(root);
  M.bloom(tl, L[0], 0.1, { dur: 2.6 }); M.bloom(tl, L[1], 0.4, { dur: 2.4 });
  M.rise(tl, $(root, '.fig'), 0.3, { dur: 2.0 });
  M.fade(tl, $$(root, '.plab'), 1.0, { y: 14, stagger: 0.3 });
  M.fade(tl, W(e[0]), 1.6, { stagger: 0.09, dur: 1.1, y: 34 });
};

/* ---------------- 5 · 275 marks ---------------- */
BUILDERS.s05 = function (root, tl, P, L) {
  var e = E(root), sc = $(root, '.sc'), hist = $(root, '.hist');
  M.fade(tl, e[0], 0.1, { y: 12 });
  M.fade(tl, e[1], 0.3, { y: 30 }); num(tl, e[1], 0.3, 1.6);
  M.bloom(tl, L[0], 0.2); M.rise(tl, sc, 0.4);
  M.fade(tl, W(e[2]), 1.4, { stagger: 0.04 });
  M.hide(tl, [hist, e[3]]);
  P(2.8);
  // the widest spread: the scales give way to the spread of scores
  tl.set(e[3], { opacity: 1 }, 2.85);
  M.fade(tl, W(e[3]), 2.85, { stagger: 0.04 });
  M.out(tl, sc, 2.85, { dur: 0.6 });
  tl.set(hist, { opacity: 1 }, 3.2);
  tl.fromTo(hist, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.6, ease: 'power3.out' }, 3.2);
  M.light(tl, L[0], { i: 0.25, duration: 1.0 }, 3.2);
  M.bloom(tl, L[1], 3.6, { dur: 1.4 }); M.bloom(tl, L[2], 4.0, { dur: 1.4 });
};

/* ---------------- 6 and 24 · numbered lists, one row per click ---------------- */
function listSlide(root, tl, P, L, rows, foot) {
  var e = E(root), icons = $$(root, '.ri'), t = head(tl, e, 0.15);
  rows.forEach(function (r, i) {
    P(t); t += 0.05;
    t = rowIn(tl, r.map(function (k) { return e[k]; }), t, icons[i], L[i], i ? L[i - 1] : null);
  });
  P(t); M.fade(tl, W(e[foot]), t + 0.05, { y: 14, stagger: 0.02 });
  M.light(tl, L[rows.length - 1], { i: 0.35, duration: 0.9 }, t + 0.05);
}
BUILDERS.s06 = function (root, tl, P, L) { listSlide(root, tl, P, L, [[2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16]], 17); };
BUILDERS.s24 = function (root, tl, P, L) { listSlide(root, tl, P, L, [[2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13]], 14); };

/* ---------------- 7 · repair the DAF ---------------- */
BUILDERS.s07 = function (root, tl, P, L) {
  var e = E(root), lens = $(root, '.lens');
  var t = head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.3); M.rise(tl, $(root, '.fig'), 0.4);
  M.hide(tl, lens);
  P(t); t += 0.05;
  // they read it closely: a lens goes over the page
  M.fade(tl, W(e[2]), t, { stagger: 0.03, y: 16 });
  tl.fromTo(lens, { opacity: 0, x: 160, y: -120 }, { opacity: 1, x: 0, y: 0, duration: 1.0, ease: 'power3.out' }, t + 0.2);
  tl.to(lens, { x: 110, y: 80, duration: 1.0, ease: 'sine.inOut' }, t + 1.2);
  tl.to(lens, { x: -10, y: 140, duration: 0.9, ease: 'sine.inOut' }, t + 2.2);
  M.pulse(tl, L[0], 1.05, 1.35, t + 1.2, 0.6);
};

/* ---------------- 8 · five entries ---------------- */
BUILDERS.s08 = function (root, tl, P, L) {
  var e = E(root), rows = $$(root, '.hlbox'), badges = $$(root, '.badge');
  var t = head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.4, { dur: 2.0 });
  reveal(tl, e[2], 0.6); M.fade(tl, e[3], 1.6, { y: 8 });
  M.hide(tl, badges);
  t = Math.max(t, 2.2);
  P(t); t += 0.05;
  // the five entries, counted off one by one
  rows.forEach(function (r, i) {
    var at = t + i * 0.55;
    box(tl, r, at, 0.6);
    tl.fromTo(badges[i], { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2.4)' }, at + 0.1);
  });
};

/* ---------------- 9 · 20 defects ---------------- */
BUILDERS.s09 = function (root, tl, P, L) {
  var e = E(root);
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.1); M.rise(tl, $(root, '.fig'), 0.3);
  M.fade(tl, $(root, '.ctr'), 1.0, { y: 12 });
  tl.fromTo(L[1], { i: 0, y: 270 }, { i: L[1].i, duration: 0.4 }, 1.5);
  tl.to(L[1], { y: 680, duration: 2.6, ease: 'none' }, 1.5);
  tl.to(L[1], { i: 0, duration: 0.5 }, 3.9);
  M.count(tl, $(root, '.c20'), 1.5, 20, 2.6);
};

/* ---------------- 10 · stop guessing ---------------- */
BUILDERS.s10 = function (root, tl, P, L) {
  var e = E(root), q1 = $(root, '.q1'), q2 = $(root, '.q2');
  var t = head(tl, e, 0.15);
  M.hide(tl, q2);
  tl.fromTo(L[0], { i: 0, r: 140 }, { i: 0.45, r: 230, duration: 1.6, ease: 'power2.out' }, 0.2);
  M.rise(tl, q1, 0.3);
  t = Math.max(t, 2.0);
  P(t); t += 0.05;
  M.fade(tl, W(e[2]), t, { stagger: 0.03, y: 14 });
  swap(tl, q1, q2, t + 0.2);
  M.light(tl, L[0], { i: 1.2, r: 290, duration: 1.4, ease: 'power3.out' }, t + 0.6);
};

/* ---------------- 11 · 129 questions, one profile ---------------- */
BUILDERS.s11 = function (root, tl, P, L) {
  var e = E(root), hs = $$(root, '.hlbox');
  head(tl, e, 0.15); num(tl, e[1], 0.4, 1.6);
  M.bloom(tl, L[0], 0.3, { dur: 2.0 });
  reveal(tl, $(root, '.cam'), 0.6); M.fade(tl, e[3], 1.7, { y: 8 });
  hs.forEach(function (h) { tl.set(h, { opacity: 0 }, 0); });
  P(2.4); var t = 2.45;
  cam(tl, root, 616, 430, 1.3, t, 1.4);
  hs.forEach(function (h, i) { tl.set(h, { opacity: 1 }, t + 1.0 + i * 0.7); box(tl, h, t + 1.0 + i * 0.7, 0.7); });
  glowPulse(tl, hs[1], t + 2.6);
};

/* ---------------- 12 · every entry opens a door ---------------- */
BUILDERS.s12 = function (root, tl, P, L) {
  var e = E(root), col = $(root, '.col'), cells = $$(root, '.cell');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.3, { dur: 2.0 });
  reveal(tl, e[2], 0.6); M.fade(tl, e[3], 1.7, { y: 8 });
  cells.forEach(function (c) { tl.set(c, { opacity: 0 }, 0); });
  P(2.4); var t = 2.45;
  box(tl, col, t, 1.0);
  tl.fromTo(L[1], { i: 0, y: 300 }, { i: 1.0, duration: 0.4, immediateRender: false }, t + 0.8);
  tl.to(L[1], { y: 790, duration: 2.6, ease: 'none' }, t + 0.8);
  tl.to(L[1], { i: 0, duration: 0.5 }, t + 3.4);
  cells.forEach(function (c, i) {   // each answer cell lights as the scan passes it
    var at = t + 0.9 + i * 0.5;
    tl.set(c, { opacity: 1 }, at); box(tl, c, at, 0.4);
    tl.to($(c, '.stroke'), { opacity: 0.35, duration: 0.6 }, at + 0.7);
  });
};

/* ---------------- 13 · two words on the form ---------------- */
BUILDERS.s13 = function (root, tl, P, L) {
  var e = E(root), py = $(root, '.py'), yi = $$(root, '.yi');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.3, { dur: 2.0 });
  reveal(tl, e[2], 0.6); M.fade(tl, e[3], 1.6, { y: 8 });
  box(tl, py, 1.9, 0.7);
  M.hide(tl, [e[7], e[4], e[6]]); tl.set(e[5], { scaleX: 0, transformOrigin: '0 50%' }, 0);
  P(2.8); var t = 2.85;
  // the two words pulled out of the form
  tl.to(e[4], { opacity: 1, duration: 0.3 }, t);
  tl.to(e[5], { scaleX: 1, duration: 0.6, ease: 'power2.out' }, t + 0.1);
  tl.to(e[6], { opacity: 1, duration: 0.3 }, t + 0.6);
  tl.fromTo(e[7], { opacity: 0, scale: 0.85, x: -40 }, { opacity: 1, scale: 1, x: 0, duration: 1.0, ease: 'back.out(1.6)' }, t + 0.6);
  M.bloom(tl, L[1], t + 0.6, { dur: 1.6 });
  P(t + 1.8); t += 1.85;
  M.fade(tl, e[8], t, { y: 16 }); num(tl, e[8], t, 1.0);
  M.fade(tl, e[9], t + 0.3, { y: 16 }); num(tl, e[9], t + 0.3, 1.6);
  rule(tl, e[10], t + 0.6, 1.0);
  M.hide(tl, $$(e[11], '.p')); M.hide(tl, yi);
  P(t + 2.0); t += 2.05;
  $$(e[11], '.p').forEach(function (p, i) {
    M.fade(tl, p, t + i * 0.35, { y: 12, dur: 0.8 });
    tl.fromTo(yi[i], { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(2)' }, t + i * 0.35);
  });
};

/* ---------------- 14 · asked, on record ---------------- */
BUILDERS.s14 = function (root, tl, P, L) {
  var e = E(root), hs = $$(root, '.hlbox');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.3, { dur: 2.0 });
  reveal(tl, $(root, '.cam'), 0.6); M.fade(tl, e[3], 1.7, { y: 8 });
  hs.forEach(function (h) { tl.set(h, { opacity: 0 }, 0); });
  var t = 2.4;
  [[561, 154], [596, 313]].forEach(function (p, i) {
    P(t); t += 0.05;
    cam(tl, root, p[0], p[1], 1.45, t, 1.3);
    tl.set(hs[i], { opacity: 1 }, t + 0.9); box(tl, hs[i], t + 0.9, 0.8);
    t += 1.8;
  });
};

/* ---------------- 15 · even the safe entry ---------------- */
BUILDERS.s15 = function (root, tl, P, L) {
  var e = E(root), hs = $$(root, '.hlbox'), masks = $(root, '.masks');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.3, { dur: 2.0 });
  reveal(tl, $(root, '.cam'), 0.6); M.fade(tl, e[3], 1.7, { y: 8 });
  hs.forEach(function (h) { tl.set(h, { opacity: 0 }, 0); });
  M.hide(tl, masks);
  P(2.4); var t = 2.45;
  cam(tl, root, 711, 300, 1.3, t, 1.3);
  tl.set(hs[0], { opacity: 1 }, t + 0.9); box(tl, hs[0], t + 0.9, 0.9);
  tl.set(hs[1], { opacity: 1 }, t + 1.8); box(tl, hs[1], t + 1.8, 0.5);
  M.rise(tl, masks, t + 1.6, { dur: 1.4 }); M.bloom(tl, L[1], t + 1.6, { dur: 1.6 });
};

/* ---------------- 16 · the topic list, the exact wording ---------------- */
BUILDERS.s16 = function (root, tl, P, L) {
  var e = E(root), pen = $(root, '.pen'), quote = $(root, '.quote');
  head(tl, e, 0.15, { line: 0 });
  M.bloom(tl, L[0], 0.1);
  tl.fromTo($(root, '.scroll'), { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 2.0, ease: 'power2.inOut' }, 0.3);
  M.hide(tl, pen); M.hide(tl, W(e[1], 1)); M.hide(tl, W(e[2]));
  P(2.4); var t = 2.45;
  M.fade(tl, W(e[1], 1), t, { stagger: 0.06, y: 30 });
  tl.fromTo(pen, { opacity: 0, x: 60, y: -40 }, { opacity: 1, x: 0, y: 0, duration: 1.2, ease: 'power3.out' }, t + 0.2);
  M.bloom(tl, L[1], t + 0.3, { dur: 1.4 });
  M.typeOn(tl, quote, t + 0.8, 2.0);
  P(t + 3.0); t += 3.05;
  tl.set($(quote, '.cur'), { opacity: 0 }, t);
  M.fade(tl, W(e[2]), t, { stagger: 0.03, y: 14 });
};

/* ---------------- 17 · the CA questionnaire ---------------- */
BUILDERS.s17 = function (root, tl, P, L) {
  var e = E(root), c = $(root, '.c200');
  var t = Math.max(head(tl, e, 0.15), 1.8);
  M.bloom(tl, L[0], 0.2); M.rise(tl, $(root, '.fig'), 0.3);
  M.hide(tl, W(e[2])); M.hide(tl, c.parentNode);
  P(t); t += 0.05;
  M.fade(tl, W(e[2]), t, { stagger: 0.03, y: 14 }); num(tl, e[2], t, 1.6);
  M.fade(tl, c.parentNode, t + 0.2, { y: 12 });
  M.count(tl, c, t + 0.2, 200, 1.8);
  M.pulse(tl, L[0], 1.05, 1.4, t + 0.4, 0.6);
};

/* ---------------- 18 · recite vs what you make of it ---------------- */
BUILDERS.s18 = function (root, tl, P, L) {
  var e = E(root), k1 = $(root, '.k1'), k2 = $(root, '.k2');
  var t = Math.max(head(tl, e, 0.15), 1.8);
  M.bloom(tl, L[0], 0.2); M.rise(tl, k1, 0.3);
  M.hide(tl, k2); M.hide(tl, W(e[2]));
  P(t); t += 0.05;
  M.fade(tl, W(e[2]), t, { stagger: 0.04, y: 14 });
  M.out(tl, k1, t, { dur: 0.6 }); M.light(tl, L[0], { i: 0, duration: 0.7 }, t);
  tl.fromTo(k2, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.4, ease: 'power3.out' }, t + 0.4);
  M.bloom(tl, L[1], t + 0.5, { dur: 2.0 });
};

/* ---------------- 19 · weekly opinion matrix ---------------- */
BUILDERS.s19 = function (root, tl, P, L) {
  var e = E(root), cells = $$(root, '.cell');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.1); M.bloom(tl, L[1], 0.4, { dur: 1.4 });
  M.rise(tl, $(root, '.cal'), 0.3, { dur: 1.4 });
  M.fade(tl, cells, 0.5, { stagger: 0.03, dur: 0.6, y: 10 });
  tl.to(cells, { background: 'rgba(200,100,42,.6)', duration: 0.35, stagger: 0.07 }, 1.8);
  tl.to([cells[2], cells[8], cells[11], cells[17]], { background: 'rgba(242,239,233,.85)', duration: 0.4 }, 3.4);
};

/* ---------------- 20 · 30 to 40 percent ---------------- */
BUILDERS.s20 = function (root, tl, P, L) {
  var e = E(root), d = $(root, '.donut'), arc = $(d, '.arc'), c = +arc.dataset.c;
  var t = Math.max(head(tl, e, 0.15), 1.8);
  M.bloom(tl, L[0], 0.3); M.fade(tl, d, 0.4, { y: 20 });
  M.hide(tl, [$(d, '.band'), $(d, '.pc'), $(d, '.pcs')]); M.hide(tl, W(e[2]));
  P(t); t += 0.05;
  M.fade(tl, W(e[2]), t, { stagger: 0.03, y: 14 });
  tl.fromTo(arc, { strokeDasharray: '0 ' + c }, { strokeDasharray: (c * 0.35) + ' ' + c, duration: 1.8, ease: 'power3.out' }, t + 0.2);
  tl.to($(d, '.band'), { opacity: 1, duration: 0.6 }, t + 1.4);
  M.fade(tl, [$(d, '.pc'), $(d, '.pcs')], t + 1.0, { y: 10, stagger: 0.2 });
  M.pulse(tl, L[0], 0.9, 1.3, t + 1.0, 0.6);
};

/* ---------------- 21 · tagged OPINION, choose a side ---------------- */
BUILDERS.s21 = function (root, tl, P, L) {
  var e = E(root), hs = $$(root, '.hlbox'), sc = $(root, '.sc');
  head(tl, e, 0.15); num(tl, e[1], 0.4, 1.4);
  M.bloom(tl, L[0], 0.3, { dur: 1.8 });
  reveal(tl, e[2], 0.6, 1.0); M.fade(tl, e[3], 1.4, { y: 8 });
  box(tl, hs[0], 1.8, 0.9); box(tl, hs[1], 2.6, 0.5);
  M.hide(tl, sc); M.hide(tl, W(e[5])); M.hide(tl, W(e[6]));
  P(3.3); var t = 3.35;
  rule(tl, e[4], t, 1.0);
  M.fade(tl, W(e[5]), t + 0.3, { stagger: 0.05, y: 20 });
  M.rise(tl, sc, t + 0.6, { dur: 1.2 }); M.bloom(tl, L[1], t + 0.6, { dur: 1.4 });
  tl.to(sc, { rotation: -10, duration: 1.2, ease: 'power3.inOut' }, t + 1.8);
  P(t + 3.1); t += 3.15;
  M.fade(tl, W(e[6]), t, { stagger: 0.03, y: 12 });
};

/* ---------------- 22 · four moves, then stop ---------------- */
BUILDERS.s22 = function (root, tl, P, L) {
  var e = E(root), w = $(root, '.walker'), s = C.STEPS22;
  var t = head(tl, e, 0.15);
  M.bloom(tl, L[1], 0.1, { dur: 2.0 }); M.rise(tl, $(root, '.fig'), 0.2);
  M.rise(tl, w, 0.6, { dur: 1.2, y: 20 }); M.bloom(tl, L[0], 0.6, { dur: 1.6 });
  t = Math.max(t, 1.9);
  [[2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13]].forEach(function (r, i) {
    P(t); t += 0.05;
    rowIn(tl, r.map(function (k) { return e[k]; }), t);
    if (i > 0) {
      tl.to(w, { x: s[i][0] - s[0][0], y: s[i][1] - s[0][1], duration: 1.2, ease: 'power2.inOut' }, t);
      M.light(tl, L[0], { x: s[i][0], y: s[i][1] - 90, duration: 1.2 }, t);
    }
    if (i === 3) M.pulse(tl, L[0], 1.15, 1.7, t + 1.2, 0.4);   // and stop
    t += 1.6;
  });
  M.hide(tl, W(e[14]));
  P(t); M.fade(tl, W(e[14]), t + 0.05, { stagger: 0.02, y: 12 });
};

/* ---------------- 23 · Wikipedia and the newspaper come later ---------------- */
BUILDERS.s23 = function (root, tl, P, L) {
  var e = E(root), g = [$(root, '.g1'), $(root, '.g2')], g3 = $(root, '.g3');
  head(tl, e, 0.15);
  M.bloom(tl, L[0], 0.2); M.rise(tl, g, 0.3, { stagger: 0.25 });
  // later: they step back out of the light
  tl.to(g, { x: 140, opacity: 0.5, scale: 0.85, duration: 1.6, ease: 'power2.inOut', stagger: 0.15 }, 2.4);
  M.light(tl, L[0], { x: 1720, i: 0.55, duration: 1.6 }, 2.4);
  M.hide(tl, g3); M.hide(tl, W(e[2]));
  P(4.2); var t = 4.25;
  M.fade(tl, W(e[2]), t, { stagger: 0.03, y: 14 });
  tl.fromTo(g3, { opacity: 0, y: 30 }, { opacity: 0.45, y: 0, duration: 1.2, ease: 'power3.out' }, t + 0.3);
  M.bloom(tl, L[1], t + 0.3, { i: 0.45, dur: 1.2 });
};

/* ---------------- 25 · winning the argument ---------------- */
BUILDERS.s25 = function (root, tl, P, L) {
  var e = E(root), f = $(root, '.fig'), locks = $$(root, '.lock');
  M.fade(tl, e[0], 0.1, { y: 12 });
  M.fade(tl, W(e[1]), 0.3, { stagger: 0.06, y: 30 });
  tl.fromTo(f, { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.9, ease: 'power4.out' }, 0.5);
  tl.fromTo(L[0], { i: 0, r: 60 }, { i: 1.5, r: 240, duration: 0.6, ease: 'power3.out' }, 0.7);
  M.light(tl, L[0], { i: 0.4, r: 170, duration: 2.0, ease: 'power1.inOut' }, 2.4);
  M.hide(tl, locks); M.hide(tl, [e[3], e[5], e[7]]); M.hide(tl, W(e[9])); M.hide(tl, W(e[10]));
  [2, 4, 6, 8].forEach(function (k) { tl.set(e[k], { scaleX: 0 }, 0); });
  P(2.6); var t = 2.65;
  rule(tl, e[2], t, 1.0);
  [[3, 4], [5, 6], [7, 8]].forEach(function (p, i) {
    var at = t + 0.3 + i * 0.35;
    M.fade(tl, e[p[0]], at, { y: 14 });
    rule(tl, e[p[1]], at + 0.2, 0.8);
    tl.fromTo(locks[i], { opacity: 0, scale: 0.4, rotation: -20 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: 'back.out(2.2)' }, at + 0.6);
  });
  P(t + 2.0); t += 2.05;
  M.fade(tl, W(e[9]), t, { stagger: 0.03, y: 12 });
  M.fade(tl, W(e[10]), t + 0.6, { stagger: 0.03, y: 12 });
};

/* ---------------- 26 · this is the floor ---------------- */
BUILDERS.s26 = function (root, tl, P, L) {
  var e = E(root), f = $(root, '.fig');
  var t = Math.max(head(tl, e, 0.15), 2.0);
  M.bloom(tl, L[1], 0.1, { dur: 1.6 });
  tl.fromTo(f, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 2.2, ease: 'power2.inOut' }, 0.3);
  M.bloom(tl, L[0], 1.4, { dur: 2.2 });
  [[2, 3, 4], [5, 6, 7], [8, 9, 10]].forEach(function (r) {
    M.hide(tl, [e[r[0]]]); M.hide(tl, W(e[r[1]])); tl.set(e[r[2]], { scaleX: 0 }, 0);
  });
  M.hide(tl, W(e[11]));
  [[2, 3, 4], [5, 6, 7], [8, 9, 10]].forEach(function (r) {
    P(t); t += 0.05;
    M.fade(tl, e[r[0]], t, { y: 14 }); num(tl, e[r[0]], t, 1.4);
    M.fade(tl, W(e[r[1]]), t + 0.15, { y: 14, stagger: 0.03 });
    rule(tl, e[r[2]], t + 0.1, 1.1);
    M.pulse(tl, L[0], 1.2, 1.5, t + 0.2, 0.5);
    t += 1.5;
  });
  P(t); M.fade(tl, W(e[11]), t + 0.05, { stagger: 0.03, y: 12 });
};

/* ---------------- 27 · enrol ---------------- */
BUILDERS.s27 = function (root, tl, P, L) {
  var e = E(root), scan = $(root, '.scan'), cs = $$(e[4], '.c');
  tl.fromTo(e[2], { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: 1.4, ease: 'expo.out' }, 0.1);
  sheen(tl, $(root, '.sheen'), 0.9);
  rule(tl, e[0], 0.3); rule(tl, e[1], 0.5);
  M.bloom(tl, L[1], 0.4, { dur: 1.6 });
  M.hide(tl, e[3]); tl.set(cs, { opacity: 0 }, 0);
  P(2.0);
  // the QR code comes up under a scan line
  tl.fromTo(e[3], { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.9, ease: 'power3.out' }, 2.05);
  M.bloom(tl, L[0], 2.05, { dur: 1.4 });
  tl.fromTo(scan, { opacity: 1, y: 0 }, { y: 428, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 1, immediateRender: false }, 2.3);
  tl.to(scan, { opacity: 0, duration: 0.3 }, 4.5);
  P(4.8);
  cs.forEach(function (c, i) { tl.fromTo(c, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: 'back.out(2)' }, 4.85 + i * 0.045); });
  M.pulse(tl, L[1], 0.5, 0.9, 5.8, 0.6);
};
