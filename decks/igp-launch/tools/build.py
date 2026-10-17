"""Build igp-launch.html: Vijaya's IGP launch deck (IGP_Launch_-Vijaya.pptx), animated, one click per build.

Every text box, rule and picture comes from model.json (tools/parse_pptx.py) at its own place, size, colour and
weight. On top of that each slide gets the pieces from the ELEVATE v6 deck: grain, stippled light that blooms
and moves, game-icons.net silhouettes (CC BY 3.0) that illustrate the line on screen, highlight boxes drawn over
the questionnaire screenshots, and count-ups. The engine, light renderer and motion helpers are reused from
videos/elevate-igp-2026/tools/deck_v6.src.html; what each click plays is in tools/slides.js.
Run: python3 tools/build.py
"""
import base64, html, json, math, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
DECK = HERE.parent
REPO = DECK.parent.parent
ELV = REPO / "videos/elevate-igp-2026"
E = html.escape
ICONS = json.load(open(ELV / "assets/icons/game-icons-subset.json"))
MODEL = json.load(open(DECK / "model.json"))
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FG = "#F2EFE9"


def ic(name):
    return re.sub(r'\sfill="[^"]*"', "", ICONS[name])


def sil(name, cx, cy, size, tone="ink", cls="", style=""):
    rim = " rim" if tone == "ink" else ""
    return (f'<svg class="sil{rim} {cls}" style="left:{cx - size / 2:.0f}px;top:{cy - size / 2:.0f}px;width:{size}px;height:{size}px;{style}" '
            f'viewBox="0 0 512 512"><g class="{tone}">{ic(name)}</g></svg>')


def pt(cx, cy, size, ix, iy):
    return round(cx - size / 2 + ix * size / 512), round(cy - size / 2 + iy * size / 512)


def hl(x, y, w, h, cls="hl", r=6):
    """An amber box drawn over a part of a screenshot."""
    return (f'<svg class="hlbox {cls}" style="left:{x - 8}px;top:{y - 8}px;width:{w + 16}px;height:{h + 16}px" viewBox="0 0 {w + 16} {h + 16}">'
            f'<rect class="glow" x="8" y="8" width="{w}" height="{h}" rx="{r}"/><rect class="stroke" x="8" y="8" width="{w}" height="{h}" rx="{r}"/></svg>')


def cap(text, x, y, cls="", style=""):
    return f'<div class="cap abs {cls}" style="left:{x}px;top:{y}px;{style}">{text}</div>'


# ---------------- PPT elements ----------------
CHARS = {(1, 13), (27, 4)}       # text boxes that animate letter by letter


def render_text(n, i, e):
    x, y, w, h = e["box"]
    l, t, r, b = e["ins"]
    just = {"t": "flex-start", "ctr": "center", "b": "flex-end"}[e["anchor"]]
    paras = []
    for p in e["paras"]:
        lh = p["lh"]
        lhcss = f"{lh}px" if lh and lh > 3 else (f"{lh * 1.17:.3f}" if lh else "1.17")
        line, spans = 0, []
        for run in p["runs"]:
            if run.get("br"):
                spans.append("<br>"); line += 1; continue
            st = f'font-size:{run["sz"]}px;font-weight:{700 if run["b"] else 400};color:{run["c"] or FG};letter-spacing:{run["spc"]}px'
            if run["i"]:
                st += ";font-style:italic"
            if (n, i) in CHARS:
                inner = "".join(f'<span class="c">{E(c)}</span>' for c in run["t"])
            else:
                inner = "".join(f'<span class="w" data-l="{line}">{E(wd)}</span>' for wd in re.split(r"(?<= )", run["t"]) if wd)
            spans.append(f'<span style="{st}">{inner}</span>')
        align = {"l": "left", "ctr": "center", "r": "right"}.get(p["algn"], "left")
        paras.append(f'<div class="p" style="text-align:{align};line-height:{lhcss}">{"".join(spans)}</div>')
    return (f'<div class="e tx" style="left:{x}px;top:{y}px;width:{w}px;min-height:{h}px;padding:{t}px {r}px {b}px {l}px;justify-content:{just}">'
            f'{"".join(paras)}</div>')


