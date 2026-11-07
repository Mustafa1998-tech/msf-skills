"""Offline smoke test for both independently installed video skills."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def smoke(locale, resolution):
    name = "msf-video-studio" + ("-ar" if locale == "ar" else "")
    with tempfile.TemporaryDirectory(prefix="studio-smoke-") as temporary:
        folder = Path(temporary)
        skill = folder / "installed-skill"
        shutil.copytree(ROOT / "skills" / name, skill)
        output = folder / "training.mp4"
        command = [sys.executable, str(skill / "scripts" / "render.py"),
                   str(HERE / f"storyboard.{locale}.json"), str(output),
                   "--resolution", resolution]
        result = subprocess.run(command, capture_output=True, text=True, timeout=240)
        assert result.returncode == 0, result.stderr
        assert output.is_file(), "missing video"
        srt = output.with_suffix(".srt").read_text(encoding="utf-8")
        assert ("لوحة" if locale == "ar" else "sample board") in srt
        assert "-->" in srt
        metadata = json.loads(output.with_suffix(".qa.json").read_text())
        assert metadata["width"] == (3840 if resolution == "4k" else 1920)
        assert metadata["height"] == (2160 if resolution == "4k" else 1080)
        assert metadata["duration_seconds"] >= 6
        assert metadata["audio_codec"] == "aac"
        assert metadata["video_codec"] == "h264"
        assert metadata["locale"] == locale
        # Decode all video and audio rather than relying on container headers.
        subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(output),
                        "-f", "null", "-"], check=True, timeout=120)
        print(f"{locale}: {metadata['width']} × {metadata['height']}, "
              f"{metadata['duration_seconds']} s, H.264/AAC and UTF-8 SRT")

        unsafe = folder / "unapproved.json"
        unsafe.write_text(json.dumps({"locale": locale, "asset_scope": "review_pending"}),
                          encoding="utf-8")
        result = subprocess.run(command[:2] + [str(unsafe), str(folder / "unsafe.mp4")],
                                capture_output=True, text=True, timeout=15)
        assert result.returncode != 0 and "asset_scope" in result.stderr
        assert not (folder / "unsafe.mp4").exists()


if __name__ == "__main__":
    for language in ("en", "ar"):
        smoke(language, "4k" if "--4k" in sys.argv else "1080p")
