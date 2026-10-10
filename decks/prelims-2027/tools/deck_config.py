"""Choreography for every slide.

Element numbers are the shape order inside each PPT slide (see model.json).
Step 0 plays automatically when a slide opens; every later step is one click.

Action forms
  7                       reveal element 7 (paper drops, text rises, chart builds fully)
  ("s", 7, [names])       reveal named parts of chart 7
  ("f", 7, [names]|None)  spotlight those parts of chart 7 (others dim); None = all bright
  ("z", 7)                camera zooms to element 7; ("z", 7, [fx, fy, fw, fh]) zooms to part of it
  ("zr", [x, y, w, h])    camera zooms to a stage rectangle
  ("o",)                  camera back to the full slide
  ("n", 9, "spot")        extra phase of a natively rebuilt chart
"""

# ---------- chart parts, in the chart image's own pixels ----------
def rows_full(ys, w, fx="r", h=None, prefix="r"):
    return [dict(name=f"{prefix}{k}", r=[0, y, w, h], fx=fx) for k, y in enumerate(ys)]

def cols(xs, y, h, fx="u", prefix="c", pad=0):
    return [dict(name=f"{prefix}{k}", r=[x0 - pad, y, x1 - x0 + 2 * pad, h], fx=fx) for k, (x0, x1) in enumerate(xs)]

SLICES = {}

# 07 dumbbell: 11 rows, label + dumbbell wipe in together
SLICES["dg/dumbbell.png"] = dict(gs=150, parts=[dict(name=f"r{k}", r=[0, round(133 + 94.6 * k - 47), 2300, 94], fx="r") for k in range(11)])
# 08 bars against six-year average
SLICES["dg/paper2026.png"] = dict(gs=160, parts=[dict(name=f"r{k}", r=[0, 31 + 104 * k, 2300, 104], fx="r") for k in range(10)])
# 11 format share columns
SLICES["dg/formats.png"] = dict(gs=200, parts=[dict(name=f"c{k}", r=[84 + 272 * k, 0, 272, 1000], fx="u") for k in range(8)])
# 13 scatter: one dot + label at a time
SLICES["dg/scatter.png"] = dict(gs=170, parts=[
    dict(name="Polity", r=[400, 242, 200, 100], fx="pop"),
    dict(name="Governance", r=[330, 668, 265, 85], fx="pop"),
    dict(name="ModHist", r=[597, 628, 330, 85], fx="pop"),
    dict(name="Environment", r=[1030, 125, 320, 100], fx="pop"),
    dict(name="Geography", r=[1185, 273, 290, 100], fx="pop"),
    dict(name="IR", r=[1110, 392, 320, 100], fx="pop"),
    dict(name="Agriculture", r=[1115, 780, 280, 90], fx="pop"),
    dict(name="Economy", r=[1680, 135, 265, 85], fx="pop"),
    dict(name="SciTech", r=[1835, 225, 280, 95], fx="pop"),
    dict(name="ArtCulture", r=[1757, 330, 320, 100], fx="pop"),
])
# 15 cumulative curve, drawn in three stretches
SLICES["dg/coverage.png"] = dict(parts=[
    dict(name="a", r=[152, 0, 638, 990], fx="r", dur=2400),
    dict(name="b", r=[790, 0, 310, 990], fx="r", dur=1600),
    dict(name="c", r=[1100, 0, 700, 990], fx="r", dur=2000),
    dict(name="d", r=[1800, 0, 500, 990], fx="r", dur=1600, d=900),
])
# 16 five tiers: stripe, label, count, bar, share
_t = []
for k in range(5):
    y = 5 + 196 * k
    _t += [dict(name=f"t{k}s", g=k, d=0, r=[0, y, 30, 190], fx="u"),
           dict(name=f"t{k}l", g=k, d=150, r=[40, y, 800, 190], fx="slide"),
           dict(name=f"t{k}n", g=k, d=450, r=[860, y, 300, 190], fx="rise"),
           dict(name=f"t{k}b", g=k, d=700, r=[1200, y, 900, 190], fx="r", dur=1600),
           dict(name=f"t{k}p", g=k, d=1500, r=[2110, y, 190, 190], fx="pop")]
