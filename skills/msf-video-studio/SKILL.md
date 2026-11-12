---
name: msf-video-studio
description: Use when producing software training videos, screen walkthroughs, feature demos, or localized tutorials with a storyboard, captured screens, cursor emphasis, accessible subtitles, optional narration, and 1080p or 4K delivery.
---

# MSF Video Studio

## Scope

Make reproducible, locally rendered English or Arabic software training videos. One video should teach one task from its starting state through a visible confirmation. Deliver a separate render and caption file for each language; record localized screens whenever button labels differ. The local renderer accepts stills or video and produces MP4, timed SRT, and technical QA. Browser recording and outside editing or voice tools are optional.

## Inputs

- Audience, task, success state, locale, target runtime, and release context.
- Approved screenshots or clips at 16:9, ideally at the delivery resolution. Keep captures and audio under the storyboard directory; use relative file paths.
- A timed script with scene length, captions, optional position cues and transitions, plus any approved narration or music. Start from [the storyboard](references/video-storyboard.json).
- A real review record for reusable software, visual assets, audio, and voices. Assign an owner to review the cut before any distribution.

## Prerequisites

Python 3.9+, `ffmpeg` and `ffprobe` on PATH, FFmpeg built with `libx264`, AAC and the libass `ass` filter, and DejaVu Sans installed. Arabic requires libass complex shaping and Arabic glyphs in the installed font. Optional capture requires Node.js, Playwright 1.48+ and its Chromium browser.

## Workflow

1. Define the outcome in one sentence. Start with the task and the screen on which it begins. Show the smallest complete sequence; end by pointing to what proves success. Keep text short enough to read before the cut.
2. Seed the fixture with fictional records. Capture the necessary states or record an authorized training run. Disable notifications and start from a clean session. Optional: serve the training fixture on loopback, write a capture plan as described in [the reference](references/studio.md), and run `node scripts/capture.cjs capture.json local-captures`.
3. Set `asset_scope` only after review. Put captions and cues on scene-local timestamps. Coordinates use a 1920 × 1080 design canvas even when exporting 4K. Position an animated cursor, a focus outline, or a short callout on the precise control, keeping the lower caption area clear. Pair edits with brief fades or use a hard cut between tightly connected actions.
4. Add approved scene narration and optional low-level music. Use the UI's exact labels in both spoken and caption text; have a fluent reviewer check Arabic pronunciation and terminology. Use separate projects for translated timing. Source clip audio is excluded; supply any retained audio separately as an approved track.
5. Render from the installed skill directory, then review a draft at normal speed. Use `--no-burn-captions` if the delivery player will load the SRT and the video should remain visually clean.
6. When the brief calls for programmable React motion graphics, branded transitions or reusable animated compositions, use the **optional Remotion workflow** in [the Remotion guide](references/remotion.md). It has a bilingual synthetic example and a separate runtime/license review. Keep the default offline FFmpeg workflow for simpler tutorials; never install outside agent skills or Remotion packages without opting in. Export a reviewed Remotion MP4 before using it as a storyboard scene source.

```bash
python3 scripts/render.py /path/to/storyboard.json /path/to/output.mp4 --resolution 1080p
# Use a different output filename and --resolution 4k for a 3840 × 2160 master.
```

## Safety

Use synthetic or approved and already sanitized inputs. Never capture production credentials, tokens, customer records, personal data, private internal URLs, or desktop notifications. Redo any contaminated capture before ingestion; cropping, focus boxes and subtitle overlays do not redact source material. Do not pass client footage, scripts, recordings, or voices to outside tools without permission covering that tool and use. Obtain affirmative consent and scope for any identifiable voice or likeness; use a locally approved generic voice or omit narration when rights are unclear. The renderer runs offline, does not accept remote assets, and never publishes; an `asset_scope` field records a review claim and cannot detect sensitive frames.

## Outputs

Deliver the editable storyboard and approved source assets to the intended owner, plus `output.mp4`, `output.srt` (UTF-8) and `output.qa.json`. The MP4 is 1920 × 1080 or 3840 × 2160, 30 fps, H.264/yuv420p with AAC stereo. When no audio is supplied the AAC track is silent. State the language, review status, and where the consent record lives without including personal details.

## Validation

- Check the QA report against the requested resolution, codecs, scene count and expected timing. Decode the entire MP4 if it will be distributed.
- Play every scene at normal speed. Confirm the taught task can be repeated, the final state is visible, the cursor lands accurately, the callouts stay clear of buttons, and captions remain readable and synchronized. Review Arabic shaping, right-to-left flow and mixed-direction labels with a fluent reviewer.
- Listen with and without headphones. Narration should remain clear above the background; adjust gains and re-render when needed. Verify any voice, music and screen recording permissions and scrub the full video for sensitive data before handoff.

## Failure handling

If `ass`, `libx264` or AAC is missing, use an FFmpeg build that includes it. Missing or disconnected Arabic glyphs require checking the font and libass shaping, then reviewing the render again. For unknown paths, move the approved inputs beneath the storyboard and avoid remote links. If the capture browser is unavailable, use authorized manually captured stills or clips; rendering does not require Playwright. If the test is visually wrong or an approval is missing, correct the inputs or omit the affected asset before release.

## References

- [Storyboard template](references/video-storyboard.json)
- [File format, capture and adapter guide](references/studio.md)
- [Optional Remotion / React motion graphics workflow](references/remotion.md)
