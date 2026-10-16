"""Demo v3: same look as v2, but every graphic depicts what the text says (deck/elevate-demo-v3.html)."""
import math, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import glyphs as G

src = (ROOT / "tools/demo_v2.src.html").read_text()

def between(s, start, end, new):
    i = s.index(start); j = s.index(end, i) + len(end)
    return s[:i] + new + s[j:]

# ---------- extra styles ----------
src = src.replace("</style>", """
.ln { fill:none; stroke:var(--fg); stroke-width:var(--sw, 3); stroke-linecap:round; stroke-linejoin:round; }
.ln.acc { stroke:var(--accent); }
.ln.dim { stroke:#55524d; }
.halo { stroke-width:2; opacity:.7; }
.fillacc { fill:var(--accent); }
.star { fill:var(--fg); opacity:.7; }
.wave { fill:none; stroke:var(--accent); stroke-width:2.5; stroke-linecap:round; stroke-dasharray:14 10; animation:breathe 2.4s linear infinite; }
@keyframes breathe { to { stroke-dashoffset:-48; } }
.qg { opacity:0; }
.mote { fill:var(--accent); opacity:0; }
.ico { position:absolute; left:0; top:50%; margin-top:-36px; overflow:visible; }
.trow .tl { padding-left:130px; width:760px !important; font-size:46px !important; white-space:nowrap; }
.ico { margin-top:-46px !important; }
</style>""", 1)

# ---------- S01: the dial holds a picture of each question ----------
ticks = "".join(f'<line class="tick{" major" if a % 30 == 0 else ""}" x1="0" y1="{-452 if a % 30 else -462}" x2="0" y2="-440" transform="rotate({a})"/>' for a in range(0, 360, 4))
motes = "".join(f'<circle class="mote" cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
                [(-60, -150, 4), (40, -170, 3), (-20, -200, 5), (70, -140, 3), (-90, -120, 3), (10, -160, 4),
                 (95, -190, 2.5), (-45, -230, 3), (30, -240, 2.5), (-110, -180, 2.5), (120, -160, 3), (0, -210, 3)])
s01 = f"""<section class="slide" id="s01">
    <div class="exit">
      <svg class="geo" viewBox="0 0 1920 1080">
        <g id="s01-rings" transform="translate(1390 470)">
          <circle class="ring" r="300"/><circle class="ring dash" r="400"/>
          <g id="s01-dial">{ticks}</g>
          <circle class="pulse" r="40"/><circle class="pulse" r="40"/><circle class="pulse" r="40"/>
          <g id="s01-orbit">
            <circle class="member" cx="0" cy="-300" r="9" fill="#55524d"/><circle class="member" cx="300" cy="0" r="9" fill="#55524d"/>
            <circle class="member" cx="0" cy="300" r="9" fill="#55524d"/><circle class="member" cx="-300" cy="0" r="9" fill="#55524d"/>
          </g>
          <g class="qg" id="qg0"><ellipse class="ln dim ripple" cx="0" cy="118" rx="80" ry="18"/><ellipse class="ln dim ripple" cx="0" cy="118" rx="150" ry="34"/>
            <g class="drop" transform="translate(0 10)">{G.pin(1.35)}</g></g>
          <g class="qg" id="qg1" transform="translate(0 50) scale(1.0)">{G.recline()}</g>
          <g class="qg" id="qg2" transform="translate(0 30)">{G.wheel(200)}<g transform="translate(0 70) scale(0.95)">{G.lotus()}</g>{motes}</g>
        </g>
      </svg>
      <div class="block low" style="gap:28px">
        <div class="ty line-s">{{{{Q1}}}}<span class="cur"></span></div>
        <div class="ty line-s">{{{{Q2}}}}<span class="cur"></span></div>
        <div class="ty line-s">{{{{Q3}}}}<span class="cur"></span></div>
      </div>
    </div>
  </section>"""
src = between(src, '<section class="slide" id="s01">', "</section>", s01)

