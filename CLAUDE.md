# reels

Short-form videos made with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP rendered to MP4).

- Each video is its own HyperFrames project under `videos/<name>/`. Start one with `npm run new -- <name>` (portrait 1080x1920 by default).
- For any video work, load the `/hyperframes` skill first. The core skills are committed in `.claude/skills/`. Creation workflows (e.g. `/motion-graphics`, `/embedded-captions`) install on demand via `npx hyperframes skills update <workflow>`.
- Inside a project: `npx hyperframes check` before rendering, `npx hyperframes render --output out.mp4` to render, `npx hyperframes snapshot` for still frames.
- The cloud sandbox blocks public CDNs (jsdelivr, unpkg, cdnjs). Load scripts from local files in `assets/vendor/`, not CDN URLs. `npm run new` already does this for GSAP. For any other library, `npm install` it at the repo root and copy its dist file into the project.
- Rendered video files (`*.mp4`, `*.webm`, `*.mov`) are gitignored.

## UPSC talking-head reels

The owner makes UPSC explainer reels and doesn't code; do the whole edit for them. Every reel uses the shared look in `kit/` (read `kit/README.md`):
`scripts/prepare-reel.sh <raw-video> <name>` → correct `transcript.json` → `python3 scripts/tighten.py <name>` → write `videos/<name>/edit.json` (zooms and cards anchored to spoken words with `@word`) → `node scripts/build-reel.mjs <name>` → check, snapshot → `scripts/render-reel.sh <name>`. Never hand-edit a reel's `index.html`; it is regenerated from `edit.json`. Fact-check every number, date and name that goes on screen. `videos/upsc-demo` is the reference example.
