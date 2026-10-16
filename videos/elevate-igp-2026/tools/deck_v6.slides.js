/* Motion for each slide. B(root, tl, P, L): root is the slide, tl its paused timeline, P(t) marks a hold
   (the deck waits there for a click), L the slide's lights {x, y, r, ry, i} in stage pixels. */
function $(r, s) { return r.querySelector(s); }
function $$(r, s) { return r.querySelectorAll(s); }

// a statement slide: the picture rises in its light, then the words
function simple(root, tl, L, o) {
  o = o || {};
  L.forEach(function (l, i) { M.bloom(tl, l, 0.1 + i * 0.3, { dur: 2.4 }); });
  $$(root, '.fig').forEach(function (f) { M.rise(tl, f, 0.3); });
  return M.fade(tl, $$(root, o.words || '.tx .w'), o.at || 0.9, { stagger: 0.07 });
}
// stacked lines, one click each, with an optional hook per line
function linesBySteps(root, tl, P, t, each) {
  $$(root, '.lines > div').forEach(function (ln, i) {
    if (i > 0) { P(t); t += 0.05; }
    var e = M.fade(tl, ln, t);
    t = Math.max(e, each ? each(i, t) || 0 : 0);
  });
  return t;
}

BUILDERS.s01 = function (root, tl, P, L) {
  var sc = $$(root, '.scene'), caps = $$(root, '.cap'), qs = $$(root, '.ty'), t = 0.2;
  M.hide(tl, [sc[1], sc[2], caps[1], caps[2]]);
  qs.forEach(function (ln, i) {
    if (i > 0) {
      P(t); t += 0.05;
      tl.set($(qs[i - 1], '.cur'), { opacity: 0 }, t);
      tl.to(qs[i - 1], { color: '#9C938A', duration: 0.8 }, t);
      M.out(tl, [sc[i - 1], caps[i - 1]], t, { y: -20, dur: 0.8 });
      M.light(tl, L[i - 1], { i: 0, duration: 1.0 }, t);
      t += 0.5;
      tl.set(sc[i], { opacity: 1 }, t);
    }
    var s = sc[i];
    M.rise(tl, $(s, '.fig'), t, { dur: 2.0 });
    if (i === 0) {
      M.bloom(tl, L[0], t, { dur: 2.6 });
      tl.fromTo($(s, '.pin'), { y: -320, opacity: 0 }, { y: 0, opacity: 1, duration: 1.2, ease: 'bounce.out' }, t + 0.9);
    }
    if (i === 1) {
      M.bloom(tl, L[1], t, { dur: 2.4 });
      tl.fromTo($(s, '.moon'), { opacity: 0, y: 30, rotation: -20 }, { opacity: 1, y: 0, rotation: 0, duration: 1.8, ease: 'power3.out' }, t + 0.5);
    }
    if (i === 2) {   // moksha: the light opens wide and the chains fall away
      M.bloom(tl, L[2], t, { dur: 3.2, ease: 'power1.inOut' });
      tl.fromTo($(s, '.chainL'), { opacity: 0, x: 120 }, { opacity: 1, x: -30, rotation: -12, duration: 1.4, ease: 'power3.out' }, t + 1.0);
      tl.fromTo($(s, '.chainR'), { opacity: 0, x: -120 }, { opacity: 1, x: 30, duration: 1.4, ease: 'power3.out' }, t + 1.0);
    }
    M.fade(tl, caps[i], t + 0.9, { y: 12 });
    t = Math.max(M.typeOn(tl, ln, t + 0.3, 1.5), t + 2.4);
  });
};

BUILDERS.s02 = function (root, tl, P, L) {
  M.bloom(tl, L[0], 0.1, { dur: 2.6 }); M.bloom(tl, L[1], 0.4, { dur: 2.4 });
  M.rise(tl, $(root, '.fig'), 0.3, { dur: 2.0 });
  M.fade(tl, $(root, '.top'), 0.2, { y: 12 });
  M.fade(tl, $$(root, '.plab'), 1.0, { y: 14, stagger: 0.3 });
  M.fade(tl, $$(root, '.hero .w'), 2.2, { stagger: 0.1, dur: 1.1, y: 40 });
};