# ---------- S21: a meditator at the hub, a symbol on every branch ----------
X0, Y0, R, HUB = 600, 540, 620, 730
pts = [(round(X0 + R * math.cos(math.radians(a))), round(Y0 + R * math.sin(math.radians(a)))) for a in (-36, -18, 0, 18, 36)]
names = ["Ashtanga", "Surya Namaskar", "Hatha", "Meditation", "Yoga as policy"]
syms = [G.sym_ashtanga(), G.sym_surya(), G.sym_hatha(), G.sym_meditation(), G.sym_policy()]
rays = "".join(f'<line class="ray fray" x1="{HUB}" y1="{Y0}" x2="{x - 40}" y2="{y}"/>' for x, y in pts)
rays += "".join(f'<circle class="spark" r="6" fill="#F5F3EF" opacity="0" cx="{HUB}" cy="{Y0}"/>' for _ in pts)
symg = "".join(f'<g class="sym" transform="translate({x} {y}) scale(1.45)" style="--sw:2.4">{sv}</g>' for (x, y), sv in zip(pts, syms))
web = " ".join(f"{x},{y}" for x, y in pts)
nodes = "".join(f'<div class="node" style="left:{x + 56}px;top:{y - 34}px">{t}</div>' for (x, y), t in zip(pts, names))
s21 = f"""<section class="slide" id="s21">
    <div class="exit">
      <svg class="geo" viewBox="0 0 1920 1080">
        <g id="s21-hub" transform="translate({HUB} {Y0})">
          <circle class="ring dash" r="96"/><circle class="ring" r="128"/>
          <g transform="translate(0 30) scale(0.5)" style="--sw:5.5">{G.lotus()}</g>
        </g>
        <polygon id="s21-web" class="web" points="{web}"/>
        {rays}{symg}
        <circle class="pulse" id="s21-pulse" cx="{HUB}" cy="{Y0}" r="30"/>
      </svg>
      <div class="centre">Practising Yoga</div>
      {nodes}
    </div>
  </section>"""
src = between(src, '<section class="slide" id="s21">', "</section>", s21)

src = src.replace("""    tl.fromTo(el, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur || 1.2, ease: 'power2.inOut' }, at);""",
"""    tl.fromTo(el, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur || 1.2, ease: 'power2.inOut' }, at);
    tl.fromTo(el, { visibility: 'hidden' }, { visibility: 'visible', duration: 0.01 }, at);   // round caps would otherwise show as dots before the line draws""")
