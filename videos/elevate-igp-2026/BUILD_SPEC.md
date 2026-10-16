# ELEVATE IGP 2026 — Launch Film Build Spec

**Purpose of this file:** hand it to Claude Code (or any build agent) to generate the slide deck / animated frames for a 13–14 minute launch video.
**Deliverable expected from the build:** 39 slides, 1920×1080, dark theme, each slide matching the `layout` named in its block below.
**Do not rewrite the `vo` text.** It is the final locked voiceover. Slide text is also locked — build it, don't improve it.

---

## 1. Design system

```yaml
canvas:
  size: 1920x1080
  safe_margin: 140px all sides

theme: dark
colors:
  bg:          "#0B0B0C"
  bg_alt:      "#141416"   # used only for stamp/attribution strips
  text_primary:"#F5F3EF"
  text_muted:  "#8A8780"
  accent:      "#C8642A"   # CivilsDaily orange — single accent, used sparingly
  rule:        "#2A2A2D"
  opinion_tag: "#B3261E"   # the red OPINION tag from the questionnaire

type:
  display_font: "a tight grotesque — Neue Haas Grotesk Display, Inter Tight, or Söhne"
  body_font:    same family, lighter weight
  scale:
    hero:      132px / weight 600 / tracking -0.03em
    statement: 84px  / weight 500 / tracking -0.02em
    line:      56px  / weight 400
    label:     26px  / weight 600 / uppercase / tracking 0.14em
    stamp:     22px  / weight 400 / text_muted
  max_line_width: 20 words — never let a slide line wrap more than twice

rules:
  - One idea per slide. Never add a bullet that isn't in the spec.
  - No icons, no stock imagery, no gradients, no drop shadows.
  - No logo on interior slides. Logo on S03 and S39 only.
  - Left-align everything except S03 and S39 (centred).
  - Text sits on the lower-left third unless the layout says otherwise.
```

## 2. Animation grammar

Six motions only. Reuse them; do not invent more.

| name | behaviour | typical duration |
|---|---|---|
| `type_on` | characters type in, cursor visible, no sound | 1.2s per line |
| `fade_up` | opacity 0→1 with 24px rise, ease-out | 0.6s |
| `stagger` | children run `fade_up` sequentially | 0.35s gap |
| `clear_to` | existing content fades out fully, new content fades up | 0.8s |
| `fan_out` | nodes radiate from a centre word along straight connectors | 0.5s per node |
| `count_up` | numerals tick from 0 to final value | 1.5s |

Hold each slide 1.5s after its last motion before cutting.

## 3. Timing map

| section | slides | runtime |
|---|---|---|
| Cold open | S01–S03 | 0:00–1:10 |
| Why the usual plan breaks | S04–S10 | 1:10–3:40 |
| 01 Repair the DAF | S11–S15 | 3:40–5:20 |
| 02 DAF PYQ Questionnaire | S16–S26 | 5:20–9:00 |
| 03 Opinion questions | S27–S30 | 9:00–10:45 |
| 04 Contemporary issues | S31–S33 | 10:45–11:45 |
| 05 Handling the board | S34–S36 | 11:45–12:50 |
| Close | S37–S39 | 12:50–13:45 |

## 4. Layout types

| layout | structure |
|---|---|
| `quote_stack` | 2–3 question lines, `type_on` in sequence, stay on screen together |
| `statement` | one hero line, centred vertically, `fade_up` |
| `title` | wordmark + programme name, centred |
| `stat_hero` | one large numeral, `count_up`, optional caption below |
| `scorecard` | document-style card, redaction bar, one value highlighted |
| `stacked_lines` | 2–4 lines, `stagger` |
| `numbered_list` | `01`–`05` with labels, `stagger` |
| `section_marker` | large number + section heading, `fade_up` |
| `table_reveal` | two-column rows, `stagger`, right column in accent |
| `stat_pair` | two numerals side by side, second one carries the OPINION tag |
| `node_fan` | centre word + 5 radiating nodes, `fan_out` |
| `branch_expand` | each node from previous slide expands into a sub-line, `stagger` |
| `instance_stamps` | quoted question + attribution strip in `bg_alt`, `stagger` |
| `labelled_quotes` | small DAF label line, then quoted questions below |
| `advantage` | `ELEVATE IGP` label in accent, then 1–2 lines |
| `delayed_reveal` | main line, 1.5s hold, then second line appears in accent |
| `blank_slots` | heading + three slots rendered as `___` |
| `count_stack` | three figures accumulating, `count_up` on each |
| `closing_card` | wordmark, programme name, 5-item feature list, CTA block |

