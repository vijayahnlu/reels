---
workflow: general-video
flow: automation
storyboard: no
message: "The interview is a separate exam about you; Elevate IGP prepares you for it."
destination: launch film (YouTube / website)
aspect: 16:9
length: 13:45
language: en
---

# ELEVATE IGP 2026 launch film

## Intent
Build the 39 slides exactly as specified in `BUILD_SPEC.md` (text and voiceover locked), rendered as HyperFrames video.
User direction: "super motion oriented, very clean, Apple brand like feel."

## Notes
- Design system, layouts and the six motions come from BUILD_SPEC.md § 1–4.
- No voiceover audio supplied yet. Slide lengths are estimated from each slide's VO word count, scaled to the
  section runtimes in the spec's timing map (`tools/durations.json`). Replace with real VO timings when recorded.
- S06 score stays masked as `2__` (consent gate, spec § 6).
- Logo on S03/S39: no logo file supplied; wordmark only.
- S39 CTA is still the spec's placeholder text.

## Delivery change (presenter request)
The film is presented live on Zoom, not voiced over: the deliverable is the click-through deck
`deck/elevate-igp-2026-deck.html` (built by `tools/deck_build.py`). The deck fills 3/4 of the recording,
so stamps, labels and sub-lines are set larger than the spec's scale. Speaker notes are the spec's VO.
