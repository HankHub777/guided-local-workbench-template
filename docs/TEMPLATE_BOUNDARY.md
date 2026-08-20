# Template boundary: canonical vs. instance files

This template is cloned once per local workbench project. The same person may build several workbenches over time from separate clones, and clones get handed off between colleagues. If the template's own contract files silently absorb project-specific edits, each clone drifts into a different shape and handoffs stop being reliable. This document exists to prevent that.

## Canonical files (template contract)

These define the template mechanism itself. Do not rewrite their rules or structure as part of building a specific tool — only as a deliberate, confirmed template-level change (see below).

- `README.md`
- `README.zh-TW.md`
- `AGENTS.md`
- `ai/ARCHITECTURE_RULES.md`
- `ai/DESIGN_RULES.md`
- `docs/FILE_MANIFEST.md` — its table structure and row set (new instance-specific files still get added as new rows)
- `docs/UPGRADE_PATH.md` — its trigger conditions and incremental infrastructure rules
- `docs/TEMPLATE_BOUNDARY.md` (this file)
- `docs/MIGRATION_FROM_SINGLE_FILE.md`
- `docs/MIGRATION_FROM_SINGLE_FILE.zh-TW.md`
- `docs/UPSTREAM_EXTRACTION.md`
- `docs/ENTERPRISE_ENVIRONMENT.md`
- `docs/WEB_DATA_APP_DESIGN_PLAYBOOK.md`
- `.gitignore`
- `.gitattributes`
- `LICENSE`
- `scripts/README.md`
- `scripts/apply_update.py`
- `scripts/build_context_bundle.py`
- `scripts/check_environment.py`
- `scripts/scan_repo_for_remote_review.py`
- `scripts/scan_public_candidates.py`
- `updates/README.md`

`scripts/apply_update.py` (see [`updates/README.md`](../updates/README.md)) enforces this boundary automatically whenever an LLM-delivered update package is applied: files outside this list apply without asking, but any change to a file on this list — or any deletion at all — always pauses for explicit confirmation first.

`scripts/build_context_bundle.py` generates `LLM_CONTEXT_BUNDLE.md`, a single-file concatenation of `AGENTS.md`, this file, `docs/FILE_MANIFEST.md`, `ai/PROJECT_CONTEXT.md`, `ai/ARCHITECTURE_RULES.md`, and `ai/DESIGN_RULES.md` (its own `BUNDLE_FILES` constant is the source of truth) for handing to an LLM chatbot at the start of a session — see README.md's "LLM chatbot 工作方式".

## Canonical tiers: always-bundled core vs. situational specialist

The canonical list above is bigger than what actually belongs in every chatbot session. Every new canonical file must be assigned to one of two tiers — do not leave it undecided; an unassigned file looks like drift, not a decision (this rule exists because that happened once — see ADR-005 in `docs/DECISIONS.md`):

- **Always-bundled core** — needed regardless of what the session is about. Add it to `scripts/build_context_bundle.py`'s `BUNDLE_FILES`.
- **Situational specialist** — only needed for a specific kind of task (an enterprise-network constraint, an upstream port, UI work). Keep it out of `BUNDLE_FILES` so the default bundle stays small, but make it discoverable two other ways instead: add a row to `docs/FILE_MANIFEST.md` with a concrete "Read or update when" trigger, and name the same trigger in `AGENTS.md`'s "Situational guidance" section.

Both tiers are equally canonical — the tier only controls whether a file rides along in every default handoff or gets found on demand.

## Instance files (this project's own content)

Fill these in and evolve them freely while building the tool — that is what they are for.

- `ai/PROJECT_CONTEXT.md`
- `docs/DATA_CONTRACT.md`
- `docs/DECISIONS.md`
- `config/*.example.json`
- `web/`, `server/`, `shared/`, `data/`, `tests/`
- project-specific content under `scripts/`; only the canonical scripts listed above belong to the template mechanism itself

## If a task seems to need a template-level change

Stop. Do not fold a canonical-file edit into the instance change you were asked for. Log it in the table below, then get explicit user confirmation before editing the canonical file's rules or structure.

## Proposed template changes

| Date | Canonical file | Problem noticed | Proposed change | Status |
| --- | --- | --- | --- | --- |
| _(none yet)_ | | | | |

Status values: `proposed`, `applied-here-by-confirmation`, `to-port-upstream`.

## Why this doesn't auto-propagate

A canonical-file edit made in one clone stays in that clone. It does not reach other clones already in progress, and it does not reach the template's origin repository on its own. A genuinely valuable change should be manually ported upstream once confirmed — that manual step is what keeps future clones consistent with each other.

Use `docs/UPSTREAM_EXTRACTION.md` and its read-only scanners to separate reusable template improvements from project-instance implementation before opening an upstream PR. Do not treat a working reference implementation as proof that every file in that instance belongs in the public template.
