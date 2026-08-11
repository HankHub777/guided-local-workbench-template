# Project context for AI

## Product intent

Enable ordinary users to build small office tools with guidance from an LLM chatbot, including in enterprise environments where agent capabilities are unavailable. The first release is normally a local, read-only React application built from spreadsheet-derived data. Its purpose is to shorten repetitive work and turn a user workflow into a testable prototype.

The template must be understandable through documents and small, reviewable changes. Chatbot assistance is a short-term interaction model, not a requirement for the resulting tool at runtime. The repository must keep a clear upgrade path to a managed web service when the real workflow requires it.

Its organizational value is to turn LLM-assisted prototypes into portable, verifiable, and handoff-ready assets. The same repository context must support a chatbot-only environment today, a controlled agent environment later, and eventual engineering ownership with low communication overhead.

## Primary users

- Ordinary user / citizen developer: knows the business process and verifies results, but is not expected to understand framework internals or have access to an agent environment.
- LLM chatbot: helps the user understand the template and produce small, reviewable changes from the provided project context.
- Engineer: owns reusable architecture, security boundaries, integrations, and escalation to a managed product.

## Definition of done

- A named user can complete the target workflow with representative data.
- The tool identifies missing or invalid input rather than silently producing misleading output.
- Data lineage is documented: source workbook, refresh procedure, and generated file.
- The change works in the current operating mode and does not require hidden manual setup.

## Required question before implementing

Ask or infer: Is the tool read-only? Who owns the source data? Can two people change the same record? Does it contain sensitive data? What is the refresh frequency? These answers determine whether local JSON remains appropriate.