BUILDERS.s03 = function (root, tl, P, L) {   // the light climbs from below the frame, the name appears in front of it
  tl.fromTo(L[0], { y: 1250, i: 0.2 }, { y: 560, i: 1.15, duration: 3.0, ease: 'power2.out' }, 0.1);
  M.fade(tl, $$(root, '.wm .w'), 1.0, { stagger: 0.09, dur: 1.4, y: 20 });
  M.fade(tl, $(root, '.sub'), 2.2, { dur: 1.2, y: 14 });
};

BUILDERS.s04 = function (root, tl, P, L) {
  M.rise(tl, $(root, '.fig'), 0.2, { y: 120, dur: 2.2 });
  M.bloom(tl, L[1], 0.2, { dur: 2.0 });
  tl.fromTo(L[0], { i: 0, r: 120 }, { i: L[0].i, r: L[0].r, duration: 2.2, ease: 'power2.out' }, 0.4);
  M.fade(tl, $(root, '.num-big'), 0.3, { dur: 0.8 });
  M.count(tl, $(root, '.num'), 0.4, 200, 2.0);
  M.fade(tl, $(root, '.suf'), 2.3, { dur: 0.7, y: 16 });
  M.fade(tl, $(root, '.cp'), 2.5, { y: 12 });
};

BUILDERS.s05 = function (root, tl, P, L) {
  M.hide(tl, $(root, '.l2'));
  M.bloom(tl, L[0], 0.1, { dur: 2.4 });
  tl.fromTo($(root, '.fig'), { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.8, ease: 'power3.out' }, 0.3);
  M.fade(tl, $(root, '.l1'), 0.4);
  M.count(tl, $(root, '.cnt'), 0.4, 275, 1.8);
  P(2.4);
  // the spread: light moves to the tallest bar, a second one finds the lowest
  M.fade(tl, $(root, '.l2'), 2.45);
  M.light(tl, L[0], { x: C.S5_TOP[0], y: C.S5_TOP[1], r: 150, i: 1.15, duration: 1.6 }, 2.5);
  M.bloom(tl, L[1], 2.9, { dur: 1.8 });
};

BUILDERS.s06 = function (root, tl, P, L) {
  M.bloom(tl, L[0], 0.1, { dur: 2.6 });
  M.rise(tl, $(root, '.fig'), 0.3, { dur: 2.0 });
  M.fade(tl, $(root, '.sc'), 0.4, { dur: 1.2 });
  M.fade(tl, $(root, '.redact'), 1.6, { y: 10 });
  P(2.6);
  tl.to($(root, '.val'), { color: '#EA9458', duration: 0.9, ease: 'power2.out' }, 2.65);
  M.pulse(tl, L[0], 1.0, 1.4, 2.65, 0.7);
};

BUILDERS.s07 = function (root, tl, P, L) {   // the light behind the hourglass shrinks to what was left over
  var g = $(root, '.fig');
  M.bloom(tl, L[0], 0.1, { dur: 2.2 }); M.rise(tl, g, 0.2);
  linesBySteps(root, tl, P, 0.6, function (i, t) {
    if (i === 1) { tl.to(g, { rotation: 180, duration: 1.4, ease: 'power3.inOut' }, t); return M.light(tl, L[0], { i: 0.75, r: 240, duration: 1.4 }, t); }
    if (i === 2) { tl.to(g, { rotation: 360, duration: 1.4, ease: 'power3.inOut' }, t); return M.light(tl, L[0], { i: 0.32, r: 120, duration: 1.8 }, t); }
  });
};

BUILDERS.s08 = function (root, tl, P, L) {
  var w1 = $(root, '.w1'), w2 = $(root, '.w2');
  M.hide(tl, w2); M.hide(tl, $$(root, '.lines > div')[1]);
  M.bloom(tl, L[0], 0.1); M.rise(tl, $(w1, '.fig'), 0.2);
  tl.fromTo($(w1, '.pen'), { opacity: 0, x: 60, y: -60 }, { opacity: 1, x: 0, y: 0, duration: 1.4, ease: 'power3.out' }, 0.6);
  tl.to($(w1, '.pen'), { x: -40, y: 12, duration: 0.5, ease: 'sine.inOut', yoyo: true, repeat: 3 }, 2.0);
  M.fade(tl, $$(root, '.lines > div')[0], 0.6);
  P(4.0);
  M.out(tl, w1, 4.05, { y: -20, dur: 0.7 }); M.light(tl, L[0], { i: 0, duration: 0.8 }, 4.05);
  tl.set(w2, { opacity: 1 }, 4.5);
  M.rise(tl, $(w2, '.fig'), 4.5);
  M.fade(tl, $$(root, '.lines > div')[1], 4.6);
  M.bloom(tl, L[1], 4.6, { dur: 1.2 });
  M.bloom(tl, L[2], 5.3, { dur: 1.2 });
  M.pulse(tl, L[1], 0.95, 1.35, 6.5, 0.45);   // back and forth
  M.pulse(tl, L[2], 0.95, 1.35, 7.4, 0.45);
};

