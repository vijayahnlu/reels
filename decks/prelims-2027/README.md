# Prelims 2027, animated deck

`prelims-2027.html` is the whole 50-slide deck in one file. It works offline in Chrome.

## Presenting
- Open the file in Chrome and press **F** for full screen. On Zoom, share that Chrome window.
- **→, Space or a clicker** shows the next build. When a slide is fully built, the next press moves to the next slide.
- **←** steps back. **R** replays the current slide from the start.
- **Click any picture or chart** to zoom it, and click again to come back.
- Type a slide number and press **Enter** to jump there (for example `27` then Enter).
- Press **N** to open your speaker notes in a separate window. Share only the deck window.

## Rebuilding after a change
```
python3 tools/parse_pptx.py <deck.pptx> model.json media   # only if the PPT changes
python3 tools/build_deck.py                                  # writes prelims-2027.html
```
What happens on each click is set in `tools/deck_config.py`.