---

# 5. Slides

---

### S01
```yaml
id: S01
section: cold_open
layout: quote_stack
animation: type_on (sequential), 1.2s each
lines:
  - "Where is the Bihar School of Yoga located?"
  - "What is Yoga Nidra, and why do people do it?"
  - "If you were offered Moksha right now, would you accept?"
note: No attribution on screen yet. The reveal is in the voiceover.
```
**vo:**
Where is the Bihar School of Yoga located. What is Yoga Nidra and why do people do it. And then, a minute later, from the same Chairman, in the same interview: if you were offered moksha right now, would you accept it.

That was the thirteenth of February this year. Sanjay Verma's board. And the candidate sitting in that room had written two words in her form, under hobbies. Hatha yoga. Two words, and the board stayed there for several minutes.

---

### S02
```yaml
id: S02
section: cold_open
layout: statement
animation: clear_to, then fade_up
lines:
  - "You are the syllabus now."
```
**vo:**
I want to start there because it tells you something about this stage that most people only figure out afterwards. For two years you've been studying a syllabus that was identical for everybody in the country. Same books, same current affairs, same questions. And then you reach the last stage, and quietly the syllabus changes. It becomes you. Your district, your degree, the firm you worked at, the hobby you filled in without thinking very hard about it.

---

### S03
```yaml
id: S03
section: cold_open
layout: title
animation: fade_up
lines:
  - "ELEVATE"
  - "Interview Guidance Program 2026"
logo: true
hold: 2.0s
```
**vo:** *(silence — no voiceover on this slide)*

---

### S04
```yaml
id: S04
section: why_plan_breaks
layout: stat_hero
animation: count_up
value: "200+"
```
**vo:**
Let me give you the number that's changed how we think about this stage. Two hundred.

A few years ago, if you got a one eighty in your personality test, that was a good interview and everybody told you so. Now look at who's actually getting the service they wanted. They're at two hundred, two ten, two fifteen. That's where the top of the list has moved, and if you're planning around one eighty you're planning around an old benchmark.

---

### S05
```yaml
id: S05
section: why_plan_breaks
layout: stacked_lines
animation: stagger
lines:
  - "275 marks."
  - "The widest spread of any paper you'll write."
```
**vo:**
And it's worth remembering what this paper actually carries. Two seventy five marks, which is the same as a full optional. Except your optional has a syllabus you can finish, and this one doesn't, and the gap between the top and the bottom here is wider than anywhere else in the exam. I've seen two candidates finish mains within eight or nine marks of each other and end up in completely different services because of what happened on one morning in Dholpur House.

---

### S06
```yaml
id: S06
section: why_plan_breaks
layout: scorecard
animation: fade_up, then highlight score
fields:
  name: "[NAME REDACTED]"       # render as a solid redaction bar
  label: "Personality Test"
  value: "2__"                   # last two digits masked until consent is on file
  footer: "Elevate IGP"
note: CONSENT GATE — see section 6 before this slide is finalised.
```
**vo:**
This is one of our candidates from last cycle. I'm keeping the name off the screen until she's comfortable with it being public, so just look at the number for now. She did not get there by knowing more than the people around her. Her mains marks weren't the highest in the room. What she did differently was treat this stage as a separate exam, with its own preparation, starting months before the result came out.

---

