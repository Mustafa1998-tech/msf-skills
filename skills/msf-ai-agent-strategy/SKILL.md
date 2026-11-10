---
name: msf-ai-agent-strategy
description: Manage long-running AI coding agents through scoped context, durable state, task isolation, checkpoints, handoffs, and evidence-based verification.
---
# MSF AI Agent Strategy

Use alongside msf-orchestrator and all specialist skills. This strategy reduces context rot; it cannot guarantee perfect recall.

## Required workflow
1. Discover requirements, repository instructions, constraints and acceptance criteria before coding.
2. Plan bounded tasks, dependencies, risks and verification criteria.
3. Load only task-relevant context; retrieve source files on demand.
4. Implement in small increments and record decisions and blockers.
5. Verify with actual builds, tests, security checks and browser workflows as applicable.
6. Checkpoint durable project state before compaction, interruptions or agent handoffs.
7. Resume by re-reading the state and validating it against current repository files.

## Context hygiene
- Conversation history is a working cache, not the source of truth.
- Watch for forgotten constraints, contradictions, repeated errors and irrelevant history; there is no guaranteed safe token threshold.
- Preserve exact requirements, decisions, file paths, test results, risks and next steps when compacting.
- Start a fresh focused session with a verified handoff when context becomes noisy.
- Never invent test outcomes, silently drop pending work, or put secrets in committed state.

## Project-local records
Reuse existing project conventions when possible; otherwise create:
- PROJECT_STATE.md: objective, current milestone, verified status, blockers.
- DECISIONS.md: dated decisions, rationale and superseded choices.
- TASKS.md: prioritized work, acceptance criteria and actual evidence.
- HANDOFF.md: completed changes, changed files, commands/results, open risks and next safe action.

## Delegation
Give each agent a bounded task, explicit inputs and acceptance criteria. The orchestrator owns integration and final verification. Avoid concurrent edits to the same files without coordination.

## Completion gate
Claim completion only for delivered and verified work. Mark untested items explicitly. Never deploy, merge or change production without authorization.
