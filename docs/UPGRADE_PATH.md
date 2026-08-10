# Upgrade path

## Stay in Local mode when all are true

- The UI is read-only or edits are exported for manual review.
- One named owner controls the input spreadsheet.
- JSON can be regenerated from the authoritative source.
- No sensitive data leaves the approved local environment.
- Failure has low operational impact and can be corrected by regenerating data.

## Move to Managed mode when any is true

- Refresh needs scheduling, shared access, or a trusted API.
- The same data is consumed by more than one tool.
- Transformation rules need central review or versioned execution.
- The data volume makes local browser loading impractical.

## Move to Product mode when any is true

- Multiple people can write the same business record.
- Authentication, roles, audit history, notifications, integrations, or external users are required.
- The tool affects finance, HR, regulated processes, or business-critical decisions.
- A database is required for durable state rather than merely a query cache.

## Handoff package

Before engineering takes over, provide: current prototype, source data sample, data contract, user workflow, known exceptions, three correct-output examples, failure impact, and named product/data owner.
