#!/usr/bin/env python3
"""Render an approved local storyboard to H.264/AAC, SRT, and technical QA."""
import argparse
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

FPS = 30
SIZES = {"1080p": (1920, 1080), "4k": (3840, 2160)}
IMAGES = {".png", ".jpg", ".jpeg", ".webp"}
VIDEOS = {".mp4", ".mov", ".mkv", ".webm"}
AUDIO = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}


def fail(message):
    raise ValueError(message)


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout


def ffmpeg(args, cwd):
    return run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                "-filter_threads", "2", "-filter_complex_threads", "2", *args], cwd)


def number(value, label, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        fail(f"{label} must be a number between {low} and {high}")
    return value


def media(base, value, label, extensions):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        fail(f"{label} must be a relative local file path")
    path = (base / value).resolve()
    if not path.is_relative_to(base) or not path.is_file() or path.suffix.lower() not in extensions:
        fail(f"{label} must be an existing supported file inside the storyboard directory")
    return path


def approved_audio(base, track, label):
    if not isinstance(track, dict) or track.get("approval") not in {
            "provided_approved", "licensed_synthetic"}:
        fail(f"{label} requires explicit recorded approval for the supplied audio")
    return media(base, track.get("source"), label, AUDIO)


def point(value, label, maximum=(1920, 1080)):
    if not isinstance(value, list) or len(value) != 2:
        fail(f"{label} must be [x,y]")
    return tuple(round(number(v, label, 0, m)) for v, m in zip(value, maximum))


def message(value, label):
    if (not isinstance(value, str) or not value.strip() or len(value) > 220
            or any(c in value for c in "{}\\\r") or any(
                not c.isprintable() and c != "\n" for c in value)
            or any(not line.strip() for line in value.split("\n"))):
        fail(f"{label} needs 1–220 printable characters, without empty lines, braces or backslashes")
    return value.strip()


def asstime(seconds, srt=False):
    fraction = round(seconds * (1000 if srt else 100))
    whole, fraction = divmod(fraction, 1000 if srt else 100)
    mins, sec = divmod(whole, 60)
    hour, mins = divmod(mins, 60)
    return (f"{hour:02}:{mins:02}:{sec:02},{fraction:03}" if srt else
            f"{hour}:{mins:02}:{sec:02}.{fraction:02}")


def localized_text(value, locale):
    # Direction marks keep punctuation and mixed UI labels in visual order for
    # players that otherwise default to a left-to-right paragraph.
    if locale == "ar":
        return "\n".join("\u200f" + line + "\u200f" for line in value.split("\n"))
    return value


def write_ass(path, events):
    lines = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080",
        "ScaledBorderAndShadow: yes", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
        " BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
        " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Caption,DejaVu Sans,49,&H00FFFFFF,&H000000FF,&H24110D0B,&H3C110D0B,"
        "0,0,0,0,100,100,0,0,4,0,12,2,110,110,64,-1",
        "Style: Callout,DejaVu Sans,36,&H00FFFFFF,&H000000FF,&H003F2519,&H003F2519,"
        "-1,0,0,0,100,100,0,0,4,0,11,5,25,25,25,-1",
        "Style: Vector,DejaVu Sans,16,&H00FFFFFF,&H000000FF,&H00301C0D,&H00301C0D,"
        "0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for layer, start, end, style, value in events:
        lines.append(f"Dialogue: {layer},{asstime(start)},{asstime(end)},{style},,0,0,0,,{value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def scene_data(base, scene, index, start, burn, locale):
    if not isinstance(scene, dict):
        fail(f"scene {index} must be an object")
    key = f"scene {index}"
    source = media(base, scene.get("source"), f"{key}.source", IMAGES | VIDEOS)
    duration = round(number(scene.get("duration"), f"{key}.duration", 0.5, 300) * FPS) / FPS
    offset = number(scene.get("source_start", 0), f"{key}.source_start", 0, 7200)
    if offset and source.suffix.lower() in IMAGES:
        fail(f"{key}.source_start only applies to video")
    transition = scene.get("transition", {})
    if not isinstance(transition, dict):
        fail(f"{key}.transition must be an object")
    fades = {side: round(number(transition.get(side, 0), f"{key}.{side}", 0, duration / 2) * FPS)
             for side in ("fade_in", "fade_out")}
    events, srt = [], []
    previous_end = 0
    for entry in scene.get("captions", []):
        if not isinstance(entry, dict):
            fail(f"{key}.captions items must be objects")
        a, b = times(entry, duration, f"{key}.captions")
        if a < previous_end:
            fail(f"{key}.captions must be sorted and cannot overlap")
        previous_end = b
        caption = localized_text(message(entry.get("text"), f"{key}.captions.text"), locale)
        srt.append((start + a, start + b, caption))
        if burn:
            events.append((5, a, b, "Caption", caption.replace("\n", r"\N")))

    for entry in scene.get("overlays", []):
        if not isinstance(entry, dict):
            fail(f"{key}.overlays items must be objects")
        a, b = times(entry, duration, f"{key}.overlays")
        kind = entry.get("type")
        if kind == "focus":
            box = entry.get("box")
            if not isinstance(box, list) or len(box) != 4:
                fail(f"{key}.focus.box must be [x,y,width,height]")
            x, y = point(box[:2], f"{key}.focus.box")
            w, h = point(box[2:], f"{key}.focus.box", (1920 - x, 1080 - y))
            if min(w, h) < 10:
                fail(f"{key}.focus width and height must be at least 10")
            draw = (f"m 0 0 l {w} 0 {w} {h} 0 {h} 0 0 "
                    f"m 5 5 l 5 {h-5} {w-5} {h-5} {w-5} 5 5 5")
            events.append((1, a, b, "Vector", rf"{{\an7\pos({x},{y})\1c&H2BCEFF&\p1}}{draw}"))
        elif kind == "cursor":
            x, y = point(entry.get("at"), f"{key}.cursor.at")
            endx, endy = point(entry.get("to", [x, y]), f"{key}.cursor.to")
            travel = round((b - a) * 1000)
            move = rf"\move({x},{y},{endx},{endy},0,{travel})"
            draw = "m 0 0 l 0 36 10 28 17 42 23 38 16 25 30 25 0 0"
            events.append((2, a, b, "Vector", rf"{{\an7{move}\bord3\p1}}{draw}"))
        elif kind == "callout":
            x, y = point(entry.get("at"), f"{key}.callout.at")
            caption = localized_text(message(entry.get("text"), f"{key}.callout.text"), locale).replace("\n", r"\N")
            events.append((3, a, b, "Callout", rf"{{\pos({x},{y})}}{caption}"))
        else:
            fail(f"{key}.overlays.type must be cursor, focus or callout")

    narration = scene.get("narration")
    audio = None
    if narration is not None:
        audio = (approved_audio(base, narration, f"{key}.narration"),
                 number(narration.get("gain", 0.85), f"{key}.narration.gain", 0, 1))
    return source, offset, duration, fades, events, srt, audio


def times(entry, duration, label):
    start = number(entry.get("start"), f"{label}.start", 0, duration)
    end = number(entry.get("end"), f"{label}.end", 0, duration)
    if end - start < 1 / FPS:
        fail(f"{label} needs at least one video frame")
    return start, end


def make_scene(tmp, index, scene, size):
    source, offset, duration, fades, events, _, _ = scene
    width, height = size
    is_image = source.suffix.lower() in IMAGES
    flags = ["-loop", "1", "-framerate", str(FPS)] if is_image else ["-ss", str(offset)]
    filters = [
        f"scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos",
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x101820",
        "setsar=1", f"fps={FPS}", "format=yuv420p",
    ]
    if not is_image:
        filters.append(f"tpad=stop_mode=clone:stop_duration={duration}")
    if events:
        overlay = f"scene-{index}.ass"
        write_ass(tmp / overlay, events)
        filters.append(f"ass={overlay}:shaping=complex")
    frames = round(duration * FPS)
    for side, amount in fades.items():
        if amount:
            pos = 0 if side == "fade_in" else frames - amount
            filters.append(f"fade=t={'in' if side == 'fade_in' else 'out'}:s={pos}:n={amount}")
    filename = f"scene-{index}.mp4"
    ffmpeg([*flags, "-protocol_whitelist", "file", "-i", str(source), "-map", "0:v:0",
            "-an", "-sn", "-dn", "-vf", ",".join(filters), "-frames:v", str(frames),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-threads", "3", "-pix_fmt", "yuv420p", filename], tmp)
    return filename


def mux(tmp, files, scenes, duration, music):
    (tmp / "scenes.ffconcat").write_text(
        "ffconcat version 1.0\n" + "".join(
            f"file {name}\nduration {scene[2]:.9f}\n" for name, scene in zip(files, scenes)),
        encoding="ascii",
    )
    command = ["-f", "concat", "-safe", "1", "-i", "scenes.ffconcat",
               "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    filters = [f"[1:a]atrim=duration={duration}[silence]"]
    tracks = ["[silence]"]
    elapsed = 0
    for _, _, length, _, _, _, voice in scenes:
        if voice:
            path, gain = voice
            index = len(tracks) + 1
            command.extend(["-protocol_whitelist", "file", "-i", str(path)])
            delay = round(elapsed * 48000)
            filters.append(f"[{index}:a:0]aresample=48000,aformat=channel_layouts=stereo,"
                           f"atrim=duration={length},asetpts=PTS-STARTPTS,"
                           f"volume={gain},adelay={delay}S:all=1[voice{index}]")
            tracks.append(f"[voice{index}]")
        elapsed += length
    if music:
        path, gain = music
        index = len(tracks) + 1
        command.extend(["-stream_loop", "-1", "-protocol_whitelist", "file", "-i", str(path)])
        filters.append(f"[{index}:a:0]aresample=48000,aformat=channel_layouts=stereo,"
                       f"atrim=duration={duration},asetpts=PTS-STARTPTS,volume={gain}[music]")
        tracks.append("[music]")
    filters.append("".join(tracks) +
                   f"amix=inputs={len(tracks)}:duration=first:normalize=0,"
                   "alimiter=limit=0.95:level=0:latency=1[audio]")
    ffmpeg([*command, "-filter_complex", ";".join(filters), "-map", "0:v:0", "-map", "[audio]",
            "-t", f"{duration:.9f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "result.mp4"], tmp)


def probe(path, size, expected_duration, locale, count, captions, audio):
    info = json.loads(run(["ffprobe", "-v", "error", "-show_streams",
                           "-show_format", "-of", "json", str(path)]))
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
    sound = next((s for s in info["streams"] if s["codec_type"] == "audio"), {})
    duration = float(info["format"]["duration"])
    if (video.get("width"), video.get("height")) != size:
        fail("rendered video does not match requested resolution")
    if (video.get("codec_name") != "h264" or video.get("pix_fmt") != "yuv420p"
            or video.get("r_frame_rate") != f"{FPS}/1" or sound.get("codec_name") != "aac"
            or sound.get("sample_rate") != "48000" or sound.get("channels") != 2):
        fail("rendered media failed the H.264/AAC 30 fps delivery checks")
    if abs(duration - expected_duration) > 2 / FPS:
        fail(f"rendered duration {duration} does not match storyboard duration {expected_duration}")
    return {"width": size[0], "height": size[1], "duration_seconds": duration,
            "video_codec": "h264", "audio_codec": "aac", "fps": FPS, "locale": locale,
            "scene_count": count, "caption_count": captions, "audio_tracks_supplied": audio,
            "human_review_required": True}


def render(storyboard, output, resolution, burn):
    if output.suffix.lower() != ".mp4":
        fail("output must end in .mp4")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            fail(f"{tool} is required on PATH")
    data = json.loads(storyboard.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("asset_scope") not in {"synthetic", "approved_sanitized"}:
        fail("asset_scope must be synthetic or approved_sanitized; review the footage before rendering")
    locale = data.get("locale")
    if locale not in ("en", "ar"):
        fail("locale must be en or ar")
    inputs = data.get("scenes")
    if not isinstance(inputs, list) or not 1 <= len(inputs) <= 40:
        fail("scenes must be a list of 1–40 scene objects")
    base = storyboard.resolve().parent
    scenes, duration, captions = [], 0, []
    for i, value in enumerate(inputs, 1):
        scene = scene_data(base, value, i, duration, burn, locale)
        scenes.append(scene)
        duration += scene[2]
        captions.extend(scene[5])
    if not captions:
        fail("include at least one timed caption")
    music = data.get("music")
    if music is not None:
        music = (approved_audio(base, music, "music"),
                 number(music.get("gain", 0.12), "music.gain", 0, 0.5))

    output = output.resolve()
    files = [output, output.with_suffix(".srt"), output.with_suffix(".qa.json")]
    if any(item.exists() for item in files):
        fail("output or a sidecar already exists; choose a new output path")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="studio-", dir=output.parent) as directory:
        tmp = Path(directory)
        segments = [make_scene(tmp, i, scene, SIZES[resolution])
                    for i, scene in enumerate(scenes)]
        mux(tmp, segments, scenes, duration, music)
        metadata = probe(tmp / "result.mp4", SIZES[resolution], duration, locale, len(scenes),
                         len(captions), int(bool(music)) + sum(bool(scene[6]) for scene in scenes))
        metadata["burned_captions"] = burn
        srt = "\n\n".join(f"{i}\n{asstime(a, True)} --> {asstime(b, True)}\n{text}"
                          for i, (a, b, text) in enumerate(captions, 1))
        (tmp / "result.srt").write_text(srt + "\n", encoding="utf-8")
        (tmp / "result.qa.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        for source, target in zip(("result.mp4", "result.srt", "result.qa.json"), files):
            (tmp / source).replace(target)
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--resolution", choices=SIZES, default="1080p")
    parser.add_argument("--no-burn-captions", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.storyboard, args.output, args.resolution,
                                not args.no_burn_captions), indent=2))
    except subprocess.CalledProcessError as error:
        parser.exit(1, f"Render failed: {error.stderr.strip()}\n")
    except (ValueError, OSError, TypeError, KeyError) as error:
        parser.exit(1, f"Render failed: {error}\n")


if __name__ == "__main__":
    main()
