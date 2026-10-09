#!/usr/bin/env python3
"""Cut dead air and filler words out of a prepared reel (jump cuts).

Usage: python3 scripts/tighten.py <name> [--gap 0.35] [--pad 0.08] [--keep-fillers]

Reads videos/<name>/assets/footage.mp4 + transcript.json, keeps only the spoken
stretches, and writes back a tightened footage.mp4, a retimed transcript.json,
metadata.json and cuts.json (the time of every cut, used for jump-cut zooms).
The untrimmed originals are kept as *-untrimmed.* so this can be re-run.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

FILLERS = {"um", "umm", "uh", "uhh", "uhm", "erm", "er", "ah", "hmm", "mm"}

ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("--gap", type=float, default=0.35, help="pauses longer than this get cut (seconds)")
ap.add_argument("--pad", type=float, default=0.08, help="breathing room kept around each spoken stretch")
ap.add_argument("--keep-fillers", action="store_true")
args = ap.parse_args()

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(root, "videos", args.name)
src = os.path.join(d, "assets", "footage-untrimmed.mp4")
tr_src = os.path.join(d, "transcript-untrimmed.json")
if not os.path.exists(tr_src):
    shutil.copyfile(os.path.join(d, "transcript.json"), tr_src)
if not os.path.exists(src):
    shutil.copyfile(os.path.join(d, "assets", "footage.mp4"), src)

words = json.load(open(tr_src))
dur = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())

norm = lambda w: re.sub(r"[^a-z]", "", w.lower())
kept = [w for w in words if args.keep_fillers or norm(w["text"]) not in FILLERS]
if not kept:
    sys.exit("transcript is empty")

# Group spoken words into stretches separated by pauses longer than --gap.
segs = []
for w in kept:
    if segs and w["start"] - segs[-1]["last_end"] <= args.gap:
        segs[-1]["last_end"] = w["end"]
        segs[-1]["words"].append(w)
    else:
        segs.append({"first_start": w["start"], "last_end": w["end"], "words": [w]})
for s in segs:
    s["a"] = max(0.0, s["first_start"] - args.pad)
    s["b"] = min(dur, s["last_end"] + args.pad)
# Padding must not make neighbours overlap.
for s, n in zip(segs, segs[1:]):
    if s["b"] > n["a"]:
        mid = (s["last_end"] + n["first_start"]) / 2
        s["b"] = n["a"] = mid

out_words, cuts, t = [], [], 0.0
for i, s in enumerate(segs):
    if i:
        cuts.append(round(t, 3))
    for w in s["words"]:
        out_words.append({**w, "start": round(w["start"] - s["a"] + t, 3), "end": round(w["end"] - s["a"] + t, 3)})
    t += s["b"] - s["a"]

# One ffmpeg pass: trim each stretch, 8ms audio fades at the joins so cuts don't click.
parts, labels = [], []
for i, s in enumerate(segs):
    ln = s["b"] - s["a"]
    parts.append(f"[0:v]trim=start={s['a']:.3f}:end={s['b']:.3f},setpts=PTS-STARTPTS[v{i}]")
    parts.append(f"[0:a]atrim=start={s['a']:.3f}:end={s['b']:.3f},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=0.008,afade=t=out:st={max(0, ln - 0.008):.3f}:d=0.008[a{i}]")
    labels.append(f"[v{i}][a{i}]")
graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
script = os.path.join(d, ".tighten-filter.txt")
open(script, "w").write(graph)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex_script", script,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", os.path.join(d, "assets", "footage.mp4")], check=True)
os.remove(script)

json.dump(out_words, open(os.path.join(d, "transcript.json"), "w"), indent=0)
json.dump(cuts, open(os.path.join(d, "cuts.json"), "w"))
subprocess.run(f'ffprobe -v error -show_entries format=duration -of json "{d}/assets/footage.mp4" > "{d}/metadata.json"',
               shell=True, check=True)
removed = dur - t
print(f"Tightened videos/{args.name}: {dur:.1f}s -> {t:.1f}s ({removed:.1f}s of pauses/fillers cut, {len(cuts)} jump cuts)")
