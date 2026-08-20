# Web Data App Design Playbook

Status: **canonical reusable design guidance**. Concrete colors, dimensions, metrics, formulas, and viewport choices remain instance decisions.

## Purpose

This playbook captures reasoning that generalizes across compact interactive web data apps. It complements `ai/DESIGN_RULES.md`: the design-rules file gives defaults; this playbook explains how to structure the analytical experience and how to know when the visual phase is actually complete.

Core principle:

> Design is the structure that helps a user inspect data and make a decision. Decoration is subordinate to that structure.

## 1. Start from the analytical question, not a dashboard template

Write the user flow in verbs before selecting components, for example:

`choose context → inspect primary measure → compare explanatory measures → identify an item/period worth attention`

Allocate the largest visual region to the question that matters most. Do not begin with "how many KPI cards should the dashboard have?"

A useful hierarchy model is:

1. Primary decision metric/view.
2. Context needed to explain it.
3. Filters that change the analysis.
4. Metadata that protects interpretation.

If a metric does not help one of these steps, it probably should not permanently consume viewport space.

## 2. Use an analytical-console layout when the task benefits from simultaneous context

For desktop engineering/business analysis, a one-page console can be better than a long scrolling dashboard when the core metric set and normal filter set are modest and related views need to be compared together.

Define a viewport budget before polishing components. Allocate approximate space for orientation, controls, summary, primary analysis, secondary context, and gaps. Treat 100% browser zoom at named target viewports as an acceptance condition rather than relying on users to zoom out.

Do not make "no scrolling" absolute. If readable information cannot fit, preserve legibility and change the information architecture. Scrolling is preferable to unreadable text.

## 3. Density comes from hierarchy and interaction, not tiny typography

Use fewer permanent elements and let interaction expose detail through tooltips, filters, and selection. A compact app still needs a readable type hierarchy.

Avoid 9–10 px text as a default density tool. If something only fits after making all metadata tiny, revisit spacing or information priority first.

Useful principle:

> Dense, not cramped; spacious, not sparse.

## 4. Prefer flat structure over cardification

Wrapping every number and chart in an independent rounded shadow card increases visual fragmentation and makes all blocks look equally important.

Prefer:

- one shared summary region rather than a card per metric;
- restrained borders and small radii;
- spacing/alignment as the primary grouping mechanism;
- shadows mainly for transient overlays that truly sit above the page;
- grouping related secondary analyses into one semantic region when that clarifies their relationship.

## 5. Build a semantic token layer after layout direction stabilizes

Centralize repeated decisions as semantic tokens:

- canvas / surface / inset surface;
- primary / muted / soft text;
- panel / control / divider / grid boundaries;
- interaction accent and focus;
- real status colors;
- chart-role colors;
- spacing, radius, elevation, and typography scales.

Name tokens by role rather than literal color. Separate interaction tokens from data-series tokens even when they currently share a literal value.

A token difference must also be perceptible at the target viewport. Technically different colors that look identical do not establish useful hierarchy.

## 6. Let neutrals carry most of the interface

Use neutral or low-chroma surfaces/text for structure. Reserve saturated color for information with a reason: current selection, primary data, real status, or a stable semantic metric identity.

Practical test:

> UI surfaces should recede; analytical data should provide most of the visible color.

A low-chroma tint can create comfortable hierarchy, but it should read as atmosphere/structure rather than decoration. Do not use red/green/amber merely to make the screen more interesting.

## 7. Finish non-chart UI with the same restraint as the charts

Once chart rendering is mature, the remaining quality gap is often consistency across header, controls, summary typography, states, and structural lines rather than "more styling."

Useful completion rule:

> Far away: quiet. Up close: precise.

- Treat grouped filters as operational units rather than unrelated form fields.
- Reserve the strongest accent for selected/focused states.
- Distinguish control, panel, divider, and grid boundaries by semantic role.
- Once surface contrast is sufficient, improve grouping with shared boundaries, separators, proximity, alignment, and consistent heights rather than repeatedly deepening colors.
- Preserve native platform behavior unless replacement creates clear task value.
- Treat hover, focus, disabled, loading, empty, and error states as part of the design system.

Freeze aesthetic micro-polish once the screen is coherent and subordinate controls no longer compete with the analytical content. Reopen only for a concrete usability, readability, accessibility, semantic, or hierarchy defect.

## 8. Choose chart type from measurement meaning

Do not make every time-based chart a line.

- Rates/trends often suit lines when continuity is meaningful.
- Per-period absolute quantities often suit bars/columns when bucket magnitude is the comparison.

Axis rules:

- absolute quantities normally need a zero baseline, especially bars;
- a narrow operating-band rate may use a non-zero domain only when the visible range is explicit and not misleading;
- axes/grids should be quieter than data marks;
- unusual axis choices should be visible/documented rather than hidden.