def render(n, i, e):
    x, y, w, h = e["box"]
    if e["k"] == "text":
        return render_text(n, i, e)
    if e["k"] == "shape":
        rule = w > 4 * h
        rad = "50%" if e["geom"] == "ellipse" else "0"
        return (f'<div class="e sh{" rule" if rule else ""}" style="left:{x}px;top:{y}px;width:{w}px;height:{max(h, 2)}px;'
                f'background:{e["fill"]};border-radius:{rad};transform:rotate({e["rot"]}deg)"></div>')
    return f'<img class="e im" alt="" src="{{{{IMG:{e["src"]}}}}}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'


# ---------------- what each slide adds: silhouettes, highlight boxes, lights ----------------
ADD = {}

# 1 · every year, the highest scorers
crowd = [(1620 + k * 56, 930 + (k % 2) * 8, 100 - (k % 3) * 10) for k in range(5)]
ADD[1] = (sil("podium-winner", 1560, 255, 360, cls="pod") + "".join(sil("person", x, y, s, cls="crowd") for x, y, s in crowd),
          [[1560, 150, 220, 1.05], [1300, 900, 90, 0.0, 10],
           [865, 546, 70, 0.0, 12], [865, 686, 70, 0.0, 12], [865, 826, 70, 0.0, 12],
           [1425, 546, 70, 0.0, 12], [1450, 708, 90, 0.0, 12], [1735, 880, 220, 0.8, 120]])

# 2 · the three toppers on YouTube: a ring is drawn round each score
ADD[2] = ('<svg class="rings abs" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" viewBox="0 0 1920 1080">'
          '<ellipse class="ring" cx="136" cy="142" rx="118" ry="74"/><ellipse class="ring" cx="566" cy="462" rx="130" ry="70"/>'
          '<ellipse class="ring" cx="436" cy="814" rx="88" ry="58"/></svg>'
          '<div class="sheen"></div>', [])

# 3 · the same process produced all three
three = [(1330, 800), (1530, 800), (1730, 800)]
ADD[3] = ("".join(sil("person", x, y, 260, cls="three") for x, y in three),
          [[x, 690, 120, 0.95] for x, y in three] + [[1530, 640, 360, 1.15, 300]])

# 4 · you are the syllabus now
labels = [("District", 1150, 330, ""), ("Degree", 1680, 250, ""), ("Firm", 1720, 600, ""), ("Hobby", 1170, 720, "acc")]
ADD[4] = (sil("person", 1520, 600, 820, cls="fig") +
          "".join(cap(f"· {t}", x, y, "plab " + c, f"font-size:30px;color:{'var(--amber)' if c else 'var(--fg)'}") for t, x, y, c in labels),
          [[1520, 400, 320, 1.05], [1520, 1030, 420, 0.45, 70]])

# 5 · 275 marks: as heavy as an optional, and the widest spread
hx, hy, hs = 1520, 470, 460
ADD[5] = (sil("scales", 1520, 470, 440, cls="sc") + sil("histogram", hx, hy, hs, cls="hist"),
          [[1520, 450, 300, 1.0], [*pt(hx, hy, hs, 184, 110), 130, 1.15], [*pt(hx, hy, hs, 272, 380), 100, 0.7]])


# 6 and 24 · numbered lists: an icon for each row, lit as the row is named
def row_icons(ys, names, x=1640):
    return ("".join(sil(nm, x, y, 84, cls="ri") for y, nm in zip(ys, names)),
            [[x, y, 95, 0.95] for y in ys])


ADD[6] = row_icons([355, 481, 607, 733, 859], ["notebook", "files", "newspaper", "scales", "round-table"])
ADD[24] = row_icons([352, 474, 596, 718], ["files", "newspaper", "india-gate", "notebook"])