SLICES["dg/tiers.png"] = dict(gs=0, parts=_t)
# 17 hot twenty: two columns of ten; name, five yearly dots, count
_h = []
for k in range(10):
    y = max(0, round(118.2 * k - 5)); h = 100
    for side, (xn, wn, xd, wd, xc, wc), base in (("L", (0, 700, 740, 300, 1040, 100), 0), ("R", (1160, 700, 1930, 290, 2240, 60), 10)):
        n = base + k
        _h += [dict(name=f"h{n}n", g=n, d=0, r=[xn, y, wn, h], fx="slide"),
               dict(name=f"h{n}d", g=n, d=350, r=[xd, y, wd, h], fx="r", dur=1100),
               dict(name=f"h{n}c", g=n, d=900, r=[xc, y, wc, h], fx="pop")]
SLICES["dg/hotlist.png"] = dict(gs=330, parts=_h)
# 18 cooled: two columns of six; name block, then the red "last 20xx"
_c = []
for k in range(6):
    y = 164 * k
    for side, (xn, wn, xl, wl), base in (("L", (0, 935, 935, 200), 0), ("R", (1150, 960, 2110, 190), 6)):
        n = base + k
        _c += [dict(name=f"q{n}n", g=n, d=0, r=[xn, y, wn, 152], fx="slide"),
               dict(name=f"q{n}l", g=n, d=600, r=[xl, y, wl, 152], fx="pop")]
SLICES["dg/cooled.png"] = dict(gs=380, parts=_c)
# 26 phases A to E
SLICES["dg/gantt.png"] = dict(parts=[
    dict(name="A", r=[0, 0, 2400, 190], fx="r", dur=1800), dict(name="B", r=[0, 190, 2400, 170], fx="r", dur=1800),
    dict(name="C", r=[0, 360, 2400, 170], fx="r", dur=1800), dict(name="D", r=[0, 530, 2400, 185], fx="r", dur=1800),
    dict(name="E", r=[0, 715, 2400, 185], fx="r", dur=1800), dict(name="P", r=[0, 900, 2400, 100], fx="rise", d=1100)])
# 28 the five-hour loop
SLICES["dg/loop.png"] = dict(parts=[dict(name="ring", r=[0, 0, 1500, 1500], fx="sweep", dur=3000),
                                    dict(name="disc", r=[0, 0, 1500, 1500], fx="disc", d=1900)], overlay=True)
# 29 a week in phase A, day by day
SLICES["dg/weekA.png"] = dict(gs=170, parts=cols([(306, 592), (603, 889), (900, 1186), (1197, 1484), (1495, 1781), (1792, 2078), (2089, 2375)], 0, 560, fx="d", prefix="d", pad=5)
                              + [dict(name="cap", r=[0, 570, 2400, 90], fx="rise", d=1500, g=99)])
# 34 the exam-clock day
SLICES["dg/testday.png"] = dict(gs=450, parts=[dict(name=f"b{k}", r=r, fx="r", dur=1300) for k, r in enumerate([[0, 0, 690, 455], [690, 0, 680, 455], [1370, 0, 680, 455], [2050, 0, 350, 455]])]
                                + [dict(name="cap", r=[0, 460, 2400, 100], fx="rise")])
# 35 the taper fortnight
SLICES["dg/taper.png"] = dict(gs=110, parts=cols([(16, 195), (206, 385), (396, 575), (586, 765), (776, 955), (966, 1145), (1156, 1335), (1346, 1525), (1536, 1715), (1726, 1905), (1916, 2095), (2106, 2285)], 0, 360, fx="pop", pad=5)
                             + [dict(name="cap", r=[0, 380, 2300, 100], fx="rise")])
