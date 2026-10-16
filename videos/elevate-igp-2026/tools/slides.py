"""Slide content for ELEVATE IGP 2026, copied verbatim from BUILD_SPEC.md (text is locked)."""

SECTIONS = [  # (first slide, last slide, runtime in seconds) from the spec's timing map
    (1, 3, 70), (4, 10, 150), (11, 15, 100), (16, 26, 220),
    (27, 30, 105), (31, 33, 60), (34, 36, 65), (37, 39, 55),
]

SLIDES = {
    1: dict(layout="quote_stack", lines=[
        "Where is the Bihar School of Yoga located?",
        "What is Yoga Nidra, and why do people do it?",
        "If you were offered Moksha right now, would you accept?"]),
    2: dict(layout="statement", lines=["You are the syllabus now."]),
    3: dict(layout="title", lines=["ELEVATE", "Interview Guidance Program 2026"], hold=2.0),
    4: dict(layout="stat_hero", value="200+"),
    5: dict(layout="stacked_lines", lines=["275 marks.", "The widest spread of any paper you'll write."]),
    6: dict(layout="scorecard", label="Personality Test", value="2__", footer="Elevate IGP"),
    7: dict(layout="stacked_lines", lines=["Hours on Prelims?", "Hours on Mains?", "Hours on this?"], accent=[2]),
    8: dict(layout="stacked_lines", lines=["In Mains you write it and it's done.", "Here, somebody argues with you."]),
    9: dict(layout="stacked_lines", lines=["A mock shows you the gap.", "It can't be the preparation itself."]),
    10: dict(layout="numbered_list", items=[
        ["01", "Repair the DAF"], ["02", "Know what's been asked of your profile"],
        ["03", "Build opinions you can defend"], ["04", "Stay current where it touches you"],
        ["05", "Handle the room"]]),
    11: dict(layout="section_marker", number="01", heading="Repair the DAF"),
    12: dict(layout="statement", lines=["They've read it more carefully than you wrote it."]),
    13: dict(layout="stacked_lines", lines=["Blank fields.", "Casual wording.", "Entries that say nothing about you."]),
    14: dict(layout="stacked_lines", lines=["The real problem isn't what you put in.", "It's what you left out."], accent=[1]),
    15: dict(layout="advantage", label="ELEVATE IGP", lines=["Your DAF, checked against 20 defects."]),
    16: dict(layout="section_marker", number="02", heading="Stop guessing. Start knowing."),
    17: dict(layout="statement", lines=["The Board isn't working from your list."]),
    18: dict(layout="table_reveal", header=["[PROFILE REDACTED]", " · CSE 2026"], gap=0.5, rows=[
        ["Law graduate", "57 questions"], ["Home state, Bihar", "29"],
        ["Legal associate, private firm", "19"], ["Yoga, mystery novels", "18"],
        ["Debating, quizzing", "6"]]),
    19: dict(layout="stat_pair", left=["129", "questions"], right=["48", "tagged OPINION"]),
    20: dict(layout="statement", lines=["Practising Yoga"], hero=True, keep=True),
    21: dict(layout="node_fan", centre="Practising Yoga",
             nodes=["Ashtanga", "Surya Namaskar", "Hatha", "Meditation", "Yoga as policy"], keep=True),
    22: dict(layout="branch_expand", branches=[
        ["Ashtanga", "eight limbs · yama · niyama · vritti · which stage are you at"],
        ["Surya Namaskar", "twelve names · mantras · breathing pattern · why sampoorna yoga"],
        ["Hatha", "how it differs · Bihar School of Yoga · Yoga Nidra · Kundalini"],
        ["Meditation", "which school · under a guru · has it made you introverted"],
        ["Yoga as policy", "why 21st June · has the government overdone it · can an atheist be spiritual"]]),
    23: dict(layout="instance_stamps", gap=0.6, items=[
        ["At which stage of yoga are you?", "Chairman · 2022"],
        ["Should people of your age be pursuing spirituality?", "M1 · Apr 2025"],
        ["Yoga started as a quest for moksha but has been reduced to physical activity. Why?", "Chairman · Feb 2026"]]),
    24: dict(layout="labelled_quotes", label="DAF: Reading classic crime / mystery novels", quotes=[
        "Who is your favourite detective, and how does Poirot differ from Holmes?",
        "Is reading fiction a useful hobby, or living in a make believe world?"], tag=[1]),
    25: dict(layout="advantage", label="ELEVATE IGP", lines=[
        "The full topic list for your profile.", "The exact wording in which each question was asked."]),
    26: dict(layout="stacked_lines", lines=["Finish this first.", "Your own list comes after."]),
    27: dict(layout="section_marker", number="03", heading="Opinion questions take the most work."),
    28: dict(layout="delayed_reveal",
             main="Opinion on the presidential reference and the SC verdict on the governor's assent to bills?",
             reveal="(Choose a side. Do not give a balanced answer.)", stamp="Chairman · 13 Feb 2026"),
    29: dict(layout="stacked_lines", lines=["Your position, in the first sentence.", "A reason that survives one push.",
                                            "What honestly cuts against you.", "Then stop."], accent=[3], gap_before=[3]),
    30: dict(layout="advantage", label="ELEVATE IGP", lines=["We iterate on your opinion answers until they actually improve."]),
    31: dict(layout="section_marker", number="04", heading="Economy · Polity and Governance · International Relations",
             sub="And the last ninety days."),
    32: dict(layout="stacked_lines", lines=["Nobody will ask you to recite a scheme.", "They'll ask what you make of it."]),
    33: dict(layout="advantage", label="ELEVATE IGP", lines=["A weekly Opinion Matrix on the major issues."]),
    34: dict(layout="section_marker", number="05", heading="Handle the room."),
    35: dict(layout="statement", lines=["Are you winning the argument and losing the interview?"]),
    36: dict(layout="blank_slots", heading="Three types of questions.", sub="Three different things to do.",
             slots=["Type 1", "Type 2", "Type 3"]),
    37: dict(layout="count_stack", items=[["", "129", " profile questions"], ["~", "200", " current affairs questions"],
                                         ["", "", "+ motivation, service preference, the standard set"]]),
    38: dict(layout="statement", lines=["This is the floor, not the ceiling."]),
    39: dict(layout="closing_card", title="ELEVATE", subtitle="Interview Guidance Program 2026", features=[
        "DAF repair against 20 defects", "Personalised DAF PYQ questionnaire", "Iterative opinion preparation",
        "Weekly Opinion Matrix", "Board interaction strategy"],
        cta="[ENROLMENT DETAILS — insert link / QR / WhatsApp number before export]"),
}