# 7 · repair the DAF
ADD[7] = (sil("notebook", 1560, 400, 380, cls="fig") + sil("magnifying-glass", 1500, 380, 220, cls="lens"),
          [[1560, 400, 280, 1.05]])

# 8 · five entries: each row of the table is boxed and numbered
T8 = [(299, 377), (377, 488), (488, 567), (567, 649), (649, 796)]
ADD[8] = ("".join(hl(337, a, 1181, b - a, "row") for a, b in T8) +
          "".join(f'<div class="badge" style="left:276px;top:{(a + b) // 2 - 24}px">{k + 1}</div>' for k, (a, b) in enumerate(T8)),
          [[960, 520, 900, 0.55, 380]])

# 9 · 20 defects
ADD[9] = (sil("checklist", 1520, 470, 440, cls="fig") +
          '<div class="abs mono ctr" style="left:1220px;width:600px;top:740px;text-align:center;font-size:40px;letter-spacing:.08em;color:var(--fg)">'
          '<span class="c20" style="color:var(--amber)">0</span> / 20 defects</div>',
          [[1520, 470, 300, 0.75], [1520, 280, 300, 0.95, 44]])

# 10 · stop guessing, find out
ADD[10] = (sil("uncertainty", 1580, 330, 340, cls="q1") + sil("light-bulb", 1580, 330, 360, cls="q2"), [[1580, 320, 280, 1.15]])

CAM = {}   # slides whose screenshot gets a camera move; these highlight boxes ride inside its frame

# 11 · the questionnaire cover: the two marked lines
CAM[11] = hl(1052, 640, 176, 30, "m1", 4) + hl(286, 680, 1080, 32, "m2", 4)
ADD[11] = ("", [[950, 500, 900, 0.5, 330]])

# 12 · every entry opens a door: the question column
cells = [(299, 377), (377, 488), (488, 567), (567, 649), (649, 796)]
ADD[12] = (hl(1329, 295, 180, 507, "col", 4) + "".join(hl(1333, a + 4, 172, b - a - 8, "cell", 3) for a, b in cells),
           [[960, 520, 900, 0.5, 380], [1418, 300, 90, 0.0, 40]])

# 13 · two words on the form
yicons = ["body-balance", "sun", "yin-yang", "meditation", "india-gate"]
ADD[13] = (hl(549, 340, 138, 30, "py", 3) + "".join(sil(nm, 1088, 712 + k * 46, 38, tone="cream", cls="yi") for k, nm in enumerate(yicons)),
           [[570, 520, 560, 0.5, 330], [1470, 360, 380, 0.7, 120]])

# 14 · the register: two dated instances
CAM[14] = hl(338, 378, 866, 35, "r1", 4) + hl(338, 538, 936, 35, "r2", 4)
ADD[14] = ("", [[950, 490, 900, 0.5, 330]])

# 15 · the safe entry: Q10 and its OPINION tag
CAM[15] = hl(362, 497, 1118, 36, "q10", 4) + hl(1246, 608, 104, 33, "tag10", 4)
ADD[15] = (sil("drama-masks", 1660, 900, 250, cls="masks"),
           [[950, 460, 900, 0.5, 300], [1660, 900, 200, 1.0]])

# 16 · topic list and exact wording
ADD[16] = (sil("scroll-unfurled", 1540, 380, 400, cls="scroll") + sil("fountain-pen", 1810, 690, 160, cls="pen") +
           '<div class="abs mono ty quote" style="position:absolute;left:1290px;top:740px;width:560px;font-size:28px;line-height:1.45;color:var(--fg)">'
           + "".join(f'<span class="ch">{E(c)}</span>' for c in "“Why do you only do asanas and not pranayam?”") + '<span class="cur"></span></div>',
           [[1540, 380, 280, 1.0], [1570, 790, 320, 0.5, 90]])

