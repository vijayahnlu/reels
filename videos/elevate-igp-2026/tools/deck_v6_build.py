"""Build deck/elevate-igp-2026-deck-v6.html: all 39 slides as a click deck in the backlit style.

Every picture is a game-icons.net silhouette (CC BY 3.0) standing in front of a stippled light that the slide
places and animates. Slide text is locked (tools/slides.py, BUILD_SPEC.md); speaker notes are the locked VO.
Markup and light positions live here; the motion for each slide is in tools/deck_v6.slides.js.
Run: python3 tools/deck_v6_build.py
"""
import base64, html, json, math, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
ICONS = json.load(open(ROOT / "assets/icons/game-icons-subset.json"))


def ic(name):  # drop the icon's own fill so the deck's tone classes apply
    return re.sub(r'\sfill="[^"]*"', "", ICONS[name])


def sil(name, cx, cy, size, tone="ink", cls="", style="", inner=None):
    rim = " rim" if tone == "ink" else ""
    body = inner if inner is not None else ic(name)
    return (f'<svg class="sil{rim} {cls}" style="left:{cx - size / 2:.0f}px;top:{cy - size / 2:.0f}px;width:{size}px;height:{size}px;{style}" '
            f'viewBox="0 0 512 512"><g class="{tone}">{body}</g></svg>')


def pt(cx, cy, size, ix, iy):  # a point inside a placed icon, in stage pixels
    return round(cx - size / 2 + ix * size / 512), round(cy - size / 2 + iy * size / 512)


def words(t):
    ws = t.split()
    return "".join(f'<span class="w">{E(w)}{" " if i < len(ws) - 1 else ""}</span>' for i, w in enumerate(ws))


def chars(t):
    return "".join(f'<span class="ch">{E(c) if c != " " else " "}</span>' for c in t) + '<span class="cur"></span>'


def icon_inline(name, cls, tone="cream"):
    return f'<svg class="{cls}" viewBox="0 0 512 512"><g class="{tone}" style="fill:var(--{"fg" if tone == "cream" else "ink"})">{ic(name)}</g></svg>'


S = {}   # n -> (markup, lights, keep)
LIGHT_ICON = (1460, 520)

# ---------------- S01 · three questions, one picture each ----------------
S[1] = (f"""
<div class="scene q0">
  {sil('meditation', 1400, 400, 470, cls='fig')}
  {sil('position-marker', 1730, 230, 150, tone='amber', cls='pin')}
</div>
<div class="scene q1">
  {sil('person-in-bed', 1400, 420, 620, cls='fig')}
  {sil('night-sleep', 1730, 190, 170, tone='amber', cls='moon')}
</div>
<div class="scene q2">
  {sil('breaking-chain', 1090, 420, 210, cls='chainL')}
  {sil('breaking-chain', 1710, 420, 210, cls='chainR', style='transform:scaleX(-1)')}
  {sil('meditation', 1400, 400, 500, cls='fig')}
</div>
<div class="cap abs c0" style="color:var(--fg);left:1000px;width:800px;text-align:center;top:690px">Bihar School of Yoga · <b>where?</b></div>
<div class="cap abs c1" style="color:var(--fg);left:1000px;width:800px;text-align:center;top:690px">Yoga Nidra · <b>why?</b></div>
<div class="cap abs c2" style="color:var(--fg);left:1000px;width:800px;text-align:center;top:690px">Moksha · <b>accept?</b></div>
<div class="tx" style="bottom:86px;width:1700px;display:flex;flex-direction:column;gap:16px">
  <div class="ty q">{chars("Where is the Bihar School of Yoga located?")}</div>
  <div class="ty q">{chars("What is Yoga Nidra, and why do people do it?")}</div>
  <div class="ty q">{chars("If you were offered Moksha right now, would you accept?")}</div>
</div>""", [[1400, 300, 250, 1.05], [1400, 470, 420, 0.85, 170], [1400, 330, 430, 1.25]])

# ---------------- S02 · the syllabus becomes you ----------------
labels = [("District", 1050, 430, ""), ("Degree", 1640, 300, ""), ("Firm", 1650, 620, ""), ("Hobby", 1080, 720, "acc")]
S[2] = (f"""
{sil('person', 1450, 560, 860, cls='fig')}
{''.join(f'<div class="cap abs plab {c}" style="left:{x}px;top:{y}px;font-size:30px;color:{"var(--amber)" if c else "var(--fg)"}">· {t}</div>' for t, x, y, c in labels)}
<div class="cap abs top" style="left:120px;top:190px">same books · same current affairs · same questions</div>
<div class="tx hero" style="bottom:110px"><div>{words("You are the")}</div><div>{words("syllabus now.")}</div></div>
""", [[1450, 380, 330, 1.05], [1450, 1010, 420, 0.45, 70]])

