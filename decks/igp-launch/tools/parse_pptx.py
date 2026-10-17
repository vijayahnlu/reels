"""Read IGP_Launch_-Vijaya.pptx into model.json + media/, keeping every text box, rule and picture at its own place.

Positions are doubled from the PPT's 960x540 to the deck's 1920x1080 stage. The Pitch export's own extras
(the slide-sized background rectangle, the "Try Pitch" badge and the closing Pitch advert) are left out; the
Civilsdaily pill is drawn once by the deck, so each slide only records whether it had one.
Run: python3 tools/parse_pptx.py <deck.pptx>
"""
import json, pathlib, re, sys, zipfile
from xml.dom import minidom

from PIL import Image

DECK = pathlib.Path(__file__).resolve().parent.parent
PX = 2 / 9525                      # EMU -> stage px
PT = 2 * 96 / 72 / 100             # hundredths of a point -> stage px


def attr(el, name, default=None):
    v = el.getAttribute(name) if el is not None else ""
    return v if v != "" else default


def first(el, tag):
    found = el.getElementsByTagName(tag)
    return found[0] if found else None


def box(el):
    xfrm = first(el, "a:xfrm")
    off, ext = first(xfrm, "a:off"), first(xfrm, "a:ext")
    return [round(int(attr(off, "x")) * PX), round(int(attr(off, "y")) * PX), round(int(attr(ext, "cx")) * PX), round(int(attr(ext, "cy")) * PX)]


def colour(el):
    c = first(el, "a:srgbClr") if el is not None else None
    return "#" + attr(c, "val") if c is not None else None


def paragraphs(tx):
    paras = []
    for p in tx.getElementsByTagName("a:p"):
        ppr = first(p, "a:pPr")
        lh = None
        ln = first(ppr, "a:lnSpc") if ppr is not None else None
        if ln is not None:
            pts, pct = first(ln, "a:spcPts"), first(ln, "a:spcPct")
            lh = round(int(attr(pts, "val")) * PT, 1) if pts is not None else round(int(attr(pct, "val")) / 100000, 3)
        runs = []
        for node in p.childNodes:
            if node.nodeName == "a:br":
                runs.append({"br": 1})
            elif node.nodeName == "a:r":
                rpr = first(node, "a:rPr")
                t = "".join(x.firstChild.data if x.firstChild else "" for x in node.getElementsByTagName("a:t"))
                runs.append({"t": t, "sz": round(int(attr(rpr, "sz", "1800")) * PT, 1), "b": attr(rpr, "b") == "1",
                             "i": attr(rpr, "i") == "1", "c": colour(first(rpr, "a:solidFill")) if rpr is not None else None,
                             "spc": round(int(attr(rpr, "spc", "0")) * PT, 2)})
        if any(r.get("t") for r in runs):
            paras.append({"algn": attr(ppr, "algn", "l"), "lh": lh, "runs": runs})
    return paras


def main(src):
    z = zipfile.ZipFile(src)
    media = DECK / "media"
    media.mkdir(exist_ok=True)
    slides = []
    order = re.findall(r'r:id="(rId\d+)"', z.read("ppt/presentation.xml").decode().split("<p:sldIdLst>")[1].split("</p:sldIdLst>")[0])
    prels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read("ppt/_rels/presentation.xml.rels").decode()))
    for n, rid in enumerate(order, 1):
        path = "ppt/" + prels[rid]
        doc = minidom.parseString(z.read(path))
        rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read(path.replace("slides/", "slides/_rels/") + ".rels").decode()))
        notes_t = next((t for r, t in rels.items() if "notesSlide" in t), None)
        notes = ""
        if notes_t:
            nd = minidom.parseString(z.read("ppt/" + notes_t.replace("../", "")))
            notes = "\n".join("".join(x.firstChild.data for x in p.getElementsByTagName("a:t") if x.firstChild) for p in nd.getElementsByTagName("a:p")).strip()
        if "pitch.com" in z.read(path.replace("slides/", "slides/_rels/") + ".rels").decode() and n == len(order):
            break                     # the Pitch advert at the end
        els, logo = [], False
        tree = first(doc, "p:spTree")
        for node in tree.childNodes:
            if node.nodeName == "p:pic":
                b = box(node)
                blip = first(node, "a:blip")
                target = rels[attr(blip, "r:embed")]
                if b == [29, 1009, 108, 48] or target.endswith(".svg"):
                    continue                                      # Try Pitch badge
                if b[0] == 1663 and b[1] == 37:
                    logo = True; continue
                name = pathlib.Path(target).name
                im = Image.open(z.open("ppt/media/" + name))
                photo = im.mode == "RGB" and name in ("image-2-1.png", "image-27-2.png")
                out = name.replace(".png", ".jpg") if photo else name
                if photo:
                    im.save(media / out, quality=88)
                else:
                    (media / out).write_bytes(z.read("ppt/media/" + name))
                els.append({"k": "img", "box": b, "src": out})
            elif node.nodeName == "p:sp":
                b = box(node)
                sppr = first(node, "p:spPr")
                fill = None
                for ch in sppr.childNodes:
                    if ch.nodeName == "a:solidFill":
                        fill = colour(ch)
                geom = attr(first(sppr, "a:prstGeom"), "prst", "rect")
                xfrm = first(sppr, "a:xfrm")
                rot = int(attr(xfrm, "rot", "0")) / 60000
                tx = first(node, "p:txBody")
                paras = paragraphs(tx) if tx is not None else []
                if paras:
                    bp = first(tx, "a:bodyPr")
                    ins = [round(int(attr(bp, k, d)) * PX) for k, d in (("lIns", "91440"), ("tIns", "45720"), ("rIns", "91440"), ("bIns", "45720"))]
                    els.append({"k": "text", "box": b, "anchor": attr(bp, "anchor", "t"), "ins": ins, "paras": paras})
                elif fill and not (b[2] >= 1900 and b[3] >= 1000):
                    els.append({"k": "shape", "box": b, "fill": fill, "geom": geom, "rot": rot})
        slides.append({"n": n, "logo": logo, "notes": notes, "els": els})
    (DECK / "model.json").write_text(json.dumps(slides, indent=1, ensure_ascii=False))
    print(len(slides), "slides ->", DECK / "model.json")


if __name__ == "__main__":
    main(sys.argv[1])
