# Architecture decisions

Record only decisions that constrain future work.

## ADR-001: Start with local JSON read models

- Status: Accepted
- Context: Early office tools need fast iteration and normally have a spreadsheet source of truth.
- Decision: ETL produces validated JSON; the browser reads it through a data adapter.
- Consequence: Concurrent editing, authentication, and durable write workflows are out of scope until an explicit upgrade decision.

## ADR-002: Make chatbot-guided local workbenches the primary template use case

- Status: Accepted
- Context: Some enterprise environments allow users to use an LLM chatbot but do not allow agent capabilities. Ordinary users still need a safe way to create and evolve small local tools.
- Decision: Keep project context, file ownership, and verification steps in short repository documents that can be supplied to a chatbot. Design the initial tool to run locally without agent capabilities at runtime, while retaining the documented path to managed and product modes.
- Consequence: Documentation and small reviewable changes are first-class template features. Chatbot output must be reviewable locally, and no secrets or sensitive data may be included in chatbot context.
