# MSF Design Review — evidence-first

## Severity

| Level | Definition | Next action |
| --- | --- | --- |
| P0 | Core task blocked, dangerous or misleading | Stop acceptance |
| P1 | Major accessibility, validation or mobile defect | Resolve before release |
| P2 | Significant hierarchy, spacing or feedback defect | Fix next iteration |
| P3 | Minor aesthetic inconsistency | Polish after workflows |

For every issue, log screen, viewport, direction, theme, reproduction, observed versus expected behavior, impact, priority, correction and evidence.

## Ten-part rubric

Score each criterion from 0 to 4: 0 = unusable or not verified; 1 = major issue; 2 = inconsistent; 3 = good with gaps; 4 = verified strong implementation.

1. Primary task and hierarchy
2. Navigation and orientation
3. Layout rhythm, space and grouping
4. Typography, language-appropriate direction and readable mixed scripts
5. Design tokens, icons and consistency
6. Loading, empty, errors, success and feedback
7. Forms, tables and interaction affordances
8. Mobile, tablet and desktop behavior
9. Keyboard focus, semantics and contrast
10. Product-fit aesthetics, distinctiveness, alignment and final polish

A review score of at least 34/40 with no unresolved P0/P1 is an **internal candidate threshold**, not proof of usability or accessibility. Mark untested criteria separately rather than awarding unearned points.

## Evidence matrix

Capture the main journey at desktop (1440px), tablet (768px), and mobile (390px), or the product's documented widths. Use equal data, theme, viewport and zoom for before/after comparisons. Test the product's actual locale and direction, long localized labels and mixed-direction identifiers, keyboard order and focus, scrolling tables, search and forms. Inspect states such as loading, empty, validation, and failures. Test dark mode and reduced motion only where applicable. Review whether the visual identity fits the specific product rather than a generic MSF template.

## Delivery

Provide a screen brief, linked implementation, real screenshots, issues ranked P0–P3, tests actually executed, limitations and review status. If no browser was used, mark browser verification BLOCKED. Explicitly label synthetic data and prototypes without a backend.
