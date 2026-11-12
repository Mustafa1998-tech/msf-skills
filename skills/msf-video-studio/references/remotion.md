# Optional Remotion composition workflow

[العربية](../../msf-video-studio-ar/references/remotion.md) · [Runnable synthetic example](../../../examples/remotion-training-video/README.md)

## When to use it

Choose **Remotion + React** for custom branded motion graphics, animated titles, programmable scenes, charts, transitions and localized compositions. Choose the existing **FFmpeg** renderer for a simple, offline screen walkthrough from approved stills or clips. Playwright remains the separate source for authorized UI capture. Do not make Remotion a requirement for every video.

## Setup and agent guidance

1. Verify Node.js, npm, any required network access and the team's eligibility under the [current Remotion license](https://www.remotion.dev/docs/license/pricing). The runtime and upstream agent skills are **not** relicensed by MSF. Use a reviewed dependency version and generate/commit a lockfile in any production project.
2. Start from [the original synthetic example](../../../examples/remotion-training-video/README.md), or create a separate Remotion project with the official tooling. From the example directory run `npm install` followed by `npm run typecheck` and `npm run dev`.
3. Optionally install Remotion's upstream skills **within the Remotion project** using `npx remotion skills add` after reviewing their source, network behavior and terms. MSF already tracks links to the official Remotion skill repository and includes a reviewed snapshot of its MIT Codex plugin in `vendor/` for inspection. Do not silently download or activate these assets.
4. Build a storyboard with a single learning outcome. Design 1920 × 1080 compositions at 30 fps, with different Arabic RTL and English LTR copy and timing where needed. Use deterministic Remotion frame-based animations; no live user data, telemetry, or remote rendering.
5. For the sample, run `npm run render:ar` and `npm run render:en` (or the corresponding `:4k` commands). 4K uses `--scale=2` to produce 3840 × 2160. Confirm composition IDs, duration and output. Do not promise 4K detail when raster source media is lower-resolution.

## Combining with MSF Video Studio

- **Capture**: Use the optional MSF Playwright capture script on synthetic loopback fixtures or use approved, already sanitized footage; no authenticated production capture by default.
- **Compose**: Create animated segments in Remotion. Export a local MP4 and review it. A Remotion composition is not a direct input to `scripts/render.py`; only the exported video is.
- **Assemble (optional)**: Place a reviewed MP4 below the storyboard directory, reference it via the scene `source`, and set the scene duration appropriately. The MSF FFmpeg renderer removes the source clip audio; provide separately approved narration/music tracks if wanted. Keep subtitles in the original MSF storyboard (or avoid burning two conflicting caption tracks).
- **Deliver**: Report what actually ran. FFmpeg renders produce MP4, SRT and QA JSON; the stand-alone Remotion example produces MP4 only. External Remotion results need `ffprobe`, full decode, playback at normal speed and human checks; don't claim SRT, audio, QA or a successful render without producing/checking them.

## Security, licenses and validation

Use fictional or explicitly approved/sanitized scenes and audio. Don't expose credentials, internal service addresses, records or identifiable voices without the necessary permission. Keep runtime dependencies and input assets local unless explicitly authorized otherwise. Inspect fonts, RTL/LTR placement, captions, contrast, cursor location, transitions, audio sync and a visible end state. Check that the selected license covers institutional/commercial or automated use. If installation or browser rendering is unavailable, record that work as BLOCKED and fall back to the offline FFmpeg path; a typecheck or static file check alone is not a render pass.

Official references: [Render](https://www.remotion.dev/docs/render), [CLI flags](https://www.remotion.dev/docs/cli/render), [Agent Skills](https://www.remotion.dev/docs/ai/skills), [License](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