# ---------- motion ----------
s01_js = r"""s01: function (root, tl, P) {
      var pulses = root.querySelectorAll('.pulse'), members = root.querySelectorAll('.member'), qg = root.querySelectorAll('.qg');
      call(tl, function () { lightTo(1390, 470); }, 0);
      root.querySelectorAll('#s01-rings > .ring').forEach(function (r, i) { draw(tl, r, 0.1 + i * 0.15, 1.4); });
      tl.fromTo(root.querySelectorAll('.tick'), { opacity: 0, scale: 0.6, svgOrigin: '0 0' }, { opacity: 1, scale: 1, svgOrigin: '0 0', duration: 0.9, ease: 'expo.out', stagger: 0.006 }, 0.2);
      tl.fromTo(members, { scale: 0, transformOrigin: '50% 50%' }, { scale: 1, duration: 0.6, ease: 'back.out(2.5)', stagger: 0.08 }, 0.7);
      var lines = root.querySelectorAll('.ty'), t = 1.0;
      lines.forEach(function (ln, i) {
        if (i > 0) {
          P(t); t += 0.05;
          tl.set(lines[i - 1].querySelector('.cur'), { opacity: 0 }, t);
          tl.to(qg[i - 1], { opacity: 0, scale: 0.9, filter: 'blur(10px)', svgOrigin: '0 0', duration: 0.5, ease: 'power2.in' }, t);
          t += 0.3;
        }
        var g = qg[i];
        tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.01, immediateRender: false }, t);
        g.querySelectorAll('.ln').forEach(function (el, j) { draw(tl, el, t + j * 0.07, 0.9); });
        if (i === 0) {   // the pin drops onto the ground
          tl.fromTo(g.querySelector('.drop'), { y: -150 }, { y: 0, duration: 0.9, ease: 'bounce.out', immediateRender: false }, t + 0.1);
          tl.fromTo(g.querySelectorAll('.ripple'), { scale: 0.4, svgOrigin: '0 118', opacity: 0 }, { scale: 1, svgOrigin: '0 118', opacity: 1, duration: 1.0, ease: 'expo.out', stagger: 0.12, immediateRender: false }, t + 0.8);
        }
        if (i === 1) {   // breath waves and stars come up after the body is drawn
          tl.fromTo(g.querySelectorAll('.wave, .star'), { opacity: 0 }, { opacity: 1, duration: 0.8, stagger: 0.15, immediateRender: false }, t + 1.0);
        }
        if (i === 2) {   // the wheel breaks open at the top and motes rise out of it
          var ring = g.querySelector('.wheelring'), L = ring.getTotalLength();
          tl.fromTo(ring, { strokeDasharray: L + ' 0', rotation: -90, svgOrigin: '0 0' }, { strokeDasharray: (L * 0.82) + ' ' + (L * 0.18), rotation: -58, svgOrigin: '0 0', duration: 1.1, ease: 'expo.inOut', immediateRender: false }, t + 1.3);
          tl.fromTo(g.querySelectorAll('.mote'), { opacity: 0, y: 40 }, { opacity: 1, y: -60, duration: 1.4, ease: 'power2.out', stagger: 0.07, immediateRender: false }, t + 1.5);
          tl.to(g.querySelectorAll('.mote'), { opacity: 0, y: -170, duration: 1.6, ease: 'power1.in', stagger: 0.07 }, t + 2.8);
        }
        ripple(tl, pulses[i], t, i === 2 ? 620 : 420);
        call(tl, function () { FIELD.pulse(1390, 470, i === 2 ? 1.6 : 1); }, t);
        var m = [members[i], members[(i + 2) % 4]]; if (i === 2) m.push(members[3], members[1]);
        tl.to(m, { attr: { fill: '#C8642A' }, duration: 0.4 }, t + 0.3);
        t = Math.max(typeOn(tl, ln, t, 1.2), t + (i === 2 ? 3.2 : 1.6));
      });
    },
    s18:"""
src = between(src, "s01: function (root, tl, P) {", "s18:", s01_js)

src = src.replace("""        fadeUp(tl, r.querySelector('.tl'), t, { y: 16 });""",
"""        fadeUp(tl, r.querySelector('.tl'), t, { y: 16 });
        r.querySelectorAll('.ico .ln').forEach(function (el, j) { draw(tl, el, t + 0.05 + j * 0.06, 0.8); });
        tl.fromTo(r.querySelector('.ico'), { scale: 0.7, transformOrigin: '50% 50%' }, { scale: 1, duration: 0.8, ease: 'back.out(2)' }, t);""")

