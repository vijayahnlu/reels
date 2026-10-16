"""Demo v4: monochrome editorial collage (scanline figures, glitched windows, grain). Writes deck/elevate-demo-v4.html."""
import base64, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
src = (ROOT / "tools/demo_v4.src.html").read_text()
f = lambda name: base64.b64encode((ROOT / "assets/fonts" / name).read_bytes()).decode()
chars = lambda t: "".join(f'<span class="ch">{E(c) if c != " " else "&nbsp;"}</span>' for c in t)
words = lambda t: "".join(f'<span class="w">{E(w)}{"&nbsp;" if i < len(t.split()) - 1 else ""}</span>' for i, w in enumerate(t.split()))

# S02 code column: the voiceover's own list (district, degree, firm, hobby) written as data
code = [
    '<span class="k">// two years: same books, same questions</span>',
    'syllabus.shared   = <span class="k">true</span>',
    '',
    '<span class="k">// the last stage</span>',
    'candidate = {',
    '  district : "████████",',
    '  degree   : "████████",',
    '  firm     : "████████",',
    '  hobbies  : ["hatha yoga"],',
    '}',
    '',
    'syllabus.shared   = <span class="k">false</span>',
    'syllabus          = <span class="hl">candidate</span>',
]
code_html = "".join(f'<span class="cl" style="display:block">{l or "&nbsp;"}</span>' for l in code)

page = (src.replace("{{FONT_400}}", f("inter-tight-latin-400-normal.woff2")).replace("{{FONT_500}}", f("inter-tight-latin-500-normal.woff2"))
        .replace("{{FONT_600}}", f("inter-tight-latin-600-normal.woff2"))
        .replace("{{MONO_400}}", f("jetbrains-mono-latin-400-normal.woff2")).replace("{{MONO_500}}", f("jetbrains-mono-latin-500-normal.woff2"))
        .replace("{{Q1}}", chars("Where is the Bihar School of Yoga located?"))
        .replace("{{Q2}}", chars("What is Yoga Nidra, and why do people do it?"))
        .replace("{{Q3}}", chars("If you were offered Moksha right now, would you accept?"))
        .replace("{{CODE}}", code_html)
        .replace("{{BIG}}", '<div>' + words("You are the") + '</div><div>' + words("syllabus now.") + '</div>')
        .replace("{{STMT}}", words("They've read it more carefully than you wrote it."))
        .replace("{{LOGO}}", (ROOT / "assets/brand/civilsdaily-logo.svg").read_text())
        .replace("{{GSAP}}", (ROOT / "assets/vendor/gsap.min.js").read_text()))
out = ROOT / "deck/elevate-demo-v4.html"; out.write_text(page); print(out.name, len(page) // 1024, "KB")
