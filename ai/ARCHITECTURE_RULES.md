# Architecture rules

## Dependency direction

```text
web UI ──> data adapter ──> shared contract <── ETL scripts
                              ^
                              └── server API (only after managed mode)
```

- `web/` may consume data through an adapter but must not read Excel files.
- `scripts/` may create generated JSON but must not contain UI code.
- `server/` may expose the shared contract but must not import browser-only modules.
- UI components must not contain business-critical rules; those migrate to `server/` when rules require trust, reuse, or auditability.

## Local-to-managed transition

Start with a `LocalDataSource` adapter. When an API is needed, add `ApiDataSource` implementing the same interface. UI code should not need a rewrite solely because its data source changes.

## Allowed defaults

- React + TypeScript + Tailwind CSS for `web/`.
- Schema validation at ETL/API boundaries.
- JSON as a generated read model, not as a concurrent write store.
- A single relational database only after a real persistence requirement exists.

## Disallowed defaults

- Authentication, database, microservices, queues, or cloud deployment in a Local-mode prototype.
- Direct database access from the browser.
- Credentials in frontend code or configuration tracked by Git.
- Adding a dependency when a small native implementation already meets the requirement.
