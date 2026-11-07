---
name: msf-backend
description: "Use for ASP.NET Core .NET 10+, C#, REST APIs, SignalR or equivalent server work. Preserve callers and existing data."
---

# msf-backend

## Scope

Use for ASP.NET Core .NET 10+, C#, REST APIs, SignalR or equivalent server work. Preserve callers and existing data.

## Inputs

Endpoint use cases, authorization rules, contracts, persistence, integration failures and operational needs.

## Prerequisites

Inspect SDK and target framework, API clients, routes and integration test setup.

## Workflow

1. Define HTTP statuses and structured errors, bounded DTOs and validators. Reuse services and DI lifetimes, pass cancellation, and maintain transaction boundaries. Keep endpoint implementation direct where domain complexity is low.
2. Enforce authentication and object permissions server-side, validate JWT issuer/audience/lifetime/signature, apply idempotency and timeouts as appropriate. Authorize hub operations, scope groups, test reconnect, and send sanitized correlation-aware logs. Bound background work and update OpenAPI.

## Safety

Never log authorization headers or PII. Use secret providers and authorized integration environments. Avoid weakening auth, allowing mass assignment or changing contracts silently.

## Outputs

Endpoints or jobs, updated API contract, migration or compatibility notes, and tests.

## Validation

Run build and tests. Verify 400, 401, 403, 404, conflicts, retry behavior and cross-object access where applicable.

## Failure handling

When integration is offline, use a controlled fake for contract paths and label live validation BLOCKED.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://learn.microsoft.com/en-us/aspnet/core/)
