"""Inline fonts and images into demo.src.html -> demo.html (one self-contained file)."""
import base64, pathlib
here = pathlib.Path(__file__).parent
b64 = lambda p: base64.b64encode((here / "assets" / p).read_bytes()).decode()
html = (here / "demo.src.html").read_text()
for key, f in {"FONT_B": "NimbusSans-Bold.otf", "FONT_BI": "NimbusSans-BoldItalic.otf",
               "BG01": "bg-01-himalaya.jpg", "BG04": "bg-04-parliament.jpg"}.items():
    html = html.replace("{{%s}}" % key, b64(f))
(here / "demo.html").write_text(html)
print("demo.html", len(html) // 1024, "KB")
