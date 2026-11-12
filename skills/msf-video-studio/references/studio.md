# Studio file format and capture

A storyboard lives next to its media. It contains `title` (a planning label, not an automatically generated title card), `locale` (`en` or `ar`), `asset_scope` (`synthetic` or `approved_sanitized` after review), and 1–40 entries in `scenes`. Keep the original review records separately from the renderable JSON.

| Field | Meaning |
| --- | --- |
| Scene `source` | Local PNG, JPG, WebP, MP4, MOV, MKV, or WebM under the storyboard directory. A still holds for the entire scene. A short video holds its last frame. Non-16:9 sources are letterboxed. |
| `duration`, `source_start` | Scene length in seconds (0.5–300, rounded to a frame); optional video seek in seconds. Audio begins at the scene boundary independently of the source video seek. |
| `transition` | Optional `fade_in` and `fade_out` in seconds, each at most half the scene. Fades run to or from black without overlapping scene timelines. Omit them for hard cuts. |
| `captions` | Sorted `{start,end,text}` entries in scene-local seconds with no overlaps. Timing is rebased into a UTF-8 SRT. Burned captions default to enabled; include relevant sound cues and concise visual context. |
| `overlays` | Timed entries share `start` and `end`. A `cursor` has `at: [x,y]` and optional `to: [x,y]`. A `focus` has `box: [x,y,width,height]`. A `callout` has `at: [x,y]` for its center and `text`. Positions are on the final 1920 × 1080 design canvas, including any letterbox. |
| Scene `narration` and global `music` | Optional `{source,approval,gain}` objects. Use a relative WAV, MP3, M4A, FLAC, or OGG. `approval` is `provided_approved` or `licensed_synthetic`, after actual review. Narration is trimmed to the scene and defaults to 0.85 linear gain; music loops, defaults to 0.12, and is mixed below narration. |

Place one cue on the important control, keep callouts under two lines, and leave space below for captions. Use native 4K media when a 4K deliverable needs native UI detail; a 1080p input upscales when exported to 4K. Verify focus and overlay locations again whenever changing aspect ratio or capture source.

## Optional local capture

Serve only your approved mock fixture on loopback, with no account or stored session. Install Playwright in a local Node environment with its Chromium build (see the installation documentation). Run the capture script with a JSON plan and a new output directory:

```json
{
  "asset_scope": "synthetic",
  "locale": "en",
  "url": "http://127.0.0.1:8765/fixture.html",
  "record_video": false,
  "steps": [
    {"wait_for":"#begin","file":"start.png"},
    {"click":"#begin","wait_for":"#success","hold_ms":500,"file":"finish.png"}
  ]
}
```

Steps optionally click a selector, select a value with `"select": {"locator":"#status","value":"ready"}`, wait for a selector to be visible, and hold up to 10 seconds before saving a PNG. Set `record_video` to `true` to also save a 1920 × 1080 browser-only WebM. The capture script blocks off-origin requests, service workers, downloads and WebSockets. It still records everything visible on the local page, so sanitize before capture and review every frame. It does not automate an authenticated production browser or capture desktop applications; use approved, already sanitized desktop clips for those.

## External adapters

Local file import is the integration boundary. If use of an external tool and the material has been approved, a team may export generic voice audio from [ElevenLabs](https://elevenlabs.io/docs/overview/intro), a licensed presenter segment from [HeyGen](https://developers.heygen.com/) or [Synthesia](https://docs.synthesia.io/), or a cut from [Descript](https://help.descript.com/). Export a local audio or video file, inspect it, and import it using the storyboard. For speech embedded in a presenter clip, export its audio separately and reference it as approved narration. These are manual file workflows. There are no vendor credentials, API calls, built-in connectors, or automatic uploads. If terms, consent, or data handling are unclear, continue with the offline workflow.

### Optional composition and caption tools

- [Remotion](https://github.com/remotion-dev/remotion) or [HyperFrames](https://github.com/heygen-com/hyperframes): evaluate when a project needs its own HTML/React motion templates. Review the applicable upstream license and runtime before use. Export the segment to a local video file; neither renderer is bundled.
  For Remotion, follow the [MSF optional bilingual workflow and working example](remotion.md); external packages remain opt-in.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper): use a locally approved model to draft subtitle text or timings. A fluent human should correct terminology, reading order, and cue timing before the draft becomes storyboard captions. The local renderer does not fetch models.
- [edge-tts](https://github.com/rany2/edge-tts): optional online voice generation for approved scripts and voices. Review service access and usage terms before generating a local narration asset. The renderer never calls it.
- The inventory separates similarly named projects: [onetake for motion films](https://github.com/feitangyuan/onetake), [onetake-videogen](https://github.com/Nael-Nathanael/onetake-videogen), and [OneTake automatic editor](https://github.com/leejersey/OneTake). Assess the named project's license and interfaces separately before using an export.

## Upstream documentation

- [FFmpeg filters](https://www.ffmpeg.org/ffmpeg-filters.html) and [ffprobe](https://www.ffmpeg.org/ffprobe.html)
- [libass](https://github.com/libass/libass)
- [Playwright installation](https://playwright.dev/docs/intro), [screenshots](https://playwright.dev/docs/screenshots), and [video recording](https://playwright.dev/docs/videos)
