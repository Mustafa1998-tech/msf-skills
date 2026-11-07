#!/usr/bin/env python3
"""Report local runtimes; require optional tools only when requested."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys


def probe(executable, *args):
    path = shutil.which(executable)
    if path is None:
        return False, f"{executable} was not found on PATH"
    try:
        result = subprocess.run([path, *args], capture_output=True, text=True,
                                errors="replace", timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode == 0, output


def checks():
    python = (sys.version_info >= (3, 11), sys.version.split()[0])
    git_ok, git = probe("git", "--version")
    node_ok, node = probe("node", "--version")
    match = re.match(r"v(\d+)\.", node) if node_ok else None
    if match and int(match[1]) < 20:
        node_ok, node = False, f"{node}; Node 20 or newer is required for the dashboard checks"
    ffmpeg_ok, ffmpeg = probe("ffmpeg", "-version")
    ffprobe_ok, ffprobe = probe("ffprobe", "-version")
    video_problems = []
    if not ffmpeg_ok:
        video_problems.append(ffmpeg)
    if not ffprobe_ok:
        video_problems.append(ffprobe)
    if ffmpeg_ok:
        for args, token in ((("-hide_banner", "-filters"), "subtitles"),
                            (("-hide_banner", "-encoders"), "libx264")):
            ok, output = probe("ffmpeg", *args)
            if not ok or not re.search(rf"(?m)^\s*\S+\s+{token}\s", output):
                video_problems.append(f"FFmpeg capability missing: {token}")
    return {
        "python": python,
        "git": (git_ok, git.splitlines()[0] if git else "no version information"),
        "node": (node_ok, node.splitlines()[0] if node else "no version information"),
        "video": (not video_problems, "; ".join(video_problems) if video_problems else
                  f"{ffmpeg.splitlines()[0]}; ffprobe, libass subtitles and libx264 available"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require", choices=("git", "node", "video"), action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    required = {"python", *args.require}
    results = {name: {"status": "PASS" if ok else "FAIL" if name in required else "BLOCKED",
                      "required": name in required, "detail": detail}
               for name, (ok, detail) in checks().items()}
    if args.json:
        print(json.dumps(results, ensure_ascii=False))
    else:
        for name, result in results.items():
            print(f"{result['status']:7} {name:6} {result['detail']}")
    return any(result["status"] == "FAIL" for result in results.values())


if __name__ == "__main__":
    sys.exit(main())