# ---------------- S03 · title: the light rises behind the name ----------------
S[3] = (f"""
<div class="abs dark wm" style="left:0;right:0;top:350px;text-align:center;font-size:230px;font-weight:600;letter-spacing:.14em;line-height:1;padding-left:.14em">{''.join(f'<span class="w">{c}</span>' for c in 'ELEVATE')}</div>
<div class="abs dark sub" style="left:0;right:0;top:630px;text-align:center;font-size:44px;font-weight:500;letter-spacing:.01em">Interview Guidance Program 2026</div>
""", [[960, 560, 820, 1.15, 300]])

# ---------------- S04 · 200+ ----------------
S[4] = (f"""
{sil('podium-winner', 1460, 560, 640, cls='fig')}
<div class="tx" style="bottom:120px">
  <div class="cap cp" style="margin-bottom:20px">Personality test · <b>top of the list</b></div>
  <div class="num-big"><span class="num">200</span><span class="suf">+</span></div>
</div>""", [[1460, 330, 300, 1.1], [1460, 900, 400, 0.4, 60]])

# ---------------- S05 · 275 marks, widest spread ----------------
hx, hy, hs = 1460, 520, 560
S[5] = (f"""
{sil('histogram', hx, hy, hs, cls='fig')}
<div class="tx lines" style="bottom:130px;width:1040px">
  <div class="stmt l1"><span class="cnt">275</span> marks.</div>
  <div class="ln l2">The widest spread of any paper you'll write.</div>
</div>""", [[hx, hy, 300, 1.0], [*pt(hx, hy, hs, 272, 380), 110, 0.7]])
S5_TOP = pt(hx, hy, hs, 184, 110)

# ---------------- S06 · scorecard, name withheld ----------------
S[6] = (f"""
<div class="card sc" style="left:120px;top:220px;width:820px;height:640px">
  <div class="lab abs" style="left:60px;top:64px">Personality Test</div>
  <div class="abs val" style="left:52px;top:170px;font-size:300px;font-weight:600;letter-spacing:-.04em;line-height:1">2__</div>
  <div class="cap abs" style="left:60px;top:540px">Elevate IGP</div>
</div>
{sil('person', 1460, 600, 820, cls='fig')}
<div class="abs redact mono" style="left:1590px;top:250px;background:var(--fg);color:#140f0c;font-size:22px;letter-spacing:.16em;padding:10px 16px">NAME WITHHELD</div>
""", [[1460, 340, 290, 1.0]])

# ---------------- S07 · hours ----------------
S[7] = (f"""
{sil('sands-of-time', 1460, 540, 560, cls='fig')}
<div class="tx lines" style="top:300px;width:1000px;gap:40px">
  <div class="ln" style="font-size:88px">Hours on Prelims?</div>
  <div class="ln" style="font-size:88px">Hours on Mains?</div>
  <div class="ln acc" style="font-size:88px">Hours on this?</div>
</div>""", [[1460, 540, 330, 1.1]])

# ---------------- S08 · written vs argued ----------------
S[8] = (f"""
<div class="scene w1">{sil('papers', 1400, 580, 440, cls='fig')}{sil('fountain-pen', 1620, 400, 300, cls='pen')}</div>
<div class="scene w2">{sil('discussion', 1460, 540, 620, cls='fig')}</div>
<div class="tx lines" style="bottom:140px;width:1050px">
  <div class="ln">In Mains you write it and it's done.</div>
  <div class="ln">Here, somebody argues with you.</div>
</div>""", [[1420, 520, 300, 1.0], [1300, 560, 170, 0.95], [1625, 560, 170, 0.95]])

# ---------------- S09 · the gap ----------------
wx, wy, ws = 1460, 500, 560
S[9] = (f"""
<svg class="sil rim fig" style="left:{wx - ws // 2}px;top:{wy - ws // 2}px;width:{ws}px;height:{ws}px" viewBox="0 0 512 512">
  <defs><mask id="gapmask"><rect width="512" height="512" fill="#fff"/><rect class="hole" x="196" y="190" width="120" height="78" fill="#000"/></mask></defs>
  <g class="ink" mask="url(#gapmask)">{ic('brick-wall')}</g></svg>
{sil('brick-pile', 1330, 880, 260, cls='pile')}
<div class="tx lines" style="bottom:140px;width:1000px">
  <div class="ln">A mock shows you the gap.</div>
  <div class="ln">It can't be the preparation itself.</div>
</div>""", [[*pt(wx, wy, ws, 256, 229), 130, 1.35], [wx, wy, 400, 0.3], [1330, 870, 170, 0.7]])