Missing data is not zero. Preserve the category/time position when the absence matters, use a gap/blank/explicit missing mark, and never invent numeric zero just to simplify rendering.

## 9. Synchronize analytical context before synchronizing visual effects

Correct dependency direction:

`filter / aggregation state → prepared view data → charts`

Do not let each chart independently implement business filtering, date logic, or aggregation. After the context boundary is stable, linked hover/selection can be added when it genuinely improves comparison.

## 10. Treat tooltips as transient detail, not hidden documentation

Tooltips should quickly answer "what exact point is this?" with human-readable category/time, measure, exact formatted value, and optional context.

Do not hide formula definitions, units, important axis behavior, or missing-data semantics exclusively inside hover content.

## 11. Remove development scaffolding from the product surface

Phase labels, placeholders, and implementation notes may help development but need a deliberate removal gate. Production UI should describe the data/task, not the development history.

Keep implementation status in repository docs, tests, changelog, or developer tooling.

## 12. Anti-AI / anti-template review

Before calling a visual phase complete, explicitly search for common generated-dashboard habits:

- card for every element;
- large radii everywhere;
- gradients without meaning;
- decorative icons beside every metric;
- excessive shadows/elevation;
- unrelated accent colors;
- oversized empty hero/header regions;
- marketing copy inside an operational tool;
- tiny axes/labels caused by overstuffing;
- charts selected for variety rather than analytical meaning;
- fake metrics added to fill space;
- large-area color added only to prove a theme exists.

The fix is not "make it plain." Every visible choice should be explainable by hierarchy, comparison, interaction, or state.

## 13. Compare against a curated reference before building

Don't design a screen from memory or guesswork — most "off" spacing, type, and color choices come from inventing a number instead of looking one up. Before building a screen, ask three questions:

1. What kind of screen is this closest to (analytical console, admin dashboard, data table, detail/record view, form)?
2. Which reference below is the closest match? Open it and find the equivalent screen.
3. Copy that screen's type scale, spacing, color usage, and interaction pattern in order — don't invent a value that isn't in `ai/DESIGN_RULES.md`'s tokens or the closest reference.

| Screen type | Reference | What to take from it |
| --- | --- | --- |
| Analytical console / admin dashboard | [shadcn-admin](https://github.com/satnaing/shadcn-admin), [TailAdmin](https://github.com/TailAdmin/free-nextjs-admin-dashboard) | Overall layout allocation, light/dark handling, table/filter/pagination patterns |
| Data-dense components, charts | [Tremor](https://github.com/tremorlabs/tremor), [shadcn/ui examples](https://ui.shadcn.com/examples) | Chart and stat-tile structure, accessible interaction details |
| Component primitives | [Radix primitives](https://www.radix-ui.com/primitives), [Mantine UI](https://ui.mantine.dev/) | Correct state handling (focus, disabled, loading) for a component you're about to build from scratch |
| General visual inspiration | [Mobbin](https://mobbin.com/), [Dribbble](https://dribbble.com/) | Real production screenshots when nothing above matches the screen's shape |

This complements the anti-template review above rather than replacing it: copying real values from a real product's equivalent screen is how you avoid the generated-dashboard habits in section 12 — a decorative-icon-per-metric habit doesn't survive contact with what an actual production dashboard looks like.

## 14. Phase workflow for a small web data app

A useful sequence is:

1. **Data contract / ETL** — make the read model trustworthy.
2. **Layout / UX contract** — define information hierarchy and viewport budget.
3. **Data adapter / shell** — prove real data reaches the UI through a boundary.
4. **Interaction / aggregation state** — freeze filters and business aggregation before charts own them.
5. **Primary visualization** — build the highest-value analysis first.
6. **Context visualizations** — add only views that explain the primary measure.
7. **Design-system polish** — centralize tokens, remove scaffolding, unify visual language.
8. **Viewport optimization** — use deterministic target-viewport evidence where practical.
9. **Final QA / anti-template review** — combine machine regression with human/LLM visual judgment.
10. **Deployment** — add the smallest hosting/operations layer justified by the real sharing requirement.

Every web phase should require a production build, not only a successful development-server screen.

## 15. Transfer checklist

Before reusing this approach, answer:

- What is the primary user decision/question?
- What is the single most important measure/view?
- Which secondary data actually explains it?
- Which aggregations are business-defined?
- What does missing mean?
- Which axis baselines/ranges could mislead?
- What is the target viewport and what must be simultaneously visible?
- Which information can move to interaction/detail-on-demand?
- Which colors are interaction, data identity, and real status?
- Do all panels consume one prepared analytical context?
- Can users tell when data is missing, invalid, or stale?
- Does the production build pass?
- Has the real target viewport been reviewed at 100% zoom?
- Has an explicit anti-template review been performed after functionality is frozen?

Keep exact metrics, formulas, units, colors, chart heights, default time windows, and domain-specific phase history in the instance rather than promoting them into this canonical playbook.
