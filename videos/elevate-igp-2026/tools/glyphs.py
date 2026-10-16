"""Line-art glyphs in the deck's geometric style. Every stroke carries class "ln" so it can be drawn on.
Coordinates are centred on (0, 0); wrap in <g transform="translate(..) scale(..)">."""

def lotus(extra=""):
    """Seated meditator: head, halo, shoulders, arms resting on knees, crossed legs."""
    return f"""<g class="lotus" {extra}>
  <circle class="ln acc halo" cx="0" cy="-118" r="46"/>
  <circle class="ln" cx="0" cy="-118" r="26"/>
  <path class="ln" d="M-34 -82 Q0 -94 34 -82"/>
  <path class="ln" d="M-34 -82 C-40 -40 -36 -5 -30 22"/>
  <path class="ln" d="M34 -82 C40 -40 36 -5 30 22"/>
  <path class="ln" d="M-34 -78 C-70 -50 -84 0 -74 34"/>
  <path class="ln" d="M34 -78 C70 -50 84 0 74 34"/>
  <circle class="ln acc" cx="-74" cy="40" r="7"/>
  <circle class="ln acc" cx="74" cy="40" r="7"/>
  <path class="ln" d="M-120 52 C-60 20 60 20 120 52 C60 84 -60 84 -120 52 Z"/>
</g>"""

def pin(scale=1.0):
    return f"""<g transform="scale({scale})">
  <path class="ln acc" d="M0 80 C-12 45 -62 10 -62 -35 A62 62 0 1 1 62 -35 C62 10 12 45 0 80 Z"/>
  <circle class="ln" cx="0" cy="-35" r="22"/>
</g>"""

def recline():
    """Shavasana under a crescent moon, with breath waves above the chest."""
    return """<g class="recline">
  <path class="ln dim" d="M-250 46 L250 46"/>
  <circle class="ln" cx="-196" cy="2" r="26"/>
  <path class="ln" d="M-168 2 Q-70 -16 40 2"/>
  <path class="ln" d="M-166 16 Q-70 4 40 14"/>
  <path class="ln" d="M40 2 L210 -2"/>
  <path class="ln" d="M40 14 L210 12"/>
  <path class="ln" d="M210 -2 L222 -16 M210 12 L224 2"/>
  <path class="ln" d="M-140 22 L-20 30"/>
  <path class="ln acc moon" d="M150 -190 A46 46 0 1 0 196 -130 A36 36 0 1 1 150 -190 Z"/>
  <circle class="star" cx="60" cy="-180" r="3"/><circle class="star" cx="250" cy="-200" r="2.5"/><circle class="star" cx="-30" cy="-150" r="2"/>
  <path class="wave" d="M-150 -40 q20 -14 40 0 t40 0 t40 0 t40 0 t40 0"/>
  <path class="wave" d="M-130 -76 q20 -14 40 0 t40 0 t40 0 t40 0"/>
  <path class="wave" d="M-110 -112 q20 -14 40 0 t40 0 t40 0"/>
</g>"""

def wheel(r=172, spokes=8):
    s = "".join(f'<line class="ln dim" x1="0" y1="{-r + 42}" x2="0" y2="{-r}" transform="rotate({i * 360 / spokes})"/>' for i in range(spokes))
    return f'<g class="wheel"><circle class="ln acc wheelring" r="{r}"/><circle class="ln dim" r="{r - 42}"/>{s}</g>'

# ---------- small icons, about 80px ----------
def icon_scales():
    return """<path class="ln" d="M0 -30 L0 30 M-22 30 L22 30 M-36 -20 L36 -20"/>
<path class="ln" d="M-36 -20 L-48 8 M-36 -20 L-24 8 M-52 8 Q-36 22 -20 8"/>
<path class="ln" d="M36 -20 L24 8 M36 -20 L48 8 M20 8 Q36 22 52 8"/>
<circle class="ln acc" cx="0" cy="-34" r="4"/>"""

def icon_pin():
    return """<path class="ln acc" d="M0 32 C-5 17 -24 3 -24 -13 A24 24 0 1 1 24 -13 C24 3 5 17 0 32 Z"/><circle class="ln" cx="0" cy="-13" r="8"/>"""

def icon_briefcase():
    return """<rect class="ln" x="-34" y="-14" width="68" height="44" rx="7"/>
<path class="ln" d="M-13 -14 L-13 -25 L13 -25 L13 -14 M-34 6 L34 6"/>
<rect class="ln acc" x="-6" y="0" width="12" height="12" rx="2"/>"""

def icon_yoga_novels():
    return f"""<g transform="translate(-26 8) scale(0.26)" style="--sw:10">{lotus()}</g>
<circle class="ln acc" cx="24" cy="-6" r="14"/><path class="ln" d="M34 4 L48 18"/>"""

def icon_debate():
    return """<path class="ln" d="M-44 -30 h40 a8 8 0 0 1 8 8 v18 a8 8 0 0 1 -8 8 h-22 l-10 10 v-10 h-8 a8 8 0 0 1 -8 -8 v-18 a8 8 0 0 1 8 -8 z"/>
<path class="ln acc" d="M4 -8 h40 a8 8 0 0 1 8 8 v18 a8 8 0 0 1 -8 8 h-8 v10 l-10 -10 h-22 a8 8 0 0 1 -8 -8 v-18 a8 8 0 0 1 8 -8 z"/>
<path class="ln acc" d="M18 2 q0 -6 6 -6 q6 0 6 6 q0 5 -6 6 v4"/><circle class="ln acc" cx="24" cy="18" r="1"/>"""

# ---------- node symbols for S21, about 50px ----------
def sym_ashtanga():
    spokes = "".join(f'<line class="ln" x1="0" y1="-7" x2="0" y2="-24" transform="rotate({i * 45})"/>' for i in range(8))
    return f'<circle class="ln acc" r="24"/>{spokes}<circle class="ln" r="5"/>'

def sym_surya():
    rays = "".join(f'<line class="ln acc" x1="0" y1="-17" x2="0" y2="-27" transform="rotate({i * 30})"/>' for i in range(12))
    return f'<circle class="ln" r="11"/>{rays}'

def sym_hatha():
    return """<circle class="ln" r="22"/><path class="fillacc" d="M0 -22 A22 22 0 0 0 0 22 Z"/>
<path class="ln" d="M6 -13 A13 13 0 1 1 6 13 A9 9 0 1 0 6 -13 Z"/>"""

def sym_meditation():
    return f'<g transform="translate(0 8) scale(0.22)" style="--sw:11">{lotus()}</g>'

def sym_policy():
    cols = "".join(f'<path class="ln" d="M{x} -6 L{x} 16"/>' for x in (-16, -5, 6, 17))
    return f'<path class="ln acc" d="M-26 -8 L0 -26 L26 -8 Z"/>{cols}<path class="ln" d="M-28 20 L28 20"/>'
