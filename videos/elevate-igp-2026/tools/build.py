"""Generate compositions/sNN.html (one per slide) and index.html from tools/slides.py.

Slide lengths come from the voiceover word count of each slide in BUILD_SPEC.md, scaled so every
section fills its runtime in the spec's timing map. Run: python3 tools/build.py
"""
import html, json, math, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from slides import SLIDES, SECTIONS

C = dict(bg="#0B0B0C", alt="#141416", fg="#F5F3EF", muted="#8A8780", accent="#C8642A", rule="#2A2A2D", tag="#B3261E")
E = html.escape

# ---------- voiceover word counts ----------
spec = (ROOT / "BUILD_SPEC.md").read_text()
WORDS = {}
for sid, body in re.findall(r"\n### S(\d\d)\n(.*?)(?=\n### S\d\d\n|\n## 6\.)", spec, re.S):
    vo = body.split("**vo:**", 1)[1]
    WORDS[int(sid)] = 0 if "silence" in vo else len(re.findall(r"[A-Za-z0-9']+", vo))

def words_html(text, cls="w"):
    ws = text.split(" ")  # each word keeps its own trailing space, so spacing survives inline-block layout
    return "".join(f'<span class="{cls}">{E(w)}{" " if i < len(ws) - 1 else ""}</span>' for i, w in enumerate(ws))

def chars_html(text):
    return "".join(f'<span class="ch">{E(c) if c != " " else "&nbsp;"}</span>' for c in text)

# ---------- layouts: each returns (markup, js body, seconds until its last motion ends) ----------
T0 = 0.4  # every slide starts its first motion here

def L_quote_stack(s, n):
    rows = "".join(f'<div class="ty line-s" id="s{n:02d}-l{i}">{chars_html(t)}<span class="cur"></span></div>' for i, t in enumerate(s["lines"]))
    js = """
    var lines = root.querySelectorAll('.ty'); var t = %s;
    lines.forEach(function (ln, i) {
      if (i > 0) tl.set(lines[i - 1].querySelector('.cur'), { opacity: 0 }, t);
      t = ELV.typeOn(tl, ln, t, 1.2) + 0.35;
    });
    ELV.blink(tl, lines[lines.length - 1].querySelector('.cur'), t - 0.35, DUR - 0.8);
    """ % T0
    end = T0 + len(s["lines"]) * 1.55
    return f'<div class="block low gap28">{rows}</div>', js, end

def L_statement(s, n):
    text = s["lines"][0]
    size = "hero" if s.get("hero") or len(text) <= 28 else "stmt"
    js = "var ws = root.querySelectorAll('.w'); ELV.fadeUp(tl, ws, %s, { stagger: 0.07, dur: 0.9 });" % T0
    end = T0 + 0.9 + 0.07 * len(text.split())
    return f'<div class="block mid"><div class="{size}" id="s{n:02d}-st">{words_html(text)}</div></div>', js, end

def L_title(s, n):
    mark = "".join(f'<span class="w">{c}</span>' for c in s["lines"][0])
    m = f'<div class="block center"><div class="wordmark">{mark}</div><div class="line-s muted sub" id="s{n:02d}-sub">{E(s["lines"][1])}</div></div>'
    js = """
    var t = ELV.fadeUp(tl, root.querySelectorAll('.wordmark .w'), %s, { stagger: 0.07, dur: 1.0, y: 30 });
    ELV.fadeUp(tl, root.querySelector('.sub'), t - 0.3, { dur: 0.9 });
    """ % T0
    return m, js, T0 + 1.0 + 0.07 * 6 + 0.6

def L_stat_hero(s, n):
    v = s["value"]; num, suf = re.match(r"(\d+)(.*)", v).groups()
    m = f'<div class="block low"><div class="stat"><span class="num" id="s{n:02d}-num">{num}</span><span class="suf accent">{E(suf)}</span></div></div>'
    js = """
    var num = root.querySelector('.num');
    ELV.fadeUp(tl, num, %s, { dur: 0.6 });
    var t = ELV.countUp(tl, num, %s, %s, { dur: 1.5 });
    ELV.fadeUp(tl, root.querySelector('.suf'), t - 0.1, { dur: 0.6, y: 24 });
    """ % (T0, T0, num)
    return m, js, T0 + 1.5 + 0.5

