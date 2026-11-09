---
name: msf-ui-ux
description: "Create distinctive, context-aware UI/UX for any software product based on its name, purpose, visual identity and users; implement and critique accessible, responsive screens without forcing a fixed design style."
---

# msf-ui-ux

## Scope

Design, implement or refine distinctive, user-facing software interfaces **for any product or industry**, with no default domain, brand colors, layout, visual trend or frontend framework. Adapt to the actual product identity and tasks instead of copying one template. Preserve existing sections and behaviors when the assignment is visual refinement only.

## Inputs

Product name and what it means, purpose, industry if known, user types, real workflows, logo/brand assets, existing UI screenshots and code, language and direction, device needs, constraints and acceptance criteria. Distinguish **confirmed facts** from design hypotheses suggested by a name, screenshot or industry.

## Prerequisites

Inspect the current product and design tokens when available. Read [Design direction discovery](references/design-direction.md), [Screen brief](references/screen-brief.md) and [Design review](references/design-review.md). For new products with limited information, use explicit, reversible assumptions; prefer synthetic data and licensed assets.

## Workflow

1. **Identify the product.** Read the product name and context to infer possible character (e.g. formal, playful, urgent, technical), but never treat the name or industry stereotype as the sole design instruction. Prioritize actual logo, website, screenshots, audience, content, and user goals. State unknowns and distinguish observation from inference.
2. **Preserve or explore as appropriate.** For an existing product, list the relevant screens, sections, actions and styling conventions; preserve behavior and explicitly constrained layout. For a new product without an established identity, develop two or three materially different, credible visual directions only when exploration adds value. Compare their suitability; choose or recommend one based on users and tasks, not personal color preferences or random decoration.
3. **Create product-specific design language.** Derive typography, color palette, spacing, density, surface treatment, corner geometry, navigation, icons, data visualization and motion from the chosen direction and functional needs. Justify each major visual choice with evidence from the current product, its users or their tasks. Avoid importing unrelated patterns, decorative cards, fake metrics or emoji icons.
4. **Model actual user flows.** Define the primary job, actors, entry, success/failure, feedback and permissions. Map the necessary screens and content. Keep primary tasks obvious and avoid ornamental elements that hurt comprehension.
5. **Implement a cohesive interface.** Build product-fit responsive components and relevant states for forms, tables, search, filters, dialogs, validation, loading, empty, error, success and disabled interactions. Use semantic controls, keyboard support, focus restoration, touch-friendly targets and safe confirmation for destructive actions.
6. **Honor locale and context.** Apply RTL and Arabic typography when Arabic is requested; use correct LTR or multilingual layout otherwise. Handle mixed-direction identifiers, long labels, content density and target devices. Support light/dark themes only when requested, existing or useful to the product.
7. **Review the delivered design.** Compare implementation against the chosen identity and actual task using the local P0–P3 critique rubric. Review visual differentiation, consistency, information hierarchy, accessibility, responsive behavior and relevant interaction states. Capture real, comparable screenshots and test outcomes where tools permit; iterate on issues rather than declaring success from a mockup.

## Safety

Use assets with appropriate licenses; protect production secrets and private data in screenshots. Do not modify live systems, permissions or destructive business workflows without authorization. Archived third-party code is a reference, not permission to execute or redistribute.

## Outputs

A short product identity/design-direction decision with rationale, screen brief, implemented screens or prototype, reusable but product-specific tokens and components, prioritized findings, screenshots/tests actually captured and explicit gaps. Do not present one preset UI as the universal MSF look.

## Validation

Test applicable target widths (1440px, 768px and 390px are examples, not fixed requirements), locale/direction, contrast, keyboard focus, responsive overflow, task flow and states. Check WCAG 2.2 AA contrast where applicable (4.5:1 normal text, 3:1 large). Distinguish verified PASS from FAIL, BLOCKED and NOT APPLICABLE. A high visual score is not proof of user research, usability or accessibility certification.

## Failure handling

When the product name is ambiguous, state alternative interpretations instead of inventing a business domain. If brand files, code or browser tools are missing, work from explicit assumptions, provide a clearly labeled prototype and mark unavailable checks BLOCKED. Ask only when a missing distinction would materially change implementation.

## References

- [Product-adaptive design direction](references/design-direction.md)
- [Screen brief](references/screen-brief.md)
- [Design review rubric](references/design-review.md)
- [Field guide](references/field-guide.md)
- [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/)
