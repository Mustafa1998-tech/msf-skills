# Install MSF Skills

[العربية](INSTALL.ar.md) · [Overview](README.md)

Use a reviewed MSF checkout and Python 3.11 or later. The helper copies complete skill folders and does not download packages, start an agent or install its dependencies. Choose the locale that fits your project. Run these commands in the MSF checkout and replace the project path.

| Host | Project | User | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` | `$msf-orchestrator`, `$msf-testing` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/msf-orchestrator`, `/msf-testing` |

```sh
python3 scripts/install-skills.py install --target codex --scope project --language en --project-root /path/to/project
python3 scripts/install-skills.py install --target claude --scope project --language ar --project-root /path/to/project
```

For user scope, use `--scope user` and omit `--project-root`. Use `--language both` to copy both variants. Add `--dry-run` to preview. For manual installation copy each whole selected directory from `skills/` to the appropriate path above, preserving its name. Avoid mixing manually managed and helper-managed copies in the same scope.

Start a new local session from the project. In Codex, use the skill picker or type the dollar-prefixed skill name. In Claude Code, type the slash-prefixed name. For Arabic use the exact `-ar` suffix. Example: `$msf-orchestrator-ar` or `/msf-orchestrator-ar`, followed by the task. In local versions supporting automatic discovery, frontmatter descriptions help the agent choose workflows.

## Update, remove and troubleshoot

- Run the helper with `list` and the same target, scope, language and project root to inspect copies. Back up locally edited skills.
- Uninstall an unmodified helper installation with `uninstall` and the same flags. Check out a reviewed revision and run `install` again. Manually copied folders should be removed or updated manually after review.
- If discovery fails, check the host, skill folder name, `SKILL.md` location and selected locale. Try a new local session and check for another same-named skill or organization policy. Use `python3 scripts/validate-skills.py` in the checkout for structural checks.
- Use an up-to-date local client with documented Agent Skills support. No minimum client build or hosted-session installation is certified here. Hosted clients and managed policies have separate rules.
- Media, scanning and framework tools have separate prerequisites. See the corresponding skill and the [upstream source register](GITHUB_SOURCES.md). For opt-in offline extraction of preserved upstream source, see the [archive guide](vendor/README.md).

[OpenAI installation conventions](https://developers.openai.com/api/reference/cli) · [Claude Code skills](https://code.claude.com/docs/en/skills) · [Agent Skills specification](https://agentskills.io/specification)