def L_stacked_lines(s, n):
    lines = s["lines"]; acc = s.get("accent", []); gb = s.get("gap_before", [])
    size = "stmt" if max(len(l) for l in lines) <= 40 else "line"
    rows = "".join(f'<div class="{size}{" accent" if i in acc else ""}{" gapb" if i in gb else ""}">{words_html(t)}</div>' for i, t in enumerate(lines))
    js = "ELV.stagger(tl, root.querySelectorAll('.block > div'), %s, 0.35);" % T0
    end = T0 + 0.35 * (len(lines) - 1) + 0.8 + 0.045 * len(lines[-1].split())
    return f'<div class="block low gap20">{rows}</div>', js, end

def L_scorecard(s, n):
    m = f'''<div class="block low"><div class="card" id="s{n:02d}-card">
      <div class="redact c1"></div>
      <div class="label muted c2">{E(s["label"])}</div>
      <div class="score c3"><span class="val" id="s{n:02d}-val">{E(s["value"])}</span></div>
      <div class="stamp c4">{E(s["footer"])}</div></div></div>'''
    js = """
    ELV.fadeUp(tl, root.querySelector('.card'), %s, { dur: 0.9 });
    var t = ELV.fadeUp(tl, root.querySelectorAll('.c1,.c2,.c3,.c4'), %s, { stagger: 0.18 });
    tl.to(root.querySelector('.val'), { color: '%s', duration: 0.6, ease: 'power2.out' }, t + 0.3);
    """ % (T0, T0 + 0.3, C["accent"])
    return m, js, T0 + 0.3 + 0.8 + 0.54 + 1.0

def L_numbered_list(s, n):
    rows = "".join(f'<div class="nrow"><span class="nno accent">{a}</span><span class="line-s">{E(b)}</span></div>' for a, b in s["items"])
    js = "ELV.stagger(tl, root.querySelectorAll('.nrow'), %s, 0.35);" % T0
    return f'<div class="block low gap24">{rows}</div>', js, T0 + 0.35 * 4 + 0.8

def L_section_marker(s, n):
    sub = f'<div class="line-s muted sub">{E(s["sub"])}</div>' if s.get("sub") else ""
    m = f'<div class="block low"><div class="secno accent">{s["number"]}</div><div class="stmt head">{words_html(s["heading"])}</div>{sub}</div>'
    js = """
    var t = ELV.fadeUp(tl, root.querySelector('.secno'), %s, { dur: 0.9, y: 40 });
    t = ELV.fadeUp(tl, root.querySelectorAll('.head .w'), %s, { stagger: 0.06 });
    var sub = root.querySelector('.sub'); if (sub) ELV.fadeUp(tl, sub, t - 0.2);
    """ % (T0, T0 + 0.35)
    return m, js, T0 + 0.35 + 0.8 + 0.06 * len(s["heading"].split()) + (0.6 if s.get("sub") else 0)

def L_advantage(s, n):
    size = "stmt" if sum(len(l) for l in s["lines"]) <= 70 else "line"
    rows = "".join(f'<div class="{size}">{words_html(l)}</div>' for l in s["lines"])
    m = f'<div class="block low gap20"><div class="label accent lab">{E(s["label"])}</div>{rows}</div>'
    js = """
    var t = ELV.fadeUp(tl, root.querySelector('.lab'), %s, { dur: 0.7, y: 16 });
    ELV.stagger(tl, root.querySelectorAll('.block > div:not(.lab)'), t - 0.25, 0.35);
    """ % T0
    return m, js, T0 + 0.7 + 0.35 * (len(s["lines"]) - 1) + 1.2

def L_table_reveal(s, n):
    rows = ""
    for a, b in s["rows"]:
        num, rest = re.match(r"(\d+)(.*)", b).groups()
        rows += f'<div class="trow"><span class="tl line-s">{E(a)}</span><span class="tr accent"><span class="tnum" data-to="{num}">{num}</span>{E(rest)}</span></div>'
    m = f'<div class="block top"><div class="thead"><span class="redact sm"></span><span class="label muted">{E(s["header"][1])}</span></div>{rows}</div>'
    js = """
    ELV.fadeUp(tl, root.querySelector('.thead'), %s, { dur: 0.7, y: 16 });
    var rows = root.querySelectorAll('.trow');
    rows.forEach(function (r, i) {
      var at = %s + i * %s;
      ELV.fadeUp(tl, r, at);
      var nEl = r.querySelector('.tnum'); ELV.countUp(tl, nEl, at + 0.1, +nEl.dataset.to, { dur: 1.2 });
    });
    """ % (T0, T0 + 0.6, s["gap"])
    return m, js, T0 + 0.6 + s["gap"] * (len(s["rows"]) - 1) + 1.3

