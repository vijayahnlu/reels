# reels

Video projects built with [HyperFrames](https://github.com/heygen-com/hyperframes): you write a composition in HTML/CSS with a GSAP timeline, and the CLI renders it to MP4 frame by frame in headless Chrome.

## Setup

Requires Node 22+ and FFmpeg.

```bash
npm install
npx hyperframes browser ensure   # downloads the headless Chrome used for rendering
npx hyperframes doctor           # optional: check everything is in place
```

In Claude Code cloud sessions this runs automatically through `.claude/hooks/session-start.sh`.

## Making a video

```bash
npm run new -- my-clip           # scaffolds videos/my-clip at 1080x1920
cd videos/my-clip
npx hyperframes preview          # live-reload studio in the browser
npx hyperframes check            # lint + runtime + layout checks
npx hyperframes render --output out.mp4
```

Or ask Claude: "Using /hyperframes, make a 15-second reel about ..." The HyperFrames skills live in `.claude/skills/`.

`videos/starter` is a minimal example (a fade-in title) that renders cleanly.

## Footage and audio

`hyperframes init` can start a project from existing media:

```bash
npm run new -- my-recut --video path/to/clip.mp4
npm run new -- my-song --audio path/to/track.mp3
```

Transcription for captions needs whisper.cpp, which isn't installed here; `npx hyperframes doctor` lists the optional extras.
