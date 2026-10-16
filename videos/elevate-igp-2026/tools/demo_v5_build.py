"""Demo v5: one recognisable illustration per thought (game-icons.net silhouettes, CC BY 3.0). Writes deck/elevate-demo-v5.html."""
import base64, html, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
src = (ROOT / "tools/demo_v5.src.html").read_text()
icons = json.load(open(ROOT / "assets/icons/game-icons-subset.json"))
f = lambda name: base64.b64encode((ROOT / "assets/fonts" / name).read_bytes()).decode()
chars = lambda t: "".join(f'<span class="ch">{E(c) if c != " " else "&nbsp;"}</span>' for c in t)
words = lambda t: "".join(f'<span class="w">{E(w)}{"&nbsp;" if i < len(t.split()) - 1 else ""}</span>' for i, w in enumerate(t.split()))

def icon(name):  # drop the icon's own fill so the deck's print texture applies
    return re.sub(r'\sfill="[^"]*"', "", icons[name])
src = re.sub(r"\{\{ICON:([a-z-]+)\}\}", lambda m: icon(m.group(1)), src)

# S02: the person is filled with the four entries the voiceover names
cycle = ["district", "degree", "firm", "hobby"]
lines = []
for i, y in enumerate(range(24, 512, 13)):
    seq = (cycle[i % 4:] + cycle[:i % 4]) * 3
    parts = "".join(f'<tspan class="hl">{w} </tspan>' if (w == "hobby" and i % 3 == 0) else f"{w} " for w in seq)
    lines.append(f'<text class="wordfill wf" x="140" y="{y}">{parts}</text>')
src = src.replace("{{WORDFILL}}", "".join(lines))

page = (src.replace("{{FONT_400}}", f("inter-tight-latin-400-normal.woff2")).replace("{{FONT_500}}", f("inter-tight-latin-500-normal.woff2"))
        .replace("{{FONT_600}}", f("inter-tight-latin-600-normal.woff2"))
        .replace("{{MONO_400}}", f("jetbrains-mono-latin-400-normal.woff2")).replace("{{MONO_500}}", f("jetbrains-mono-latin-500-normal.woff2"))
        .replace("{{Q1}}", chars("Where is the Bihar School of Yoga located?"))
        .replace("{{Q2}}", chars("What is Yoga Nidra, and why do people do it?"))
        .replace("{{Q3}}", chars("If you were offered Moksha right now, would you accept?"))
        .replace("{{BIG}}", '<div>' + words("You are the") + '</div><div>' + words("syllabus now.") + '</div>')
        .replace("{{STMT}}", words("They've read it more carefully than you wrote it."))
        .replace("{{LOGO}}", (ROOT / "assets/brand/civilsdaily-logo.svg").read_text())
        .replace("{{GSAP}}", (ROOT / "assets/vendor/gsap.min.js").read_text()))
out = ROOT / "deck/elevate-demo-v5.html"; out.write_text(page); print(out.name, len(page) // 1024, "KB")
