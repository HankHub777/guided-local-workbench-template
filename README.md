# Guided Local Workbench Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Public](https://img.shields.io/badge/status-public-brightgreen.svg)](https://github.com/HankHub777/guided-local-workbench-template)
[![Read in English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![閱讀中文版](https://img.shields.io/badge/lang-繁體中文-lightgrey.svg)](README.zh-TW.md)

This is a template that lets an ordinary user build a personal local workbench **guided by an LLM chatbot**, without needing agent capabilities in a company environment. The template provides clear documentation, data contracts, and safety boundaries so a chatbot can help the user work through an acceptance-testable local tool step by step.

By default, the tool runs locally — for example, Excel goes through an ETL step into JSON, which a React front end then reads. As requirements mature, the same repository can progressively add an API, a database, deployment, and formal service governance. That upgrade path existing is not a reason to add those pieces early, during the prototype stage.

## How to Start

You don't need to know git well to get this template onto your computer. This section only covers getting the files onto your machine — for what to do once you have them, keep reading the sections below.

### The easy way (recommended)

1. Go to the [template's GitHub page](https://github.com/HankHub777/guided-local-workbench-template).
2. Click the green **Use this template** button, then **Create a new repository**. This makes your own independent copy under your own GitHub account — changes you make won't affect the original template, and changes to the original template won't automatically show up in yours either.
3. Give it a name (this becomes your project's name) and click **Create repository**.
4. On your new repository's page, click the green **Code** button and copy the URL shown there (it looks like `https://github.com/your-username/your-project-name.git`).
5. Open a terminal — macOS: the **Terminal** app; Windows: **PowerShell** — and go to the folder where you want this project to live, for example:
   ```bash
   cd ~/Documents
   ```
6. Run:
   ```bash
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```
   This downloads all the template's files into a new folder named after your project, and puts you inside it.

You now have your own copy, ready to go — continue with "Choose an operating mode first," below.

### If "Use this template" isn't available to you

Some company GitHub accounts turn this button off. If that's your situation:

1. Create a new, empty repository on GitHub yourself — don't add a README, license, or `.gitignore` when creating it; leave it completely empty. Copy its URL.
2. Open a terminal, go to where you want the project to live, and run:
   ```bash
   git clone https://github.com/HankHub777/guided-local-workbench-template.git my-project
   cd my-project
   ```
   ("Cloning" downloads a full copy of a repository. This one command does everything a beginner would otherwise need separate `git init` and `git remote add` commands for, which is why they don't appear here as extra steps.)
3. Point this copy at your own empty repository instead of the original template, then upload everything to it:
   ```bash
   git remote remove origin
   git remote add origin https://github.com/your-username/your-new-repo-name.git
   git push -u origin main
   ```

Either way, you end up in the same place: your own project, on your own GitHub account, with nothing connecting it back to the original template.

## Why a template, not just a single HTML file

A single HTML file plus an ongoing conversation with an LLM is a great fit for a one-off, personal-use tool. This template handles a different situation: the tool keeps changing, uses real data, gets handed to other people, or will eventually need to become a real service.

The template's goal isn't to turn everyone into an agent engineer — it's to let more people with LLM experience become **guided, template-backed LLM tool builders**. This kind of user can break a business need down into small, acceptance-testable changes, let the chatbot collaborate within clear boundaries, and know when to hand things off to an engineering team.

| Aspect | Long chat + single HTML file only | Guided, template-backed LLM tool builder |
| --- | --- | --- |
| Project context | Lives in chat history or personal memory | Lives in the README, data contract, decisions, and file manifest |
| Chatbot judgment | Infers current state from long text, prone to guessing wrong or rewriting existing features | Makes small, checkable changes based on designated documents and responsibility boundaries |
| Changing person, model, or computer | Background must be re-explained from scratch | Handing over the same repository context is enough |
| Real data | Easily leaks into the UI, gets hand-edited, or can't be regenerated | Has clear boundaries for input, validation, generated data, and lineage |
| Upgrade and handoff | Engineers must first reverse-engineer the prototype | Data sources, rules, exceptions, acceptance criteria, and upgrade triggers are ready to hand over |

These documents don't eliminate a chatbot's mistakes or hallucinations; they confine errors to a smaller, more explicit, verifiable, and reversible scope. Control over the project no longer depends on one chat transcript or one model — it lives in files anyone can inspect.

**Already have real work built up as a single-file HTML prototype and want to bring it in here instead of starting over?** See [docs/MIGRATION_FROM_SINGLE_FILE.md](docs/MIGRATION_FROM_SINGLE_FILE.md) for a guided, prompt-by-prompt process — it tells you exactly which copy-paste prompt to use for your situation.

## Benefits for users, engineering, and the organization

For the user, the template lowers the barrier to *keeping going*: without understanding the full software architecture, they can still know where data lives, which files must not be hand-edited, how to ask the chatbot for a small change, and how to verify the result.

For the engineering team, the template raises the quality of a handoff. The prototype isn't just a UI — it carries its data sources, data definitions, exception rules, a reproducible process, and validated usage scenarios. Engineers can spend their time on security, integration, permissions, reliability, and productionization, instead of guessing the prototype's intent from scratch.

For managers and the organization, this is a capability-scaling path: it turns a large pool of people who can use an LLM but can't independently maintain a tool into people who can safely build, verify, and hand off local workflows. Even when today's enterprise environment only allows a chatbot, once a controlled agent environment opens up later — or once an engineering team takes over development — the clear repository context, contracts, and decisions let the work continue with low friction and low communication cost.

## Choose an operating mode first

| Mode | When to use | Required directories |
| --- | --- | --- |
| Local | Solo/small team, read-heavy, JSON is rebuildable | `web/`, `data/`, `scripts/`, `shared/` |
| Managed | Needs scheduled ETL, shared by multiple people, or a controlled API | Add `server/` and CI |
| Product | Accounts, permissions, multi-person writes, audit, or public-facing | Enable `server/`, `config/database.*`, deployment, and testing |

Don't enable a backend or database just because the directory exists. See [docs/UPGRADE_PATH.md](docs/UPGRADE_PATH.md) for upgrade triggers.

## Quick rules

1. `data/input/` is input; `data/generated/` is ETL output — never hand-edit it.
2. The UI never depends directly on a JSON file path; it only reads data through the adapter in `web/src/data/`.
3. `shared/` is the single source of truth for data contracts: types, schemas, and field names are all defined here.
4. Secrets never go into Git; use `.env` locally, and put shareable examples in `config/*.example.*`.
5. Every time the data structure changes, update the schema, ETL, test data, and `docs/DATA_CONTRACT.md` together.

## The boundary between the template contract and project content

The same person may use this template to build more than one local workbench over time, and clones get handed off between colleagues. If the template's own contract files get casually rewritten as part of ordinary changes, each clone gradually drifts into a different shape, and versions stop matching each other at handoff.

- **Template contract (don't change its rules or structure while building a single tool)**: `README.md`, `README.zh-TW.md`, `AGENTS.md`, `ai/ARCHITECTURE_RULES.md`, `ai/DESIGN_RULES.md`, the table structure of `docs/FILE_MANIFEST.md`, the upgrade triggers in `docs/UPGRADE_PATH.md`, `docs/MIGRATION_FROM_SINGLE_FILE.md`, `docs/MIGRATION_FROM_SINGLE_FILE.zh-TW.md`, `.gitignore`, `LICENSE`, `scripts/apply_update.py`, `updates/README.md`, `scripts/build_context_bundle.py`.
- **Project content (keep filling in and changing this while building the tool)**: `ai/PROJECT_CONTEXT.md`, `docs/DATA_CONTRACT.md`, `docs/DECISIONS.md`, `config/*.example.json`, and `web/`, `server/`, `shared/`, `scripts/` (except `apply_update.py` and `build_context_bundle.py`), `data/`, `tests/`. `CHANGELOG.md` is only ever appended to by `scripts/apply_update.py` — no update package should overwrite it directly. `LLM_CONTEXT_BUNDLE.md` is a build artifact, not tracked in Git, rebuilt by `scripts/build_context_bundle.py`.

For the full list, how to classify a file, and the process for when the template itself seems to need a change, see [docs/TEMPLATE_BOUNDARY.md](docs/TEMPLATE_BOUNDARY.md).

## Working with an LLM chatbot

In an environment where you can't use an agent, run this before starting a conversation:

```bash
python3 scripts/build_context_bundle.py
```

This produces a single file, `LLM_CONTEXT_BUNDLE.md` (containing six documents in order, each with a one-line description of what it's for: collaboration rules, which files must not be casually changed, the whole project's file index, what this tool is for, the boundaries of the code architecture, and the default frontend design rules). Upload or paste this one file to your chatbot, instead of uploading six files one by one — and it's less likely to hit your chat tool's upload limit. This bundle is a rebuildable artifact and isn't tracked in Git; just run it again before starting a new conversation, and you don't need to worry about it going stale.

If the generated file starts with a warning like "still template placeholder content," it means the document describing what this tool is for (`ai/PROJECT_CONTEXT.md`) hasn't been filled in with your own project's real content yet — it's still the generic content the template ships with. Seeing that warning means the chatbot is currently working from generic placeholder text, not the real facts about *your* tool. Take the time to rewrite that document for your own project, and the chatbot's suggestions will actually be useful.

If this task touches a specific data structure, attach the corresponding `shared/` data contract file separately — the bundle deliberately doesn't include it, since it's task-specific rather than something to hand over every time.

After providing context, make **one acceptance-testable request** at a time, and ask the chatbot to first state which files it will change and which acceptance criteria will pass, before producing a patch. Don't ask it to "build a complete system." The user should still inspect the patch locally, run the verification steps, and only give the chatbot content that contains no confidential information.

### Applying the chatbot's output locally

If your chatbot can only export the whole set of updated files (no agent capability, can't touch local files directly), don't manually overwrite your local folder with the whole package. Instead:

1. Ask the chatbot to export the changes as a zip, named per the fixed format `update_YYYYMMDD_HHMMSS.zip` (for example `update_20260811_153000.zip`), and to include the `manifest.json` defined in `updates/README.md` whenever possible.
2. Put that file into `updates/incoming/`.
3. Run `scripts/apply_update.py` for your OS (macOS Terminal or Windows PowerShell) — for the exact copy-paste commands and what the interactive prompts mean, see [updates/README.md](updates/README.md).
4. After the script finishes, it prints a short block starting with "Paste this back into the chatbot so it knows what actually happened." **If you're going to ask the chatbot for anything else in the same conversation, copy that whole block and paste it as your next message.** The chatbot only knows what it *proposed* — not whether you actually went through with all of it. If you just skipped a change to some file and don't tell it, it'll assume that file was already changed, and its next suggestion may be built on a wrong assumption.

This script automatically applies ordinary project content, but always pauses for confirmation on template contract files or any deletion, and records the result of every run in `CHANGELOG.md`.

## Directory summary

See [docs/FILE_MANIFEST.md](docs/FILE_MANIFEST.md) for the full definitions. Start with that file the first time you pick up the template.

```text
ai/        AI project context and change rules
config/    Version-controlled configuration examples
data/      Input, test fixtures, ETL output
docs/      Human-readable decisions, contracts, and handoff documents
scripts/   Repeatable jobs like Excel/CSV → JSON
shared/    Types, schemas, and constants shared between front and back end
updates/   Inbox and script for applying a chatbot's packaged update
web/       React + TypeScript + Tailwind front end
server/    Boundary for API/background work (only a README for now)
```