BUILDERS.s09 = function (root, tl, P, L) {
  M.hide(tl, $(root, '.pile')); M.hide(tl, $$(root, '.lines > div')[1]);
  M.bloom(tl, L[1], 0.1, { dur: 2.2 });
  M.rise(tl, $(root, '.fig'), 0.2);
  M.bloom(tl, L[0], 1.2, { dur: 1.8 });   // light comes through the missing brick
  M.fade(tl, $$(root, '.lines > div')[0], 0.8);
  P(3.0);
  M.fade(tl, $$(root, '.lines > div')[1], 3.05);
  M.rise(tl, $(root, '.pile'), 3.2, { dur: 1.4 });
  M.bloom(tl, L[2], 3.3, { dur: 1.6 });
  M.light(tl, L[0], { i: 0.9, duration: 1.6 }, 3.3);
};

BUILDERS.s10 = function (root, tl, P, L) {   // a light settles on each part as it is named
  var rows = $$(root, '.nrow'), t = 0.2;
  rows.forEach(function (r, i) {
    if (i > 0) { P(t); t += 0.05; M.light(tl, L[i - 1], { i: 0.55, duration: 1.0 }, t); }
    M.bloom(tl, L[i], t, { dur: 1.6 });
    t = M.fade(tl, r, t + 0.1, { y: 20 }) + 0.2;
  });
};

function sectionMarker(root, tl, L, extra) {
  M.fade(tl, $(root, '.secno'), 0.1, { dur: 1.4, y: 40 });
  M.bloom(tl, L[0], 0.2, { dur: 2.6 });
  $$(root, '.fig').forEach(function (f) { M.rise(tl, f, 0.4, { dur: 2.0 }); });
  var t = M.fade(tl, $$(root, '.head .stmt .w'), 0.9, { stagger: 0.07 });
  var sub = $(root, '.head .sub'); if (sub) t = M.fade(tl, sub, t - 0.3);
  if (extra) extra(t);
}
BUILDERS.s11 = function (root, tl, P, L) { sectionMarker(root, tl, L); };
BUILDERS.s16 = function (root, tl, P, L) {   // the question mark gives way to a lit bulb on "Start knowing"
  var q1 = $(root, '.q1'), q2 = $(root, '.q2');
  M.fade(tl, $(root, '.secno'), 0.1, { dur: 1.4, y: 40 });
  M.hide(tl, q2);
  tl.fromTo(L[0], { i: 0, r: 150 }, { i: 0.45, r: 260, duration: 1.6, ease: 'power2.out' }, 0.2);
  M.rise(tl, q1, 0.3);
  var ws = $$(root, '.head .w');
  M.fade(tl, [].slice.call(ws, 0, 2), 0.8, { stagger: 0.08 });
  M.out(tl, q1, 2.2, { dur: 0.6 });
  tl.fromTo(q2, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 1.0, ease: 'power3.out' }, 2.5);
  M.light(tl, L[0], { i: 1.2, r: 330, duration: 1.4, ease: 'power3.out' }, 2.5);
  M.fade(tl, [].slice.call(ws, 2), 2.5, { stagger: 0.08 });
};
BUILDERS.s27 = BUILDERS.s11;
BUILDERS.s31 = BUILDERS.s11;
BUILDERS.s34 = function (root, tl, P, L) {
  M.hide(tl, $(root, '.lamp'));
  tl.fromTo($(root, '.lamp'), { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: 1.6, ease: 'power3.out' }, 0.2);
  sectionMarker(root, tl, L);
};