# 17 · the CA questionnaire
ADD[17] = (sil("newspaper", 1560, 380, 380, cls="fig") +
           '<div class="abs mono" style="left:1310px;width:500px;top:650px;text-align:center;font-size:38px;letter-spacing:.06em;color:var(--fg)">'
           '~<span class="c200" style="color:var(--amber)">0</span> questions</div>',
           [[1560, 380, 280, 1.05]])

# 18 · recite vs what you make of it
ADD[18] = (sil("open-book", 1580, 460, 400, cls="k1") + sil("think", 1580, 440, 420, cls="k2"), [[1580, 460, 280, 0.6], [1580, 400, 300, 1.15]])

# 19 · weekly opinion matrix
cellsm = "".join(f'<div class="cell" style="left:{c * 98}px;top:{r * 78}px"></div>' for r in range(4) for c in range(5))
ADD[19] = (sil("calendar", 1330, 250, 170, cls="cal") + f'<div class="abs matrix" style="left:1270px;top:400px;width:476px;height:298px">{cellsm}</div>',
           [[1508, 550, 340, 0.85, 270], [1330, 250, 120, 0.9]])

# 20 · 30 to 40 percent: a ring fills to the band
R, CX, CY = 190, 1600, 650
circ = 2 * math.pi * R
ADD[20] = (f'<svg class="donut abs" style="left:{CX - 260}px;top:{CY - 260}px;width:520px;height:520px" viewBox="-260 -260 520 520">'
           f'<circle r="{R}" class="track"/><circle r="{R}" class="band" style="stroke-dasharray:{circ * .1:.1f} {circ:.1f};stroke-dashoffset:{-circ * .3:.1f}"/>'
           f'<circle r="{R}" class="arc" style="stroke-dasharray:0 {circ:.1f}" data-c="{circ:.1f}"/>'
           f'<text class="pc" y="22" text-anchor="middle">30–40%</text><text class="pcs" y="76" text-anchor="middle">TAKE A POSITION</text></svg>',
           [[CX, CY, 300, 0.9]])

# 21 · tagged OPINION, choose a side
ADD[21] = (hl(274, 356, 1357, 41, "q55", 4) + hl(694, 404, 120, 33, "tag55", 4) +
           sil("scales", 1650, 790, 250, cls="sc", style="transform-origin:50% 22%"),
           [[960, 384, 900, 0.5, 150], [1650, 780, 180, 1.0]])

# 22 · four moves, then stop
stx, sty, sts = 1500, 560, 400
STEPS22 = [pt(stx, sty, sts, 32 + 64 * k, 448 - 64 * k) for k in (1, 3, 5, 6)]
ADD[22] = (sil("stairs", stx, sty, sts, cls="fig") + sil("person", STEPS22[0][0], STEPS22[0][1] - 52, 110, cls="walker"),
           [[STEPS22[0][0], STEPS22[0][1] - 90, 130, 1.15], [stx, sty, 330, 0.22]])

# 23 · Wikipedia and the newspaper come later
ADD[23] = (sil("globe", 1440, 380, 300, cls="g1") + sil("newspaper", 1720, 400, 260, cls="g2") + sil("notebook", 1600, 760, 200, cls="g3"),
           [[1580, 390, 330, 1.0, 230], [1600, 760, 150, 0.0]])

# 25 · winning the argument; three types kept locked
ADD[25] = (sil("sword-clash", 1640, 290, 300, cls="fig") + "".join(sil("padlock", x + 330, 568, 60, tone="cream", cls="lock") for x in (96, 656, 1216)),
           [[1640, 270, 200, 1.3]])

# 26 · this is the floor
ADD[26] = (sil("stairs-goal", 1660, 600, 440, cls="fig"), [[*pt(1660, 600, 440, 385, 85), 200, 1.2], [1620, 720, 360, 0.3]])

# 27 · enrol: poster, QR, number
ADD[27] = ('<div class="scan" style="left:1426px;top:236px;width:432px"></div><div class="sheen"></div>',
           [[1642, 452, 300, 0.9], [700, 900, 700, 0.5, 120]])

