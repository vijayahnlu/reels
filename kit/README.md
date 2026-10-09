# UPSC reel kit

The shared look for every talking-head reel: newsprint paper, marker-yellow highlights, word-by-word captions, zoom punches, and explainer cards. A reel is just `videos/<name>/edit.json` plus the footage. `scripts/build-reel.mjs` turns that into `index.html`.

## Making a reel from raw footage

```bash
scripts/prepare-reel.sh /path/to/raw.mp4 <name>   # footage.mp4, audio.mp3, transcript.json
# fix ASR mistakes in videos/<name>/transcript.json (keep start/end), then write edit.json
node scripts/build-reel.mjs <name>
cd videos/<name> && npx hyperframes check && npx hyperframes snapshot --at 2,8,15
npx hyperframes render --output <name>.mp4
```

Transcription downloads its model from huggingface.co, so that host has to be allowed in the cloud environment's network settings.

## edit.json

```jsonc
{
  "title": "Ken-Betwa link",
  "duration": 38.4,                       // seconds, from metadata.json
  "captions": {
    "hot": ["Ken-Betwa", "1980."],         // words drawn with a yellow box (match the transcript token)
    "maxWords": 3, "maxChars": 16,         // optional grouping limits
    "off": [[0, 4.6]],                     // optional: time ranges with no captions
    "enabled": true
  },
  "sfx": true,                             // whooshes, pops and ticks on transitions
  "zooms": [                               // camera on the speaker, applied in order
    { "at": 0, "scale": 1.08, "style": "push", "dur": 4.6 },  // slow drift in
    { "at": 5.05, "scale": 1.22, "style": "punch" },          // hard punch-in on a key line
    { "at": 7.5, "scale": 1.0, "style": "smooth" }            // ease back out
  ],
  "cards": [ ... ]
}
```

`==text==` inside any title or label gets a marker highlight that sweeps in.

### Card types

Full-bleed (video stays full screen, card sits in the top third):

| type | fields |
| --- | --- |
| `hook` | `kicker`, `title` |
| `keyword` | `lines` (array) or `text`, optional `sub` |

Paper (video shrinks into a framed window at the top, card fills the area below; back-to-back paper cards share one window):

| type | fields |
| --- | --- |
| `headline` | `source`, `date`, `title`, `sub` (a clipping; use a neutral `source` like "Prelims Pointer", never a real paper's name for invented text) |
| `stat` | `value`, `from`, `decimals`, `prefix`, `unit`, `label`, `source` |
| `map` | `states` (ids below), `kicker`, `title`, `labels`, `note` |
| `timeline` | `kicker`, `title`, `items: [{year, text}]` (2 to 4 items), `step` |
| `term` | `kicker`, `title`, `body` |
| `compare` | `a: {title, items}`, `b: {title, items}` |

Every card takes `start` and `end` in seconds.

Map state ids: an ap ar as br ch ct dn dd dl ga gj hr hp jk jh ka kl ld mp mh mn ml mz nl or py pb rj sk tn tg tr up ut wb. The outline comes from `@svg-maps/india` (CC BY 4.0) and uses pre-2019 boundaries (no separate Ladakh), so check it against the official Survey of India map before using it for anything about J&K or Ladakh.

## Layout safe zones (1080x1920)

Instagram covers about the top 220px and bottom 380px, plus a strip on the right for buttons. Hooks and keywords start at y=240, paper cards live in y=920–1480, captions sit at y=1290 (full-bleed) or y=1515 (paper mode).