BUILDERS.s12 = function (root, tl, P, L) {
  var daf = $(root, '.daf'), board = $(root, '.board');
  M.hide(tl, daf);
  tl.fromTo($(root, '.lamp'), { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: 1.6, ease: 'power3.out' }, 0.1);
  M.bloom(tl, L[0], 0.5, { dur: 2.2 });
  M.rise(tl, $(root, '.fig'), 0.6);
  M.fade(tl, $$(root, '.stmt .w'), 1.0, { stagger: 0.06 });
  P(3.0);
  // the form they read: three things get marked
  tl.to(board, { opacity: 0.18, duration: 0.9 }, 3.05);
  M.light(tl, L[0], { x: 1470, y: 570, r: 400, ry: 340, i: 0.8, duration: 1.4 }, 3.05);
  tl.fromTo(daf, { opacity: 0, y: 60, rotation: 3 }, { opacity: 1, y: 0, rotation: -1.5, duration: 1.3, ease: 'power3.out' }, 3.2);
  var mk = $$(root, '.mark');
  M.draw(tl, mk[0], 4.6, 0.6); M.draw(tl, mk[1], 5.4, 0.45); M.draw(tl, mk[2], 6.1, 0.9);
};

BUILDERS.s13 = function (root, tl, P, L) {
  var form = $(root, '.form'), lines = $$(root, '.lines > div'), blanks = $$(form, '.blank');
  M.hide(tl, [lines[1], lines[2]]);
  M.bloom(tl, L[0], 0.1, { dur: 2.2 });
  M.fade(tl, form, 0.3, { dur: 1.2 });
  M.fade(tl, lines[0], 0.5);
  tl.fromTo(blanks, { scaleX: 0, transformOrigin: '0 50%' }, { scaleX: 1, duration: 0.8, ease: 'expo.out', stagger: 0.18 }, 1.0);
  tl.to(blanks, { background: 'rgba(234,148,88,.8)', duration: 0.35, yoyo: true, repeat: 1, stagger: 0.12 }, 2.2);
  P(3.4);
  M.fade(tl, lines[1], 3.45);
  tl.set(blanks[0], { opacity: 0 }, 3.6);
  M.typeOn(tl, $(form, '.hob'), 3.6, 1.6);
  P(5.6);
  M.fade(tl, lines[2], 5.65);
  tl.set($(form, '.hob .cur'), { opacity: 0 }, 5.65);
  tl.to(form, { opacity: 0.45, duration: 1.4 }, 5.8);
  M.light(tl, L[0], { i: 0.22, duration: 1.8 }, 5.8);
};

BUILDERS.s14 = function (root, tl, P, L) {
  var sheet = $(root, '.sheet'), lines = $$(root, '.lines > div');
  M.hide(tl, lines[1]);
  M.bloom(tl, L[0], 0.1); M.rise(tl, $(root, '.fig'), 0.2);
  tl.set(sheet, { opacity: 0 }, 0);
  M.fade(tl, lines[0], 0.6);
  P(2.6);
  // the page that never made it into the folder
  tl.fromTo(sheet, { opacity: 0, x: -250, y: 160, rotation: -6 }, { opacity: 1, x: 0, y: 0, rotation: 9, duration: 1.6, ease: 'power3.out' }, 2.65);
  M.light(tl, L[0], { i: 0.35, duration: 1.4 }, 2.7);
  M.bloom(tl, L[1], 3.0, { dur: 1.8 });
  M.fade(tl, lines[1], 2.9);
};

BUILDERS.s15 = function (root, tl, P, L) {
  M.bloom(tl, L[0], 0.1); M.rise(tl, $(root, '.fig'), 0.2);
  M.fade(tl, $(root, '.lab'), 0.4, { y: 14 });
  M.fade(tl, $$(root, '.l1 .w'), 0.7, { stagger: 0.06 });
  M.fade(tl, $(root, '.ctr'), 1.2, { y: 12 });
  // a band of light reads the list top to bottom while the count runs
  tl.fromTo(L[1], { i: 0, y: 260 }, { i: L[1].i, duration: 0.4 }, 1.6);
  tl.to(L[1], { y: 720, duration: 2.6, ease: 'none' }, 1.6);
  tl.to(L[1], { i: 0, duration: 0.5 }, 4.0);
  M.count(tl, $(root, '.c20'), 1.6, 20, 2.6);
};

