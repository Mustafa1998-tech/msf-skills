---
name: msf-security
description: "Use for defensive threat modeling, app/API audits, authorization, dependency or container scanning and security regression. Operate only in authorized scope."
---

# msf-security

## Scope

Use for defensive threat modeling, app/API audits, authorization, dependency or container scanning and security regression. Operate only in authorized scope.

## Inputs

Assets, trust boundaries, role/object matrix, environment authorization and project stack.

## Prerequisites

Confirm authorized target and test intensity. Read existing controls and inspect applicable OWASP guidance and scanner configuration.

## Workflow

1. Map data flows and abuse cases. Test authentication, RBAC, tenant and object ownership, validation, parameterized SQL, XSS, CSRF for credentialed browser flows and exact CORS origins. Check error and logging redaction, limits, secrets and secure defaults.
2. Run approved static analysis, dependency/SCA and image checks using reviewed, pinned tooling. Restrict DAST to authorized disposable environments and non-destructive checks. Triage findings with reproduction, impact, scope and fix; add focused regression tests.

## Safety

Never attack external systems, attempt destructive exploitation, publish secrets or change access controls and secret values without approval.

## Outputs

Threat model, prioritized findings, safe reproduction and regression evidence, scanner versions and scope.

## Validation

Prove object access denial for another tenant/role and expected access for the owner. Record each tool exit and evidence path; a clean scan is bounded by scanner coverage.

## Failure handling

If tooling or approval is absent, complete source review, mark remaining checks BLOCKED and document prerequisites.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://owasp.org/www-project-top-ten/)
