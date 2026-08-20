# Scripts

Scripts convert data or support repeatable local work. Each script must document inputs, outputs, error behaviour, and a safe re-run procedure.

## Canonical template helpers

| Script | Input → output | Rule |
| --- | --- | --- |
| `apply_update.py` | `updates/incoming/` package → applied files + `CHANGELOG.md` entry | Protects canonical files from silent overwrite. Usage: `updates/README.md`. |
| `build_context_bundle.py` | canonical orientation files → `LLM_CONTEXT_BUNDLE.md` | Always regenerates from scratch; refuses to write a partial bundle if a source file is missing. Run before starting a new chatbot session. |
| `check_environment.py` | local runtime/tooling state → plain-text or JSON capability report | Read-only. Reports tool availability and only the names of proxy/CA variables; never installs packages or prints secret values. |
| `scan_repo_for_remote_review.py` | repository/Git state → `artifacts/remote_repo_review/repo_remote_review.{md,json}` | Read-only first-stage inventory for separating reusable template material from instance state. |
| `scan_public_candidates.py` | explicit candidate paths → content/diff review report | Read-only second-stage audit. Candidate paths are supplied by the human/LLM; the script does not decide what should be published. |

See `docs/UPSTREAM_EXTRACTION.md` for the complete upstream-port workflow and `docs/ENTERPRISE_ENVIRONMENT.md` for enterprise setup boundaries.

## Typical instance scripts added later

| Script | Input → output | Rule |
| --- | --- | --- |
| `refresh-data` | Excel/CSV → validated JSON | Never silently drop invalid data. |
| `validate-data` | JSON/fixture → validation report | Runs before the UI consumes new data. |
| `start-local` | project → local browser URL | Avoid asking office users to remember build commands. |

Do not add a scheduled job until Managed mode is explicitly approved.
