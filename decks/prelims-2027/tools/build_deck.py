"""Build the animated deck: model.json + deck_config.py + media -> prelims-2027.html (one file)."""
import base64, io, json, pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import deck_config as C

model = json.load(open(ROOT / "model.json"))
media_cache = {}

def webp(key, kind):
    if key in media_cache: return key
    im = Image.open(ROOT / "media" / key)
    b = io.BytesIO()
    if im.mode in ("RGBA", "LA", "P"):
        im.convert("RGBA").save(b, "WEBP", quality=92, alpha_quality=100, method=6)
    else:
        im.convert("RGB").save(b, "WEBP", quality=84 if kind == "bg" else 90, method=6)
    media_cache[key] = ("data:image/webp;base64," + base64.b64encode(b.getvalue()).decode(), im.size)
    return key

def inside(a, b):  # centre of a inside box b
    cx, cy = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
    return b["x"] <= cx <= b["x"] + b["w"] and b["y"] <= cy <= b["y"] + b["h"]

def box(e): return {k: round(e[k], 2) for k in ("x", "y", "w", "h", "rot")}

def rgba(c):
    if not c: return None
    h = c["hex"]; r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return f"rgba({r},{g},{b},{c['a']:.3f})" if c["a"] < 1 else h

def run_text(e): return "".join(r["t"] for p in e["text"]["paras"] for r in p["runs"])

