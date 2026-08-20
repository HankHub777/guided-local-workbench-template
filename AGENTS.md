# AI collaboration rules

## Scope

This repository is a guided template for building local workbenches with an LLM chatbot. It may grow into a managed product. Preserve that upgrade path without introducing services that the current mode does not require.

## Chatbot-only and agent-driven sessions follow the same rules

Everything in this file applies the same way whether an LLM chatbot with no file access or a coding agent with direct file access is reading it. This repository does not have a separate agent-oriented mode or a heavier governance track for agent sessions — see ADR-006 in `docs/DECISIONS.md` for why that was deliberately not adopted.

The only difference is mechanical, not procedural:

- **Chatbot-only, no file access**: use `scripts/build_context_bundle.py` to hand over context and `scripts/apply_update.py` to apply an exported update package — see README.md's "Working with an LLM chatbot" section. This exists because the chatbot cannot touch files directly.
- **Agent with direct file access**: skip that bootstrapping. Read `docs/FILE_MANIFEST.md` and the relevant canonical docs directly, then edit tracked files yourself.

Direct file access changes *how* a change gets made, not *who* approves it: the Change protocol below, human review of the diff, and the canonical-file confirmation rule apply identically either way. This template's guardrail is the human in the loop, not automated review gates or a task/backlog governance layer — do not introduce those to compensate for having agent access; that would be a different, larger project, not this one (see `docs/DECISIONS.md` ADR-006).

## Non-negotiable rules

- Read `docs/FILE_MANIFEST.md`, `ai/PROJECT_CONTEXT.md`, `ai/ARCHITECTURE_RULES.md`, `ai/DESIGN_RULES.md`, and the relevant document in `docs/` before editing.
- Treat `README.md`, this file, `ai/ARCHITECTURE_RULES.md`, `ai/DESIGN_RULES.md`, and `docs/FILE_MANIFEST.md`'s structure as template contract, not project content, per `docs/TEMPLATE_BOUNDARY.md`. Do not rewrite their rules or structure as part of an ordinary feature/data/UI change.
- Treat `shared/` as the canonical contract. Do not duplicate types in `web/`, `server/`, or `scripts/`.
- Validate untrusted runtime data. TypeScript types alone do not validate JSON, spreadsheets, forms, or API responses.
- Do not put secrets, personal data samples, access tokens, or production connection strings in tracked files.
- Keep local mode usable without a server or database.
- For every change, update the smallest relevant documentation and give a manual verification step.

## Situational guidance

The rules above always apply. These apply only when the situation matches:

- Building or changing UI in `web/`: also read `docs/WEB_DATA_APP_DESIGN_PLAYBOOK.md` (layout, hierarchy, chart choice, anti-template review) alongside `ai/DESIGN_RULES.md`.
- The workflow must run on a company-managed or restricted machine (proxy, CA, mirror, offline, firewall): read `docs/ENTERPRISE_ENVIRONMENT.md` before treating it as an ordinary bug.
- Extracting reusable lessons from a mature or production instance clone back into this template: read `docs/UPSTREAM_EXTRACTION.md` first; do not port instance-specific content directly.

`docs/FILE_MANIFEST.md`'s "Read or update when" column is the general index for anything not covered above.

## Change protocol

1. State the user-visible outcome and files to change.
2. Make the smallest coherent change.
3. Run the applicable check or provide exact manual verification.
4. If the request triggers an item in `docs/UPGRADE_PATH.md`, stop treating it as a local-only change and record the decision in `docs/DECISIONS.md`.
5. If the request would alter a canonical file's rules or structure (see `docs/TEMPLATE_BOUNDARY.md`), stop, name it explicitly as a template-level change, log it in that file's proposal table, and get explicit user confirmation before editing it.
