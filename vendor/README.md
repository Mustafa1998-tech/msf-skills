# Archived upstream sources

[العربية](README.ar.md) · [Full source register](../GITHUB_SOURCES.md)

These ZIP snapshots preserve selected upstream skill source, scripts, and references at fixed Git revisions. Each archive carries its original license and applicable notices included in the reviewed scope. The snapshots retain their upstream licenses. Use the [index](index.json) for exact revisions, SHA-256 digests and archive scope.

| Upstream snapshot | License | Preserved scope |
| --- | --- | --- |
| [Superpowers](archives/superpowers.zip) | MIT | All 15 skill folders and their bundled scripts and references. Repository plugins, hooks and tests outside skills are omitted. |
| [Impeccable](archives/impeccable.zip) | Apache-2.0 | Generated Codex skill, references and scripts. Two derived platform guides and the generated browser bundle are omitted pending separate attribution review. The CLI is separate. |
| [UI UX Pro Max](archives/ui-ux-pro-max.zip) | MIT | Complete UI/UX Pro Max skill folder, including datasets, provenance and Python scripts. |
| [Anthropic Skills (Frontend Design)](archives/anthropic-frontend-design.zip) | Apache-2.0 | Complete Frontend Design skill only, with its own license. |
| [Vercel Web Interface Guidelines](archives/web-interface-guidelines.zip) | MIT | Guidelines and command source. The upstream installer is omitted. |
| [Remotion Codex Plugin](archives/remotion-codex.zip) | MIT | Skill text, references and source scripts from the MIT Codex plugin. Logos, media and the separately licensed Remotion runtime are omitted. |
| [HyperFrames](archives/hyperframes.zip) | Apache-2.0 | Core, CLI and registry skill code, references and HTML/CSS templates. Fonts, media and the CLI runtime are omitted. |
| [onetake-videogen](archives/onetake-videogen.zip) | MIT | Skill, pipeline scripts, Remotion project source and original notices. Media, upstream patches and installer are omitted. External runtimes are separate. |

## Read or extract offline

From the repository root, with Python 3.11 or later:

```sh
python3 scripts/vendor-skills.py list
python3 scripts/vendor-skills.py verify
python3 scripts/vendor-skills.py extract superpowers ./superpowers-review
```

The destination must be new. Extraction verifies the archive and writes files without loading a skill or running upstream code. Review the instructions, scripts and runtime requirements before using or manually enabling any archived skill. Keep the applicable license and notices with any copied material. The MSF installer installs original MSF skills only. Some archives omit assets or rely on separately installed runtimes, packages, services or other network resources. A snapshot alone does not make those workflows fully offline.

OneTake Motion stays in the [source register](../GITHUB_SOURCES.md) under its noncommercial license. The separate Remotion Skills and Remotion Claude plugin repositories also stay as references because their licenses were not established. The archive comes from the MIT-licensed Remotion Codex plugin and covers its selected skill sources.
