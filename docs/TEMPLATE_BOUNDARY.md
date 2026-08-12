# Template boundary: canonical vs. instance files

This template is cloned once per local workbench project. The same person may build several workbenches over time from separate clones, and clones get handed off between colleagues. If the template's own contract files silently absorb project-specific edits, each clone drifts into a different shape and handoffs stop being reliable. This document exists to prevent that.

## Canonical files (template contract)

These define the template mechanism itself. Do not rewrite their rules or structure as part of building a specific tool — only as a deliberate, confirmed template-level change (see below).

- `README.md`
- `AGENTS.md`
- `ai/ARCHITECTURE_RULES.md`
- `docs/FILE_MANIFEST.md` — its table structure and row set (new instance-specific files still get added as new rows)
- `docs/UPGRADE_PATH.md` — its trigger conditions
- `docs/TEMPLATE_BOUNDARY.md` (this file)

## Instance files (this project's own content)

Fill these in and evolve them freely while building the tool — that is what they are for.

- `ai/PROJECT_CONTEXT.md`
- `docs/DATA_CONTRACT.md`
- `docs/DECISIONS.md`
- `config/*.example.json`
- `web/`, `server/`, `shared/`, `scripts/`, `data/`, `tests/`

## If a task seems to need a template-level change

Stop. Do not fold a canonical-file edit into the instance change you were asked for. Log it in the table below, then get explicit user confirmation before editing the canonical file's rules or structure.

## Proposed template changes

| Date | Canonical file | Problem noticed | Proposed change | Status |
| --- | --- | --- | --- | --- |
| _(none yet)_ | | | | |

Status values: `proposed`, `applied-here-by-confirmation`, `to-port-upstream`.

## Why this doesn't auto-propagate

A canonical-file edit made in one clone stays in that clone. It does not reach other clones already in progress, and it does not reach the template's origin repository on its own. A genuinely valuable change should be manually ported upstream (for example, a PR against the origin template repo) once confirmed — that manual step is what keeps future clones consistent with each other.
