# Visual guide roadmap

`docs/visual-guide.html` is a self-contained, bilingual (zh-TW/EN) onboarding artifact meant to eventually ship with the template so a new clone has a visual, hands-on reference instead of text alone. It is under active iteration, not finished. This file exists so a session picking this work up later — with none of the conversation history that produced these decisions — can resume without re-deriving them.

See `docs/DECISIONS.md` ADR-009 for the short, durable version of the two rules below. This file carries the full reasoning, current build status, and ordered next steps.

## Four tabs, each with exactly one job

The guide grew by adding tabs as new needs came up (a migration path, a multi-source example), which surfaced a real risk: without a distinct, non-overlapping job per tab, a reader can't build a mental map of what to read when, and worked-example tabs start to feel redundant or coupled to each other.

| Tab | Job | Explicitly does not |
| --- | --- | --- |
| **Visual Guide** (視覺化指南) | Generic, data-agnostic mechanics: environment setup, choosing a mode, one acceptance-testable request, the `apply_update.py` loop. The operating manual for the tool itself. | Walk through any one complete business scenario end to end. |
| **Case 1: From one dataset to a complete demo** (案例一：從一份資料到完整 Demo) | The *first* full end-to-end worked journey — one real dataset, all the way to a real small presentable demo web data app. | Re-explain the mechanics already in Visual Guide — link back to those steps instead. |
| **Case 2: Integrating two data sources** (案例二：整合兩個資料來源 — rename of the current "兩來源整合案例" tab) | Only the *delta* beyond Case 1: schema reconciliation, contract-writing, and validation-rejection when a second, incompatible data source joins the first. | Re-walk the end-to-end journey Case 1 already covers; assumes the reader has been through Case 1. |
| **Migrate from single-file HTML** (單檔 HTML 遷移) | Retroactive recovery: you didn't start clean, you already have a messy single-file HTML prototype (which may itself already tangle together the same problems Case 1/2 teach), and need to decompose it into the template's structure. | Re-teach reconciliation or basic mechanics — links back to Case 2 and Visual Guide instead. |

Reading order matches the table: manual → first worked example → harder worked example → real-world recovery scenario. The numbered "Case 1 / Case 2" naming is deliberate — the numbering itself signals the sequence without needing prose to explain it.

## Case-study tabs must be backed by a real reference implementation

This is the more important, and currently unmet, standard.

The existing "兩來源整合案例" (soon: Case 2) tab has schema tables, a reconciliation diagram, and chatbot dialogue — all invented to illustrate the concept. Nothing behind it is real: no actual dataset, no actual ETL, no actual running app. That makes it closer to a mockup of what a tutorial would look like than an actual tutorial.

The bar to hold this to (raised directly from experience with commercial statistical software — JMP, SPSS, Minitab-style tutorials): a real example dataset, a real scenario/question, a step-by-step walkthrough of an actual problem, ending with a real, comparable result. Completing it should leave the reader with real operational capability, not just conceptual familiarity. Visual Guide's own Steps 2, 4, and 6 already meet this bar — their screenshots are real captures from an actual build. The case-study tabs currently do not.

**Decision**: build and author case-study tabs the same way, in this order:

1. Build a minimal real reference implementation for **Case 1** first (small real fixture data, a real ETL/contract step, a real running minimal frontend) — small enough to build quickly, real enough to produce genuine screenshots and transcripts.
2. Write Case 1's guide content *from* that real implementation's actual artifacts — real screenshots, real chatbot transcripts — not invented dialogue.
3. Once that pattern is validated on Case 1, apply the same treatment to Case 2: replace its current illustrative content with content drawn from an actual two-source reference implementation.

## Current build status

- **Visual Guide**: 7 steps, fully built. Ink Navy palette applied (chosen over four other options compared side by side; the unused three are saved at `~/Developer/design-notes/palettes/technical-manual-palettes.md`, outside any repo). "Why bother with this extra step" hook added before Step 1, translating the template's value proposition into felt, relatable pain points instead of engineering vocabulary. `.case-card` component in place to visually separate case-specific demo content from generic instructions.
- **"兩來源整合案例" (to become Case 2)**: 7 steps built — scenario + diagram, both sources' schema, a target contract, an example request, a validation-rejection lesson, applying the update, and the payoff. Cross-linked from the migration tab. **Conceptual/illustrative only — not yet backed by a real implementation; needs the treatment above before it meets the bar.**
- **Migrate from single-file HTML**: 6 steps, fully built, cross-linked to both Visual Guide and the two-source tab.
- **Case 1 (single-source, real worked example)**: not started. This is the next priority — see below.
- **Image workflow**: still fully inline base64 (six screenshots account for 92.9% of the file's 1.6MB). Not yet externalized — see below.

## Next steps, in order

1. Design and build a minimal real reference implementation for Case 1: pick a small, business-neutral dataset and question, build it for real using this template (real fixture data, real ETL, a real small running frontend).
2. Author the Case 1 tab from that implementation's real artifacts (screenshots, transcripts), following the existing cross-link discipline (link to Visual Guide for anything mechanical; only case-specific content stays local).
3. Repeat the same real-implementation treatment for Case 2, and rename its tab/nav label to match the "Case 2" numbering.
4. Externalize the six current Visual Guide screenshots: move them to real files under `docs/assets/`, reference them via `<img src="assets/....png" id="...">`, and write a small one-off author-side script (not part of the template's canonical `scripts/`) that re-embeds them as base64 by `id` when a version is ready to ship as a single portable file. Do this because 92.9% of the file's current size is base64 image payload, which makes every edit slower without adding any real functionality.
5. Add real, Excel-style sample-data-row tables (not just field/type definitions) to Case 2's schema explanation, and commit matching real fixture files under `data/fixtures/` — the template's existing convention for small, safe-to-commit example data (see `docs/FILE_MANIFEST.md`), rather than inventing a new folder for this.
6. Once all tabs are stable and the real-implementation bar is met, formally register `docs/visual-guide.html` (and its assets) in `docs/FILE_MANIFEST.md`.

## Not yet decided

- Exactly what dataset/scenario Case 1's reference implementation should use (deliberately deferred — pick something as minimal and business-neutral as the Case 2 warehouse example, but distinct enough not to feel like a rehash of it).
- Whether Case 1 and Case 2's real reference implementations live as throwaway local scratch work, or as a small tracked fixture project somewhere in this repo.