### S07
```yaml
id: S07
section: why_plan_breaks
layout: stacked_lines
animation: stagger
lines:
  - "Hours on Prelims?"
  - "Hours on Mains?"
  - "Hours on this?"
note: Third line in accent colour.
```
**vo:**
So let me ask you something, and answer it honestly, because nobody's listening. How many hours did you put into prelims. How many into mains. And then this one.

For most people the third number is whatever was left over. Two or three mocks after the result, one reading of the DAF the night before, and the newspaper, which you were doing anyway. And then you walk into a room with four people who have your form in front of them and have been doing this for years.

---

### S08
```yaml
id: S08
section: why_plan_breaks
layout: stacked_lines
animation: stagger
lines:
  - "In Mains you write it and it's done."
  - "Here, somebody argues with you."
```
**vo:**
The reason leftover preparation doesn't work here is that the format is nothing like anything you've trained for. In mains you write your answer, you shut the booklet, and whatever you wrote is what they're marking. Nobody follows up.

Here you say something and the person across the table disagrees with it. Or asks you to narrow it. Or says, you've given me three points, now tell me which one matters most. Or pushes you to pick a side when you were sitting very comfortably in the middle, giving a balanced answer. And knowing more facts does not rescue you in that moment. That's a different skill and it has to be built separately.

---

### S09
```yaml
id: S09
section: why_plan_breaks
layout: stacked_lines
animation: stagger
lines:
  - "A mock shows you the gap."
  - "It can't be the preparation itself."
```
**vo:**
There's one more thing people do, which I want to flag early. They treat mocks as the preparation. Mock is a test. Showing you what's missing is its job, and it does that job well. But you can't build a plan out of whatever three panels happened to ask you on three random mornings, because the next three would have asked you something else entirely. You prepare first and then you test yourself. That order matters, and most people have it backwards.

---

### S10
```yaml
id: S10
section: why_plan_breaks
layout: numbered_list
animation: stagger
items:
  - ["01", "Repair the DAF"]
  - ["02", "Know what's been asked of your profile"]
  - ["03", "Build opinions you can defend"]
  - ["04", "Stay current where it touches you"]
  - ["05", "Handle the room"]
note: This list is reused as the spine. S11, S16, S27, S31, S34 are its section markers.
```
**vo:**
So here's what we do in Elevate, and I'd ask you to pay attention to the order as much as the list, because the order is where most preparation goes wrong.

---

### S11
```yaml
id: S11
section: pillar_1_daf
layout: section_marker
animation: fade_up
number: "01"
heading: "Repair the DAF"
```
**vo:**
Everything else is built on this one document, which is why it's first.

---

### S12
```yaml
id: S12
section: pillar_1_daf
layout: statement
animation: fade_up
lines:
  - "They've read it more carefully than you wrote it."
```
**vo:**
It's the only thing the board has about you before you walk in. They've had it for days. By the time you sit down, somebody on that panel has read it, marked two or three things on it, and decided where they're going to start. You filled that form in an afternoon, probably in a hurry, probably while you were still waiting for the mains result.

---

### S13
```yaml
id: S13
section: pillar_1_daf
layout: stacked_lines
animation: stagger
lines:
  - "Blank fields."
  - "Casual wording."
  - "Entries that say nothing about you."
```
**vo:**
And it shows. Blank fields create an impression before you've said a single word. So do entries filled in language you'd never use anywhere else in your life. Hobby: reading. Hobby: listening to music. There are four people reading that and thinking, alright, so what are we going to ask her. It reads as careless, and once in a while it reads as unprofessional, and you've given them that impression for free.

---

### S14
```yaml
id: S14
section: pillar_1_daf
layout: stacked_lines
animation: stagger
lines:
  - "The real problem isn't what you put in."
  - "It's what you left out."
note: Second line in accent.
```
**vo:**
But the mistake I see most often is the opposite of what you'd expect. Everyone worries about exaggerating. Almost nobody does. What actually happens is that something genuinely interesting happened in your life, and you kept it off the form, because you looked at the column and decided it didn't fit there. It fits. Very often it's the single most interesting thing you could have put on that page, and you've left the board with nothing to work with except your degree and your district.

