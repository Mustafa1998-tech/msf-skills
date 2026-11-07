---
name: msf-testing
description: "Use for unit, integration, API, browser, accessibility, visual regression, responsive or CRUD verification."
---

# msf-testing

## Scope

Use for unit, integration, API, browser, accessibility, visual regression, responsive or CRUD verification.

## Inputs

Acceptance criteria, route and API contracts, roles, fixtures and relevant build/test scripts.

## Prerequisites

Use an isolated authorized test environment and uniquely identified synthetic fixtures.

## Workflow

1. Pick the lowest useful test layer and reserve Playwright for cross-boundary journeys. For CRUD verify create, save, read after reload, edit, update, archive/delete and restore where supported. Verify invalid input, session expiry, duplicate submit and each denied role.
2. Use semantic locators, visible state assertions and isolated data. Test RTL, LTR, dark mode, viewport and keyboard. Stabilize fonts/time for visual baselines, capture errors and screenshots when permitted, and compare performance against a named baseline.

## Safety

Keep cleanup scoped to generated fixture IDs and do not record personal data or live sessions. Obtain approval for destructive testing or live targets.

## Outputs

Traceability matrix, commands and actual exits, screenshots/traces as applicable, and failures with reproducible steps.

## Validation

Run the applicable tests on the current revision and separate FAIL, BLOCKED and NOT APPLICABLE. Document what mocks prove versus real integrations.

## Failure handling

If setup breaks, classify setup separately, save safe logs, continue independent tests, and rerun after resolving it.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://playwright.dev/docs/best-practices)