# ---------------- page ----------------
SLIDE_CSS = """
#stage { background:#0E1113; }
.e { position:absolute; }
.tx { display:flex; flex-direction:column; color:var(--fg); }
.tx .w, .tx .c { display:inline-block; white-space:pre; }
.rule { transform-origin:0 50%; }
.im { box-shadow:0 30px 90px rgba(0,0,0,.55); }
.hlbox { position:absolute; overflow:visible; pointer-events:none; }
.hlbox .stroke { fill:none; stroke:var(--amber); stroke-width:4; }
.hlbox .glow { fill:rgba(234,148,88,.16); stroke:rgba(234,148,88,.35); stroke-width:14; filter:blur(6px); }
.badge { position:absolute; width:48px; height:48px; border-radius:24px; background:var(--amber); color:#14100d; font:700 26px/48px Arimo, Arial, sans-serif; text-align:center; }
.ring { fill:none; stroke:var(--amber); stroke-width:6; filter:drop-shadow(0 0 10px rgba(234,148,88,.7)); }
.sheen { position:absolute; inset:0; pointer-events:none; background:linear-gradient(105deg, transparent 40%, rgba(255,255,255,.16) 50%, transparent 60%); background-size:300% 100%; background-position:120% 0; mix-blend-mode:screen; }
.scan { position:absolute; height:4px; background:var(--amber); box-shadow:0 0 18px 4px rgba(234,148,88,.7); opacity:0; }
.matrix .cell { position:absolute; width:84px; height:64px; border:1.5px solid rgba(242,239,233,.38); border-radius:4px; background:rgba(234,148,88,0); }
.donut circle { fill:none; stroke-width:34; }
.donut .track { stroke:#23282c; }
.donut .band { stroke:rgba(242,239,233,.22); transform:rotate(-90deg); }
.donut .arc { stroke:var(--amber); transform:rotate(-90deg); }
.donut .pc { fill:var(--fg); font:700 74px Arimo, Arial, sans-serif; letter-spacing:-2px; }
.donut .pcs { fill:var(--muted); font:500 22px "JetBrains Mono", monospace; letter-spacing:.14em; }
#s02 .e.im:first-child { animation:drift 26s ease-in-out infinite alternate; transform-origin:50% 50%; }
@keyframes drift { from { transform:scale(1) rotate(0deg); } to { transform:scale(1.09) rotate(2.5deg); } }
#logo { left:auto; right:41px; top:37px; width:216px; opacity:1; transition:opacity .5s; }
#logo img { display:block; width:100%; height:auto; }
body.nologo #logo { opacity:0 !important; }
"""

slides, lights, notes = [], {}, {}
for s in MODEL:
    n = s["n"]
    sid = f"s{n:02d}"
    add, lt = ADD.get(n, ("", []))
    parts = []
    for i, e in enumerate(s["els"]):
        if n in CAM and e["k"] == "img":
            # the screenshot sits in a fixed frame; the camera moves inside it, carrying its highlight boxes along
            x, y, w, h = e["box"]
            inner = re.sub(r'class="hlbox ([^"]*)" style="left:(-?\d+)px;top:(-?\d+)px',
                           lambda m: f'class="hlbox {m.group(1)}" style="left:{int(m.group(2)) - x}px;top:{int(m.group(3)) - y}px', CAM[n])
            img = render(n, i, dict(e, box=[0, 0, w, h]))
            parts.append(f'<div class="cam" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden;border-radius:2px">'
                         f'<div class="cami" style="position:absolute;inset:0">{img}{inner}</div></div>')
        else:
            parts.append(render(n, i, e))
    body = "".join(parts)
    # over screenshots the highlights sit on top; elsewhere the silhouettes sit behind the text
    markup = body + add if n in (2, 8, 11, 12, 13, 14, 15, 21, 27) else add + body
    slides.append(f'<section class="slide" id="{sid}" data-keep="0" data-logo="{1 if s["logo"] else 0}"><div class="exit">{markup}</div></section>')
    lights[sid] = [[round(v, 1) for v in l] for l in lt]
    notes[sid] = "" if s["notes"].strip().isdigit() else s["notes"]