# ---------------- S10 · the five parts, in order ----------------
items = [("01", "Repair the DAF", "id-card"), ("02", "Know what's been asked of your profile", "magnifying-glass"),
         ("03", "Build opinions you can defend", "shield"), ("04", "Stay current where it touches you", "newspaper"),
         ("05", "Handle the room", "round-table")]
rows, lts = [], []
for i, (no, t, icn) in enumerate(items):
    top = 200 + i * 158
    rows.append(f'<div class="abs nrow" style="left:120px;top:{top}px;height:120px;width:1700px">'
                f'<span class="mono acc abs" style="left:0;top:40px;font-size:34px">{no}</span>'
                f'{sil(icn, 196, 60, 100, cls="ni")}'
                f'<span class="abs" style="left:300px;top:24px;font-size:64px;font-weight:500;letter-spacing:-.02em;white-space:nowrap">{E(t)}</span></div>')
    lts.append([316, top + 60, 110, 0.95])
S[10] = ("".join(rows), lts)


# ---------------- section markers ----------------
def section(no, heading, icons_html, sub=None, size=100):
    sub_html = f'<div class="ln muted sub" style="font-size:56px;margin-top:28px">{E(sub)}</div>' if sub else ""
    return (f'<div class="secno">{no}</div>{icons_html}'
            f'<div class="tx head" style="bottom:120px;width:1060px"><div class="stmt" style="font-size:{size}px">{words(heading)}</div>{sub_html}</div>')


S[11] = (section("01", "Repair the DAF", sil('notebook', 1460, 520, 520, cls='fig')), [[1460, 500, 320, 1.05]])

# ---------------- S12 · the board read your form ----------------
lamp = sil('ceiling-light', 1460, 170, 240, cls='lamp') + sil('round-table', 1460, 600, 540, cls='fig')
S[12] = (f"""
<div class="scene board">{lamp}</div>
<div class="card daf" style="left:1150px;top:290px;width:640px;height:560px">
  <div class="bar mono">DETAILED APPLICATION FORM</div>
  <div class="frow" style="top:80px"><span class="fl mono">DISTRICT</span><span class="blank"></span></div>
  <div class="frow" style="top:180px"><span class="fl mono">DEGREE</span><span class="fv">LL.B.</span></div>
  <div class="frow" style="top:280px"><span class="fl mono">EMPLOYER</span><span class="blank"></span></div>
  <div class="frow" style="top:380px;border:0"><span class="fl mono">HOBBIES</span><span class="fv">Hatha yoga</span></div>
  <svg class="marks" viewBox="0 0 640 560">
    <path class="mark" d="M36 176 C140 182 250 172 340 178"/>
    <path class="mark" d="M210 236 L236 262 L290 204"/>
    <path class="mark" d="M264 424 C262 398 160 394 92 398 C22 402 16 432 26 452 C40 478 150 484 232 476 C284 470 294 446 274 428"/>
  </svg>
</div>
<div class="tx stmt" style="bottom:110px;width:960px;font-size:96px">{words("They've read it more carefully than you wrote it.")}</div>
""", [[1460, 420, 300, 1.0, 260]])

# ---------------- S13 · what the form looks like ----------------
S[13] = (f"""
<div class="card form" style="left:1180px;top:210px;width:620px;height:560px">
  <div class="bar mono">DETAILED APPLICATION FORM</div>
  <div class="frow" style="top:80px"><span class="fl mono">HOBBIES</span><span class="blank"></span><span class="fv ty hob">{chars("reading, listening to music")}</span></div>
  <div class="frow" style="top:180px"><span class="fl mono">EXTRA-CURRICULAR</span><span class="blank"></span></div>
  <div class="frow" style="top:280px"><span class="fl mono">PRIZES</span><span class="blank"></span></div>
  <div class="frow" style="top:380px;border:0"><span class="fl mono">POSITIONS HELD</span><span class="blank"></span></div>
</div>
<div class="tx lines" style="top:260px;width:980px;gap:40px">
  <div class="ln" style="font-size:80px">Blank fields.</div>
  <div class="ln" style="font-size:80px">Casual wording.</div>
  <div class="ln" style="font-size:80px">Entries that say nothing about you.</div>
</div>""", [[1490, 490, 380, 0.95, 330]])

