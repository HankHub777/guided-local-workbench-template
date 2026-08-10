# Scripts

Scripts convert data or support repeatable local work. Each script must document inputs, outputs, error behaviour, and a safe re-run procedure.

Recommended future scripts:

| Script | Input → output | Rule |
| --- | --- | --- |
| `refresh-data` | Excel/CSV → validated JSON | Never silently drop invalid data. |
| `validate-data` | JSON/fixture → validation report | Runs before the UI consumes new data. |
| `start-local` | project → local browser URL | Avoid asking office users to remember build commands. |

Do not add a scheduled job until Managed mode is explicitly approved.
