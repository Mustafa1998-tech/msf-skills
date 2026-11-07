# MSF Skills · Mustafa AI Software Factory

**From Idea to Enterprise-Grade Software.**

Created by Mustafa. MSF Skills is an independent, bilingual collection of agent workflows, implementation references, checks and examples for software delivery. Pick one language and start with the orchestrator, or invoke a specialized skill directly.

[العربية](README.ar.md) · [Install](INSTALL.md) · [Source and license register](GITHUB_SOURCES.md)

## Skill catalog

Every English ID has an equivalent Arabic ID with the suffix `-ar`. The registry lists all 24 installable directories.

| Skill | Applies to |
| --- | --- |
| `msf-orchestrator` | Intent, repository discovery, selective routing and evidence |
| `msf-planning` | Requirements, processes, stories, tasks, risk and ADRs |
| `msf-architecture` | Boundaries, architecture decisions, refactoring and review |
| `msf-ui-ux` | Enterprise interfaces, RTL/LTR, themes, accessibility and critique |
| `msf-frontend` | Angular, TypeScript, forms, state and API integration |
| `msf-backend` | ASP.NET Core, REST, auth, jobs and SignalR |
| `msf-database` | SQL Server, EF Core, queries, integrity and migrations |
| `msf-security` | Authorized defensive security and DevSecOps |
| `msf-testing` | CRUD, API, browser, accessibility and regressions |
| `msf-devops` | CI/CD, IIS, containers, infrastructure, reliability and release |
| `msf-documentation` | Manuals, OpenAPI, deployment, troubleshooting and release notes |
| `msf-video-studio` | Capture, narration, captions, rendering and media QA |

## Start

Install from a reviewed checkout using [INSTALL.md](INSTALL.md). For a new work item, invoke the orchestrator and state the goal, repository, acceptance criteria and safety limits. The orchestrator inspects the workspace, routes only applicable work and attaches evidence. Existing repository conventions and authorization apply.

```sh
python3 scripts/verify-environment.py
python3 scripts/run-quality-gates.py
python3 scripts/run-quality-gates.py --with-video
```

The offline checks are reproducible without internet. Optional integrations require their own environment, dependencies and authorization. [Quality and release](docs/en/quality.md) explains local evidence versus publication. [Verification report](docs/en/verification.md) lists the checks run on the initial candidate.

## Examples and contribution

- [Inventory feature](examples/angular-dotnet-sqlserver/README.md) with Arabic RTL, Angular, .NET and SQL Server.
- [Bilingual dashboard](examples/arabic-rtl-dashboard/README.md) with directional and theme switching.
- [Training video](examples/software-training-video/README.md) with a runnable synthetic production workflow.
- [Contribute](CONTRIBUTING.md) or [report a security issue](SECURITY.md).

Original MSF content is [MIT](LICENSE). Linked tools and assets have their own terms. MSF Skills is independent of the organizations whose software it references.
