# ELEVATE IGP launch, animated deck

`igp-launch.html` is the whole 27-slide deck in one file, with every picture inside it. It works offline in Chrome.
It is built from `IGP_Launch_-Vijaya.pptx`: every text box, line, screenshot and the QR code sit where the PPT has them.

## Presenting
- Open the file in Chrome and press **F** for full screen. On Zoom, share that Chrome window.
- **→, Space or a clicker** plays the next build. Pressing again while a build is playing finishes it at once.
  When a slide is fully built, the next press moves to the next slide.
- **←** steps back. **R** replays the current slide.
- Type a slide number and press **Enter** to jump there.
- **N** opens your speaker notes (the notes from the PPT) in a separate window. Share only the deck window.

## Rebuilding after a change
```
python3 tools/parse_pptx.py <deck.pptx>   # only if the PPT changes; writes model.json and media/
python3 tools/build.py                    # writes igp-launch.html
```
What each click plays is in `tools/slides.js`; the drawings and light positions per slide are in `tools/build.py`.
Drawings: game-icons.net (Lorc, Delapouite and contributors), CC BY 3.0. Font: Liberation Sans (SIL OFL), metric match for Arimo.