# 36 sittings per month
SLICES["dg/testload.png"] = dict(gs=200, parts=[dict(name=f"m{k}", r=[c - 130, 95, 260, 795], fx="u", dur=1500) for k, c in enumerate([235, 504, 774, 1045, 1314, 1584, 1855, 2124])])
# 38 spacing rule, one interval at a time
SLICES["dg/spacing.png"] = dict(parts=[dict(name="a", r=[0, 0, 262, 620], fx="r", dur=1400), dict(name="b", r=[262, 0, 498, 620], fx="r", dur=1600),
                                      dict(name="c", r=[760, 0, 1540, 620], fx="r", dur=2400)])
# 40 revisions per tier
_rv = []
for k, y in enumerate([20, 188, 356, 524, 692]):
    _rv.append(dict(name=f"v{k}l", g=0, d=0, r=[0, y - 12, 450, 125], fx="slide"))
    for j in range(8):
        _rv.append(dict(name=f"v{k}c{j}", g=0, d=350 + 110 * j, r=[505 + 200 * j, y - 12, 111, 125], fx="pop"))
SLICES["dg/revcount.png"] = dict(parts=_rv)
# 43 score lines
SLICES["dg/scoremath.png"] = dict(parts=[dict(name="lines", r=[160, 0, 2140, 745], fx="r", dur=2600)])
# 44 expected marks per option cut
SLICES["dg/elimev.png"] = dict(gs=500, parts=[dict(name=f"r{k}", r=r, fx="r", dur=1500) for k, r in enumerate([[0, 40, 2300, 140], [0, 210, 2300, 170], [0, 395, 2300, 170], [0, 575, 2300, 170]])])
# 45 four error boxes
SLICES["dg/errorlog.png"] = dict(parts=[dict(name=f"q{k + 1}", r=r, fx="rise") for k, r in enumerate([[0, 0, 1150, 455], [1150, 0, 1150, 455], [0, 470, 1150, 490], [1150, 470, 1150, 490]])])
# 46 mock score trajectory, month by month
SLICES["dg/trajectory.png"] = dict(parts=[dict(name=f"p{k + 1}", r=r, fx="r", dur=1500) for k, r in enumerate([[0, 0, 450, 800], [450, 0, 620, 800], [1070, 0, 620, 800], [1690, 0, 610, 800]])])
# 47 CSAT
SLICES["dg/csat.png"] = dict(gs=300, parts=[dict(name="bar", r=[0, 100, 2300, 220], fx="r", dur=1800)]
                             + [dict(name=f"c{k + 1}", r=r, fx="rise") for k, r in enumerate([[0, 370, 760, 170], [760, 370, 760, 170], [1520, 370, 780, 170]])])

HOT_L1, HOT_L2, HOT_R1, HOT_R2 = [0, 0, .5, .48], [0, .46, .5, .54], [.5, 0, .5, .48], [.5, .46, .5, .54]
def hot(ns): return [p for n in ns for p in (f"h{n}n", f"h{n}d", f"h{n}c")]
def cool(ns): return [p for n in ns for p in (f"q{n}n", f"q{n}l")]
def tier(k): return [f"t{k}{p}" for p in "slnbp"]
def rev(k): return [f"v{k}l"] + [f"v{k}c{j}" for j in range(8)]

