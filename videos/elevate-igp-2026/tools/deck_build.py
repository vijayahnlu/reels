"""Build the click-through presenting deck: deck/elevate-igp-2026-deck.html (one self-contained file).

Same 39 slides, layouts and motions as the HyperFrames scenes (tools/build.py); here every build plays
on a click instead of on a clock, so the presenter sets the pace live. Run: python3 tools/deck_build.py
"""
import base64, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build as B
from slides import SLIDES

# ---------- speaker notes: the locked voiceover for each slide ----------
spec = (ROOT / "BUILD_SPEC.md").read_text()
NOTES = {}
for sid, body in re.findall(r"\n### S(\d\d)\n(.*?)(?=\n### S\d\d\n|\n## 6\.)", spec, re.S):
    vo = body.split("**vo:**", 1)[1].split("\n---")[0].strip()
    NOTES[int(sid)] = re.sub(r"^\*\((.*)\)\*$", r"(\1)", vo)

# ---------- what each click plays. P(t) marks a hold: the deck stops there until the next click ----------
T0 = "0.25"
JS = {
"quote_stack": """
  var lines = root.querySelectorAll('.ty'), t = T0;
  lines.forEach(function (ln, i) {
    if (i > 0) { P(t); t += 0.05; tl.set(lines[i - 1].querySelector('.cur'), { opacity: 0 }, t); }
    t = ELV.typeOn(tl, ln, t, 1.2);
  });""",
"statement": """
  ELV.fadeUp(tl, root.querySelectorAll('.w'), T0, { stagger: 0.07, dur: 0.9 });""",
"title": """
  var t = ELV.fadeUp(tl, root.querySelectorAll('.wordmark .w'), T0, { stagger: 0.07, dur: 1.0, y: 30 });
  ELV.fadeUp(tl, root.querySelector('.sub'), t - 0.3, { dur: 0.9 });""",
"stat_hero": """
  var num = root.querySelector('.num');
  ELV.fadeUp(tl, num, T0, { dur: 0.6 });
  var t = ELV.countUp(tl, num, T0, +num.dataset.to, { dur: 1.5 });
  ELV.fadeUp(tl, root.querySelector('.suf'), t - 0.1, { dur: 0.6 });""",
"stacked_lines": """
  var t = T0;
  root.querySelectorAll('.block > div').forEach(function (r, i) {
    if (i > 0) { P(t); t += 0.05; }
    t = ELV.stagger(tl, [r], t, 0);
  });""",
"scorecard": """
  ELV.fadeUp(tl, root.querySelector('.card'), T0, { dur: 0.9 });
  var t = ELV.fadeUp(tl, root.querySelectorAll('.c1,.c2,.c3,.c4'), T0 + 0.3, { stagger: 0.18 });
  P(t); tl.to(root.querySelector('.val'), { color: '%(accent)s', duration: 0.7, ease: 'power2.out' }, t + 0.05);""",
"numbered_list": """
  var t = T0;
  root.querySelectorAll('.nrow').forEach(function (r, i) { if (i > 0) { P(t); t += 0.05; } t = ELV.fadeUp(tl, r, t); });""",
"section_marker": """
  var t = ELV.fadeUp(tl, root.querySelector('.secno'), T0, { dur: 0.9, y: 40 });
  t = ELV.fadeUp(tl, root.querySelectorAll('.head .w'), T0 + 0.35, { stagger: 0.06 });
  var sub = root.querySelector('.sub'); if (sub) ELV.fadeUp(tl, sub, t - 0.2);""",
"advantage": """
  var t = ELV.fadeUp(tl, root.querySelector('.lab'), T0, { dur: 0.7, y: 16 });
  t = t - 0.25;
  root.querySelectorAll('.block > div:not(.lab)').forEach(function (r, i) { if (i > 0) { P(t); t += 0.05; } t = ELV.stagger(tl, [r], t, 0); });""",
"table_reveal": """
  ELV.fadeUp(tl, root.querySelector('.thead'), T0, { dur: 0.7, y: 16 });
  var t = T0 + 0.5;
  root.querySelectorAll('.trow').forEach(function (r, i) {
    if (i > 0) { P(t); t += 0.05; }
    ELV.fadeUp(tl, r, t);
    var nEl = r.querySelector('.tnum'); t = ELV.countUp(tl, nEl, t + 0.1, +nEl.dataset.to, { dur: 1.2 });
  });""",
"stat_pair": """
  var t = T0;
  root.querySelectorAll('.pcol').forEach(function (c, i) {
    if (i > 0) { P(t); t += 0.05; }
    var nEl = c.querySelector('.pnum'); ELV.fadeUp(tl, c, t); t = ELV.countUp(tl, nEl, t, +nEl.dataset.to, { dur: 1.5 });
  });""",
"statement_hero_anchor": """
  ELV.fadeUp(tl, root.querySelectorAll('.w'), T0, { stagger: 0.09, dur: 1.0 });""",
"node_fan": """
  var centre = root.querySelector('.centre');
  tl.fromTo(centre, { scale: 1 }, { scale: %(small)s, duration: 1.1, ease: 'expo.inOut' }, 0.15);
  P(1.3);
  var conns = root.querySelectorAll('.conn'), dots = root.querySelectorAll('.dot'), nodes = root.querySelectorAll('.node');
  conns.forEach(function (c, i) {
    var len = Math.hypot(c.x2.baseVal.value - c.x1.baseVal.value, c.y2.baseVal.value - c.y1.baseVal.value);
    var at = 1.35 + i * 0.5;
    tl.fromTo(c, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: 0.45, ease: 'power2.out' }, at);
    tl.fromTo(dots[i], { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(2.2)' }, at + 0.3);
    ELV.fadeUp(tl, nodes[i], at + 0.32, { dur: 0.6, y: 12 });
  });""",
"branch_expand": """
  tl.to(root.querySelectorAll('.centre, .fan, .dot'), { opacity: 0, filter: 'blur(6px)', duration: 0.6, ease: 'power2.in' }, 0.1);
  root.querySelectorAll('.node').forEach(function (nd, i) {
    tl.fromTo(nd, { x: +nd.dataset.dx, y: +nd.dataset.dy }, { x: 0, y: 0, duration: 1.2, ease: 'expo.inOut' }, 0.2 + i * 0.07);
  });
  var t = 1.75;
  root.querySelectorAll('.bsub').forEach(function (b, i) { P(t); t = ELV.fadeUp(tl, b, t + 0.05, { y: 16 }); });""",
"instance_stamps": """
  var t = T0;
  root.querySelectorAll('.inst').forEach(function (r, i) { if (i > 0) { P(t); t += 0.05; } t = ELV.fadeUp(tl, r, t); });""",
"labelled_quotes": """
  var t = ELV.fadeUp(tl, root.querySelector('.lab'), T0, { dur: 0.7, y: 16 });
  root.querySelectorAll('.q').forEach(function (q, i) { if (i > 0) { P(t); t += 0.05; } t = ELV.fadeUp(tl, q, i === 0 ? t - 0.3 : t); });""",
"delayed_reveal": """
  var t = ELV.fadeUp(tl, root.querySelectorAll('.main .w'), T0, { stagger: 0.04 });
  ELV.fadeUp(tl, root.querySelector('.st'), t - 0.2, { dur: 0.6, y: 12 });
  P(t + 0.4);
  ELV.fadeUp(tl, root.querySelectorAll('.rev .w'), t + 0.45, { stagger: 0.06, dur: 0.9 });""",
"blank_slots": """
  var t = ELV.fadeUp(tl, root.querySelectorAll('.head .w'), T0, { stagger: 0.06 });
  t = ELV.fadeUp(tl, root.querySelector('.sub'), t - 0.3);
  P(t); t += 0.05;
  root.querySelectorAll('.slot').forEach(function (sl, i) {
    var at = t + i * 0.35;
    ELV.fadeUp(tl, sl, at);
    tl.fromTo(sl.querySelector('.blank'), { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: 'expo.out' }, at + 0.2);
  });""",
"count_stack": """
  var t = T0;
  root.querySelectorAll('.crow').forEach(function (r, i) {
    if (i > 0) { P(t); t += 0.05; }
    var e = ELV.fadeUp(tl, r, t), v = r.querySelector('.cval');
    t = v ? ELV.countUp(tl, v, t, +v.dataset.to, { dur: 1.5 }) : e;
  });""",
"closing_card": """
  var t = ELV.fadeUp(tl, root.querySelectorAll('.wordmark .w'), T0, { stagger: 0.07, dur: 1.0, y: 30 });
  t = ELV.fadeUp(tl, root.querySelector('.sub'), t - 0.4, { dur: 0.8 });
  P(t); t += 0.05;
  t = ELV.stagger(tl, root.querySelectorAll('.feat'), t, 0.3, { y: 16 });
  P(t); ELV.fadeUp(tl, root.querySelector('.cta'), t + 0.05);""",
}