BUILDERS.s17 = function (root, tl, P, L) {   // the light leaves your notebook and finds the board's files
  M.bloom(tl, L[0], 0.1, { dur: 1.6 });
  M.rise(tl, $(root, '.nb'), 0.2, { dur: 1.4 });
  M.hide(tl, $(root, '.fig'));
  M.fade(tl, $$(root, '.stmt .w'), 0.8, { stagger: 0.07 });
  M.light(tl, L[0], { i: 0.12, duration: 1.4 }, 2.0);
  M.bloom(tl, L[1], 2.2, { dur: 2.2 });
  M.rise(tl, $(root, '.fig'), 2.3);
};

BUILDERS.s18 = function (root, tl, P, L) {   // each row's count is drawn as a bar of light
  M.fade(tl, $(root, '.thead'), 0.2, { y: 14 });
  var t = 0.7;
  $$(root, '.trow').forEach(function (r, i) {
    if (i > 0) { P(t); t += 0.05; }
    M.fade(tl, r, t, { y: 18 });
    var l = L[i];
    tl.fromTo(l, { i: 0, r: 10, x: 1040 }, { i: l.i, r: l.r, x: l.x, duration: 1.4, ease: 'power2.out' }, t + 0.2);
    var n = $(r, '.tnum');
    t = M.count(tl, n, t + 0.2, +n.dataset.to, 1.4) + 0.1;
  });
};

BUILDERS.s19 = function (root, tl, P, L) {
  var cols = $$(root, '.pcol'), t = 0.2;
  cols.forEach(function (c, i) {
    if (i > 0) { P(t); t += 0.05; }
    M.bloom(tl, L[i], t, { dur: 2.0 });
    M.fade(tl, c, t + 0.2);
    var n = $(c, '.pnum');
    t = M.count(tl, n, t + 0.2, +n.textContent, 1.6) + 0.2;
  });
};

BUILDERS.s20 = function (root, tl, P, L) {   // the reference picture: a seated figure, light behind the head
  M.bloom(tl, L[0], 0.1, { dur: 3.0 });
  M.rise(tl, $(root, '.fig'), 0.3, { dur: 2.4 });
  M.fade(tl, $$(root, '.centre .w'), 1.2, { stagger: 0.12, dur: 1.2 });
};

