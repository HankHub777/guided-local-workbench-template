# Data contract

## Dataset register

Copy this section for each dataset.

| Field | Definition |
| --- | --- |
| Dataset name | `example_records` |
| Business owner | Name / team responsible for correctness |
| Source | Workbook, sheet, or approved system |
| Refresh cadence | Manual / daily / weekly |
| Consumer | Tool or report using it |
| Sensitivity | Public / internal / confidential / restricted |

## Schema

Document every field: machine name, business label, type, allowed values, nullability, and example. The implementation schema in `shared/` must match this document.

## Validation policy

- Missing required column: fail the refresh and explain the missing column.
- Invalid row: report row number and reason; choose explicitly whether to reject the entire file or quarantine that row.
- Schema change: record the migration in `docs/DECISIONS.md` and retain a compatible reader or migration path.

## Data lineage

`input file → ETL script/version → generated JSON → UI view` must be traceable for every displayed metric.
