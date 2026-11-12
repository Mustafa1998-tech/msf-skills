# Remotion training-video example (optional)

[العربية](README.ar.md) · [MSF Video Studio](../../skills/msf-video-studio/SKILL.md)

This is an **original MSF** sample with synthetic UI and a visible save confirmation, in separate Arabic RTL and English LTR compositions. It does not capture a real system, record audio, use external media, or publish anything. It complements, rather than replaces, the offline FFmpeg training-video example.

## Prerequisites and setup

Node.js and npm, network access for the **optional** dependency installation and Remotion's browser/runtime when requested. Review the pinned packages and [Remotion licensing](https://www.remotion.dev/docs/license/pricing) first; organizational and automated rendering use cases may require a paid license.

Run from this example directory:

```sh
cd examples/remotion-training-video
npm install
npm run typecheck
npm run dev
```

In another terminal, render a composition:

```sh
npm run render:ar
npm run render:en
npm run render:ar:4k
npm run render:en:4k
```

The 1080p renders are 1920 × 1080 at 30 fps. The 4K commands use Remotion's `--scale=2` (3840 × 2160). The source is vector/text-only, so no raster footage is silently upscaled. Output goes into the local `out/` directory; no output or npm packages are checked in.

## Agent skills (optional)

Inside a reviewed Remotion project, `npx remotion skills add` installs upstream Remotion Agent Skills for supported agents. Alternatively read the already indexed [Remotion source entries](../../GITHUB_SOURCES.md) and inspect the archived MIT Codex plugin in `vendor/`. This does **not** make the Remotion runtime or upstream skill licenses part of MSF's MIT license.

## Adaptation and review

Replace the fictional scene with **approved, sanitized** captures or re-create an explicitly permitted interface. Ensure cursor positions match rendered controls. For real software training, verify the beginning and successful end state, keep localized UI labels and narration in sync, and examine each exported frame for secrets, personal data, layout overflow, Arabic glyph shaping, and readability. Add separately approved voice/audio only when needed. A passing typecheck is not equivalent to a successful video render or human visual QA.

If the project does not need React-based animation, keep using [MSF's offline FFmpeg pipeline](../software-training-video/README.md). See [the optional Remotion workflow](../../skills/msf-video-studio/references/remotion.md).
