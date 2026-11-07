# Routing and evidence

Match by deliverable and risk. Combine routes only when the requested feature crosses boundaries. Use the fallback when the named skill is unavailable. Skills are instructions; discover local tools before running commands.

| Objective | Skill | Fallback |
| --- | --- | --- |
| Unknown requirements or existing repo | `msf-planning` | Inventory affected actors, paths, dependencies and acceptance criteria. |
| Service boundaries or refactor | `msf-architecture` | Map writes, invariants, contracts and failure modes before changes. |
| Dashboard or form usability | `msf-ui-ux` | Inspect real tasks, both themes, keyboard behavior and applicable directions. |
| Browser application implementation | `msf-frontend` | Trace route, state, API contract, form and request lifecycle. |
| Endpoint or job | `msf-backend` | Verify authorization, validation, error behavior and retries. |
| Schema, query or data change | `msf-database` | Review constraints and compatibility; measure on the target engine. |
| Trust boundary or security review | `msf-security` | Use a threat model and defensive, authorized tests. |
| Regression or acceptance | `msf-testing` | Run applicable checks, record exact results and scope gaps. |
| Infrastructure, rollout or incident | `msf-devops` | Prepare health thresholds, evidence, approval and rollback. |
| Manual, API reference or changelog | `msf-documentation` | Compare docs with real entry points, output and versions. |
| Software training video | `msf-video-studio` | Use a storyboard, authorized captures, accessible captions and probe results. |

## Decision examples

- A dark theme regression selects UI/UX and testing. Read the frontend implementation before editing and add frontend only when a component or state change is necessary.
- A new inventory API selects backend, database if persistence changes, security for access and testing. Add architecture only if boundaries or contracts need a decision.
- A guide from supplied screenshots selects video or documentation based on the requested artifact. Release stays out of scope until publication is requested.

Record each gate with status, exact command or artifact, scope, revision and reason. A check that ran and failed is FAIL. Missing authorization, dependencies or evidence is BLOCKED. A gate outside the agreed scope is NOT APPLICABLE with a reason. Use PASS only for positive current evidence.
