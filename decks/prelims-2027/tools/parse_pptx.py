"""Read the source .pptx into a plain JSON model (positions in 1920x1080 px, 1pt = 2px)."""
import json, re, sys, zipfile, hashlib
from xml.dom import minidom

EMU = 6350.0
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def kids(el, ns, name):
    return [c for c in el.childNodes if c.nodeType == 1 and c.namespaceURI == ns and c.localName == name]
def kid(el, ns, name):
    k = kids(el, ns, name); return k[0] if k else None
def find(el, ns, name):
    r = el.getElementsByTagNameNS(ns, name); return r[0] if r.length else None

def color(fill):
    if fill is None: return None
    c = find(fill, A, "srgbClr")
    if c is None: return None
    al = find(c, A, "alpha")
    return {"hex": "#" + c.getAttribute("val"), "a": int(al.getAttribute("val")) / 100000 if al else 1}

def xfrm(sppr):
    x = find(sppr, A, "xfrm")
    off, ext = find(x, A, "off"), find(x, A, "ext")
    return {"x": int(off.getAttribute("x")) / EMU, "y": int(off.getAttribute("y")) / EMU,
            "w": int(ext.getAttribute("cx")) / EMU, "h": int(ext.getAttribute("cy")) / EMU,
            "rot": int(x.getAttribute("rot") or 0) / 60000}

def shadow(sppr):
    s = find(sppr, A, "outerShdw")
    if s is None: return None
    c = color(s)
    return {"blur": int(s.getAttribute("blurRad")) / EMU, "dist": int(s.getAttribute("dist")) / EMU, "a": c["a"] if c else .5}

def text(body):
    bp = find(body, A, "bodyPr")
    paras = []
    for p in kids(body, A, "p"):
        ppr = kid(p, A, "pPr")
        algn = ppr.getAttribute("algn") if ppr else "l"
        ls = find(ppr, A, "spcPct") if ppr else None
        runs = []
        for r in kids(p, A, "r"):
            rp = kid(r, A, "rPr"); t = kid(r, A, "t")
            runs.append({"t": "".join(n.data for n in t.childNodes if n.nodeType == 3) if t else "",
                         "sz": int(rp.getAttribute("sz") or 1800) / 100 * 2,
                         "b": rp.getAttribute("b") == "1", "i": rp.getAttribute("i") == "1",
                         "spc": int(rp.getAttribute("spc") or 0) / 100 * 2,
                         "color": color(kid(rp, A, "solidFill"))})
        end = kid(p, A, "endParaRPr")
        paras.append({"algn": algn or "l", "lnSpc": int(ls.getAttribute("val")) / 100000 if ls else None,
                      "runs": runs, "endSz": int(end.getAttribute("sz")) / 100 * 2 if end and end.getAttribute("sz") else None})
    return {"anchor": bp.getAttribute("anchor"), "paras": paras}

def main(src, out, media_out):
    z = zipfile.ZipFile(src)
    pres = minidom.parseString(z.read("ppt/presentation.xml"))
    prels = minidom.parseString(z.read("ppt/_rels/presentation.xml.rels"))
    rmap = {r.getAttribute("Id"): r.getAttribute("Target") for r in prels.getElementsByTagName("Relationship")}
    slides, media = [], {}
    for n, sid in enumerate(pres.getElementsByTagNameNS(P, "sldId"), 1):
        path = "ppt/" + rmap[sid.getAttributeNS(R, "id")]
        relp = path.replace("slides/", "slides/_rels/") + ".rels"
        rels = {r.getAttribute("Id"): r.getAttribute("Target") for r in minidom.parseString(z.read(relp)).getElementsByTagName("Relationship")}
        doc = minidom.parseString(z.read(path))
        tree = find(doc, P, "spTree")
        els = []
        for el in tree.childNodes:
            if el.nodeType != 1: continue
            if el.localName == "pic":
                emb = find(el, A, "blip").getAttributeNS(R, "embed")
                target = rels[emb].split("/")[-1]
                data = z.read("ppt/media/" + target)
                key = hashlib.md5(data).hexdigest()[:10] + "." + target.split(".")[-1]
                media[key] = data
                sppr = kid(el, P, "spPr")
                els.append({"k": "pic", "src": key, "name": find(el, P, "cNvPr").getAttribute("descr").split("p27/")[-1],
                            **xfrm(sppr), "shadow": shadow(sppr)})
            elif el.localName == "sp":
                sppr = kid(el, P, "spPr")
                geom = find(sppr, A, "prstGeom").getAttribute("prst")
                adj = find(sppr, A, "gd")
                g = xfrm(sppr)
                e = {"k": "sp", "geom": geom, **g, "fill": color(kid(sppr, A, "solidFill")), "shadow": shadow(sppr)}
                if geom == "roundRect":
                    e["radius"] = (int(adj.getAttribute("fmla").split()[1]) / 100000 if adj else .16667) * min(g["w"], g["h"])
                tb = kid(el, P, "txBody")
                if tb is not None and any(r["t"] for p in text(tb)["paras"] for r in p["runs"]):
                    e["text"] = text(tb)
                els.append(e)
        notes = ""
        for t, rel in rels.items():
            if "notesSlide" in rel:
                nd = minidom.parseString(z.read("ppt/notesSlides/" + rel.split("/")[-1]))
                notes = "\n".join("".join(t.firstChild.data for t in p.getElementsByTagNameNS(A, "t") if t.firstChild)
                                  for p in nd.getElementsByTagNameNS(A, "p")).strip()
                notes = re.sub(r"^\d+\s*$", "", notes, flags=re.M).strip()
        slides.append({"n": n, "els": els, "notes": notes})
    import os
    os.makedirs(media_out, exist_ok=True)
    for k, d in media.items():
        open(os.path.join(media_out, k), "wb").write(d)
    json.dump(slides, open(out, "w"), indent=1)
    print(len(slides), "slides,", len(media), "media files")

if __name__ == "__main__":
    main(*sys.argv[1:4])
