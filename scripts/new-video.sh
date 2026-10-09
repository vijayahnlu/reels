#!/bin/bash
# Usage: npm run new -- <name> [extra hyperframes init flags]
# Scaffolds videos/<name> in portrait (1080x1920) and swaps the GSAP CDN link
# for a local copy, since the cloud sandbox can't reach cdn.jsdelivr.net.
set -euo pipefail

name="${1:?usage: npm run new -- <name>}"
shift
root="$(cd "$(dirname "$0")/.." && pwd)"
dir="$root/videos/$name"

mkdir -p "$root/videos"
cd "$root/videos"
HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "$name" --non-interactive --resolution portrait "$@"

mkdir -p "$dir/assets/vendor"
cp "$root/node_modules/gsap/dist/gsap.min.js" "$dir/assets/vendor/"
sed -i 's|https://cdn.jsdelivr.net/npm/gsap@[^"]*/dist/gsap.min.js|assets/vendor/gsap.min.js|' "$dir/index.html"
echo "Ready: videos/$name"