STEPS = {
    1: [[9]],
    2: [[9], [11], [13], [("z", 13)]],
    3: [[8, 9], [10, 11], [13], [("z", 13, [0, 0, 1, .55])], [("z", 13, [0, .45, 1, .55])]],
    4: [[9], [("n", 9, "spot")]],
    5: [],
    6: [[("z", 7, [0, 0, 1, .52])], [("z", 7, [0, .48, 1, .52])], [("o",)]],
    7: [[10], [("f", 10, ["r4", "r5", "r6"])], [("f", 10, ["r0", "r1", "r7", "r8", "r9", "r10"])], [("f", 10, None)]],
    8: [[9, 11], [("f", 11, ["r0", "r1", "r2"])], [("f", 11, ["r6", "r7", "r8", "r9"])], [("f", 11, None)]],
    9: [[7], [("z", 7)], [("o",), 9], [("z", 9)]],
    10: [[10], [("z", 10)], [("o",), 12], [("z", 12)]],
    11: [[10], [("f", 10, ["c4", "c5", "c6"])], [("f", 10, None)]],
    12: [[9], [11], [13], [("z", 11)]],
    13: [[9], [11], [("f", 11, ["Polity", "Governance", "ModHist"])], [("f", 11, None)]],
    14: [[7], [("z", 7)], [("o",), 9], [("z", 9)]],
    15: [[("s", 10, ["a"])], [("s", 10, ["b"])], [("s", 10, ["c", "d"])]],
    16: [[("s", 7, tier(0))]] + [[("s", 7, tier(k)), ("f", 7, tier(k))] for k in range(1, 5)] + [[("f", 7, None)]],
    17: [[("z", 7, z), ("s", 7, hot(r)), ("f", 7, hot(r))] for z, r in ((HOT_L1, range(0, 5)), (HOT_L2, range(5, 10)), (HOT_R1, range(10, 15)), (HOT_R2, range(15, 20)))]
        + [[("o",), ("f", 7, None)]],
    18: [[("z", 9, z), ("s", 9, cool(r)), ("f", 9, cool(r))] for z, r in (([0, 0, .5, .5], range(0, 3)), ([0, .46, .5, .54], range(3, 6)), ([.5, 0, .5, .5], range(6, 9)), ([.5, .46, .5, .54], range(9, 12)))]
        + [[("o",), ("f", 9, None)]],
    19: [[10, 12]],
    20: [[10], [12], [("z", 12)], [("o",), 14, 16]],
    21: [[7], [9, 11], [13, 15]],
    22: [[10], [12], [("z", 12)]],
    23: [[10], [12, 14], [("z", 10)]],
    24: [[7, 9], [11, 13], [("zr", [1095, 300, 760, 490])]],
    25: [],
    26: [[("s", 7, ["A"])], [("s", 7, ["B"])], [("s", 7, ["C"])], [("s", 7, ["D"])], [("s", 7, ["E", "P"])]],
    27: [[9, 10, 11, 12], [13], [15], [("z", 15)]],
    28: [[10, 12], [13]],
    29: [[7], [9], [11]],
    30: [[7, 9], [11, 13], [("z", 9)]],
    31: [[9, 10, 11, 12], [13], [15, 17]],
    32: [[9, 11, 13, 15, 17, 19, 21], [23, 25, 27, 29, 31, 33, 35], [36], [38, 40]],
    33: [[9, 10, 11, 12], [13], [15, 17], [("z", 15)]],
    34: [[("s", 10, ["b0", "b1", "b2", "b3"])], [("s", 10, ["cap"])]],
    35: [[("s", 9, [f"c{k}" for k in range(12)])], [("f", 9, ["c1", "c4", "c7"])], [("f", 9, None), ("s", 9, ["cap"])]],
    36: [[9], [11]],
    37: [],
    38: [[("s", 9, ["a"])], [("s", 9, ["b"])], [("s", 9, ["c"])]],
    39: [[9], [10], [11], [13], [("z", 13)]],
    40: [[("s", 7, rev(k))] for k in range(5)] + [[9]],
    41: [[9], [11, 13, 15], [("z", 13)]],
    42: [],
    43: [[9, 10], [12]],
    44: [[10], [("s", 12, ["r0", "r1"])], [("s", 12, ["r2"])], [("s", 12, ["r3"])]],
    45: [[("s", 7, ["q1"])], [("s", 7, ["q2"])], [("s", 7, ["q3"])], [("s", 7, ["q4"])], [9], [11]],
    46: [[9], [("s", 11, ["p1"])], [("s", 11, ["p2"])], [("s", 11, ["p3"])], [("s", 11, ["p4"])]],
    47: [[("s", 9, ["bar"])], [("s", 9, ["c1", "c2", "c3"])]],
    48: [[9, 10], [11, 12], [14, 16]],
    49: [[10, 12], [14]],
    50: [[9, 10, 11]],
}

# heat map reveals as a left-to-right sweep across the years
FX = {(3, 13): "paperwipe", (6, 7): "paperwipe", (49, 14): "paperwipe"}
NATIVE = {"dg/countdown.png": "countdown", "dg/cutoff.png": "cutoff"}
