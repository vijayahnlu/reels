"""Inline fonts, GSAP and the logo into the three-slide visual demo (deck/elevate-demo-v2.html)."""
import base64, html, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
src = (ROOT / "tools/demo_v2.src.html").read_text()
font = lambda w: base64.b64encode((ROOT / f"assets/fonts/inter-tight-latin-{w}-normal.woff2").read_bytes()).decode()
chars = lambda t: "".join(f'<span class="ch">{E(c) if c != " " else "&nbsp;"}</span>' for c in t)

rows = [["Law graduate", 57, "questions"], ["Home state, Bihar", 29, ""], ["Legal associate, private firm", 19, ""],
        ["Yoga, mystery novels", 18, ""], ["Debating, quizzing", 6, ""]]
rh = ""
for i, (lab, n, unit) in enumerate(rows):
    top = 290 + i * 132
    dots = "".join(f'<span class="dot" style="left:{(j // 2) * 22}px;top:{(j % 2) * 22}px"></span>' for j in range(n))
    u = f'<span class="tunit">{unit}</span>' if unit else ""
    rh += (f'<div class="rule" style="top:{top}px"></div>'
           f'<div class="trow" style="top:{top}px"><span class="tl">{E(lab)}</span><span class="dots">{dots}</span>'
           f'<span class="tnum"><span class="n">{n}</span>{u}</span></div>')

X0, Y0, R = 600, 540, 620
pts = [(round(X0 + R * math.cos(math.radians(a))), round(Y0 + R * math.sin(math.radians(a)))) for a in (-36, -18, 0, 18, 36)]
names = ["Ashtanga", "Surya Namaskar", "Hatha", "Meditation", "Yoga as policy"]
rays = "".join(f'<line class="ray fray" x1="730" y1="{Y0}" x2="{x}" y2="{y}"/>' for x, y in pts)
rays += "".join(f'<circle class="spark" r="6" fill="#F5F3EF" opacity="0" cx="730" cy="{Y0}"/>' for _ in pts)
nodes = "".join(f'<div class="ndot" style="left:{x - 8}px;top:{y - 8}px"></div><div class="node" style="left:{x + 30}px;top:{y - 34}px">{E(t)}</div>'
                for (x, y), t in zip(pts, names))
web = " ".join(f"{x},{y}" for x, y in pts)

ticks = "".join(f'<line class="tick{" major" if a % 30 == 0 else ""}" x1="0" y1="{-452 if a % 30 else -462}" x2="0" y2="-440" transform="rotate({a})"/>' for a in range(0, 360, 4))
src = src.replace("{{TICKS}}", ticks)
page = (src.replace("{{FONT_400}}", font(400)).replace("{{FONT_500}}", font(500)).replace("{{FONT_600}}", font(600))
        .replace("{{Q1}}", chars("Where is the Bihar School of Yoga located?"))
        .replace("{{Q2}}", chars("What is Yoga Nidra, and why do people do it?"))
        .replace("{{Q3}}", chars("If you were offered Moksha right now, would you accept?"))
        .replace("{{ROWS}}", rh).replace("{{RAYS}}", rays).replace("{{NODES}}", nodes).replace("{{WEB}}", web)
        .replace("{{LOGO}}", (ROOT / "assets/brand/civilsdaily-logo.svg").read_text())
        .replace("{{GSAP}}", (ROOT / "assets/vendor/gsap.min.js").read_text()))
out = ROOT / "deck/elevate-demo-v2.html"; out.write_text(page); print(out.name, len(page) // 1024, "KB")