def build_slide(s):
    n, els = s["n"], s["els"]
    items, alias = [], {}
    used = set()
    for i, e in enumerate(els):
        if i in used: continue
        it = {"id": i}
        if e["k"] == "pic":
            if i == 0 and e["w"] > 1900:
                it.update(role="bg", src=webp(e["src"], "bg"))
            elif e["name"] in C.NATIVE:
                it.update(role="native", kind=C.NATIVE[e["name"]], box=box(e))
            elif e["name"].startswith("dg/"):
                spec = C.SLICES.get(e["name"], {"parts": []})
                src = webp(e["src"], "dg"); W, H = media_cache[e["src"]][1]
                parts = spec["parts"]
                if not spec.get("overlay"):
                    for a in range(len(parts)):
                        for b in range(a + 1, len(parts)):
                            ra, rb = parts[a]["r"], parts[b]["r"]
                            ov = min(ra[0] + ra[2], rb[0] + rb[2]) - max(ra[0], rb[0]) > 0.5 and min(ra[1] + ra[3], rb[1] + rb[3]) - max(ra[1], rb[1]) > 0.5
                            assert not ov, (n, e["name"], parts[a]["name"], parts[b]["name"])
                it.update(role="chart", src=src, nat=[W, H], box=box(e), parts=parts, gs=spec.get("gs"), overlay=bool(spec.get("overlay")), name=e["name"])
            else:
                it.update(role="pic", src=webp(e["src"], "cut"), box=box(e), shadow=e["shadow"])
        else:
            t = e.get("text")
            fill = e["fill"]
            if not t and fill and fill["hex"] == "#000000" and e["w"] > 1900:
                it.update(role="band", box=box(e), fill=rgba(fill))
            elif not t and fill and fill["hex"] == "#FFFFFF" and i + 1 < len(els) and els[i + 1]["k"] == "pic":
                p = els[i + 1]; used.add(i + 1); alias[i + 1] = i
                it.update(role="paper", box=box(e), src=webp(p["src"], "cut"),
                          pic={"x": round(p["x"] - e["x"], 2), "y": round(p["y"] - e["y"], 2), "w": round(p["w"], 2), "h": round(p["h"], 2)},
                          shadow=e["shadow"], fx=C.FX.get((n, i + 1), "drop"))
            elif not t and e["geom"] == "roundRect" and fill and fill["hex"] == "#000000":
                it.update(role="card", box=box(e), fill=rgba(fill), radius=round(e["radius"], 2))
            elif not t and e["geom"] == "roundRect" and fill and i + 1 < len(els) and els[i + 1].get("text") and abs(els[i + 1]["x"] - e["x"]) < 1 and abs(els[i + 1]["y"] - e["y"]) < 1:
                used.add(i + 1); alias[i] = i + 1; it["id"] = i + 1
                it.update(role="tile", box=box(e), fill=rgba(fill), radius=round(e["radius"], 2), text=els[i + 1]["text"])
            elif not t and e["h"] < 12:
                it.update(role="rule", box=box(e), fill=rgba(fill))
            elif t:
                tx = run_text(e)
                role = "num" if e["x"] > 1700 and e["y"] > 990 else "footer" if e["y"] > 990 else "kicker" if e["y"] < 100 else "text"
                maxsz = max(r["sz"] for p in t["paras"] for r in p["runs"])
                import re
                count = bool(re.fullmatch(r"\+?[\d,]{1,5}(%| h)?", tx.strip())) and maxsz >= 140
                it.update(role=role, box=box(e), text=t, title=(maxsz >= 76 and not count), count=count)
            else:
                it.update(role="shape", box=box(e), fill=rgba(fill))
        items.append(it)
    byid = {}
    for it in items:
        byid[it["id"]] = it
    for a, b in alias.items():
        byid[a] = byid[b]

    # steps: normalise actions; record first step each item appears in
    steps = []
    first = {}
    for k, raw in enumerate(C.STEPS.get(n, []), 1):
        acts = []
        for a in raw:
            if isinstance(a, int):
                it = byid[a]; acts.append({"t": "reveal", "id": it["id"]}); first.setdefault(it["id"], k)
            elif a[0] == "s":
                it = byid[a[1]]; acts.append({"t": "slices", "id": it["id"], "names": a[2]}); first.setdefault(it["id"], k)
                known = {p["name"] for p in it["parts"]}
                assert set(a[2]) <= known, (n, set(a[2]) - known)
            elif a[0] == "f":
                acts.append({"t": "focus", "id": byid[a[1]]["id"], "names": a[2]})
            elif a[0] == "z":
                acts.append({"t": "zoom", "id": byid[a[1]]["id"], "frac": a[2] if len(a) > 2 else None})
            elif a[0] == "zr":
                acts.append({"t": "zoomr", "r": a[1]})
            elif a[0] == "o":
                acts.append({"t": "out"})
            elif a[0] == "n":
                acts.append({"t": "native", "id": byid[a[1]]["id"], "phase": a[2]})
        steps.append(acts)
    chrome = {"bg", "band", "num", "footer", "kicker"}
    for it in items:
        if it["role"] in chrome: it["step"] = 0
        elif it["role"] != "card": it["step"] = first.get(it["id"], 0)
    # a card arrives with the first thing it holds
    for it in items:
        if it["role"] == "card":
            held = [o for o in items if o is not it and o["role"] not in chrome and o["role"] != "card" and "box" in o and inside(o["box"], it["box"])]
            it["step"] = min((o["step"] for o in held), default=0)
            for o in held: o.setdefault("card", it["id"])
    return {"n": n, "items": items, "steps": steps, "notes": s["notes"]}

slides = [build_slide(s) for s in model]
fonts = {k: base64.b64encode((ROOT / "assets" / f).read_bytes()).decode() for k, f in (("B", "NimbusSans-Bold.otf"), ("BI", "NimbusSans-BoldItalic.otf"))}
tpl = (ROOT / "tools" / "deck.template.html").read_text()
html = (tpl.replace("{{FONT_B}}", fonts["B"]).replace("{{FONT_BI}}", fonts["BI"])
        .replace("{{MEDIA_JSON}}", json.dumps({k: v[0] for k, v in media_cache.items()}))
        .replace("{{DECK_JSON}}", json.dumps(slides, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")))
out = ROOT / "prelims-2027.html"
out.write_text(html)
print(f"{out.name}: {len(slides)} slides, {len(html) / 1e6:.1f} MB, {sum(len(s['steps']) for s in slides)} clicks after the openers")
