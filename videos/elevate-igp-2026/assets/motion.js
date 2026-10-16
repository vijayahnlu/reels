// The film's six motions (spec § 2), shared by every scene. Each helper adds tweens to a paused,
// seekable GSAP timeline at an absolute time and returns when its motion ends.
(function () {
  var EASE = "expo.out";
  var M = {};

  // fade_up: opacity 0 -> 1 with a 24px rise; a light blur settles with it
  M.fadeUp = function (tl, targets, at, o) {
    o = o || {};
    var dur = o.dur || 0.8, stagger = o.stagger || 0;
    var n = gsap.utils.toArray(targets).length;
    tl.fromTo(targets,
      { opacity: 0, y: o.y == null ? 24 : o.y, filter: "blur(" + (o.blur == null ? 8 : o.blur) + "px)" },
      { opacity: 1, y: 0, filter: "blur(0px)", duration: dur, ease: o.ease || EASE, stagger: stagger }, at);
    return at + dur + stagger * Math.max(0, n - 1);
  };

  // stagger: children run fade_up one after another
  M.stagger = function (tl, items, at, gap, o) {
    var t = at, end = at;
    items.forEach(function (it, i) {
      var words = it.querySelectorAll(".w");
      var e = words.length ? M.fadeUp(tl, words, at + i * gap, Object.assign({ stagger: 0.045 }, o))
                           : M.fadeUp(tl, it, at + i * gap, o);
      end = Math.max(end, e);
    });
    return end;
  };

  // type_on: characters appear one by one behind a visible cursor (no sound)
  M.typeOn = function (tl, line, at, dur) {
    var chars = line.querySelectorAll(".ch"), cursor = line.querySelector(".cur");
    var n = chars.length, step = dur / n;
    tl.set(cursor, { opacity: 1, x: chars[0].offsetLeft }, at);
    for (var i = 0; i < n; i++) {
      var c = chars[i];
      tl.set(c, { opacity: 1 }, at + i * step);
      tl.set(cursor, { x: c.offsetLeft + c.offsetWidth + 4 }, at + i * step);
    }
    return at + dur;
  };

  // blinking cursor, a finite number of blinks
  M.blink = function (tl, cursor, from, until) {
    var cycles = Math.max(0, Math.floor((until - from) / 1.0) - 1);
    tl.to(cursor, { opacity: 0, duration: 0.5, ease: "steps(1)", repeat: cycles * 2 + 1, yoyo: true }, from);
  };

  // count_up: numerals tick from 0 to the final value
  M.countUp = function (tl, el, at, to, o) {
    o = o || {};
    var dur = o.dur || 1.5, pre = o.pre || "", suf = o.suf || "";
    var p = { v: 0 };
    tl.set(el, { textContent: pre + "0" + suf }, 0);
    tl.to(p, { v: to, duration: dur, ease: "power3.out",
      onUpdate: function () { el.textContent = pre + Math.round(p.v) + suf; } }, at);
    return at + dur;
  };

  // clear_to: existing content fades out fully before the next slide fades up
  M.clearOut = function (tl, el, end) {
    tl.to(el, { opacity: 0, y: -16, filter: "blur(6px)", duration: 0.7, ease: "power2.in" }, end - 0.75);
  };

  // slow push-in that keeps long voiceover holds alive
  M.drift = function (tl, el, dur) {
    tl.fromTo(el, { scale: 1 }, { scale: 1.018, duration: dur, ease: "none" }, 0);
  };

  window.ELV = M;
})();
