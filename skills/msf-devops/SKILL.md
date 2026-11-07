---
name: msf-devops
description: "Use for Git, GitHub Actions, Docker, Kubernetes, Terraform, IIS, deployment, reliability, release or incident response."
---

# msf-devops

## Scope

Use for Git, GitHub Actions, Docker, Kubernetes, Terraform, IIS, deployment, reliability, release or incident response.

## Inputs

Target environment, commit, manifests, secrets references, SLO, rollback and approval owner.

## Prerequisites

Inspect branch rules, supported runtimes, IaC plan, config and monitoring access within scope.

## Workflow

1. Build a reproducible artifact and map it to an immutable revision. Use least privilege, reviewed pinned actions and protected environments. For IIS verify hosting bundle, app pool, binding and health; for Docker use trusted bases and appropriate non-root runtime; for Kubernetes validate probes and resource bounds.
2. Review Terraform plan and state protections. Verify health, readiness, logs, observability and performance smoke. Document backup and rollback and rehearse in staging. For incidents establish timeline, stabilize safely and separate signals from hypotheses.

## Safety

Require explicit approval for production deployment, infrastructure changes, deletion or secret mutation. Treat live commands and rollbacks as change operations.

## Outputs

CI workflow or runbook, artifact digest, run IDs, health evidence, rollback plan and release/incident notes.

## Validation

Check statuses for the same commit, stage rollout and measure health against thresholds. Distinguish local build from remote deployment and a plan from apply.

## Failure handling

If permissions, CI, environment or backups are missing, mark BLOCKED and deliver the independently validated artifact and next action.

## References

- [Field guide](references/field-guide.md)
- [Primary source](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
