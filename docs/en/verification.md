# Initial candidate verification

[العربية](../ar/verification.md)

| Scope | Evidence | Outcome |
| --- | --- | --- |
| Repository | `python3 scripts/run-quality-gates.py --with-video` | Eight local gates pass. Remote release requires separate evidence. |
| Skills and installation | `python3 scripts/validate-skills.py` and installer lifecycle tests | 24 skill folders validated. All 24 copied into a temporary Codex project; English and Arabic removal exercised separately. Claude Code user layout tested with an isolated home. |
| Sources | `python3 scripts/check-sources.py` | 43 source records checked against the bilingual register. The source audit recorded public repo metadata and head SHAs; see the register for licensing exceptions. |
| Dashboard | Node model tests and Chromium | Three model tests, desktop and mobile interaction checks, language direction and theme, keyboard, search and table behavior. Screenshots are synthetic. |
| Inventory | Angular 20.3.35 build, ASP.NET Core .NET 10 build, HTTP boundary and Chromium | Angular and API build. Auth and validation tested against a running API; browser lifecycle tested with simulated responses. SQL Server integration remains BLOCKED. |
| Video | 1080p and 4K smoke plus Playwright screenshot capture | English and Arabic 12.9-second renders decoded; four browser frames captured per locale at 1920×1080. The 4K sample upscales 1080p assets. Arabic sample uses captions and an optional narration input. |
| CI and release | Workflow YAML, least-privilege permissions and pinned action reviewed locally | GitHub Actions, anonymous repository access and release remain BLOCKED until remote verification. |

The offline runner checks formats and configured tests. It does not authenticate a reviewer, run independent third-party security scanners, or certify live agent discovery. Evidence from a targeted test applies only to its stated environment.