# The deck plays inside 3/4 of a Zoom recording, so the smallest type is raised for legibility.
DECK_CSS_EXTRA = """
#%(id)s .stamp { font-size:28px; }
#%(id)s .label { font-size:30px; }
#%(id)s .nno { font-size:30px; width:70px; }
#%(id)s .bsub { font-size:38px; margin-top:12px; }
#%(id)s .brow { height:150px; }
#%(id)s .feat { font-size:42px; }
#%(id)s .feats { gap:12px; margin-top:48px; }
#%(id)s .cta { font-size:30px; margin-top:48px; }
#%(id)s .tag { font-size:28px; }
#%(id)s .cur { background:none; }
#%(id)s .cur::after { content:""; position:absolute; inset:0; background:%(fg)s; animation:elvBlink 1.06s steps(1) infinite; }
"""

slides_html, scripts = [], []
for n in sorted(SLIDES):
    s = SLIDES[n]
    key = "statement_hero_anchor" if n == 20 else s["layout"]
    markup, _, _ = B.LAYOUTS[key](s, n)
    sid = f"s{n:02d}"
    origin = "50% 50%" if s["layout"] in ("title", "closing_card") else "0% 50%"
    css = B.SCENE_CSS % dict(id=sid, origin=origin, anchor_top=540 - 69, **B.C) + DECK_CSS_EXTRA % dict(id=sid, **B.C)
    css = css.replace(f"#{sid} {{ position:absolute; inset:0; background:", f"#{sid} {{ position:absolute; inset:0; visibility:hidden; background:")
    # stat_hero needs its target number on the element
    markup = re.sub(r'<span class="num" id="(s\d\d-num)">(\d+)</span>', r'<span class="num" id="\1" data-to="\2">\2</span>', markup)
    slides_html.append(f'<style>{css}</style>\n<section id="{sid}" class="slide" data-n="{n}" data-keep="{1 if s.get("keep") else 0}">'
                       f'<div class="drift"><div class="exit">{markup}</div></div></section>')
    js = JS[key] % dict(accent=B.C["accent"], small=B.SMALL)
    scripts.append(f'  "{sid}": function (root, tl, P) {{ var T0 = {T0};{js}\n  }}')

