# AI collaboration rules

## Scope

This repository is a guided template for building local workbenches with an LLM chatbot. It may grow into a managed product. Preserve that upgrade path without introducing services that the current mode does not require.

## Non-negotiable rules

- Read `docs/FILE_MANIFEST.md`, `ai/PROJECT_CONTEXT.md`, `ai/ARCHITECTURE_RULES.md`, and the relevant document in `docs/` before editing.
- Treat `README.md`, this file, `ai/ARCHITECTURE_RULES.md`, and `docs/FILE_MANIFEST.md`'s structure as template contract, not project content, per `docs/TEMPLATE_BOUNDARY.md`. Do not rewrite their rules or structure as part of an ordinary feature/data/UI change.
- Treat `shared/` as the canonical contract. Do not duplicate types in `web/`, `server/`, or `scripts/`.
- Validate untrusted runtime data. TypeScript types alone do not validate JSON, spreadsheets, forms, or API responses.
- Do not put secrets, personal data samples, access tokens, or production connection strings in tracked files.
- Keep local mode usable without a server or database.
- For every change, update the smallest relevant documentation and give a manual verification step.

## Change protocol

1. State the user-visible outcome and files to change.
2. Make the smallest coherent change.
3. Run the applicable check or provide exact manual verification.
4. If the request triggers an item in `docs/UPGRADE_PATH.md`, stop treating it as a local-only change and record the decision in `docs/DECISIONS.md`.
5. If the request would alter a canonical file's rules or structure (see `docs/TEMPLATE_BOUNDARY.md`), stop, name it explicitly as a template-level change, log it in that file's proposal table, and get explicit user confirmation before editing it.
