"""Build the animated ELEVATE IGP launch deck from Vijaya's PPT (IGP_Launch_-Vijaya.pptx).

Layout, text, colours and logo follow the PPT exactly (its 960x540 positions doubled to a 1920x1080 stage).
On top of that sit the motion pieces from the ELEVATE v6 deck: grain, stippled light that blooms and moves,
game-icons.net silhouettes (CC BY 3.0) that illustrate the line on screen, and click-by-click builds.
The engine, light renderer and motion helpers are reused from videos/elevate-igp-2026/tools/deck_v6.src.html.
Run: python3 decks/igp-launch/tools/build.py
"""
import base64, html, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
DECK = HERE.parent
REPO = DECK.parent.parent
ELV = REPO / "videos/elevate-igp-2026"
E = html.escape
ICONS = json.load(open(ELV / "assets/icons/game-icons-subset.json"))
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def ic(name):
    return re.sub(r'\sfill="[^"]*"', "", ICONS[name])


def sil(name, cx, cy, size, tone="ink", cls="", style=""):
    rim = " rim" if tone == "ink" else ""
    return (f'<svg class="sil{rim} {cls}" style="left:{cx - size / 2:.0f}px;top:{cy - size / 2:.0f}px;width:{size}px;height:{size}px;{style}" '
            f'viewBox="0 0 512 512"><g class="{tone}">{ic(name)}</g></svg>')


def words(t):
    ws = t.split()
    return "".join(f'<span class="w">{E(w)}{" " if i < len(ws) - 1 else ""}</span>' for i, w in enumerate(ws))


def T(text, x, y, size, cls="", style=""):
    """A text box from the PPT, at its own position (already doubled)."""
    return f'<div class="t {cls}" style="left:{x}px;top:{y}px;font-size:{size}px;{style}">{text}</div>'


S = {}   # n -> (markup, lights)

# ---------------- slide 1 · every year, the highest scorers ----------------
rows_l = [("Komal", "216", 470), ("Sumit", "198", 610), ("Zenden", "210", 750)]
m = [T("ELEVATE IGP  ·  PERSONALITY TEST", 96, 74, 22, "label"),
     T(f'<div>{words("Every year, the")}</div><div>{words("highest scorers.")}</div>', 96, 150, 76, "title")]
for i, (name, score, y) in enumerate(rows_l):
    m.append(f'<div class="row rl">{T(E(name), 96, y, 62, "name")}{T(f"<span class=n>{score}</span>", 820, y + 6, 52, "score")}'
             f'<div class="rule" style="left:96px;top:{y + 96}px;width:1024px"></div></div>')
m.append(f'<div class="row rr">{T("Shashwat", 960, 460, 62, "name")}{T("<span class=n>210</span>", 1378, 470, 52, "score")}</div>')
m.append(f'<div class="row rr">{T("Aniket", 960, 616, 62, "name")}{T("Rank <span class=n>48</span>", 1378, 632, 52, "score")}</div>')
m.append(T('Many more<span class="dots">' + "".join('<span class="d">.</span>' for _ in range(13)) + '</span>', 996, 878, 62, "name more"))
m.append(sil("podium-winner", 1560, 255, 360, cls="pod"))
crowd = [(1560 + k * 66, 930 + (k % 2) * 10, 118 - (k % 3) * 12) for k in range(6)]
m.append("".join(sil("person", x, y, s, cls="crowd") for x, y, s in crowd))
S[1] = ("".join(m), [[1560, 150, 220, 1.05],          # behind the winner
                     [1300, 900, 360, 0.0, 70],         # a glint that runs along each rule
                     [865, 546, 70, 0.0, 12], [865, 686, 70, 0.0, 12], [865, 826, 70, 0.0, 12],   # score glints, left
                     [1425, 546, 70, 0.0, 12], [1450, 708, 90, 0.0, 12],                       # score glints, right
                     [1730, 880, 260, 0.8, 120]])        # the crowd behind "many more"