# ---------------- S14 · what you left out ----------------
sheet = ('<svg class="sil sheet" style="left:1590px;top:270px;width:240px;height:300px" viewBox="0 0 240 300">'
         '<rect x="10" y="10" width="220" height="280" rx="6" fill="#EFE7DE"/>'
         + "".join(f'<rect x="36" y="{y}" width="{w}" height="10" rx="3" fill="#2a2320"/>' for y, w in ((50, 150), (82, 168), (114, 120), (146, 160), (178, 100)))
         + '<rect x="36" y="220" width="96" height="30" rx="4" fill="#EA9458"/></svg>')
S[14] = (f"""
{sheet}
{sil('full-folder', 1400, 560, 520, cls='fig')}
<div class="tx lines" style="bottom:140px;width:1000px">
  <div class="ln">The real problem isn't what you put in.</div>
  <div class="ln acc">It's what you left out.</div>
</div>""", [[1400, 540, 310, 1.0], [1710, 420, 220, 1.15]])

# ---------------- S15 · 20 defects ----------------
S[15] = (f"""
{sil('checklist', 1460, 480, 520, cls='fig')}
<div class="abs mono ctr" style="left:1160px;width:600px;top:790px;text-align:center;font-size:40px;letter-spacing:.08em"><span class="c20 acc">0</span> / 20 defects</div>
<div class="tx" style="bottom:130px;width:1000px">
  <div class="lab">ELEVATE IGP</div>
  <div class="stmt l1" style="font-size:96px;margin-top:24px">{words("Your DAF, checked against 20 defects.")}</div>
</div>""", [[1460, 480, 320, 0.75], [1460, 270, 330, 0.95, 46]])

# ---------------- S16 · stop guessing, start knowing ----------------
S[16] = (section("02", "Stop guessing. Start knowing.",
                 sil('uncertainty', 1460, 500, 480, cls='q1') + sil('light-bulb', 1460, 500, 500, cls='q2')),
         [[1460, 480, 320, 1.15]])

# ---------------- S17 · not your list ----------------
S[17] = (f"""
{sil('notebook', 1220, 680, 270, cls='nb')}
{sil('files', 1580, 460, 480, cls='fig')}
<div class="tx stmt" style="bottom:120px;width:960px">{words("The Board isn't working from your list.")}</div>
""", [[1220, 680, 170, 0.95], [1580, 450, 300, 1.15]])

# ---------------- S18 · the questionnaire ----------------
trows = [("Law graduate", "57 questions", 57, "gavel"), ("Home state, Bihar", "29", 29, "position-marker"),
         ("Legal associate, private firm", "19", 19, "briefcase"), ("Yoga, mystery novels", "18", 18, "meditation"),
         ("Debating, quizzing", "6", 6, "talk")]
html18, l18 = [], []
for i, (lab, val, n, icn) in enumerate(trows):
    top = 260 + i * 148
    suffix = val.replace(str(n), "", 1)
    html18.append(f'<div class="trow" style="top:{top}px">{icon_inline(icn, "ti")}<span class="tl">{E(lab)}</span>'
                  f'<span class="tn"><span class="tnum" data-to="{n}">{n}</span><span class="muted" style="font-size:36px;font-weight:500;letter-spacing:0">{E(suffix)}</span></span></div>')
    w = 520 * n / 57
    l18.append([1040 + w / 2, top + 60, w / 2 + 18, 1.05, 20])
S[18] = (f"""<div class="cap abs thead" style="left:120px;top:180px;font-size:28px"><span style="color:var(--fg)">[PROFILE REDACTED]</span> · CSE 2026</div>{''.join(html18)}""", l18)

# ---------------- S19 · 129 and 48 ----------------
S[19] = (f"""
<div class="abs pcol c1" style="left:160px;width:800px;top:300px;text-align:center">
  <div class="dark pn" style="font-size:300px;font-weight:600;letter-spacing:-.05em;line-height:1"><span class="pnum">129</span></div>
  <div style="font-size:56px;font-weight:500;margin-top:150px">questions</div>
</div>
<div class="abs pcol c2" style="left:960px;width:800px;top:300px;text-align:center">
  <div class="dark pn" style="font-size:300px;font-weight:600;letter-spacing:-.05em;line-height:1"><span class="pnum">48</span></div>
  <div style="font-size:56px;font-weight:500;margin-top:150px">tagged <span class="tag" style="font-size:40px">OPINION</span></div>
</div>""", [[560, 450, 300, 1.05, 230], [1360, 450, 300, 1.15, 230]])