---

### S15
```yaml
id: S15
section: pillar_1_daf
layout: advantage
animation: fade_up
label: "ELEVATE IGP"
lines:
  - "Your DAF, checked against 20 defects."
```
**vo:**
We don't leave this to instinct or to one person's feel for it. Your DAF goes through a fixed checklist of twenty defects, line by line, and we fix what's broken before any of the other work starts.

---

### S16
```yaml
id: S16
section: pillar_2_questionnaire
layout: section_marker
animation: fade_up
number: "02"
heading: "Stop guessing. Start knowing."
```
**vo:**
Now the second thing, and this is where most of the work in this programme actually sits.

---

### S17
```yaml
id: S17
section: pillar_2_questionnaire
layout: statement
animation: fade_up
lines:
  - "The Board isn't working from your list."
```
**vo:**
Everyone makes a list of expected questions. You sit down with a notebook, you look at your form, and you guess. And your guess is built on what seems relevant to you, from where you're sitting, with your own blind spots. Meanwhile the board is working from years of its own practice, and that practice leaves a record. Those interviews happened. People remember what they were asked. We've been collecting it for years.

---

### S18
```yaml
id: S18
section: pillar_2_questionnaire
layout: table_reveal
animation: stagger (0.5s gap — this slide needs breathing room)
header: "[PROFILE REDACTED] · CSE 2026"
rows:
  - ["Law graduate", "57 questions"]
  - ["Home state, Bihar", "29"]
  - ["Legal associate, private firm", "19"]
  - ["Yoga, mystery novels", "18"]
  - ["Debating, quizzing", "6"]
note: Right column in accent. Numbers should land with weight.
```
**vo:**
This is a questionnaire we built for a candidate this cycle. Look at the profile first. A law degree, a job at a firm in Noida, Bihar as her home state, two hobbies, and two college prizes. There is nothing unusual on this page. Half the people watching this video have a form that looks roughly like this.

Now look at the right hand column. Fifty seven questions out of a law degree. Twenty nine out of the state she happens to be from. Six out of a quizzing prize she won in college and had probably stopped thinking about.

---

### S19
```yaml
id: S19
section: pillar_2_questionnaire
layout: stat_pair
animation: count_up on both
left:  { value: "129", caption: "questions" }
right: { value: "48",  caption: "tagged OPINION", tag: true }
note: Render the OPINION tag exactly like the questionnaire's — white text on opinion_tag red.
```
**vo:**
One hundred and twenty nine in total. And forty eight of those are not asking her what she knows. They're asking her where she stands, which is a completely different thing to prepare for.

---

### S20
```yaml
id: S20
section: pillar_2_questionnaire
layout: statement
animation: clear_to, then fade_up
lines:
  - "Practising Yoga"
note: Set at hero scale. Nothing else on the slide. This is the pivot of the whole film.
```
**vo:**
I want to take the smallest entry on her form and open it up, because this is the part that surprises people. Two words.

---

### S21
```yaml
id: S21
section: pillar_2_questionnaire
layout: node_fan
animation: fan_out
centre: "Practising Yoga"
nodes:
  - "Ashtanga"
  - "Surya Namaskar"
  - "Hatha"
  - "Meditation"
  - "Yoga as policy"
note: Centre word shrinks from hero to line scale as the nodes appear.
```
**vo:**
You wrote one phrase. The board doesn't read it as one phrase. It reads the words sitting inside it, and every one of those is a separate direction they can walk in.

---

### S22
```yaml
id: S22
section: pillar_2_questionnaire
layout: branch_expand
animation: stagger
branches:
  - ["Ashtanga",       "eight limbs · yama · niyama · vritti · which stage are you at"]
  - ["Surya Namaskar", "twelve names · mantras · breathing pattern · why sampoorna yoga"]
  - ["Hatha",          "how it differs · Bihar School of Yoga · Yoga Nidra · Kundalini"]
  - ["Meditation",     "which school · under a guru · has it made you introverted"]
  - ["Yoga as policy", "why 21st June · has the government overdone it · can an atheist be spiritual"]
```
**vo:**
Eight questions, and sixty seven recorded instances of them being asked across the last few years. Some of it is what you'd expect. Sheel Vardhan Singh's board asking for the eight limbs of ashtanga, asking what vritti means, asking at what level you practise and how long you've been doing it.

