# Upstream extraction from an instance clone

## Purpose

A successful workbench clone often accumulates two different kinds of value at the same time:

- **instance value** — domain code, data contracts, UI, fixtures, evidence, operational history;
- **template value** — reusable methods, guardrails, tooling, documentation patterns, and upgrade rules that should benefit future clones.

Do not upstream the whole successful instance. Extract only the reusable capability.

## Core rule

> A file can be valuable without belonging in the public template.

Ask whether a new project in a different domain would still benefit from the asset. If the answer depends on the current dataset, workflow, phase names, metrics, host, or evidence, keep it instance-only or generalize the lesson before upstreaming.

## Stage 1 — read-only repository inventory

From the instance repository root:

```text
python scripts/scan_repo_for_remote_review.py
```

Outputs are written under the git-ignored directory:

```text
artifacts/remote_repo_review/
  repo_remote_review.md
  repo_remote_review.json
```

The report inventories tracked, untracked, ignored, generated, data-like, and evidence-like paths. It does not stage, delete, reset, or edit anything.

Review the report before sharing it outside the approved environment: it can contain local filenames and repository paths even though embedded credentials in remote URLs are redacted.

## Stage 2 — explicit content-level candidate audit

Choose only the paths that actually need content-level review. Put one repository-relative path per line in a local file such as:

```text
artifacts/remote_repo_review/candidates.txt
```

Then run:

```text
python scripts/scan_public_candidates.py --paths-file artifacts/remote_repo_review/candidates.txt
```

You may also pass paths directly:

```text
python scripts/scan_public_candidates.py docs/example.md scripts/example.py
```

The second report includes current file content and tracked Git diffs so a human/LLM can classify each path without guessing from filenames alone.

Use this vocabulary:

- `PUSH AS-IS`
- `GENERICIZE THEN PUSH`
- `RESET / DON'T PUSH`
- `LOCAL ONLY`

The scripts never make that decision automatically.

## Stage 3 — create a clean upstream workspace

Do not create the upstream PR from a heavily modified instance working tree.

Preferred pattern:

1. Leave the instance clone untouched as the reference source.
2. Create a separate clean clone/worktree from the current upstream default branch.
3. Create a dedicated feature branch there.
4. Port only the approved reusable changes.

This prevents old instance commits, project data, generated evidence, and unrelated local modifications from leaking into the PR.

## Stage 4 — generalize methods, not names

Renaming a domain term does not automatically create a reusable abstraction.

Before promoting code, ask:

- Which inputs/paths/ports/workflows are truly invariant?
- Which values must become configuration?
- What behavior has actually been proven in more than one context?
- Is the reusable value currently a design rule/document rather than a stable code abstraction?

If only the principle is proven, upstream the principle and keep the reference implementation in the instance until another project validates the abstraction.

## Never upstream by default

- real/private input data;
- generated runtime data;
- credentials or local environment values;
- `updates/applied/` history;
- screenshots/logs/reports produced as acceptance evidence;
- project-specific `CHANGELOG.md` history;
- domain-specific contracts, metrics, UI, ETL, fixtures, or phase history;
- build caches and compiler state.

Directory shape or a synthetic example may still belong in the template when it teaches the contract without carrying instance state.

## Stage 5 — verify the clean PR branch

Before staging:

```text
git status --short
git diff --check
python -m py_compile scripts/scan_repo_for_remote_review.py scripts/scan_public_candidates.py scripts/check_environment.py
python scripts/build_context_bundle.py
python scripts/scan_repo_for_remote_review.py
```

Generated reports and `LLM_CONTEXT_BUNDLE.md` should remain ignored.

Then inspect the diff and stage **explicit paths** rather than using `git add .` for an upstream-extraction PR.

## Re-run the extraction workflow when

- a reference project closes;
- a new project proves a previously tentative abstraction;
- enterprise/environment friction reveals a reusable guardrail;
- a canonical template rule was changed inside an instance by explicit confirmation;
- the public template is about to be used as the starting point for another project.
