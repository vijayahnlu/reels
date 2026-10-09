#!/bin/bash
# Usage: scripts/render-reel.sh <name>
# Full-quality render for upload: lossless PNG frame extraction from the footage (no JPEG
# softening on faces) and the high-quality encoder preset.
set -euo pipefail
name="${1:?usage: scripts/render-reel.sh <name>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root/videos/$name"
npx hyperframes check
npx hyperframes render --quality delivery --video-frame-format png --output "$name.mp4"