BUILDERS.s21 = function (root, tl, P, L) {
  var centre = $(root, '.centre');
  tl.to($(root, '.fig'), { opacity: 0, duration: 1.0, ease: 'power2.inOut' }, 0.15);
  M.light(tl, L[0], { i: 0, duration: 1.2 }, 0.15);
  tl.fromTo(centre, { scale: 1 }, { scale: C.SMALL, duration: 1.2, ease: 'expo.inOut' }, 0.2);
  var conns = $$(root, '.conn'), dots = $$(root, '.dot'), nodes = $$(root, '.node');
  M.hide(tl, nodes); tl.set(dots, { opacity: 0 }, 0);
  P(1.45);
  conns.forEach(function (c, i) {
    var at = 1.5 + i * 0.55;
    M.draw(tl, c, at, 0.5);
    tl.fromTo(dots[i], { opacity: 0, scale: 0, transformOrigin: '50% 50%' }, { opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2.2)' }, at + 0.35);
    M.fade(tl, nodes[i], at + 0.4, { dur: 0.8, y: 12 });
    M.bloom(tl, L[i + 1], at + 0.4, { dur: 1.0 });
  });
};

BUILDERS.s22 = function (root, tl, P, L) {
  tl.to($$(root, '.fan, .centre'), { opacity: 0, filter: 'blur(6px)', duration: 0.6, ease: 'power2.in' }, 0.1);
  M.hide(tl, $$(root, '.bsub'));
  $$(root, '.node').forEach(function (nd, i) {
    tl.fromTo(nd, { x: +nd.dataset.dx, y: +nd.dataset.dy }, { x: 0, y: 0, duration: 1.3, ease: 'expo.inOut' }, 0.2 + i * 0.07);
    tl.to(L[i], { x: C.ROWS22[i][0], y: C.ROWS22[i][1], i: 0.75, duration: 1.3, ease: 'expo.inOut' }, 0.2 + i * 0.07);
  });
  var t = 1.85;
  $$(root, '.bsub').forEach(function (b, i) {
    P(t);
    M.pulse(tl, L[i], 0.75, 1.1, t + 0.05, 0.5);
    t = M.fade(tl, b, t + 0.05, { y: 16 });
  });
};

BUILDERS.s23 = function (root, tl, P, L) {
  M.bloom(tl, L[0], 0.1, { dur: 2.2 }); M.rise(tl, $(root, '.fig'), 0.2);
  var t = 0.5;
  $$(root, '.inst').forEach(function (r, i) {
    if (i > 0) { P(t); t += 0.05; }
    M.fade(tl, $(r, '.q'), t);
    tl.fromTo($(r, '.stamp'), { opacity: 0, scale: 1.25, transformOrigin: '0% 50%' }, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2)' }, t + 0.7);
    if (i > 0) M.pulse(tl, L[0], 0.95, 1.3, t + 0.1, 0.5);
    t += 1.4;
  });
};

BUILDERS.s24 = function (root, tl, P, L) {
  var b1 = $(root, '.b1'), b2 = $(root, '.b2'), qq = $$(root, '.qq');
  M.hide(tl, b2); M.hide(tl, qq[1]);
  M.bloom(tl, L[0], 0.1);
  M.rise(tl, $(b1, '.fig'), 0.2);
  tl.fromTo($(b1, '.lens'), { opacity: 0, x: 120, y: -80, rotation: 10 }, { opacity: 1, x: 0, y: 0, rotation: 0, duration: 1.6, ease: 'power3.out' }, 0.6);
  tl.to($(b1, '.lens'), { x: 70, y: 30, duration: 1.2, ease: 'sine.inOut', yoyo: true, repeat: 1 }, 2.2);
  M.fade(tl, $(root, '.lb'), 0.3, { y: 14 });
  M.fade(tl, qq[0], 0.8);
  P(2.6);
  // the hobby question turns into an opinion question: the book becomes masks
  M.out(tl, b1, 2.65, { dur: 0.7 });
  tl.set(b2, { opacity: 1 }, 3.1);
  M.rise(tl, $(b2, '.fig'), 3.1);
  M.pulse(tl, L[0], 1.0, 1.35, 3.1, 0.6);
  M.fade(tl, qq[1], 2.8);
  tl.fromTo($(qq[1], '.tag'), { scale: 1.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2.5)' }, 3.8);
};

BUILDERS.s25 = function (root, tl, P, L) {
  var l2 = $(root, '.l2'), pen = $(root, '.pen');
  M.hide(tl, [l2, pen]);
  M.bloom(tl, L[0], 0.1);
  tl.fromTo($(root, '.scroll'), { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 2.0, ease: 'power2.inOut' }, 0.3);
  M.fade(tl, $(root, '.lb'), 0.3, { y: 14 });
  M.fade(tl, $(root, '.l1'), 0.7);
  P(2.6);
  M.fade(tl, l2, 2.65);
  tl.fromTo(pen, { opacity: 0, x: 60, y: -40 }, { opacity: 1, x: 0, y: 0, duration: 1.2, ease: 'power3.out' }, 2.8);
  M.bloom(tl, L[1], 2.9, { dur: 1.4 });
  M.typeOn(tl, $(root, '.quote'), 3.4, 2.0);
};

BUILDERS.s26 = function (root, tl, P, L) {
  var l2 = $(root, '.l2');
  M.hide(tl, l2);
  M.bloom(tl, L[2], 0.1, { dur: 2.0 });
  M.rise(tl, $(root, '.fig'), 0.2);
  M.bloom(tl, L[0], 0.8, { dur: 1.8 });
  M.fade(tl, $(root, '.l1'), 0.6);
  P(2.6);
  // the light walks the path to the second stop
  tl.fromTo(L[1], { x: L[0].x, y: L[0].y, i: 0 }, { x: C.PIN2[0], y: C.PIN2[1], i: L[1].i, duration: 2.0, ease: 'power2.inOut' }, 2.65);
  M.light(tl, L[0], { i: 0.45, duration: 1.4 }, 2.8);
  M.fade(tl, l2, 2.7);
};

BUILDERS.s28 = function (root, tl, P, L) {
  var rev = $(root, '.rev'), sc = $(root, '.fig');
  M.hide(tl, $$(rev, '.w'));
  M.bloom(tl, L[0], 0.1); M.rise(tl, sc, 0.2);
  var t = M.fade(tl, $$(root, '.main .w'), 0.5, { stagger: 0.04 });
  M.fade(tl, $(root, '.st'), t - 0.3, { y: 12 });
  P(t + 0.4);
  t += 0.45;
  M.fade(tl, $$(rev, '.w'), t, { stagger: 0.06 });
  tl.to(sc, { rotation: -9, duration: 1.4, ease: 'power3.inOut' }, t + 0.2);
  M.light(tl, L[0], { i: 0.3, duration: 1.2 }, t + 0.2);
  M.bloom(tl, L[1], t + 0.5, { dur: 1.4 });
};

BUILDERS.s29 = function (root, tl, P, L) {   // a figure climbs a step per line, and stops
  var w = $(root, '.walker'), s = C.STEPS29;
  M.bloom(tl, L[1], 0.1, { dur: 2.0 }); M.rise(tl, $(root, '.fig'), 0.2);
  M.rise(tl, w, 0.6, { dur: 1.2, y: 20 });
  M.bloom(tl, L[0], 0.6, { dur: 1.6 });
  linesBySteps(root, tl, P, 0.7, function (i, t) {
    if (i === 1 || i === 2) {
      var p = s[i];
      tl.to(w, { x: p[0] - s[0][0], y: p[1] - s[0][1], duration: 1.3, ease: 'power2.inOut' }, t);
      return M.light(tl, L[0], { x: p[0], y: p[1] - 100, duration: 1.3 }, t);
    }
    if (i === 3) return M.pulse(tl, L[0], 1.15, 1.6, t + 0.2, 0.4);
  });
};

BUILDERS.s30 = function (root, tl, P, L) {   // every turn of the loop, the answer gets a little brighter
  var dr = $$(root, '.dr'), cyc = $(root, '.fig');
  M.hide(tl, dr);
  M.bloom(tl, L[0], 0.1, { i: 0.5, dur: 1.6 });
  M.rise(tl, cyc, 0.2);
  M.fade(tl, $(root, '.lab'), 0.3, { y: 14 });
  M.fade(tl, $$(root, '.l1 .w'), 0.6, { stagger: 0.05 });
  tl.to(dr[0], { opacity: 1, duration: 0.4 }, 1.2);
  for (var k = 0; k < 3; k++) {
    var at = 1.4 + k * 1.3;
    tl.to(cyc, { rotation: '+=360', duration: 1.2, ease: 'power2.inOut' }, at);
    tl.to(dr[k], { opacity: 0, duration: 0.25 }, at + 0.9);
    tl.to(dr[k + 1], { opacity: 1, duration: 0.3 }, at + 1.0);
    M.light(tl, L[0], { i: 0.5 + 0.25 * (k + 1), r: 220 + 30 * (k + 1), duration: 1.2 }, at);
  }
};

BUILDERS.s32 = function (root, tl, P, L) {
  var k1 = $(root, '.k1'), k2 = $(root, '.k2'), lines = $$(root, '.lines > div');
  M.hide(tl, [k2, lines[1]]);
  M.bloom(tl, L[0], 0.1); M.rise(tl, $(k1, '.fig'), 0.2);
  M.fade(tl, $(k1, '.cap'), 1.0, { y: 12 });
  M.fade(tl, lines[0], 0.6);
  P(2.6);
  M.out(tl, k1, 2.65, { dur: 0.7 }); M.light(tl, L[0], { i: 0, duration: 0.8 }, 2.65);
  tl.set(k2, { opacity: 1 }, 3.0);
  M.rise(tl, $(k2, '.fig'), 3.0);
  M.bloom(tl, L[1], 3.1, { dur: 2.2 });
  M.fade(tl, lines[1], 2.9);
};

BUILDERS.s33 = function (root, tl, P, L) {
  var cells = $$(root, '.cell');
  M.bloom(tl, L[0], 0.1); M.bloom(tl, L[1], 0.4, { dur: 1.4 });
  M.rise(tl, $(root, '.cal'), 0.3, { dur: 1.4 });
  M.fade(tl, cells, 0.5, { stagger: 0.03, dur: 0.6, y: 10 });
  M.fade(tl, $(root, '.lab'), 0.4, { y: 14 });
  M.fade(tl, $$(root, '.l1 .w'), 0.8, { stagger: 0.06 });
  // the matrix fills in, one issue at a time
  tl.to(cells, { background: 'rgba(234,148,88,.55)', duration: 0.35, stagger: { each: 0.07, from: 'start' } }, 1.8);
  tl.to([cells[2], cells[8], cells[11], cells[17]], { background: 'rgba(239,231,222,.85)', duration: 0.4 }, 3.4);
};

BUILDERS.s35 = function (root, tl, P, L) {   // the clash flares, then the light goes out of it
  var f = $(root, '.fig');
  tl.fromTo(f, { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.9, ease: 'power4.out' }, 0.2);
  tl.fromTo(L[0], { i: 0, r: 60 }, { i: 1.5, r: 300, duration: 0.6, ease: 'power3.out' }, 0.4);
  M.fade(tl, $$(root, '.stmt .w'), 0.8, { stagger: 0.06 });
  M.light(tl, L[0], { i: 0.5, r: 210, duration: 2.0, ease: 'power1.inOut' }, 2.4);
};

BUILDERS.s36 = function (root, tl, P, L) {
  var t = M.fade(tl, $$(root, '.head .w'), 0.2, { stagger: 0.06 });
  M.fade(tl, $(root, '.sub'), t - 0.4);
  var doors = $$(root, '.door'), slots = $$(root, '.slot');
  M.hide(tl, doors); M.hide(tl, slots);
  P(t + 0.2); t += 0.25;
  doors.forEach(function (d, i) {
    var at = t + i * 0.45;
    M.rise(tl, d, at, { dur: 1.4 });
    M.bloom(tl, L[i], at + 0.2, { dur: 1.6 });
    M.fade(tl, slots[i], at + 0.4, { y: 14 });
    tl.fromTo($(slots[i], '.blank'), { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: 'expo.out' }, at + 0.7);
  });
};

BUILDERS.s37 = function (root, tl, P, L) {   // the pile grows with each number
  var pile = $(root, '.fig'), rows = $$(root, '.crow'), t = 0.2;
  M.bloom(tl, L[0], 0.1, { i: 0.6, r: 220 });
  tl.fromTo(pile, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 0.55, duration: 1.4, ease: 'power3.out' }, 0.3);
  rows.forEach(function (r, i) {
    if (i > 0) {
      P(t); t += 0.05;
      tl.to(pile, { scale: i === 1 ? 0.8 : 1, duration: 1.4, ease: 'power3.out' }, t);
      M.light(tl, L[0], { i: i === 1 ? 0.85 : 1.15, r: i === 1 ? 270 : 330, duration: 1.4 }, t);
    }
    var e = M.fade(tl, r, t), v = $(r, '.cval');
    t = v ? M.count(tl, v, t, +v.dataset.to, 1.6) : e;
  });
};

BUILDERS.s38 = function (root, tl, P, L) {
  M.bloom(tl, L[1], 0.1, { dur: 1.6 });
  // the stairs build from the floor up, toward the light at the top
  tl.fromTo($(root, '.fig'), { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 2.4, ease: 'power2.inOut' }, 0.3);
  M.bloom(tl, L[0], 1.6, { dur: 2.4 });
  M.fade(tl, $$(root, '.stmt .w'), 1.0, { stagger: 0.07 });
};

BUILDERS.s39 = function (root, tl, P, L) {
  tl.fromTo(L[0], { y: -260, i: 0.2 }, { y: 270, i: 1.1, duration: 2.6, ease: 'power2.out' }, 0.1);
  var t = M.fade(tl, $$(root, '.wm .w'), 0.6, { stagger: 0.08, dur: 1.2, y: 20 });
  t = M.fade(tl, $(root, '.sub'), t - 0.6, { dur: 1.0, y: 12 });
  M.fade(tl, $(root, '.credit'), t - 0.5, { y: 0 });
  P(t); t += 0.05;
  t = M.fade(tl, $$(root, '.feat'), t, { stagger: 0.3, y: 16 });
  P(t);
  M.fade(tl, $(root, '.cta'), t + 0.05);
};

