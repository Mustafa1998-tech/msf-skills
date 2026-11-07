---
name: msf-documentation
description: "Use for READMEs, user/admin manuals, OpenAPI, architecture, installs, deployment, troubleshooting, changelogs or release notes."
---

# msf-documentation

## Scope

Use for READMEs, user/admin manuals, OpenAPI, architecture, installs, deployment, troubleshooting, changelogs or release notes.

## Inputs

Audience, current build or UI, repository, API schema, languages and target deployment.

## Prerequisites

Inspect actual commands, entry points, error responses and artifact versions. Use safe screenshots or synthetic examples.

## Workflow

1. Organize by reader task. Document prerequisites, a minimal quick start, verification, update/uninstall or rollback and troubleshooting based on observable symptoms. Explain parameters, exit states and roles.
2. For APIs reconcile OpenAPI with actual routes and examples; distinguish deployment and management procedures from everyday user steps. Pair Arabic and English by section and preserve identifiers and commands. Trace release notes to verified changes.

## Safety

Redact account details and secrets. Avoid licensing claims without evidence; label planned features and environment-dependent checks explicitly.

## Outputs

Bilingual docs, runnable snippets, license/source links, versioned changelog and release notes.

## Validation

Run example commands where feasible, validate local links, compare parity and verify claims against outputs. Show output state with evidence.

## Failure handling

If a tool or app is unavailable, label the procedure unverified and record the exact validation step.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://spec.openapis.org/oas/latest.html)
