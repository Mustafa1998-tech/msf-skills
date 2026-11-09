---
name: msf-ui-ux
description: "Design and critique professional enterprise screens, forms, tables and dashboards with measurable Arabic RTL, accessibility and responsive quality."
---

# msf-ui-ux

## Scope

Design, implement or refine user-facing enterprise screens with evidence-based critique. Prefer usable task flows to decoration. Preserve existing sections and actions when the request is visual refinement only.

## Inputs

Product identity, repository or screenshots, users, task flows, exact sections, locale, devices, theme and acceptance criteria. Clarify whether changes may alter layout or only visual styling.

## Prerequisites

Inspect existing UI and design tokens. Read the local design-review rubric and screen-brief template. Use synthetic data for standalone demonstrations; inspect licenses before incorporating any external assets.

## Workflow

1. **Discover and preserve:** inventory screens, navigation, form fields, sections and actions. Do not silently add or remove controls or reorder information when asked to improve appearance only.
2. **Specify flows:** define the primary task, actor, entry point, expected outcome, validation, errors and permissions; complete the screen brief.
3. **Design a coherent system:** define semantic light/dark colors, readable typography, spacing, iconography, hierarchy, focus and feedback states. Prefer simple balanced layouts, restrained effects and non-emoji icons.
4. **Implement real states:** search, filtering, tables, sorting, empty/loading/error, required fields, confirmation, success, disabled, and permission states where applicable. Use semantic HTML and keyboard-operable controls.
5. **Honor Arabic and responsiveness:** use RTL and CSS logical properties, direction isolation for Latin codes, long Arabic labels, mobile touch targets, and appropriate table overflow. Do not add an English UI to an Arabic-only product.
6. **Critique visually:** evaluate actual screenshots with the severity-based rubric, compare before/after using identical viewport, data and zoom; record problem, reproduction, impact and correction.
7. **Iterate and verify:** fix blocking issues before polish, exercise key flows in a browser, and attach screenshots and test logs. Distinguish observed PASS from unverified assumptions.

## Safety

Use appropriately licensed content. Avoid real secrets and private data in screenshots. Respect authorization for destructive operations, live systems and production changes. Do not execute archived external code without review and opt-in.

## Outputs

Interactive screen or implementation, visual tokens, completed brief, prioritized critique, before/after evidence, responsive and state coverage, and remaining gaps.

## Validation

Evaluate 1440px, 768px and 390px or documented target widths, RTL mixed-direction text, keyboard focus, status feedback, and relevant themes. Check applicable WCAG 2.2 AA text contrast (4.5:1 normal and 3:1 large text), reduced motion and responsive overflow. Report unrun checks as BLOCKED, not PASS. A critique score is not accessibility certification.

## Failure handling

If the app, browser, asset or permission is unavailable, supply a self-contained annotated prototype and mark unavailable verification BLOCKED. Do not invent screenshots or test outcomes.

## References

- [Screen brief](references/screen-brief.md)
- [Design review rubric](references/design-review.md)
- [Field guide](references/field-guide.md)
- [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/)
