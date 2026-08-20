# Enterprise environment and bootstrap guidance

## Purpose

A correct workbench can still fail on a company-managed machine before the user reaches the application workflow. Common causes include authenticated proxies, TLS interception and enterprise CAs, internal package registries, restricted/offline networks, browser policy, missing runtimes, firewall/network rules, and host power/availability.

Treat these as explicit environment capabilities and ownership boundaries rather than hidden setup friction.

## Start with a read-only preflight

Run:

```text
python scripts/check_environment.py
```

For machine-readable output:

```text
python scripts/check_environment.py --json
```

The checker is intentionally non-invasive. It does not install packages, test credentials, alter proxy variables, modify registries, change Windows Firewall, or rewrite browser/OS policy.

It reports:

- Python and Git availability;
- Node/npm availability for web-development work;
- installed Chrome/Edge/Chromium candidates when discoverable;
- the **names only** of detected proxy and certificate-related environment variables;
- capability-oriented status so a maintainer can see what is ready and what still needs preparation.

## Environment modes to recognize

Do not assume every company machine is simply "online" or "offline". A useful planning vocabulary is:

- **ready/prepared** — required runtimes and dependencies are already available;
- **direct-online** — public package/download endpoints are allowed directly;
- **proxy-online** — approved authenticated proxy configuration is required;
- **internal-mirror** — dependencies must come from company PyPI/npm/browser-artifact mirrors;
- **offline/restricted** — dependencies must be pre-provisioned or installed from approved offline media/cache.

The repository should respect the organization's existing mechanism rather than inventing a company-specific proxy subsystem.

## Standard configuration, not secret-bearing repository config

Depending on company policy, relevant ecosystem mechanisms may include:

- `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`;
- pip index/proxy/certificate configuration;
- npm registry/proxy/certificate configuration;
- enterprise CA variables such as `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, or `NODE_EXTRA_CA_CERTS`;
- approved Playwright/browser download mirrors or preinstalled browsers.

Do not commit real proxy URLs containing credentials, tokens, internal hostnames, certificate secrets, or user-specific values. Tracked files may document variable **names** and safe examples only.

## Loopback health checks must stay local

A localhost service check should not accidentally traverse the enterprise HTTP proxy.

When checking a service bound to `127.0.0.1`/loopback, prefer a direct loopback connection or a narrowly scoped local bypass. Do not globally disable the company proxy merely to make a health check pass.

This prevents a healthy local service from being misclassified by an authenticated proxy response such as HTTP 407 while preserving enterprise policy for non-local traffic.

## Safe automation boundary

The tool may safely automate deterministic local checks such as:

- required files exist;
- expected runtime executable is available;
- a configured local port is free or occupied;
- generated data parses/validates;
- a direct loopback health request succeeds;
- plausible local interface addresses are displayed;
- browser/runtime capability is present.

The tool should normally **not** automatically:

- disable or broadly modify Windows Firewall;
- create company-wide proxy settings;
- write credentials into environment variables or config files;
- install unapproved root certificates;
- change DHCP/static-IP, VLAN, DNS, Group Policy, or power policy;
- kill an unknown process merely because a port is occupied.

Those are human/IT-owned decisions unless the organization has explicitly delegated them to approved automation.

## When environment friction unlocks a new architecture decision

Do not hide a new requirement as a bootstrap tweak:

- stable enterprise URL/name → IT-managed addressing/DNS/reverse proxy as appropriate;
- unattended always-on hosting → approved service/autostart/supervision/monitoring;
- per-user visibility → authentication/authorization + trusted server layer;
- shared writes → backend + durable database/write rules;
- public/untrusted network → formal production hosting, TLS, security review.

See `docs/UPGRADE_PATH.md` for the Local → Managed → Product progression.

## Handoff expectation

Before ordinary colleagues depend on the tool, document at least:

- who owns the host/runtime environment;
- who owns source-data refresh/validation;
- which environment mode applies;
- how dependencies are provisioned on a fresh machine;
- which limitations are accepted versus owned by IT;
- what must never be placed in Git or chatbot context.
