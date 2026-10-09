#!/bin/bash
# Usage: scripts/prepare-reel.sh <path/to/raw-video> <name>
# Sets up videos/<name>/ from a raw phone recording:
#   - re-encodes to 1080x1920, 30fps, dense keyframes (assets/footage.mp4)
#   - writes metadata.json and audio.mp3
#   - transcribes to transcript.json (word timings for captions)
# Then write videos/<name>/edit.json and run: node scripts/build-reel.mjs <name>
set -euo pipefail

src="${1:?usage: scripts/prepare-reel.sh <video> <name>}"
name="${2:?usage: scripts/prepare-reel.sh <video> <name>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
dir="$root/videos/$name"
mkdir -p "$dir/assets"

# Fill 9:16 (crop if the source is wider), 30fps, keyframe every frame-second so seeking never freezes.
ffmpeg -y -loglevel error -i "$src" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
  -c:v libx264 -crf 18 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$dir/assets/footage.mp4"

ffprobe -v error -show_entries format=duration -of json "$dir/assets/footage.mp4" > "$dir/metadata.json"
ffmpeg -y -loglevel error -i "$dir/assets/footage.mp4" -vn -acodec libmp3lame -q:a 2 "$dir/audio.mp3"

if npx hyperframes transcribe "$dir/audio.mp3" -d "$dir" --model "${WHISPER_MODEL:-small.en}"; then
  echo "Transcript: videos/$name/transcript.json"
else
  echo "Transcription failed. If the error mentions huggingface.co, allow that host in the environment's network settings." >&2
fi
echo "Ready: videos/$name (duration $(python3 -c "import json;print(round(float(json.load(open('$dir/metadata.json'))['format']['duration']),2))")s)"
