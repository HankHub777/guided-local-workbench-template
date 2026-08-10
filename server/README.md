# Server boundary

No executable server is required in Local mode. This directory exists to make the later transition explicit rather than forcing a repository redesign.

Create server code only when [docs/UPGRADE_PATH.md](../docs/UPGRADE_PATH.md) requires Managed or Product mode. It then owns:

- API endpoints and authorization;
- trusted business rules and write workflows;
- scheduled jobs and external integrations;
- database access, migrations, and audit requirements.

It must expose contracts defined in `shared/`, never expose database credentials to `web/`, and retain a local-development path.
