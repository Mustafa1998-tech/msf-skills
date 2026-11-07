---
name: msf-architecture
description: "Use for system boundaries, modular monoliths, integration design, technical debt, scalability, refactoring or code review. Pick complexity proportionate to the system."
---

# msf-architecture

## Scope

Use for system boundaries, modular monoliths, integration design, technical debt, scalability, refactoring or code review. Pick complexity proportionate to the system.

## Inputs

Use cases, current dependency graph, data owners, load estimates, failure constraints.

## Prerequisites

Inspect deployment units, public contracts, persistence and operational metrics when available.

## Workflow

1. Map write ownership, trust boundaries and invariants. Start with the smallest cohesive design. Compare a direct API or modular monolith with layering only if rules, integration or replaceability make separation pay off. Apply SOLID where it reduces coupling, with concrete examples.
2. Choose contract and schema versioning, transaction boundaries, error mapping, correlation, background job retries and deduplication. Define timeouts, overload behavior and rollback. Refactor in observable slices behind stable interfaces and review callers plus old data.

## Safety

Avoid breaking clients, irreversible migrations and broad access changes without authorization. Keep latency and scaling claims tied to measurements.

## Outputs

Context and dependency maps, API and data contracts, ADR, failure matrix, migration plan and review findings.

## Validation

Trace use cases and failures across boundaries. Verify contracts against existing clients, demonstrate an invariant test and record performance assumptions.

## Failure handling

If baseline evidence is missing, measure before optimization or describe the risk and a reversible experiment.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://learn.microsoft.com/en-us/azure/architecture/)