But watch how fast it stops being about yoga at all. Preeti Sudan's board asked a candidate what change she'd seen in herself because of it. Somebody else was asked whether meditation had made her introverted, or self critical. That's not a question about yoga, that's a question about her personality, and it arrived through a hobby entry. Dinesh Dasa's board asked whether meditation has any practical value for military personnel. Another board asked whether the government has overdone the promotion of yoga, which is a policy opinion, and you'd better have one.

---

### S23
```yaml
id: S23
section: pillar_2_questionnaire
layout: instance_stamps
animation: stagger (0.6s gap)
items:
  - quote: "At which stage of yoga are you?"
    stamp: "Chairman · 2022"
  - quote: "Should people of your age be pursuing spirituality?"
    stamp: "M1 · Apr 2025"
  - quote: "Yoga started as a quest for moksha but has been reduced to physical activity. Why?"
    stamp: "Chairman · Feb 2026"
note: Stamps sit in a bg_alt strip under each quote, in text_muted at stamp scale.
```
**vo:**
These aren't questions we invented to frighten you into joining a programme. Every one of them carries a year, a board, a member and a date, and you can see them in the document.

And look at the middle one. Should somebody your age be pursuing spirituality at all. Nobody sits at home preparing for that. That's the board checking whether the entry is actually yours or whether it went on the form because it looked good there.

---

### S24
```yaml
id: S24
section: pillar_2_questionnaire
layout: labelled_quotes
animation: fade_up label, then stagger quotes
label: "DAF: Reading classic crime / mystery novels"
quotes:
  - "Who is your favourite detective, and how does Poirot differ from Holmes?"
  - "Is reading fiction a useful hobby, or living in a make believe world?"
note: Second quote carries the OPINION tag.
```
**vo:**
The same thing happens to the entry you thought was completely safe. She wrote that she reads crime fiction, because it's true, and because it seemed harmless.

The first question checks whether she's actually read them. Fine, she has. The second one has nothing to do with books. Is reading fiction useful, or is it living in a make believe world. That's an opinion question wearing a hobby's clothes, and that's the one that catches people, because they've prepared Agatha Christie's plots and they haven't prepared a view on whether fiction is worth an adult's time.

---

### S25
```yaml
id: S25
section: pillar_2_questionnaire
layout: advantage
animation: stagger
label: "ELEVATE IGP"
lines:
  - "The full topic list for your profile."
  - "The exact wording in which each question was asked."
```
**vo:**
Two things you get out of this. You get the topic list, so you know where the boundary is and you can stop preparing in the dark, which is what most people are doing in December and January. And you get the exact wording, which matters more than people realise, because what are the benefits of yoga and why do you only do asanas and not pranayam are two very different questions, and the second one has a slight edge in it that you need to hear coming.

---

### S26
```yaml
id: S26
section: pillar_2_questionnaire
layout: stacked_lines
animation: stagger
lines:
  - "Finish this first."
  - "Your own list comes after."
```
**vo:**
I'll be direct about the sequence, because this is where people lose months. Your own list of likely questions is not priority one. Cover what has actually been asked of profiles like yours, finish that properly, and then put your own thinking on top of it. Not before. The reason we widen the scope deliberately, going from yoga into ashtanga and surya namaskar and the Bihar School of Yoga, is so that you have a larger surface area to stand on, and you're not caught off guard when somebody comes at your hobby from an angle you never considered.

---

### S27
```yaml
id: S27
section: pillar_3_opinion
layout: section_marker
animation: fade_up
number: "03"
heading: "Opinion questions take the most work."
```
**vo:**
Somewhere between thirty and forty percent of your interview is going to ask you to take a position on something.