def L_stat_pair(s, n):
    (lv, lc), (rv, rc) = s["left"], s["right"]
    word, tag = rc.split(" ")
    m = f'''<div class="block low"><div class="pair">
      <div class="pcol pl"><div class="pnum" data-to="{lv}">{lv}</div><div class="line-s muted">{E(lc)}</div></div>
      <div class="pcol pr"><div class="pnum accent" data-to="{rv}">{rv}</div><div class="line-s muted">{E(word)} <span class="tag">{E(tag)}</span></div></div>
    </div></div>'''
    js = """
    var cols = root.querySelectorAll('.pcol');
    cols.forEach(function (c, i) {
      var at = %s + i * 0.6, nEl = c.querySelector('.pnum');
      ELV.fadeUp(tl, c, at);
      ELV.countUp(tl, nEl, at, +nEl.dataset.to, { dur: 1.5 });
    });
    """ % T0
    return m, js, T0 + 0.6 + 1.5

# Practising Yoga: S20 -> S21 -> S22 share coordinates so the word and its five branches carry across cuts.
FAN_X0, FAN_Y0, FAN_R = 600, 540, 620
FAN_ANG = [-36, -18, 0, 18, 36]
FAN_PTS = [(round(FAN_X0 + FAN_R * math.cos(math.radians(a))), round(FAN_Y0 + FAN_R * math.sin(math.radians(a)))) for a in FAN_ANG]
ROW_TOP = [176 + i * 152 for i in range(5)]
SMALL = 56 / 132

def L_statement_hero_anchor(s, n):  # S20: same spot the node fan starts from
    m = f'<div class="anchorword hero" id="s{n:02d}-st">{words_html(s["lines"][0])}</div>'
    js = "ELV.fadeUp(tl, root.querySelectorAll('.w'), %s, { stagger: 0.09, dur: 1.0 });" % T0
    return m, js, T0 + 1.2

def L_node_fan(s, n):
    lines = "".join(f'<line class="conn" x1="{FAN_X0}" y1="{FAN_Y0}" x2="{x}" y2="{y}" />' for x, y in FAN_PTS)
    dots = "".join(f'<div class="dot" style="left:{x - 7}px;top:{y - 7}px"></div>' for x, y in FAN_PTS)
    labels = "".join(f'<div class="node line-s" style="left:{x + 28}px;top:{y - 34}px">{E(t)}</div>' for (x, y), t in zip(FAN_PTS, s["nodes"]))
    m = f'''<div class="anchorword hero centre">{E(s["centre"])}</div>
      <svg class="fan" width="1920" height="1080" viewBox="0 0 1920 1080">{lines}</svg>{dots}{labels}'''
    js = """
    var centre = root.querySelector('.centre');
    tl.fromTo(centre, { scale: 1 }, { scale: %s, duration: 1.1, ease: 'expo.inOut' }, 0.3);
    var conns = root.querySelectorAll('.conn'), dots = root.querySelectorAll('.dot'), nodes = root.querySelectorAll('.node');
    conns.forEach(function (c, i) {
      var len = Math.hypot(c.x2.baseVal.value - c.x1.baseVal.value, c.y2.baseVal.value - c.y1.baseVal.value);
      var at = 1.2 + i * 0.5;
      tl.fromTo(c, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: 0.45, ease: 'power2.out' }, at);
      tl.fromTo(dots[i], { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(2.2)' }, at + 0.3);
      ELV.fadeUp(tl, nodes[i], at + 0.32, { dur: 0.6, y: 12 });
    });
    """ % SMALL
    return m, js, 1.2 + 0.5 * 4 + 0.95

