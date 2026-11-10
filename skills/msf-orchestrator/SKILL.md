---
name: msf-orchestrator
description: "Route software ideas, repository changes, reviews or releases to relevant workflows. Keep a task limited to the authorized outcome."
---

# msf-orchestrator

## Scope

Route software ideas, repository changes, reviews or releases to relevant workflows. Keep a task limited to the authorized outcome.

## Inputs

User objective, target repository, affected environments, acceptance criteria and restrictions.

## Prerequisites

Read-only workspace access for repository tasks, available tools list and permission boundaries.

## Workflow

1. Classify intent as plan, implement, review, document, produce media or release. Read repository status, scoped conventions, manifests, lockfiles, CI, entry points and existing checks before editing. Record stack, dependencies and unknowns.
2. Build a short plan tied to acceptance and risk. Discover installed skills, select the smallest relevant set using the routing table, and explain exclusions. Separate independent tasks for delegation only when permitted. Define file ownership and integrate and verify outputs yourself.

3. For an explicitly selected upstream reference available in the MSF checkout, prefer the pinned source archive in `vendor/`. Verify and extract it for review only. Keep installation and execution of external scripts, packages or telemetry opt-in.

For long-running or multi-agent tasks, apply [MSF AI Agent Strategy](../msf-ai-agent-strategy/SKILL.md) to manage scoped context, durable state, checkpoints and verified handoffs.

## Safety

Order user and platform constraints ahead of repo conventions and specialist advice. Stop the dependent operation for unresolved permission or conflicting requirements. Require explicit approval for destructive operations, production deployment, infrastructure, secrets or live data changes.

## Outputs

Scoped plan, chosen skills with reasons, implementation or review artifacts, gate table and evidence report.

## Validation

Run relevant checks on the exact revision. For each of nine gates record PASS, FAIL, BLOCKED or NOT APPLICABLE with command or evidence and scope. Separate failure from missing tooling and published state from local state.

## Failure handling

If a skill is missing use its routing fallback. Keep working on independent parts; record the exact missing permission, tool or evidence and where to resume.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://agentskills.io/specification)