# ---------------- S20 → S21 → S22 · Practising Yoga opens up ----------------
MED = (1500, 560, 560)
HEAD = pt(*MED, 256, 70)
HERO_TOP = 540 - 75
SMALL = 0.43
centre = f'<div class="tx hero centre" style="top:{HERO_TOP}px;width:auto;white-space:nowrap;transform-origin:0% 50%">{words("Practising Yoga")}</div>'
S[20] = (f"""{sil('meditation', *MED, cls='fig')}{centre}""", [[HEAD[0], HEAD[1] + 20, 270, 1.15]], True)

NODES = [("Ashtanga", "body-balance"), ("Surya Namaskar", "sun"), ("Hatha", "yin-yang"), ("Meditation", "meditation"), ("Yoga as policy", "india-gate")]
FX0, FY0, FR = 630, 540, 540
fan, l21, dots, nodes21 = [], [[HEAD[0], HEAD[1] + 20, 270, 1.15]], [], []
fanpos = []
for i, (lab, icn) in enumerate(NODES):
    a = math.radians(-36 + 18 * i)
    x, y = FX0 + FR * math.cos(a), FY0 + FR * math.sin(a)
    fanpos.append((x, y))
    fan.append(f'<line class="conn" x1="{FX0}" y1="{FY0}" x2="{x:.0f}" y2="{y:.0f}"/>')
    dots.append(f'<circle class="dot" cx="{x:.0f}" cy="{y:.0f}" r="9"/>')
    l21.append([x + 28 + 39, y, 80, 0.85])


def node(lab, icn, left, top, extra=""):
    return (f'<div class="node" style="left:{left:.0f}px;top:{top:.0f}px" {extra}>'
            f'<svg class="ni sil rim" viewBox="0 0 512 512" style="position:static"><g class="ink">{ic(icn)}</g></svg><span class="nl">{E(lab)}</span></div>')


S[21] = (f"""{sil('meditation', *MED, cls='fig')}
<svg class="fan abs" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" viewBox="0 0 1920 1080">{''.join(fan)}{''.join(dots)}</svg>
{''.join(node(lab, icn, fanpos[i][0] + 28, fanpos[i][1] - 39) for i, (lab, icn) in enumerate(NODES))}
{centre}""", l21, True)

SUBS = ["eight limbs · yama · niyama · vritti · which stage are you at",
        "twelve names · mantras · breathing pattern · why sampoorna yoga",
        "how it differs · Bihar School of Yoga · Yoga Nidra · Kundalini",
        "which school · under a guru · has it made you introverted",
        "why 21st June · has the government overdone it · can an atheist be spiritual"]
rows22, l22 = [], []
for i, (lab, icn) in enumerate(NODES):
    top = 150 + i * 172
    fx, fy = fanpos[i][0] + 28, fanpos[i][1] - 39
    rows22.append(node(lab, icn, 120, top, f'data-dx="{fx - 120:.0f}" data-dy="{fy - top:.0f}"'))
    rows22.append(f'<div class="bsub" style="left:220px;top:{top + 86}px">{E(SUBS[i])}</div>')
    l22.append([fx + 39, fy + 39, 80, 0.85])
S[22] = (f"""<svg class="fan abs" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" viewBox="0 0 1920 1080">{''.join(fan)}{''.join(dots)}</svg>
<div class="tx hero centre" style="top:{HERO_TOP}px;width:auto;white-space:nowrap;transform-origin:0% 50%;transform:scale({SMALL})">{words("Practising Yoga")}</div>
{''.join(rows22)}""", l22)
ROWS22 = [(120 + 39, 150 + i * 172 + 39) for i in range(5)]

# ---------------- S23 · on the record ----------------
inst = [("At which stage of yoga are you?", "Chairman · 2022"),
        ("Should people of your age be pursuing spirituality?", "M1 · Apr 2025"),
        ("Yoga started as a quest for moksha but has been reduced to physical activity. Why?", "Chairman · Feb 2026")]
S[23] = (f"""
{sil('round-table', 1580, 520, 440, cls='fig')}
<div class="tx" style="top:190px;width:1180px;display:flex;flex-direction:column;gap:56px">
{''.join(f'<div class="inst"><div class="q" style="font-size:54px">{E(q)}</div><div class="stamp" style="margin-top:14px"><span class="acc">●</span> {E(s)}</div></div>' for q, s in inst)}
</div>""", [[1580, 500, 260, 0.95]])