def L_branch_expand(s, n):
    lines = "".join(f'<line class="conn" x1="{FAN_X0}" y1="{FAN_Y0}" x2="{x}" y2="{y}" />' for x, y in FAN_PTS)
    dots = "".join(f'<div class="dot" style="left:{x - 7}px;top:{y - 7}px"></div>' for x, y in FAN_PTS)
    rows = ""
    for i, ((x, y), (lab, sub)) in enumerate(zip(FAN_PTS, s["branches"])):
        dx, dy = x + 28 - 140, y - 34 - ROW_TOP[i]
        rows += f'<div class="brow" style="top:{ROW_TOP[i]}px"><div class="node line-s" data-dx="{dx}" data-dy="{dy}">{E(lab)}</div><div class="bsub">{E(sub)}</div></div>'
    m = f'''<div class="anchorword hero centre" style="transform:scale({SMALL})">{E("Practising Yoga")}</div>
      <svg class="fan" width="1920" height="1080" viewBox="0 0 1920 1080">{lines}</svg>{dots}{rows}'''
    js = """
    var gone = root.querySelectorAll('.centre, .fan, .dot');
    tl.to(gone, { opacity: 0, filter: 'blur(6px)', duration: 0.6, ease: 'power2.in' }, 0.2);
    root.querySelectorAll('.node').forEach(function (nd, i) {
      tl.fromTo(nd, { x: +nd.dataset.dx, y: +nd.dataset.dy }, { x: 0, y: 0, duration: 1.2, ease: 'expo.inOut' }, 0.3 + i * 0.07);
    });
    ELV.stagger(tl, root.querySelectorAll('.bsub'), 1.5, 0.35, { y: 16 });
    """
    return m, js, 1.5 + 0.35 * 4 + 0.9

def L_instance_stamps(s, n):
    rows = "".join(f'<div class="inst"><div class="line-s q">{E(q)}</div><div class="stampstrip"><span class="stamp">{E(st)}</span></div></div>' for q, st in s["items"])
    js = "ELV.stagger(tl, root.querySelectorAll('.inst'), %s, %s);" % (T0, s["gap"] + 0.6)
    return f'<div class="block low gap44">{rows}</div>', js, T0 + (s["gap"] + 0.6) * 2 + 0.8

def L_labelled_quotes(s, n):
    qs = "".join(f'<div class="line-s q">{E(q)}{" <span class=tag>OPINION</span>" if i in s["tag"] else ""}</div>' for i, q in enumerate(s["quotes"]))
    m = f'<div class="block low gap32"><div class="label muted lab">{E(s["label"])}</div>{qs}</div>'
    js = """
    var t = ELV.fadeUp(tl, root.querySelector('.lab'), %s, { dur: 0.7, y: 16 });
    ELV.stagger(tl, root.querySelectorAll('.q'), t + 0.2, 0.9);
    """ % T0
    return m, js, T0 + 0.7 + 0.2 + 0.9 + 0.8

def L_delayed_reveal(s, n):
    m = f'''<div class="block low gap28"><div class="line-s main">{words_html(s["main"])}</div>
      <div class="line-s accent rev">{words_html(s["reveal"])}</div>
      <div class="stampstrip st"><span class="stamp">{E(s["stamp"])}</span></div></div>'''
    js = """
    var t = ELV.fadeUp(tl, root.querySelectorAll('.main .w'), %s, { stagger: 0.04 });
    ELV.fadeUp(tl, root.querySelector('.st'), t - 0.2, { dur: 0.6, y: 12 });
    ELV.fadeUp(tl, root.querySelectorAll('.rev .w'), t + 1.5, { stagger: 0.06, dur: 0.9 });
    """ % T0
    end = T0 + 0.8 + 0.04 * len(s["main"].split()) + 1.5 + 0.9 + 0.06 * len(s["reveal"].split())
    return m, js, end

def L_blank_slots(s, n):
    slots = "".join(f'<div class="slot"><span class="line-s">{E(t)}</span><span class="blank"></span></div>' for t in s["slots"])
    m = f'<div class="block low gap20"><div class="stmt head">{words_html(s["heading"])}</div><div class="line-s muted sub">{E(s["sub"])}</div><div class="slots">{slots}</div></div>'
    js = """
    var t = ELV.fadeUp(tl, root.querySelectorAll('.head .w'), %s, { stagger: 0.06 });
    ELV.fadeUp(tl, root.querySelector('.sub'), t - 0.3);
    root.querySelectorAll('.slot').forEach(function (sl, i) {
      var at = t + 0.4 + i * 0.35;
      ELV.fadeUp(tl, sl, at);
      tl.fromTo(sl.querySelector('.blank'), { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: 'expo.out' }, at + 0.2);
    });
    """ % T0
    return m, js, T0 + 0.8 + 0.06 * 4 + 0.4 + 0.7 + 0.9

