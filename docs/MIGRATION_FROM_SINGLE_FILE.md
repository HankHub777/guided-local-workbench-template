# Migrating a single-file HTML prototype into this template

You already have real work built up in a chatbot conversation as one big HTML file — inline CSS, inline JavaScript, data hardcoded into the markup. You want to bring that into this template's structure without starting over.

This is a one-time on-ramp, not the ongoing workflow. Once migration is done, go back to the small-change loop in [README.md](../README.md)'s "Working with an LLM chatbot" section.

## Why this needs its own process

Splitting a monolith into `web/` components, `shared/` types, `data/`, and `config/` requires judgment about what each piece of content actually is — that's not something a fixed script can do reliably. But it's a good fit for a chatbot, guided by a documented procedure with a human checkpoint in the middle, so you're reviewing a proposal instead of doing the split yourself.

## Which prompt do I need?

| Your situation | Use |
| --- | --- |
| First migration, file is small/medium, you're fine reviewing one classification list for the whole thing | **Prompt 1 — Full Inventory** |
| File is large, complex, or you'd rather reduce risk by migrating one feature/page at a time | **Prompt 2 — Section-by-Section Inventory** |
| You have an approved classification (from Prompt 1 or 2) and are ready to actually produce files | **Prompt 3 — Split & Package** |
| You just applied a migration update and want to confirm nothing broke | **Prompt 4 — Parity Check** |

## The flow

1. Generate your context bundle as usual: `python3 scripts/build_context_bundle.py`.
2. Run **Prompt 1** or **Prompt 2** (pick from the table above) with your single-file HTML attached or pasted. The chatbot proposes a classification — it does not produce any files yet.
3. **You review the classification** — see the checklist below. This is the one step that needs your judgment, and it's a review, not a rewrite.
4. Run **Prompt 3** with the approved classification. The chatbot produces `update_YYYYMMDD_HHMMSS.zip` with a `manifest.json`, exactly like any other update package.
5. Apply it: `python3 scripts/apply_update.py --dry-run` first — always, for a migration-sized change — then run for real once the plan looks right. See [updates/README.md](../updates/README.md) if you need the terminal steps.
6. Run **Prompt 4** to get help confirming the new structure behaves the same as the original file, then manually click through the flows yourself before calling the migration done.

## Reviewing a classification (step 3): what to check

- **Any row marked `contains_real_data: yes` must target a path under `data/input/`.** Never let one land in `data/fixtures/`, `config/*.example.json`, or anywhere else that gets committed to Git. If the chatbot proposed a tracked location for real data, fix that in the table before moving on — don't let Prompt 3 run against it uncorrected.
- **No row should target a canonical path** (`README.md`, `AGENTS.md`, `docs/TEMPLATE_BOUNDARY.md`, and the rest of the list in [docs/TEMPLATE_BOUNDARY.md](TEMPLATE_BOUNDARY.md)). If your prototype genuinely needs to change one of those, that's a separate, deliberate template-level decision — not part of an ordinary migration.
- **Watch for the same logic repeated across multiple UI sections.** If business logic shows up as several separate classification rows because it's pasted into multiple places in the original file, ask the chatbot to consolidate it into one `shared/` location instead of migrating each copy separately.
- **If the table is long enough that you're skimming instead of reading, switch to Prompt 2** and migrate section by section instead of trying to review one giant table.

## Prompt 1 — Full Inventory

Copy this, attach or paste your single-file HTML and your `LLM_CONTEXT_BUNDLE.md`, and send it as-is.

```
I have an existing prototype built as a single HTML file (attached/pasted below).
I want to migrate it into a structured project, but do not produce any files yet —
this is a classification pass only.

Read the attached LLM_CONTEXT_BUNDLE.md first so you know the target project
structure and rules, especially which files are canonical — nothing should be
classified as going into a canonical file.

Go through the single-file HTML and classify every distinct piece of content into
a table with these columns:
- id: a short label for this piece (e.g. "header-nav", "sales-table-data")
- category: one of `ui-component`, `styling`, `business-logic`, `static-config`,
  `real-data`
- description: one sentence on what it is
- proposed_target: the file path in the template structure this should become
  (e.g. `web/src/components/Header.tsx`, `shared/types.ts`, `data/input/sales.csv`,
  `config/app.config.example.json`)
- contains_real_data: yes/no — mark "yes" for anything that looks like real
  business numbers, real customer or personal information, real names, real dates
  tied to actual events, or anything that isn't a placeholder/example value. If in
  doubt, say yes.

Output only this classification table. Do not write code or produce any files —
I need to review the table first.
```

## Prompt 2 — Section-by-Section Inventory

Same idea as Prompt 1, scoped to one part of the file at a time — use this when the file is too large to review in one pass.

```
I have an existing prototype built as a single HTML file. It's large enough that
I want to migrate it one feature/section at a time instead of all at once.

Read the attached LLM_CONTEXT_BUNDLE.md first so you know the target project
structure and rules.

For this pass, I'm only giving you this section: [describe it — e.g. "the
dashboard summary panel, roughly lines 120-340"]. Classify only this section
using the same table format as a full migration:
- id, category (ui-component / styling / business-logic / static-config /
  real-data), description, proposed_target, contains_real_data (yes/no)

Do not reference or assume anything about parts of the file I haven't given you
yet. Do not produce any files — classification table only.

I'll come back with the next section once this one is approved and migrated.
```

## Prompt 3 — Split & Package

Use this once a classification table (from Prompt 1 or Prompt 2) is approved.

```
Here is the classification table I've approved for this migration pass:

[paste the approved table here]

Produce the actual files for every row, following the target project structure
and rules in LLM_CONTEXT_BUNDLE.md:
- Package everything as a single zip named `update_YYYYMMDD_HHMMSS.zip`, using
  today's date and time.
- Include a `manifest.json` at the root of the zip listing every file with
  `path`, `type: "added"`, and a one-line `reason` that references the
  classification id it came from.
- Any row marked `contains_real_data: yes` must go under `data/input/` — never
  into a tracked path.
- Do not produce or modify anything at a canonical path (see
  docs/TEMPLATE_BOUNDARY.md in the bundle). If a row's proposed_target is
  canonical, stop and tell me instead of producing it.
- Keep each generated file focused — don't merge unrelated rows into one file.

Give me the zip to download.
```

## Prompt 4 — Parity Check

Use this after applying the migration update, to help confirm nothing was lost.

```
I've applied the migration update. Here's what actually happened:

[paste the sync note apply_update.py printed, or updates/applied/.../apply_log.json]

Here is the original single-file HTML for reference:

[paste or attach it]

Help me verify nothing was lost in the migration:
1. List every user-facing flow or interactive feature you can identify in the
   original file (e.g. "clicking X filters the table", "the form submits and
   shows Y").
2. For each one, tell me which new file(s) it should now live in, based on the
   classification.
3. Flag anything from the original file that doesn't appear anywhere in the new
   structure — that's a possible gap, not something to assume is fine.

I'll manually click through each flow in the new version myself before treating
the migration as done.
```

## After migration

- The original single-file HTML isn't deleted automatically. Decide whether to keep it as an archived reference or remove it once parity is confirmed — that's your call, not something this process does for you.
- From here on, use the normal small-change loop: one acceptance-testable request at a time, applied through the same `apply_update.py` flow, as described in [README.md](../README.md).
