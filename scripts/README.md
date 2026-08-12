# Scripts

Scripts convert data or support repeatable local work. Each script must document inputs, outputs, error behaviour, and a safe re-run procedure.

| Script | Input → output | Rule |
| --- | --- | --- |
| `apply_update.py` | `updates/incoming/` package → applied files + `CHANGELOG.md` entry | Canonical (see `docs/TEMPLATE_BOUNDARY.md`) — protects itself and the other canonical files from silent overwrite. Usage: `updates/README.md`. |
| `build_context_bundle.py` | canonical orientation files → `LLM_CONTEXT_BUNDLE.md` | Canonical. Always regenerates from scratch; refuses to write a partial bundle if a source file is missing. Run before starting a new chatbot session. |

Recommended future scripts:

| Script | Input → output | Rule |
| --- | --- | --- |
| `refresh-data` | Excel/CSV → validated JSON | Never silently drop invalid data. |
| `validate-data` | JSON/fixture → validation report | Runs before the UI consumes new data. |
| `start-local` | project → local browser URL | Avoid asking office users to remember build commands. |

Do not add a scheduled job until Managed mode is explicitly approved.
