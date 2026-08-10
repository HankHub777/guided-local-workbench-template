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

## ADR-003: Treat repository context as a portable handoff package

- Status: Accepted
- Context: A working single-file prototype may depend on one user's chat history or a particular model's temporary context. This makes it difficult to move work between people, LLMs, controlled agent environments, and engineering teams.
- Decision: Keep the project's intent, file ownership, data contracts, validation expectations, and upgrade triggers in versioned repository documents. Prefer small, reviewable changes that preserve these boundaries.
- Consequence: The template adds some initial documentation work, but a chatbot-only prototype can later move to a controlled agent environment or engineering ownership with lower communication cost and less reverse engineering.