---

### S28
```yaml
id: S28
section: pillar_3_opinion
layout: delayed_reveal
animation: fade_up main, 1.5s hold, then reveal
main: "Opinion on the presidential reference and the SC verdict on the governor's assent to bills?"
reveal: "(Choose a side. Do not give a balanced answer.)"
stamp: "Chairman · 13 Feb 2026"
note: The reveal line is the single most important beat in this section. Give it the accent colour and a full 1.5s hold before it lands.
```
**vo:**
Here's one from February. Opinion on the presidential reference and the Supreme Court verdict on the governor's assent to bills. And then read the line underneath it, which is what the Chairman added. Choose a side. Don't give me a balanced answer.

If your plan for the hard questions is to say there's merit on both sides and then stop talking, this is the sentence waiting for you. And it's a bad moment to be building an opinion for the first time, in front of four people, with somebody watching your face while you do it.

---

### S29
```yaml
id: S29
section: pillar_3_opinion
layout: stacked_lines
animation: stagger
lines:
  - "Your position, in the first sentence."
  - "A reason that survives one push."
  - "What honestly cuts against you."
  - "Then stop."
note: Fourth line in accent, slightly larger gap above it.
```
**vo:**
Seeing the other side of an argument is a strength, and I'd never tell you to drop it. Hiding behind it is a different thing and the board can tell the difference immediately.

So lead with your judgement, in the first sentence, before anything else. Then give one reason you can actually defend when somebody leans on it, not three reasons you half believe. Then say honestly what cuts against your position, because that's what makes the first part credible. And then stop talking. I'd say most answers in that room lose their marks in the sentences that came after the point had already been made.

---

### S30
```yaml
id: S30
section: pillar_3_opinion
layout: advantage
animation: fade_up
label: "ELEVATE IGP"
lines:
  - "We iterate on your opinion answers until they actually improve."
```
**vo:**
One attempt at a question like that gives you a draft and nothing more. So we go back to the same question, again, and again, with feedback in between, until there's a real difference in how you frame it and how you hold it when somebody argues with you.

---

### S31
```yaml
id: S31
section: pillar_4_current_affairs
layout: section_marker
animation: fade_up
number: "04"
heading: "Economy · Polity and Governance · International Relations"
subheading: "And the last ninety days."
```
**vo:**
Current affairs for the interview is a different animal from what you revised for prelims. It's weighted heavily towards what's moved recently, and towards whatever touches your own profile. If you're a lawyer, the three new criminal laws are going to come up. If you're from Bihar, prohibition is going to come up, and so is the caste survey, and you should know that before you walk in.

---

### S32
```yaml
id: S32
section: pillar_4_current_affairs
layout: stacked_lines
animation: stagger
lines:
  - "Nobody will ask you to recite a scheme."
  - "They'll ask what you make of it."
```
**vo:**
And the questions are not what you've practised for. You can know every feature of a scheme, every number, every year, and still have nothing to say when somebody asks you whether it was designed well, or whether it should have been a central scheme at all. Same news item, two completely separate jobs: knowing it, and having a view on it that holds up.

---

### S33
```yaml
id: S33
section: pillar_4_current_affairs
layout: advantage
animation: fade_up
label: "ELEVATE IGP"
lines:
  - "A weekly Opinion Matrix on the major issues."
```
**vo:**
Which is why every week you get the major issues laid out properly. The competing positions, what the evidence actually supports on each side, and where a follow up is likely to take you if you commit to one of them. You build the view in advance, with time to think about it, instead of assembling it on the spot in front of a board.

---

### S34
```yaml
id: S34
section: pillar_5_board
layout: section_marker
animation: fade_up
number: "05"
heading: "Handle the room."
```
**vo:**
And the last piece, which people almost never prepare for at all.

Being challenged in that room is just part of the format. It doesn't mean you were wrong, and it isn't a signal to fold either, and the whole skill is working out which of the two is happening in front of you, in real time, while you're also trying to answer.