def L_count_stack(s, n):
    rows = ""
    for pre, num, rest in s["items"]:
        big = f'<span class="cnum accent"><span class="cpre">{E(pre)}</span><span class="cval" data-to="{num}">{num}</span></span>' if num else ""
        rows += f'<div class="crow">{big}<span class="line-s{" muted" if not num else ""}">{E(rest.strip())}</span></div>'
    js = """
    root.querySelectorAll('.crow').forEach(function (r, i) {
      var at = %s + i * 1.0;
      ELV.fadeUp(tl, r, at);
      var v = r.querySelector('.cval'); if (v) ELV.countUp(tl, v, at, +v.dataset.to, { dur: 1.5 });
    });
    """ % T0
    return f'<div class="block low gap28">{rows}</div>', js, T0 + 2.0 + 1.5

def L_closing_card(s, n):
    mark = "".join(f'<span class="w">{c}</span>' for c in s["title"])
    feats = "".join(f'<div class="feat">{E(f)}</div>' for f in s["features"])
    m = f'''<div class="block center closing"><div class="wordmark">{mark}</div><div class="line-s muted sub">{E(s["subtitle"])}</div>
      <div class="feats">{feats}</div><div class="cta"><span>{E(s["cta"])}</span></div></div>'''
    js = """
    var t = ELV.fadeUp(tl, root.querySelectorAll('.wordmark .w'), %s, { stagger: 0.07, dur: 1.0, y: 30 });
    t = ELV.fadeUp(tl, root.querySelector('.sub'), t - 0.4, { dur: 0.8 });
    t = ELV.stagger(tl, root.querySelectorAll('.feat'), t, 0.35, { y: 16 });
    ELV.fadeUp(tl, root.querySelector('.cta'), t + 0.1);
    """ % T0
    return m, js, T0 + 1.42 + 0.4 + 0.35 * 4 + 0.8 + 0.9

LAYOUTS = {k[2:]: v for k, v in globals().items() if k.startswith("L_")}