fonts = {w: base64.b64encode((ROOT / "assets/fonts" / f"inter-tight-latin-{w}-normal.woff2").read_bytes()).decode() for w in (400, 500, 600)}
gsap_js = (ROOT / "assets/vendor/gsap.min.js").read_text()
motion_js = (ROOT / "assets/motion.js").read_text()
notes = {f"s{n:02d}": NOTES[n] for n in sorted(SLIDES)}

page = (ROOT / "tools/deck.template.html").read_text()
page = (page.replace("{{FONT_400}}", fonts[400]).replace("{{FONT_500}}", fonts[500]).replace("{{FONT_600}}", fonts[600])
        .replace("{{BG}}", B.C["bg"]).replace("{{FG}}", B.C["fg"]).replace("{{ACCENT}}", B.C["accent"])
        .replace("{{SLIDES}}", "\n".join(slides_html))
        .replace("{{BUILDERS}}", ",\n".join(scripts))
        .replace("{{NOTES}}", json.dumps(notes, ensure_ascii=False).replace("</", "<\\/"))
        .replace("{{GSAP}}", gsap_js).replace("{{MOTION}}", motion_js))
out = ROOT / "deck" / "elevate-igp-2026-deck.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page)
print(f"{out.relative_to(ROOT)}: {len(SLIDES)} slides, {len(page) / 1024:.0f} KB")
