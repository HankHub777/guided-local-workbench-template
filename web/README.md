# Web application

This directory owns React UI, presentation state, and the data adapter boundary. The initial implementation may read generated JSON. It must not assume that local files will remain the permanent source.

Recommended future layout:

```text
web/src/
  components/      Reusable UI pieces
  features/        User workflows grouped by business capability
  data/            Local/API adapters and query functions
  pages/           Route-level composition
  styles/          Tailwind entry point and minimal global styles
```

When an API replaces JSON, change the adapter in `web/src/data/`; avoid changing components solely to change transport.