# ---------------- S24 · the safe hobby ----------------
S[24] = (f"""
<div class="scene b1">{sil('open-book', 1560, 680, 400, cls='fig')}{sil('magnifying-glass', 1500, 450, 380, cls='lens')}</div>
<div class="scene b2">{sil('drama-masks', 1540, 540, 470, cls='fig')}</div>
<div class="tx" style="top:200px;width:1150px">
  <div class="lab lb">DAF: Reading classic crime / mystery novels</div>
  <div class="q qq" style="font-size:56px;margin-top:56px">Who is your favourite detective, and how does Poirot differ from Holmes?</div>
  <div class="q qq" style="font-size:56px;margin-top:56px">Is reading fiction a useful hobby, or living in a make believe world? <span class="tag">OPINION</span></div>
</div>""", [[1540, 560, 310, 1.0]])

# ---------------- S25 · the list and the wording ----------------
S[25] = (f"""
{sil('scroll-unfurled', 1430, 420, 440, cls='scroll')}
{sil('fountain-pen', 1790, 690, 190, cls='pen')}
<div class="abs mono ty quote" style="position:absolute;left:1160px;top:800px;width:620px;font-size:30px;line-height:1.45;color:var(--fg)">{chars("“Why do you only do asanas and not pranayam?”")}</div>
<div class="tx" style="top:250px;width:1000px">
  <div class="lab lb">ELEVATE IGP</div>
  <div class="ln l1" style="margin-top:40px">The full topic list for your profile.</div>
  <div class="ln l2" style="margin-top:36px">The exact wording in which each question was asked.</div>
</div>""", [[1430, 420, 290, 1.0], [1470, 840, 330, 0.55, 90]])

# ---------------- S26 · order ----------------
px_, py_, ps_ = 1460, 520, 560
S[26] = (f"""
{sil('path-distance', px_, py_, ps_, cls='fig')}
<div class="tx lines" style="bottom:140px;width:1000px">
  <div class="stmt l1">Finish this first.</div>
  <div class="ln l2">Your own list comes after.</div>
</div>""", [[*pt(px_, py_, ps_, 96, 90), 150, 1.2], [*pt(px_, py_, ps_, 432, 340), 150, 1.2], [px_, py_, 380, 0.25]])

S[27] = (section("03", "Opinion questions take the most work.", sil('push', 1460, 520, 520, cls='fig')), [[1460, 500, 320, 1.05]])

# ---------------- S28 · choose a side ----------------
sx, sy, ss = 1540, 540, 480
S[28] = (f"""
{sil('scales', sx, sy, ss, cls='fig', style='transform-origin:50% 22%')}
<div class="tx" style="top:200px;width:1120px">
  <div class="ln main" style="font-size:64px">{words("Opinion on the presidential reference and the SC verdict on the governor's assent to bills?")}</div>
  <div class="stamp st" style="margin-top:22px"><span class="acc">●</span> Chairman · 13 Feb 2026</div>
  <div class="ln acc rev" style="font-size:64px;margin-top:70px">{words("(Choose a side. Do not give a balanced answer.)")}</div>
</div>""", [[sx, sy - 20, 300, 1.0], [*pt(sx, sy, ss, 92, 330), 150, 1.25]])

# ---------------- S29 · how to answer ----------------
stx, sty, sts = 1480, 560, 520
def tread(k):
    x, y = pt(stx, sty, sts, 32 + 64 * k, 448 - 64 * k)
    return x, y
STEPS29 = [tread(2), tread(4), tread(6)]
S[29] = (f"""
{sil('stairs', stx, sty, sts, cls='fig')}
{sil('person', STEPS29[0][0], STEPS29[0][1] - 62, 130, cls='walker')}
<div class="tx lines" style="top:200px;width:1000px;gap:34px">
  <div class="ln">Your position, in the first sentence.</div>
  <div class="ln">A reason that survives one push.</div>
  <div class="ln">What honestly cuts against you.</div>
  <div class="ln acc" style="margin-top:36px">Then stop.</div>
</div>""", [[STEPS29[0][0], STEPS29[0][1] - 100, 150, 1.15], [stx, sty, 400, 0.22]])

# ---------------- S30 · iterate ----------------
S[30] = (f"""
{sil('cycle', 1480, 480, 460, cls='fig')}
{''.join(f'<div class="abs mono dr" style="left:1180px;width:600px;top:790px;text-align:center;font-size:36px;letter-spacing:.14em">DRAFT {i}</div>' for i in range(1, 5))}
<div class="tx" style="bottom:130px;width:1000px">
  <div class="lab">ELEVATE IGP</div>
  <div class="stmt l1" style="font-size:88px;margin-top:24px">{words("We iterate on your opinion answers until they actually improve.")}</div>
</div>""", [[1480, 480, 300, 1.2]])

