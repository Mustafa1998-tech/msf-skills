---
name: msf-frontend
description: "Use for Angular, TypeScript or equivalent frontend work involving UI, state, forms, routing or API contracts."
---

# msf-frontend

## Scope

Use for Angular, TypeScript or equivalent frontend work involving UI, state, forms, routing or API contracts.

## Inputs

Target route and state, API contract, package lockfile, auth and UX constraints.

## Prerequisites

Detect installed framework, Node and test scripts. Respect supported versions and project conventions.

## Workflow

1. Trace route, component, store and network boundaries. For Angular use standalone components where appropriate, typed reactive forms for validation and signals for synchronous view state. Keep request cancellation and reactive streams explicit.
2. Reuse interceptors and guards while enforcing permissions on the server. Handle loading, empty, malformed response and error states, preserve dirty state on failures, and guard against duplicate submission. Use logical SCSS, responsive media and lazy routes where measured.

## Safety

Keep credentials out of browser storage where project security rules require it; avoid injecting raw HTML and redact fixtures. Require evidence for dependency upgrades.

## Outputs

Implemented components, integration code, tests, and browser or performance evidence.

## Validation

Run the repo build, unit tests and browser flow. Check form, authorization display, mobile, RTL and error behavior when applicable.

## Failure handling

If API access is blocked, test through a contract-accurate fixture and mark real integration BLOCKED.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://angular.dev/overview)
