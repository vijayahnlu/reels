// Builds the reel's single paused GSAP timeline from window.REEL (written by
// scripts/build-reel.mjs) plus the static DOM. Inlined into index.html.
(function () {
  const R = window.REEL;
  const tl = gsap.timeline({ paused: true });
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  // ---------- camera: punch-ins, slow pushes, pull-outs ----------
  let cam = { scale: 1, x: 0, y: 0 };
  gsap.set("#cam", cam);
  R.zooms.forEach((z) => {
    const next = { scale: z.scale, x: z.x || 0, y: z.y || 0 };
    tl.fromTo("#cam", { ...cam }, { ...next, duration: z.dur, ease: z.ease, immediateRender: false }, z.at);
    cam = next;
  });

  // ---------- paper mode: the video shrinks into a framed window ----------
  const FULL = { clipPath: "inset(0% 0% 0% 0% round 0px)", scale: 1, y: 0 };
  const WINDOW = { clipPath: "inset(18% 6% 30% 6% round 28px)", scale: 0.62, y: -285 };
  gsap.set("#cam-wrap", FULL);
  R.paper.forEach((seg) => {
    tl.fromTo("#cam-wrap", FULL, { ...WINDOW, duration: 0.6, ease: "power3.inOut", immediateRender: false }, seg.in);
    tl.fromTo(".cam-frame", { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, seg.in + 0.4);
    tl.fromTo(".vignette", { opacity: 1 }, { opacity: 0, duration: 0.4, immediateRender: false }, seg.in);
    tl.fromTo("#captions", { y: 0, scale: 1 }, { y: 225, scale: 0.88, duration: 0.6, ease: "power3.inOut", immediateRender: false }, seg.in);
    if (seg.out !== null) {
      tl.fromTo(".cam-frame", { opacity: 1 }, { opacity: 0, duration: 0.15, immediateRender: false }, seg.out);
      tl.fromTo("#cam-wrap", WINDOW, { ...FULL, duration: 0.6, ease: "power3.inOut", immediateRender: false }, seg.out);
      tl.fromTo(".vignette", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, seg.out + 0.2);
      tl.fromTo("#captions", { y: 225, scale: 0.88 }, { y: 0, scale: 1, duration: 0.6, ease: "power3.inOut", immediateRender: false }, seg.out);
    }
  });

  // ---------- captions: word-by-word ----------
  $$(".cap-group").forEach((g) => {
    const gs = +g.dataset.gs, ge = +g.dataset.ge;
    tl.set(g, { opacity: 1 }, gs);
    tl.fromTo(g, { y: 16, scale: 0.94 }, { y: 0, scale: 1, duration: 0.16, ease: "power2.out", immediateRender: false }, gs);
    tl.set(g, { opacity: 0 }, ge);
    $$(".w", g).forEach((w) => {
      const ws = +w.dataset.ws, we = +w.dataset.we;
      if (w.classList.contains("hot")) {
        tl.fromTo(w, { scale: 1 }, { scale: 1.12, duration: 0.1, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, ws);
      } else {
        tl.set(w, { color: "#ffd31a" }, ws);
        tl.set(w, { color: "#ffffff" }, we);
      }
    });
  });

  // ---------- cards ----------
  const marks = (root, t) => {
    const m = $$(".mark-bg", root);
    if (m.length) tl.fromTo(m, { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.inOut", stagger: 0.2, immediateRender: false }, t);
  };
  const fmt = (v, dec) => Number(v).toLocaleString("en-IN", { minimumFractionDigits: dec, maximumFractionDigits: dec });

  R.cards.forEach((c) => {
    const root = document.getElementById(c.id);
    const s = c.start, e = c.end;
    const exitAt = e - 0.3;

    if (c.type === "hook") {
      tl.fromTo($(".kicker", root), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, s);
      tl.fromTo($(".hook-title", root), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }, s + 0.12);
      marks(root, s + 0.6);
      tl.to($(".hook", root), { y: -40, opacity: 0, duration: 0.3, ease: "power2.in" }, exitAt);
    }

    if (c.type === "keyword") {
      const lines = $$(".kw-line", root);
      tl.fromTo($$(".kw-bg", root), { scaleX: 0 }, { scaleX: 1, duration: 0.28, ease: "power3.out", stagger: 0.12 }, s);
      tl.fromTo($$(".kw-text", root), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.3, ease: "power2.out", stagger: 0.12 }, s + 0.12);
      tl.fromTo(lines, { rotation: -2 }, { rotation: 0, duration: 0.5, ease: "back.out(2)" }, s);
      tl.to($(".kw", root), { y: -30, opacity: 0, duration: 0.25, ease: "power2.in" }, exitAt);
    }

    if (c.type === "headline") {
      const clip = $(".clipping", root);
      tl.fromTo(clip, { y: 180, rotation: -9, opacity: 0 }, { y: 0, rotation: -2, opacity: 1, duration: 0.7, ease: "back.out(1.3)" }, s);
      marks(root, s + 0.8);
      tl.to(clip, { y: -60, opacity: 0, duration: 0.3, ease: "power2.in" }, exitAt);
    }

    if (c.type === "stat") {
      const num = $(".stat-val", root);
      const o = { v: c.from };
      tl.fromTo(root.querySelector(".stat"), { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }, s);
      tl.to(o, { v: c.value, duration: 1.2, ease: "power2.out", onUpdate: () => { num.textContent = fmt(o.v, c.decimals); } }, s + 0.15);
      tl.fromTo($(".stat-bar", root), { width: 0 }, { width: 420, duration: 0.6, ease: "power2.out" }, s + 0.5);
      tl.fromTo($$(".stat-label, .stat-src", root), { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.15 }, s + 0.6);
      marks(root, s + 1.1);
      tl.to($(".stat", root), { opacity: 0, scale: 0.95, duration: 0.3, ease: "power2.in" }, exitAt);
    }

    if (c.type === "map") {
      tl.fromTo($(".map-wrap", root), { scale: 0.85, opacity: 0, rotation: -3 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.6, ease: "power3.out" }, s);
      const hl = $$("path.hl", root);
      tl.to(hl, { fill: "#c22b22", duration: 0.35, stagger: 0.3, ease: "power1.out" }, s + 0.6);
      tl.fromTo(hl, { scale: 1 }, { scale: 1.06, transformOrigin: "50% 50%", duration: 0.18, yoyo: true, repeat: 1, stagger: 0.3, immediateRender: false }, s + 0.6);
      tl.fromTo($$(".map-side > *", root), { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.18 }, s + 0.35);
      marks(root, s + 0.9);
      tl.to($$(".map-wrap, .map-side", root), { opacity: 0, duration: 0.3 }, exitAt);
    }

    if (c.type === "timeline") {
      tl.fromTo($$(".kicker, .tl-title", root), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, s);
      marks(root, s + 0.4);
      tl.fromTo($(".tl-line", root), { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.inOut" }, s + 0.2);
      $$(".tl-item", root).forEach((it, i) => {
        const t = s + 0.9 + i * c.step;
        tl.fromTo($(".tl-dot", it), { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(2.5)" }, t);
        tl.fromTo($$(".tl-year, .tl-text", it), { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out", stagger: 0.08 }, t + 0.05);
      });
      tl.to($$(".kicker, .tl-title, .tl-line, .tl-item", root), { opacity: 0, duration: 0.3 }, exitAt);
    }

    if (c.type === "term") {
      tl.fromTo($(".term", root), { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.55, ease: "power3.out" }, s);
      tl.fromTo($(".term .kicker", root), { scaleX: 0 }, { scaleX: 1, transformOrigin: "0 50%", duration: 0.35, ease: "power2.out" }, s + 0.3);
      tl.fromTo($$(".term-body .tw", root), { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.035 }, s + 0.6);
      marks(root, s + 0.7);
      tl.to($(".term", root), { x: 80, opacity: 0, duration: 0.3, ease: "power2.in" }, exitAt);
    }

    if (c.type === "compare") {
      tl.fromTo($(".cmp-col.a", root), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, s);
      tl.fromTo($(".cmp-col.b", root), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, s + 0.15);
      tl.fromTo($$(".cmp-col.a li", root), { x: -20, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, stagger: c.step }, s + 0.6);
      tl.fromTo($$(".cmp-col.b li", root), { x: 20, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, stagger: c.step }, s + 0.6 + c.step * 0.5);
      tl.to($(".cmp", root), { opacity: 0, y: 30, duration: 0.3, ease: "power2.in" }, exitAt);
    }
  });

  window.__timelines["reel"] = tl;
})();