---

### S35
```yaml
id: S35
section: pillar_5_board
layout: statement
animation: fade_up
lines:
  - "Are you winning the argument and losing the interview?"
```
**vo:**
I've watched candidates defend a point long past the moment it stopped being worth defending. You can be entirely correct, factually, and still walk out of that room having cost yourself fifteen marks, because somewhere in those four minutes it stopped being an answer and became an argument you wanted to win. You're there to win the interview. The argument is not the thing.

---

### S36
```yaml
id: S36
section: pillar_5_board
layout: blank_slots
animation: stagger
heading: "Three types of questions."
subheading: "Three different things to do."
slots: ["Type 1 ___", "Type 2 ___", "Type 3 ___"]
note: The blanks stay blank. This is deliberate — do not fill them in.
```
**vo:**
Inside the programme we break board questions into three types and work through exactly what you do with each one. Where you commit, where you concede and move on, where you take a breath before you answer. I'm leaving the blanks on screen deliberately, because that session is for people who've enrolled.

---

### S37
```yaml
id: S37
section: close
layout: count_stack
animation: count_up on each, stagger
items:
  - "129 profile questions"
  - "~200 current affairs questions"
  - "+ motivation, service preference, the standard set"
```
**vo:**
Let me give you the real volume before you sign up for anything, so there are no surprises in January. For the profile I showed you, a hundred and twenty nine questions from the DAF. Roughly two hundred on current affairs. And then the standard set on top of that, why civil services, why IAS and not IPS, your service preference, your cadre preference.

---

### S38
```yaml
id: S38
section: close
layout: statement
animation: clear_to, then fade_up
lines:
  - "This is the floor, not the ceiling."
```
**vo:**
That number shouldn't frighten you. If anything it should recalibrate what you thought this stage was going to take. This is the minimum, not some ambitious target. You did this much work for prelims without complaining, and prelims wasn't even about you. This one is entirely about you, which is the one advantage you have here, and almost nobody uses it.

---

### S39
```yaml
id: S39
section: close
layout: closing_card
animation: fade_up, then stagger the feature list
logo: true
title: "ELEVATE"
subtitle: "Interview Guidance Program 2026"
features:
  - "DAF repair against 20 defects"
  - "Personalised DAF PYQ questionnaire"
  - "Iterative opinion preparation"
  - "Weekly Opinion Matrix"
  - "Board interaction strategy"
cta: "[ENROLMENT DETAILS — insert link / QR / WhatsApp number before export]"
```
**vo:**
So that's the programme. Fix the document, find out what's actually been asked of people with your profile, build positions you can stand behind when somebody pushes, stay current where it touches you, and learn to read the room. Enrolment details are on the screen and the link is below.

And whether you join us or not, do one thing this week. Open your DAF and read it the way four strangers are going to read it in January. Start there, not after the result.

---

## 6. Pre-production sign-offs

**S06 — consent gate.** The slide shows a real candidate's personality test score. Written consent must be on file before export, even with the name redacted, because the profile details on S18 could identify her to anyone who knows her. Until that consent exists, keep the score masked as `2__` or drop S06 and bridge S05 → S07 directly.

**S04 / S38 — the 200+ claim.** This is framed throughout as the speaker's reading of where outcomes have moved, not as a published UPSC benchmark. Keep it that way in the edit. Do not add a source citation, a chart, or any on-screen framing that makes it look like official data.

**Not in this script, by decision.** The alpha / beta / sigma board-personality framing from the original brief has been replaced by the three question types on S36. A public launch film claiming we can type named UPSC board members by personality is the most clippable liability in the brief, and the coaching underneath it survives without the taxonomy.

## 7. Source material

All questions, boards, members and dates are drawn from the CivilsDaily Personalised DAF Analysis & Questionnaire (UPSC CSE Personality Test 2026) built for the redacted candidate profile. The source document is watermarked "FOR PERSONAL USE ONLY" — do not screenshot it directly into the film. Rebuild every quote as typeset slide text.