# ---------- shared look, injected into every scene ----------
SCENE_CSS = """
#%(id)s { position:absolute; inset:0; background:%(bg)s; color:%(fg)s; overflow:hidden; font-kerning:normal; }
#%(id)s .drift { position:absolute; inset:0; transform-origin:%(origin)s; }
#%(id)s .exit { position:absolute; inset:0; }
#%(id)s .block { position:absolute; left:140px; right:140px; display:flex; flex-direction:column; }
#%(id)s .block.low { bottom:140px; }
#%(id)s .block.top { top:140px; }
#%(id)s .block.mid { top:0; bottom:0; justify-content:center; }
#%(id)s .block.center { top:0; bottom:0; justify-content:center; align-items:center; text-align:center; }
#%(id)s .gap20 { gap:20px; } #%(id)s .gap24 { gap:24px; } #%(id)s .gap28 { gap:28px; } #%(id)s .gap32 { gap:32px; } #%(id)s .gap44 { gap:44px; }
#%(id)s .hero { font-size:132px; font-weight:600; letter-spacing:-0.03em; line-height:1.04; }
#%(id)s .stmt { font-size:84px; font-weight:500; letter-spacing:-0.02em; line-height:1.1; max-width:1500px; }
#%(id)s .line, #%(id)s .line-s { font-size:56px; font-weight:400; letter-spacing:-0.01em; line-height:1.2; max-width:1560px; }
#%(id)s .label { font-size:26px; font-weight:600; letter-spacing:0.14em; text-transform:uppercase; }
#%(id)s .stamp { font-size:22px; font-weight:400; color:%(muted)s; }
#%(id)s .muted { color:%(muted)s; }
#%(id)s .accent { color:%(accent)s; }
#%(id)s .w { display:inline-block; white-space:pre; }
#%(id)s .gapb { margin-top:36px; }
#%(id)s .ty { position:relative; white-space:nowrap; }
#%(id)s .ch { opacity:0; }
#%(id)s .cur { position:absolute; left:0; top:0.14em; width:4px; height:1em; background:%(fg)s; opacity:0; }
#%(id)s .stat { font-size:320px; font-weight:600; letter-spacing:-0.04em; line-height:0.9; display:flex; align-items:baseline; font-variant-numeric:tabular-nums; }
#%(id)s .stat .suf { display:inline-block; }
#%(id)s .card { width:1040px; padding:64px 72px; border:1px solid %(rule)s; border-radius:28px; display:flex; flex-direction:column; gap:22px; }
#%(id)s .redact { display:block; width:380px; height:40px; border-radius:6px; background:%(muted)s; }
#%(id)s .redact.sm { width:420px; height:30px; }
#%(id)s .score { position:relative; align-self:flex-start; font-size:260px; font-weight:600; letter-spacing:-0.02em; line-height:1; }
#%(id)s .score .val { display:inline-block; }
#%(id)s .uline { position:absolute; left:0; right:0; bottom:-10px; height:4px; background:%(accent)s; transform-origin:0 50%%; transform:scaleX(0); }
#%(id)s .nrow { display:flex; align-items:baseline; gap:40px; }
#%(id)s .nno { font-size:26px; font-weight:600; letter-spacing:0.14em; width:60px; font-variant-numeric:tabular-nums; }
#%(id)s .secno { font-size:260px; font-weight:600; letter-spacing:-0.05em; line-height:0.85; margin-bottom:28px; font-variant-numeric:tabular-nums; }
#%(id)s .sub { margin-top:18px; }
#%(id)s .thead { display:flex; align-items:center; margin-bottom:34px; }
#%(id)s .trow { display:flex; justify-content:space-between; align-items:baseline; padding:26px 0; border-top:1px solid %(rule)s; }
#%(id)s .tr { font-size:56px; font-weight:600; letter-spacing:-0.02em; font-variant-numeric:tabular-nums; }
#%(id)s .pair { display:flex; gap:180px; }
#%(id)s .pnum { font-size:280px; font-weight:600; letter-spacing:-0.05em; line-height:0.9; font-variant-numeric:tabular-nums; }
#%(id)s .tag { display:inline-block; font-size:26px; font-weight:600; letter-spacing:0.14em; color:#FFFFFF; background:%(tag)s; padding:10px 16px 8px; border-radius:6px; vertical-align:middle; margin-left:14px; }
#%(id)s .anchorword { position:absolute; left:140px; top:%(anchor_top)spx; white-space:nowrap; transform-origin:0 50%%; }
#%(id)s .fan { position:absolute; left:0; top:0; }
#%(id)s .conn { stroke:%(muted)s; stroke-width:2; opacity:0.6; }
#%(id)s .dot { position:absolute; width:14px; height:14px; border-radius:50%%; background:%(accent)s; }
#%(id)s .node { position:absolute; white-space:nowrap; font-weight:500; }
#%(id)s .brow { position:absolute; left:140px; right:140px; height:140px; }
#%(id)s .brow .node { position:relative; }
#%(id)s .bsub { font-size:32px; font-weight:400; color:%(muted)s; margin-top:10px; }
#%(id)s .inst { display:flex; flex-direction:column; align-items:flex-start; gap:16px; }
#%(id)s .stampstrip { display:inline-block; background:%(alt)s; padding:10px 18px; border-radius:8px; }
#%(id)s .st { align-self:flex-start; }
#%(id)s .slots { display:flex; gap:80px; margin-top:44px; }
#%(id)s .slot { display:flex; align-items:baseline; gap:20px; }
#%(id)s .blank { display:block; width:220px; height:3px; background:%(fg)s; transform-origin:0 50%%; transform:scaleX(0); }
#%(id)s .crow { display:flex; align-items:baseline; gap:30px; }
#%(id)s .cnum { font-size:132px; font-weight:600; letter-spacing:-0.04em; line-height:1; font-variant-numeric:tabular-nums; min-width:360px; }
#%(id)s .wordmark { font-size:150px; font-weight:600; letter-spacing:0.14em; line-height:1; margin-right:-0.14em; }
#%(id)s .closing .wordmark { font-size:120px; }
#%(id)s .feats { display:flex; flex-direction:column; gap:14px; margin-top:56px; }
#%(id)s .feat { font-size:36px; font-weight:400; }
#%(id)s .cta { margin-top:56px; background:%(alt)s; border-radius:12px; padding:20px 30px; font-size:26px; color:%(muted)s; }
"""