s21_js = r"""s21: function (root, tl, P) {
      call(tl, function () { lightTo(600, 540); }, 0);
      var centre = root.querySelector('.centre');
      fadeUp(tl, centre, 0.1, { dur: 0.9 });
      tl.to(centre, { scale: 56 / 132, duration: 1.1, ease: 'expo.inOut' }, 0.9);
      call(tl, function () { lightTo(730, 540); }, 1.4);
      root.querySelectorAll('#s21-hub .ring, #s21-hub .ln').forEach(function (el, i) { draw(tl, el, 1.5 + i * 0.07, 1.0); });
      P(3.0);
      var rays = root.querySelectorAll('.fray'), sparks = root.querySelectorAll('.spark'), nodes = root.querySelectorAll('.node'), sy = root.querySelectorAll('.sym');
      var t = 3.05;
      call(tl, function () { lightTo(1100, 540); FIELD.pulse(730, 540, 1.3); }, t);
      ripple(tl, root.querySelector('#s21-pulse'), t, 700);
      rays.forEach(function (ray, i) {
        var at = t + 0.15 + i * 0.4;
        draw(tl, ray, at, 0.55);
        tl.fromTo(sparks[i], { opacity: 0, attr: { cx: 730, cy: 540 } }, { opacity: 1, duration: 0.05 }, at);
        tl.to(sparks[i], { attr: { cx: +ray.getAttribute('x2'), cy: +ray.getAttribute('y2') }, duration: 0.55, ease: 'power2.inOut' }, at);
        tl.to(sparks[i], { opacity: 0, duration: 0.3 }, at + 0.55);
        sy[i].querySelectorAll('.ln, .fillacc').forEach(function (el, j) {
          if (el.classList.contains('fillacc')) tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.5 }, at + 0.7);
          else draw(tl, el, at + 0.45 + j * 0.03, 0.6);
        });
        fadeUp(tl, nodes[i], at + 0.55, { y: 12, dur: 0.6 });
        call(tl, function () { FIELD.pulse(+ray.getAttribute('x2') + 40, +ray.getAttribute('y2'), 0.7); }, at + 0.55);
      });
      draw(tl, root.querySelector('#s21-web'), t + 0.15 + 5 * 0.4 + 0.3, 1.4);
      tl.fromTo(root.querySelector('#s21-web'), { fillOpacity: 0 }, { fillOpacity: 1, duration: 1.2 }, t + 2.7);
    }
  };"""
src = between(src, "s21: function (root, tl, P) {", "\n  };", s21_js)
src = src.replace("""  gsap.to('#s21 .spin-a', { rotation: 360, svgOrigin: '0 0', duration: 60, ease: 'none', repeat: -1 });
  gsap.to('#s21 .spin-b', { rotation: -360, svgOrigin: '0 0', duration: 80, ease: 'none', repeat: -1 });
""", "")

# ---------- reuse the v2 builder for fonts, rows, logo and GSAP ----------
import demo_v2_build as V2  # noqa: E402  (writes v2 as a side effect, harmless)
icons = [G.icon_scales(), G.icon_pin(), G.icon_briefcase(), G.icon_yoga_novels(), G.icon_debate()]
rows_v2 = V2.rh
# insert one icon per row, in order
parts = rows_v2.split('<div class="trow"')
rows_v3 = parts[0] + "".join('<div class="trow"' + p.replace('"><span class="tl">', f'"><svg class="ico" width="118" height="92" viewBox="-60 -45 120 90" style="--sw:3.2">{icons[i]}</svg><span class="tl">', 1)
                              for i, p in enumerate(parts[1:]))
out_src = src
# Build the final page the same way v2 does, but from the v3 source.
import base64, html as H
font = lambda w: base64.b64encode((ROOT / f"assets/fonts/inter-tight-latin-{w}-normal.woff2").read_bytes()).decode()
chars = lambda t: "".join(f'<span class="ch">{H.escape(c) if c != " " else "&nbsp;"}</span>' for c in t)
page = (out_src.replace("{{FONT_400}}", font(400)).replace("{{FONT_500}}", font(500)).replace("{{FONT_600}}", font(600))
        .replace("{{Q1}}", chars("Where is the Bihar School of Yoga located?"))
        .replace("{{Q2}}", chars("What is Yoga Nidra, and why do people do it?"))
        .replace("{{Q3}}", chars("If you were offered Moksha right now, would you accept?"))
        .replace("{{ROWS}}", rows_v3)
        .replace("{{LOGO}}", (ROOT / "assets/brand/civilsdaily-logo.svg").read_text())
        .replace("{{GSAP}}", (ROOT / "assets/vendor/gsap.min.js").read_text()))
out = ROOT / "deck/elevate-demo-v3.html"; out.write_text(page); print(out.name, len(page) // 1024, "KB")
