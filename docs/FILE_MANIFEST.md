# Template file manifest

This is the short map for ordinary users, LLM chatbots, and AI agents. Read this file first, then open only the files relevant to the requested change.

## Always-present foundation

"Canonical" files define the template mechanism itself and should not have their rules or structure rewritten while building a specific tool. "Instance" files are this project's own content — fill them in and evolve them freely. See `docs/TEMPLATE_BOUNDARY.md` for the full rule.

| Path | Canonical / Instance | Why it exists | Read or update when |
| --- | --- | --- | --- |
| `README.md` | Canonical | Explains the template, operating modes, and core rules. English is the default language. | Starting the project or changing its user-facing setup. |
| `README.zh-TW.md` | Canonical | Traditional Chinese translation of `README.md`; must stay in sync with it. | Whenever `README.md` changes. |
| `AGENTS.md` | Canonical | Required collaboration and safe-change rules for chatbot- or agent-assisted changes. | Before every change. |
| `ai/PROJECT_CONTEXT.md` | Instance | Product intent, users, definition of done, and questions that determine the operating mode. | Scoping a feature. |
| `ai/ARCHITECTURE_RULES.md` | Canonical | Dependency direction and local-to-managed boundaries. | Changing code structure or data flow. |
| `docs/FILE_MANIFEST.md` | Canonical (structure) | This plain-language inventory of the shared template base. | Orienting a person or agent. |
| `docs/TEMPLATE_BOUNDARY.md` | Canonical | Defines which files are template contract vs. project content, and how to propose a template-level change. | Before any change; whenever a request seems to touch a canonical file. |
| `docs/MIGRATION_FROM_SINGLE_FILE.md` | Canonical | Guided, prompt-by-prompt process (with routing) for bringing an existing single-file HTML prototype into this structure. | Someone arrives with a working single-file HTML prototype and wants to continue building it here. |
| `docs/DATA_CONTRACT.md` | Instance | Dataset ownership, schema, validation, and lineage. | Adding or changing data. |
| `docs/UPGRADE_PATH.md` | Canonical | Objective triggers for adding a server, database, or managed service. | A request needs shared access, scheduling, writes, auth, or audit. |
| `docs/DECISIONS.md` | Instance | Durable architectural decisions (ADRs). | A choice constrains future work. |
| `config/*.example.json` | Instance | Safe, versioned examples of non-secret app, data-source, API, and database configuration. | Adding configurable behavior; never put real credentials here. |
| `.gitignore` | Canonical | Excludes dependencies, secrets, generated data, and local inputs from Git. | Introducing a new local artifact type. |
| `LICENSE` | Canonical | MIT license terms covering this template and everything built from it. | A deliberate licensing decision, not a per-project change. |
| `CHANGELOG.md` | Instance | Dated, narrative record of every applied/declined change, written by `scripts/apply_update.py` and appendable by hand; substitutes for git history during the chatbot-only phase. | After every `apply_update.py` run; before an engineering handoff. |
| `LLM_CONTEXT_BUNDLE.md` | Generated (git-ignored) | Single-file concatenation of the canonical orientation files, built by `scripts/build_context_bundle.py`, for uploading to an LLM chatbot at the start of a session. Never hand-edit; regenerate instead. | Before starting a new chatbot session. |

## Directories that become active as the tool is implemented

| Path | Responsibility | First file to add |
| --- | --- | --- |
| `shared/` | Canonical runtime schemas, types, and constants used across boundaries. | A schema for the first dataset. |
| `scripts/` | Repeatable ETL, validation, and local helper commands. Instance content, except `scripts/apply_update.py` and `scripts/build_context_bundle.py`, which are canonical. | A documented data refresh/validation command. |
| `updates/` | Canonical mechanism for applying LLM-delivered update packages without manual file placement; see `updates/README.md`. `incoming/` and `applied/` hold transient, git-ignored working data. | Already present; used whenever a chatbot exports a whole-project update. |
| `data/input/` | Private local source spreadsheets or CSV files; ignored by Git. | The owner-provided source file. |
| `data/fixtures/` | Small anonymized test data that is safe to commit. | A representative fixture. |
| `data/generated/` | Rebuildable JSON read models; never hand-edit. | ETL output. |
| `web/` | React UI and its local/API data adapters. | The front-end project only when a named workflow is ready. |
| `tests/` | Fixture, contract, ETL, and critical workflow checks. | A test for the first user workflow. |
| `server/` | Future API, jobs, authorization, and trusted write rules. | Only after an upgrade trigger is met. |

## Files to add with the first implementation

Do not create empty dependency files before code exists. Once the first web and ETL implementation is approved, add these together:

| File | Purpose |
| --- | --- |
| `web/package.json` and its lockfile | Pins front-end dependencies and provides `dev`, `build`, and `test` commands. |
| `pyproject.toml` and `uv.lock` | Pins Python ETL and developer dependencies reproducibly. |
| `docs/DEVELOPMENT.md` | Lists prerequisites and exact install, run, and test commands for a new machine. |
| `docs/OPERATIONS.md` | Documents source-data ownership, refresh steps, outputs, and recovery from validation errors. |
| `.env.example` | Lists configuration variable names without secrets. |

## Maintenance rule

When adding, removing, or changing the responsibility of a shared template file or directory, update this manifest and the closest detailed document in the same change. Generated data, real input data, `.env` files, and credentials do not belong in this manifest or Git.