src = (ELV / "tools/deck_v6.src.html").read_text()
src = re.sub(r'@font-face \{ font-family:"Inter Tight".*?\n', "", src)
src = src.replace('@font-face { font-family:"JetBrains Mono"; font-weight:400;',
                  '@font-face { font-family:"Arimo"; font-weight:400; src:url(data:font/ttf;base64,{{ARIMO_400}}) format("truetype"); }\n'
                  '@font-face { font-family:"Arimo"; font-weight:700; src:url(data:font/ttf;base64,{{ARIMO_700}}) format("truetype"); }\n'
                  '@font-face { font-family:"JetBrains Mono"; font-weight:400;', 1)
src = src.replace('font-family:"Inter Tight", "Helvetica Neue", Arial, sans-serif;', 'font-family:"Arimo", Arial, "Helvetica Neue", sans-serif;')
src = src.replace("--bg:#1a1614; --fg:#EFE7DE; --muted:#9C938A; --ink:#0d0a09; --amber:#EA9458;",
                  "--bg:#0E1113; --fg:#F2EFE9; --muted:#7D7B75; --ink:#06080a; --amber:#C8642A;")
src = src.replace("<title>ELEVATE IGP 2026</title>", "<title>ELEVATE IGP Launch</title>")
src = src.replace("base[y * W + x] = 0.105 * Math.max(0.25, 1 - 0.55 * d);", "base[y * W + x] = 0.075 * Math.max(0.3, 1 - 0.5 * d);")
src = src.replace("var r = (b + lit) * 255, gg = b * 222 + lit * 238, bb = b * 196 + lit * 214;",
                  "var r = b * 190 + lit * 246, gg = b * 228 + lit * 240, bb = b * 255 + lit * 232;")
# the Civilsdaily pill shows on the slides that had it in the PPT
src = src.replace("d.el.style.visibility = 'visible'; cur = i;",
                  "d.el.style.visibility = 'visible'; cur = i; document.body.classList.toggle('nologo', d.el.dataset.logo !== '1');")
assert "{{ARIMO_400}}" in src and "lit * 246" in src and "0.075" in src and "nologo" in src

page = src
for k, v in {
    "{{ARIMO_400}}": b64(DECK / "assets/LiberationSans-Regular.ttf"), "{{ARIMO_700}}": b64(DECK / "assets/LiberationSans-Bold.ttf"),
    "{{MONO_400}}": b64(ELV / "assets/fonts/jetbrains-mono-latin-400-normal.woff2"),
    "{{MONO_500}}": b64(ELV / "assets/fonts/jetbrains-mono-latin-500-normal.woff2"),
    "{{SLIDE_CSS}}": SLIDE_CSS, "{{SLIDES}}": "\n".join(slides),
    "{{LOGO}}": f'<img alt="Civilsdaily IAS" src="data:image/png;base64,{b64(DECK / "assets/civilsdaily-pill.png")}">',
    "{{NOTES}}": json.dumps(notes, ensure_ascii=False).replace("</", "<\\/"), "{{LIGHTS}}": json.dumps(lights),
    "{{BUILDERS}}": "var C = " + json.dumps({"STEPS22": STEPS22, "H5": pt(hx, hy, hs, 184, 110)}) + ";\n" + (HERE / "slides.js").read_text(),
    "{{GSAP}}": (ELV / "assets/vendor/gsap.min.js").read_text(),
}.items():
    page = page.replace(k, v)
page = re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: f"data:image/{'jpeg' if m.group(1).endswith('.jpg') else 'png'};base64,{b64(DECK / 'media' / m.group(1))}", page)
assert "{{" not in page
out = DECK / "igp-launch.html"
out.write_text(page)
print(f"{out.relative_to(REPO)}: {len(slides)} slides, {len(page) // 1024} KB")
