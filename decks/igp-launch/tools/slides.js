/* Motion for each slide. B(root, tl, P, L): root is the slide, tl its paused timeline, P(t) marks a hold
   (the deck waits there for a click), L the slide's lights {x, y, r, ry, i} in stage pixels. */
function $(r, s) { return r.querySelector(s); }
function $$(r, s) { return r.querySelectorAll(s); }

// one result row: the name rises, the score counts up under its own glint, the rule draws with a light running along it
function scoreRow(tl, row, at, glint, runner) {
  M.fade(tl, $(row, '.name'), at, { y: 22, dur: 0.9 });
  var n = $(row, '.n'), score = $(row, '.score'), to = +n.textContent;
  M.fade(tl, score, at + 0.15, { y: 0, dur: 0.5 });
  M.count(tl, n, at + 0.15, to, 1.3);
  tl.fromTo(glint, { i: 0 }, { i: 1.1, duration: 0.6, ease: 'power2.out', immediateRender: false }, at + 0.2);
  tl.to(glint, { i: 0.22, duration: 1.2, ease: 'power2.inOut' }, at + 1.3);
  var rule = $(row, '.rule');
  if (rule) {
    var y = rule.offsetTop + 1;
    tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: 'expo.out' }, at + 0.1);
    tl.fromTo(runner, { x: 96, y: y, i: 0.9 }, { x: 1120, duration: 1.1, ease: 'expo.out', immediateRender: false }, at + 0.1);
    tl.to(runner, { i: 0, duration: 0.4 }, at + 1.0);
  }
  return at + 1.5;
}

BUILDERS.s01 = function (root, tl, P, L) {
  var pod = $(root, '.pod'), rl = $$(root, '.rl'), rr = $$(root, '.rr'), crowd = $$(root, '.crowd'), dots = $$(root, '.d');
  L[1].ry = 10; L[1].r = 90;
  // build 1: the heading, and the winner rising into a light that opens behind them
  M.fade(tl, $(root, '.label'), 0.15, { y: 12 });
  M.fade(tl, $$(root, '.title .w'), 0.35, { stagger: 0.08, dur: 1.1, y: 34 });
  M.bloom(tl, L[0], 0.3, { dur: 2.6 });
  tl.fromTo(pod, { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 2.2, ease: 'power3.out' }, 0.4);
  M.hide(tl, crowd); tl.set(dots, { opacity: 0 }, 0);
  // build 2: Komal, Sumit, Zenden
  P(2.6);
  var t = 2.65;
  rl.forEach(function (r, i) { scoreRow(tl, r, t + i * 0.75, L[2 + i], L[1]); });
  M.pulse(tl, L[0], 1.05, 1.35, t + 0.3, 0.5);
  // build 3: Shashwat, Aniket
  P(t + 0.75 * 2 + 1.6);
  t = t + 0.75 * 2 + 1.65;
  rr.forEach(function (r, i) { scoreRow(tl, r, t + i * 0.75, L[5 + i]); });
  // build 4: many more, and the crowd behind them
  P(t + 0.75 + 1.6);
  t = t + 0.75 + 1.65;
  M.fade(tl, $(root, '.more'), t, { y: 18, dur: 0.8 });
  dots.forEach(function (d, i) { tl.set(d, { opacity: 1 }, t + 0.5 + i * 0.07); });
  M.bloom(tl, L[7], t + 0.4, { dur: 1.8 });
  crowd.forEach(function (c, i) { tl.fromTo(c, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out' }, t + 0.6 + i * 0.16); });
  M.pulse(tl, L[0], 1.05, 1.3, t + 0.6, 0.6);
};
