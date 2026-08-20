# Upgrade path

## Governing rule

Add infrastructure because a requirement needs it, not because a mature architecture diagram normally contains it. Preserve boundaries so an upgrade replaces the smallest necessary layer instead of forcing a rewrite of the working tool.

## Stay in Local mode when all are true

- The UI is read-only or edits are exported for manual review.
- One named owner controls the input spreadsheet or other authoritative source.
- Generated read models can be regenerated from that source.
- No sensitive data leaves the approved local environment.
- Failure has low operational impact and can be corrected by regenerating data.

## Move to Managed mode when any is true

- Refresh needs scheduling, shared access, or a trusted API.
- The same data is consumed by more than one tool.
- Transformation rules need central review or versioned execution.
- The data volume makes local browser loading impractical.

Managed mode is not one fixed stack. Add the smallest reliable layer that satisfies the new requirement.

| New requirement | Smallest layer that normally becomes justified |
| --- | --- |
| Other approved users need the same read-only app | Shared HTTP/static hosting for the production build when the app already consumes a generated read model |
| Data refresh must run without a person | Scheduler / managed job around the existing validated refresh command |
| Several tools need the same queryable data | Trusted API or shared data service |
| Transformation rules must execute centrally | Managed job/service with versioned rules and observable failures |
| Browser loading is no longer practical | Server-side query/aggregation or a more appropriate read model |
| Host must remain available unattended | Approved service/autostart/supervision/monitoring design |

For a read-only web app, prefer this progression when it fits the real requirement:

`validated data boundary → production frontend → smallest shared host → independent data refresh → second-client acceptance → repeatable operations → enterprise-environment review`

Do not introduce a database, authentication system, queue, container platform, or application backend merely because the app moved from one browser to several browsers.

Before a Managed rollout, check the relevant enterprise environment constraints in `docs/ENTERPRISE_ENVIRONMENT.md`.

## Managed-mode acceptance

The exact checks depend on the project, but a shared read-only deployment should normally prove:

- the production build is served rather than a development server;
- data refresh and code deployment have separate lifecycles where the architecture allows it;
- at least one real second client can use the normal workflow;
- start/status/stop/recovery steps are understandable by the named maintainer;
- network, proxy, certificate, firewall, host power, and addressing limitations are explicit rather than hidden;
- data sensitivity and the intended audience are approved before network exposure.

## Move to Product mode when any is true

- Multiple people can write the same business record.
- Authentication, roles, audit history, notifications, integrations, or external users are required.
- The tool affects finance, HR, regulated processes, or business-critical decisions.
- A database is required for durable state rather than merely a query cache.

These requirements usually unlock trusted server-side state and controls rather than being safe configuration tweaks to a local/static app.

Examples:

- per-user visibility → authentication/authorization + trusted server layer;
- shared durable writes → backend + database + write/audit rules;
- public or untrusted-network access → formal production hosting, TLS, security review, and organization-approved operations;
- business-critical unattended availability → service supervision, monitoring, ownership, and recovery expectations.

## Handoff package

Before engineering takes over, provide: current prototype, source data sample, data contract, user workflow, known exceptions, three correct-output examples, failure impact, named product/data owner, current operating mode, and any known enterprise-environment limitations.
