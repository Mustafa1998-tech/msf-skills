---
name: msf-planning
description: "Use for requirements discovery, business processes, product planning, brainstorming, existing code analysis or decomposing work. Stop at agreed scope when the request is planning-only."
---

# msf-planning

## Scope

Use for requirements discovery, business processes, product planning, brainstorming, existing code analysis or decomposing work. Stop at agreed scope when the request is planning-only.

## Inputs

Stakeholder goal, current workflow or repo, scope, known constraints and examples.

## Prerequisites

Read the relevant documents, entry points, tests and dependency manifests. Use synthetic examples where business data is sensitive.

## Workflow

1. Map actors, permissions, current steps and exceptions. Separate evidence, assumptions and open decisions. Compare two plausible routes when the tradeoff affects delivery; capture the selected option and why.
2. Write stories with Given/When/Then acceptance, including denial and recovery paths. Map dependency direction and debt by impact. Split into independently verifiable increments with owners, dependencies, test commands and rollback criteria. Record structural choices in an ADR.

## Safety

Keep approval and policy boundaries visible. Ask only for decisions that block scoped work; defer speculative work and protect internal business details.

## Outputs

Process map, prioritized stories, traceable acceptance, risk register and implementation plan or ADR.

## Validation

Every must-have links to a story, test or review criterion. Each risk has an owner, trigger, mitigation and contingency.

## Failure handling

If stakeholders disagree, record options and isolate an agreed increment. Mark assumptions and revisit after observable feedback.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://github.com/obra/superpowers)
