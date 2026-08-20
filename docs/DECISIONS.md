# Architecture decisions

Record only decisions that constrain future work.

## ADR-001: Start with local JSON read models

- Status: Accepted
- Context: Early office tools need fast iteration and normally have a spreadsheet source of truth.
- Decision: ETL produces validated JSON; the browser reads it through a data adapter.
- Consequence: Concurrent editing, authentication, and durable write workflows are out of scope until an explicit upgrade decision.

## ADR-002: Make chatbot-guided local workbenches the primary template use case

- Status: Accepted
- Context: Some enterprise environments allow users to use an LLM chatbot but do not allow agent capabilities. Ordinary users still need a safe way to create and evolve small local tools.
- Decision: Keep project context, file ownership, and verification steps in short repository documents that can be supplied to a chatbot. Design the initial tool to run locally without agent capabilities at runtime, while retaining the documented path to managed and product modes.
- Consequence: Documentation and small reviewable changes are first-class template features. Chatbot output must be reviewable locally, and no secrets or sensitive data may be included in chatbot context.

## ADR-003: Treat repository context as a portable handoff package

- Status: Accepted
- Context: A working single-file prototype may depend on one user's chat history or a particular model's temporary context. This makes it difficult to move work between people, LLMs, controlled agent environments, and engineering teams.
- Decision: Keep the project's intent, file ownership, data contracts, validation expectations, and upgrade triggers in versioned repository documents. Prefer small, reviewable changes that preserve these boundaries.
- Consequence: The template adds some initial documentation work, but a chatbot-only prototype can later move to a controlled agent environment or engineering ownership with lower communication cost and less reverse engineering.

## ADR-004: Ship default frontend design rules as template contract

- Status: Accepted
- Context: A separate, mature project (a static HTML/CSS/SVG report-generation pipeline) had already worked out and human-approved a set of general-purpose frontend visual rules — typography scale and line-height ranges, WCAG contrast targets, an 8pt spacing grid, CJK/Latin mixed-script spacing, table styling conventions, and image fit/crop priority. Its per-page human-approval gate workflow, fixed-canvas page-zone layout, and numeric-value approval-tier system are specific to one-shot slide/deck production and do not fit this template's iterative, small-change model — only the underlying visual rules generalize to a responsive `web/` application.
- Decision: Add `ai/DESIGN_RULES.md` as a new canonical file, sibling to `ai/ARCHITECTURE_RULES.md`, so every workbench built from this template starts with the same frontend defaults and an ordinary UI change cannot silently rewrite them. Register it everywhere `ai/ARCHITECTURE_RULES.md` is already registered: `docs/TEMPLATE_BOUNDARY.md`'s canonical list, `docs/FILE_MANIFEST.md`, `AGENTS.md`'s read-before-editing and template-contract rules, `README.md`/`README.zh-TW.md`'s template-contract list, `scripts/apply_update.py`'s `CANONICAL_PATHS`, and `scripts/build_context_bundle.py`'s `BUNDLE_FILES`.
- Consequence: A new clone's chatbot/agent session gets these frontend defaults automatically via `LLM_CONTEXT_BUNDLE.md`, without needing to reference the originating project. Individual tools may still deviate from any specific value; a deviation beyond a small tuning tweak should be logged here, the same as any other architectural decision.

## ADR-005: Split canonical docs into an always-bundled core and situational specialists

- Status: Accepted
- Context: PR #2 (`feat: extract reusable workbench engineering lessons`, merged 2026-08-20) added three new canonical files as engineering legacy from a real production instance built on this template: `docs/WEB_DATA_APP_DESIGN_PLAYBOOK.md`, `docs/ENTERPRISE_ENVIRONMENT.md`, and `docs/UPSTREAM_EXTRACTION.md`. They were correctly registered in `docs/TEMPLATE_BOUNDARY.md`, `docs/FILE_MANIFEST.md`, and `scripts/apply_update.py`'s `CANONICAL_PATHS`, but not added to `scripts/build_context_bundle.py`'s `BUNDLE_FILES`, and no ADR was recorded — leaving the omission looking like drift rather than a decision.
- Decision: Keep these three docs canonical but out of the default `LLM_CONTEXT_BUNDLE.md`; they apply only in a specific situation (building UI, enterprise network friction, upstream-porting a mature instance), not every session. Make discoverability explicit instead of relying on it being noticed inside an already-bundled file: `AGENTS.md` gained a "Situational guidance" section naming each doc and its trigger, and `scripts/build_context_bundle.py` documents the exclusion rationale in code.
- Consequence: The default bundle stays at its original 6 files as the canonical surface grows around it. A future canonical addition must explicitly decide "always-bundled core" vs. "situational specialist" and update `AGENTS.md`'s situational-guidance section accordingly, rather than silently landing in neither.

## ADR-006: Extract visual-quality rules from Monstrare (pjwang2022), not the workflow around them

- Status: Accepted
- Context: [Monstrare](https://github.com/pjwang2022/Monstrare) (pjwang2022) is a mature gate-based workflow layer for AI coding agents: Epic/User Story/Task decomposition, a 12-lane kanban board, 6 human review gates run partly by dedicated architect/security/test/UX subagents, cross-model routing, and a mandatory 5-stage "Epic 0" design-system ritual before any feature ships. It assumes full agent access and full-SDLC project scale. This template's primary persona has no agent access and builds one small tool through one acceptance-testable change at a time — importing that apparatus would replace the template's own change protocol with a heavier, differently-scoped one. Its `ai/skills/design-craft.md` and `ai/checklists/design-review-checklist.md`, however, contain visual-quality rules (interactive/data states, a grayscale-first workflow, a depth-pick-one-of-three discipline, Traditional Chinese font-stack/`lang` handling, and a discipline of comparing against curated real-product references instead of guessing values) that are genuinely useful independent of that workflow.
- Decision: Extract only the visual-quality rules, fold them into the existing `ai/DESIGN_RULES.md` and `docs/WEB_DATA_APP_DESIGN_PLAYBOOK.md` rather than adding new canonical files, and do not adopt the kanban board, review-gate/subagent apparatus, model routing, Epic/User Story/Task decomposition, or the 5-stage design-system ritual. `ai/DESIGN_RULES.md`'s Non-goals section records this exclusion and why, mirroring how it already records the Agent_html_report exclusions from ADR-004.
- Consequence: `web/` UI work gets a handful of concrete, previously-missing rules (states, depth, grayscale-first, CJK font-stack/`lang`, reference comparison) without adding a second workflow apparatus alongside this template's own change protocol, canonical-tier system, and `docs/DECISIONS.md`. If a future clone genuinely needs full multi-agent SDLC governance, that is a deliberate, separate template-level decision — not something this ADR pre-authorizes.