S[31] = (section("04", "Economy · Polity and Governance · International Relations", sil('globe', 1480, 480, 480, cls='fig'),
                 sub="And the last ninety days.", size=80), [[1480, 470, 310, 1.05]])

# ---------------- S32 · recite vs view ----------------
S[32] = (f"""
<div class="scene k1">{sil('open-book', 1480, 560, 480, cls='fig')}<div class="cap abs" style="left:1240px;top:300px">features · numbers · years</div></div>
<div class="scene k2">{sil('think', 1480, 520, 520, cls='fig')}</div>
<div class="tx lines" style="bottom:140px;width:1020px">
  <div class="ln">Nobody will ask you to recite a scheme.</div>
  <div class="ln">They'll ask what you make of it.</div>
</div>""", [[1480, 560, 300, 0.6], [1480, 470, 310, 1.15]])

# ---------------- S33 · weekly opinion matrix ----------------
cells = "".join(f'<div class="cell" style="left:{c * 98}px;top:{r * 78}px"></div>' for r in range(4) for c in range(5))
S[33] = (f"""
{sil('calendar', 1300, 250, 170, cls='cal')}
<div class="abs matrix" style="left:1240px;top:400px;width:476px;height:298px">{cells}</div>
<div class="tx" style="bottom:130px;width:1000px">
  <div class="lab">ELEVATE IGP</div>
  <div class="stmt l1" style="font-size:96px;margin-top:24px">{words("A weekly Opinion Matrix on the major issues.")}</div>
</div>""", [[1478, 550, 340, 0.85, 270], [1300, 250, 120, 0.9]])

S[34] = (section("05", "Handle the room.", lamp), [[1460, 420, 300, 1.0, 260]])

# ---------------- S35 · winning the argument ----------------
S[35] = (f"""
{sil('sword-clash', 1480, 500, 560, cls='fig')}
<div class="tx stmt" style="bottom:120px;width:1000px;font-size:96px">{words("Are you winning the argument and losing the interview?")}</div>
""", [[1480, 470, 260, 1.3]])

# ---------------- S36 · three types, left blank ----------------
doors, l36 = [], []
for i, x in enumerate((560, 960, 1360)):
    doors.append(sil('doorway', x, 640, 300, cls='door'))
    doors.append(f'<div class="abs slot" style="left:{x - 150}px;width:300px;top:820px;text-align:center"><div class="mono acc" style="font-size:30px;letter-spacing:.14em">TYPE {i + 1}</div><div class="blank" style="margin:26px auto 0;width:220px;height:3px;background:rgba(239,231,222,.45);transform-origin:0 50%"></div></div>')
    l36.append([x, 670, 70, 1.15, 115])
S[36] = (f"""{''.join(doors)}
<div class="tx head" style="top:170px;width:1500px">
  <div class="stmt" style="font-size:88px">{words("Three types of questions.")}</div>
  <div class="ln muted sub" style="font-size:56px;margin-top:18px">Three different things to do.</div>
</div>""", l36)

# ---------------- S37 · the volume ----------------
S[37] = (f"""
{sil('book-pile', 1500, 600, 480, cls='fig', style='transform-origin:50% 80%')}
<div class="abs crow" style="left:120px;top:190px;white-space:nowrap"><span class="num-big cval" data-to="129" style="font-size:150px">129</span><span class="ln" style="font-size:56px"> profile questions</span></div>
<div class="abs crow" style="left:120px;top:420px;white-space:nowrap"><span class="num-big" style="font-size:150px">~<span class="cval" data-to="200">200</span></span><span class="ln" style="font-size:56px"> current affairs questions</span></div>
<div class="abs crow ln muted" style="left:120px;top:680px;width:1100px;font-size:56px">+ motivation, service preference, the standard set</div>
""", [[1500, 560, 300, 0.6]])

# ---------------- S38 · the floor ----------------
S[38] = (f"""
{sil('stairs-goal', 1480, 580, 660, cls='fig')}
<div class="tx stmt" style="bottom:120px;width:980px;font-size:110px">{words("This is the floor, not the ceiling.")}</div>
""", [[*pt(1480, 580, 660, 385, 85), 250, 1.25], [1420, 760, 420, 0.32]])