SLIDE_CSS = """
#stage { background:#0E1113; }
.t { position:absolute; white-space:nowrap; font-weight:700; color:var(--fg); }
.label { letter-spacing:6.4px; color:var(--amber); }
.title { letter-spacing:-3px; line-height:1.17; }
.name { letter-spacing:-3px; }
.score { color:var(--amber); letter-spacing:-0.5px; font-variant-numeric:tabular-nums; }
.rule { position:absolute; height:2px; background:#2A2E31; transform-origin:0 50%; }
.dots .d { display:inline-block; }
#logo { left:auto; right:41px; top:37px; width:216px; opacity:1; }
#logo img { display:block; width:100%; height:auto; }
"""

# speaker notes straight from the PPT
NOTES = {"s01": "Every year, the highest scorers in the personality test come out of this programme. Komal. Sumit. Zenden. "
                "Different profiles, different states, four different boards between them."}

src = (ELV / "tools/deck_v6.src.html").read_text()
# the PPT's type (Arimo; Liberation Sans has the same metrics) and colours
src = re.sub(r'@font-face \{ font-family:"Inter Tight".*?\n', "", src)
src = src.replace('@font-face { font-family:"JetBrains Mono"; font-weight:400;',
                  '@font-face { font-family:"Arimo"; font-weight:400; src:url(data:font/ttf;base64,{{ARIMO_400}}) format("truetype"); }\n'
                  '@font-face { font-family:"Arimo"; font-weight:700; src:url(data:font/ttf;base64,{{ARIMO_700}}) format("truetype"); }\n'
                  '@font-face { font-family:"JetBrains Mono"; font-weight:400;', 1)
src = src.replace('font-family:"Inter Tight", "Helvetica Neue", Arial, sans-serif;', 'font-family:"Arimo", Arial, "Helvetica Neue", sans-serif;')
src = src.replace("--bg:#1a1614; --fg:#EFE7DE; --muted:#9C938A; --ink:#0d0a09; --amber:#EA9458;",
                  "--bg:#0E1113; --fg:#F2EFE9; --muted:#8C9196; --ink:#06080a; --amber:#C8642A;")
src = src.replace("<title>ELEVATE IGP 2026</title>", "<title>ELEVATE IGP Launch</title>")
# cooler base under the light, to match the PPT's #0E1113
src = src.replace("base[y * W + x] = 0.105 * Math.max(0.25, 1 - 0.55 * d);", "base[y * W + x] = 0.075 * Math.max(0.3, 1 - 0.5 * d);")
src = src.replace("var r = (b + lit) * 255, gg = b * 222 + lit * 238, bb = b * 196 + lit * 214;",
                  "var r = b * 190 + lit * 246, gg = b * 228 + lit * 240, bb = b * 255 + lit * 232;")
assert "{{ARIMO_400}}" in src and "lit * 246" in src and "0.075" in src

slides, lights = [], {}
for n in sorted(S):
    markup, lt = S[n]
    sid = f"s{n:02d}"
    lights[sid] = [[round(v, 1) for v in l] for l in lt]
    slides.append(f'<section class="slide" id="{sid}" data-keep="0"><div class="exit">{markup}</div></section>')

fonts = ELV / "assets/fonts"
for k, v in {
    "{{ARIMO_400}}": b64(DECK / "assets/LiberationSans-Regular.ttf"), "{{ARIMO_700}}": b64(DECK / "assets/LiberationSans-Bold.ttf"),
    "{{MONO_400}}": b64(fonts / "jetbrains-mono-latin-400-normal.woff2"), "{{MONO_500}}": b64(fonts / "jetbrains-mono-latin-500-normal.woff2"),
    "{{SLIDE_CSS}}": SLIDE_CSS, "{{SLIDES}}": "\n".join(slides),
    "{{LOGO}}": f'<img alt="Civilsdaily IAS" src="data:image/png;base64,{b64(DECK / "assets/civilsdaily-pill.png")}">',
    "{{NOTES}}": json.dumps(NOTES, ensure_ascii=False).replace("</", "<\\/"), "{{LIGHTS}}": json.dumps(lights),
    "{{BUILDERS}}": (HERE / "slides.js").read_text(), "{{GSAP}}": (ELV / "assets/vendor/gsap.min.js").read_text(),
}.items():
    src = src.replace(k, v)
assert "{{" not in src
out = DECK / "igp-launch-demo.html"
out.write_text(src)
print(f"{out.relative_to(REPO)}: {len(slides)} slide(s), {len(src) // 1024} KB")
