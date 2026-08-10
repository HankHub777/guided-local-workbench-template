# Shared contract module

This directory contains the canonical TypeScript types and runtime schemas shared by ETL, frontend, and (later) backend code.

Recommended future layout:

```text
shared/
  schemas/        Runtime validators for external data
  types/          Types inferred from or aligned with schemas
  constants/      Shared enumerations and business-neutral constants
```

Rule: a TypeScript interface documents code expectations; a runtime schema validates external input. Keep both aligned, preferably deriving types from schemas.
