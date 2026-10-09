# reels

Short-form videos made with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP rendered to MP4).

- Each video is its own HyperFrames project under `videos/<name>/`. Start one with `npm run new -- <name>` (portrait 1080x1920 by default).
- For any video work, load the `/hyperframes` skill first. The core skills are committed in `.claude/skills/`. Creation workflows (e.g. `/motion-graphics`, `/embedded-captions`) install on demand via `npx hyperframes skills update <workflow>`.
- Inside a project: `npx hyperframes check` before rendering, `npx hyperframes render --output out.mp4` to render, `npx hyperframes snapshot` for still frames.
- The cloud sandbox blocks public CDNs (jsdelivr, unpkg, cdnjs). Load scripts from local files in `assets/vendor/`, not CDN URLs. `npm run new` already does this for GSAP. For any other library, `npm install` it at the repo root and copy its dist file into the project.
- Rendered video files (`*.mp4`, `*.webm`, `*.mov`) are gitignored.