def scene(n, s, dur):
    sid = f"s{n:02d}"
    fn = LAYOUTS["statement_hero_anchor"] if n == 20 else LAYOUTS[s["layout"]]
    markup, js, _ = fn(s, n)
    origin = "50% 50%" if s["layout"] in ("title", "closing_card") else "0% 50%"
    css = SCENE_CSS % dict(id=sid, origin=origin, anchor_top=540 - 69, **C)
    keep = s.get("keep")
    exit_js = "" if keep else "ELV.clearOut(tl, root.querySelector('.exit'), DUR);"
    drift_js = "" if s["layout"] in ("node_fan", "branch_expand") or n == 20 else "ELV.drift(tl, root.querySelector('.drift'), DUR);"
    return f"""<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><title>{sid}</title></head>
  <body>
    <template>
      <style>{css}</style>
      <div id="{sid}" data-composition-id="{sid}" data-width="1920" data-height="1080">
        <div class="drift"><div class="exit">{markup}</div></div>
      </div>
      <script>
        (function () {{
          var DUR = {dur:.2f};
          var root = document.getElementById("{sid}");
          document.fonts.ready.then(function () {{
            var tl = gsap.timeline({{ paused: true }});
            {js}
            {exit_js}
            {drift_js}
            window.__timelines["{sid}"] = tl;
            if (window.__hfForceTimelineRebind) window.__hfForceTimelineRebind();
          }});
        }})();
      </script>
    </template>
  </body>
</html>
"""

# ---------- durations ----------
ends = {}
for n, s in SLIDES.items():
    fn = LAYOUTS["statement_hero_anchor"] if n == 20 else LAYOUTS[s["layout"]]
    ends[n] = fn(s, n)[2]
DUR = {}
for a, b, total in SECTIONS:
    ids = list(range(a, b + 1))
    floor = {n: ends[n] + (SLIDES[n].get("hold") or 1.5) + 0.8 for n in ids}
    fixed, free = {}, ids[:]
    while True:  # give each slide its share of the section by voiceover words, never less than its floor
        budget = total - sum(fixed.values())
        w = sum(WORDS[n] for n in free) or 1
        share = {n: budget * WORDS[n] / w for n in free}
        low = [n for n in free if share[n] < floor[n]]
        if not low: break
        for n in low: fixed[n] = floor[n]; free.remove(n)
    DUR.update(fixed); DUR.update({n: share[n] for n in free})
DUR = {n: round(d, 2) for n, d in DUR.items()}

(ROOT / "compositions").mkdir(exist_ok=True)
for n, s in SLIDES.items():
    (ROOT / "compositions" / f"s{n:02d}.html").write_text(scene(n, s, DUR[n]))

hosts, t = [], 0.0
for n in sorted(SLIDES):
    hosts.append(f'      <div id="h{n:02d}" class="clip" data-composition-id="s{n:02d}" data-composition-src="compositions/s{n:02d}.html" '
                 f'data-start="{t:.2f}" data-duration="{DUR[n]:.2f}" data-track-index="1" data-width="1920" data-height="1080"></div>')
    t = round(t + DUR[n], 2)
total = t
index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>ELEVATE IGP 2026 launch film</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/motion.js"></script>
    <style>
      @font-face {{ font-family: "Inter Tight"; font-weight: 400; src: url("assets/fonts/inter-tight-latin-400-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter Tight"; font-weight: 500; src: url("assets/fonts/inter-tight-latin-500-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter Tight"; font-weight: 600; src: url("assets/fonts/inter-tight-latin-600-normal.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {C["bg"]}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {C["bg"]}; font-family: "Inter Tight", "Helvetica Neue", Arial, sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1920" data-height="1080" data-fps="30">
{chr(10).join(hosts)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(index)
json.dump({f"S{n:02d}": DUR[n] for n in sorted(DUR)}, open(ROOT / "tools" / "durations.json", "w"), indent=1)
print(f"{len(SLIDES)} scenes, {total:.1f}s ({int(total // 60)}:{total % 60:04.1f})")
for a, b, tot in SECTIONS:
    print(f"  S{a:02d}-S{b:02d}: {sum(DUR[n] for n in range(a, b + 1)):.1f}s (target {tot})", " ".join(f"{DUR[n]:.0f}" for n in range(a, b + 1)))