# ---------------- S39 · close ----------------
feats = [("DAF repair against 20 defects", "notebook"), ("Personalised DAF PYQ questionnaire", "files"),
         ("Iterative opinion preparation", "scales"), ("Weekly Opinion Matrix", "calendar"), ("Board interaction strategy", "round-table")]
S[39] = (f"""
<div class="abs dark wm" style="left:0;right:0;top:170px;text-align:center;font-size:150px;font-weight:600;letter-spacing:.14em;line-height:1;padding-left:.14em">{''.join(f'<span class="w">{c}</span>' for c in 'ELEVATE')}</div>
<div class="abs dark sub" style="left:0;right:0;top:345px;text-align:center;font-size:38px;font-weight:500">Interview Guidance Program 2026</div>
<div class="abs" style="left:0;right:0;top:470px;display:flex;flex-direction:column;align-items:center;gap:20px">
{''.join(f'<div class="feat" style="display:flex;align-items:center;gap:22px;font-size:42px;font-weight:500;width:820px">{icon_inline(icn, "fi")}<span>{E(t)}</span></div>' for t, icn in feats)}
</div>
<div class="abs mono acc cta" style="left:0;right:0;top:880px;text-align:center;font-size:28px;letter-spacing:.04em">[ENROLMENT DETAILS — insert link / QR / WhatsApp number before export]</div>
<div class="abs mono credit" style="left:0;right:0;bottom:34px;text-align:center;font-size:18px;color:#7d746b;letter-spacing:.06em">Illustrations: game-icons.net (Lorc, Delapouite and contributors), CC BY 3.0</div>
""", [[960, 270, 760, 1.1, 190]])

SLIDE_CSS = """
.scene { position:absolute; inset:0; }
.trow .ti, .feat .fi { width:84px; height:84px; flex:none; }
.feat .fi { width:52px; height:52px; }
.matrix .cell { position:absolute; width:84px; height:64px; border:1.5px solid rgba(239,231,222,.38); border-radius:4px; background:rgba(234,148,88,0); }
"""

# ---------------- page ----------------
spec = (ROOT / "BUILD_SPEC.md").read_text()
NOTES = {}
for sid, body in re.findall(r"\n### S(\d\d)\n(.*?)(?=\n### S\d\d\n|\n## 6\.)", spec, re.S):
    vo = body.split("**vo:**", 1)[1].split("\n---")[0].strip()
    NOTES[f"s{int(sid):02d}"] = re.sub(r"^\*\((.*)\)\*$", r"(\1)", vo)

slides, lights = [], {}
for n in sorted(S):
    markup, lt, *keep = S[n]
    sid = f"s{n:02d}"
    lights[sid] = [[round(v, 1) for v in l] for l in lt]
    slides.append(f'<section class="slide" id="{sid}" data-keep="{1 if keep and keep[0] else 0}"><div class="exit">{markup}</div></section>')
assert len(slides) == 39, len(slides)

consts = {"S5_TOP": S5_TOP, "STEPS29": STEPS29, "ROWS22": ROWS22, "SMALL": SMALL, "PIN2": pt(px_, py_, ps_, 432, 340)}
js = "var C = " + json.dumps(consts) + ";\n" + (ROOT / "tools/deck_v6.slides.js").read_text()
f = lambda name: base64.b64encode((ROOT / "assets/fonts" / name).read_bytes()).decode()
page = (ROOT / "tools/deck_v6.src.html").read_text()
for k, v in {
    "{{FONT_400}}": f("inter-tight-latin-400-normal.woff2"), "{{FONT_500}}": f("inter-tight-latin-500-normal.woff2"),
    "{{FONT_600}}": f("inter-tight-latin-600-normal.woff2"), "{{MONO_400}}": f("jetbrains-mono-latin-400-normal.woff2"),
    "{{MONO_500}}": f("jetbrains-mono-latin-500-normal.woff2"), "{{SLIDE_CSS}}": SLIDE_CSS,
    "{{SLIDES}}": "\n".join(slides), "{{LOGO}}": (ROOT / "assets/brand/civilsdaily-logo.svg").read_text(),
    "{{NOTES}}": json.dumps(NOTES, ensure_ascii=False).replace("</", "<\\/"), "{{LIGHTS}}": json.dumps(lights),
    "{{BUILDERS}}": js, "{{GSAP}}": (ROOT / "assets/vendor/gsap.min.js").read_text(),
}.items():
    page = page.replace(k, v)
out = ROOT / "deck/elevate-igp-2026-deck-v6.html"
out.write_text(page)
print(f"{out.relative_to(ROOT)}: {len(slides)} slides, {len(page) // 1024} KB")
