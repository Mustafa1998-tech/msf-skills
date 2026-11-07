# Quality and release

[العربية](../ar/quality.md)

Record every gate with scope, command or artifact, result and relevant revision. A PASS covers only the evidence named. FAIL records an executed check that failed. BLOCKED identifies missing access, runtime or evidence. NOT APPLICABLE includes a reason tied to scope.

| Gate | Evidence |
| --- | --- |
| Discovery | Task, boundaries, repo rules, skill selection |
| Architecture | Contracts, ADR, compatibility and risk |
| Design | Theme/direction matrix, keyboard, viewport and visual review |
| Engineering | Implementation diff, build or focused code checks |
| Security | Authorized scope, findings, secret and license review |
| Testing | Actual tests, exit and environment |
| Documentation | Link, parity and command checks |
| Video | Media probe, decode, timing, language and human review |
| Release | Exact remote SHA, public access, successful CI and approval |

The default quality command runs the local baseline. Add `--with-video` for the bundled render smoke test. Strict mode requires review evidence alongside local checks. See `python3 scripts/run-quality-gates.py --help`. A local pass cannot establish remote Actions, platform discovery, deployment or release. Review the exact candidate in CI before creating a public tag and keep earlier artifacts available for rollback.
