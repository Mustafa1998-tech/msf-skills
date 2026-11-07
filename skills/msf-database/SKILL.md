---
name: msf-database
description: "Use for SQL Server, T-SQL, EF Core, schema, stored procedures, indexing, query optimization or migration. Prefer engine-native verification."
---

# msf-database

## Scope

Use for SQL Server, T-SQL, EF Core, schema, stored procedures, indexing, query optimization or migration. Prefer engine-native verification.

## Inputs

Schema, key queries, workload size, invariants and permitted environment.

## Prerequisites

Inspect migration history, actual database engine/version, provider configuration and test data.

## Workflow

1. Define keys, referential integrity, uniqueness and nullability. Align transaction and concurrency policy with invariants. Inspect actual execution plans in a safe environment, compare reads and duration, and document index write costs.
2. Parameterize queries and procedures, handle legacy rows, and use expand/backfill/validate/contract where compatibility is needed. Test batch behavior, retry, contention and restore. Record backup and recovery assumptions with a restore rehearsal.

## Safety

Require approval before live writes, data deletion or schema rollout. Use least privilege and redact data and plans before sharing.

## Outputs

Migration, query or procedure, plan and measurements, data validation and rollback/restore steps.

## Validation

Exercise forward migration on synthetic legacy data and verify constraints, concurrent writes, retry and rollback where supported. Capture real SQL Server evidence for engine-specific claims.

## Failure handling

If the database is unavailable, run static checks or tests on available tooling and record SQL Server execution BLOCKED.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://learn.microsoft.com/en-us/sql/sql-server/)
