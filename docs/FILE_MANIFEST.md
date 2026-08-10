# Template file manifest

This is the short map for ordinary users, LLM chatbots, and AI agents. Read this file first, then open only the files relevant to the requested change.

## Always-present foundation

| Path | Why it exists | Read or update when |
| --- | --- | --- |
| `README.md` | Explains the template, operating modes, and core rules. | Starting the project or changing its user-facing setup. |
| `AGENTS.md` | Required collaboration and safe-change rules for chatbot- or agent-assisted changes. | Before every change. |
| `ai/PROJECT_CONTEXT.md` | Product intent, users, definition of done, and questions that determine the operating mode. | Scoping a feature. |
| `ai/ARCHITECTURE_RULES.md` | Dependency direction and local-to-managed boundaries. | Changing code structure or data flow. |
| `docs/FILE_MANIFEST.md` | This plain-language inventory of the shared template base. | Orienting a person or agent. |
| `docs/DATA_CONTRACT.md` | Dataset ownership, schema, validation, and lineage. | Adding or changing data. |
| `docs/UPGRADE_PATH.md` | Objective triggers for adding a server, database, or managed service. | A request needs shared access, scheduling, writes, auth, or audit. |
| `docs/DECISIONS.md` | Durable architectural decisions (ADRs). | A choice constrains future work. |
| `config/*.example.json` | Safe, versioned examples of non-secret app, data-source, API, and database configuration. | Adding configurable behavior; never put real credentials here. |
| `.gitignore` | Excludes dependencies, secrets, generated data, and local inputs from Git. | Introducing a new local artifact type. |

## Directories that become active as the tool is implemented

| Path | Responsibility | First file to add |
| --- | --- | --- |
| `shared/` | Canonical runtime schemas, types, and constants used across boundaries. | A schema for the first dataset. |
| `scripts/` | Repeatable ETL, validation, and local helper commands. | A documented data refresh/validation command. |
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
