# Updates

This folder is how changes from an LLM chatbot get onto your machine — without you having to find and overwrite files by hand, and without silently rewriting this template's own contract files (see [`docs/TEMPLATE_BOUNDARY.md`](../docs/TEMPLATE_BOUNDARY.md)).

## 1. Get an update package from your chatbot

Ask your chatbot to export the files it changed as a **zip file**, named:

```
update_YYYYMMDD_HHMMSS.zip
```

using the date and time right now — for example `update_20260811_153000.zip`. If your chatbot can't name the file itself, download it however it gives it to you, then rename it yourself before the next step. The timestamp is how the script tells which package is the newest one if more than one is sitting in this folder.

If your chatbot can also include a `manifest.json` file at the root of the zip, ask it to — this gives you a one-line reason for every changed file in `CHANGELOG.md` instead of a generic note. Format:

```json
{
  "version": 1,
  "summary": "Optional one-line description of this update",
  "changes": [
    { "path": "web/src/components/Dashboard.tsx", "type": "modified", "reason": "Added the missing empty-state message" },
    { "path": "web/src/components/NewWidget.tsx", "type": "added", "reason": "New widget for the summary page" },
    { "path": "web/src/components/OldWidget.tsx", "type": "removed", "reason": "Replaced by NewWidget.tsx" }
  ]
}
```

No `manifest.json`? That's fine — the script compares the package to your current files itself and figures out what's new or changed. It just won't know *why*, and it will never delete a file on its own without a manifest telling it to.

## 2. Drop the package into this folder

Put the zip file (or, if you already unzipped it, the folder) directly inside `updates/incoming/`. Don't rename it further — leave the timestamp as-is.

## 3. Run the script

### macOS (Terminal)

1. Open **Terminal** (Spotlight → type "Terminal" → Enter).
2. Get into your project folder: type `cd ` (with a trailing space), then drag the project folder from Finder into the Terminal window — it fills in the path for you — then press Enter.
3. Check Python is available:
   ```bash
   python3 --version
   ```
   If that fails, install Python from [python.org](https://www.python.org/downloads/) first.
4. Preview what would happen, with no changes made yet:
   ```bash
   python3 scripts/apply_update.py --dry-run
   ```
5. If the plan looks right, run it for real:
   ```bash
   python3 scripts/apply_update.py
   ```

### Windows (PowerShell)

1. Open your project folder in **File Explorer**.
2. Click the address bar, type `powershell`, and press Enter — this opens PowerShell already inside the project folder. (Alternative: Shift + right-click inside the folder → "Open PowerShell window here".)
3. Check Python is available:
   ```powershell
   python --version
   ```
   If that fails, try `py --version` instead, or install Python from [python.org](https://www.python.org/downloads/) (tick "Add python.exe to PATH" during install).
4. Preview what would happen, with no changes made yet:
   ```powershell
   python scripts/apply_update.py --dry-run
   ```
5. If the plan looks right, run it for real:
   ```powershell
   python scripts/apply_update.py
   ```

## 4. Answer the prompts

Most files apply automatically. Two kinds always stop and ask first:

- **Canonical files** — the template's own contract files (per `docs/TEMPLATE_BOUNDARY.md`), so a routine update can never silently rewrite them.
- **Any deletion** — so nothing disappears without you seeing it first.

You'll see something like:

```
[CANONICAL] docs/FILE_MANIFEST.md (modified)
Reason: Added a row for the new component
--- current
+++ incoming
... diff ...
Apply this change? [y/N/d]
```

Type `y` to apply it, `N` (or just press Enter) to skip it, or `d` to see the full diff before deciding.

## 5. Tell the chatbot what actually happened

If you're going to ask the chatbot for another change in the same conversation, don't skip this step. The chatbot only knows what it *proposed* — not whether you actually approved every part of it. If you declined anything, the chatbot's idea of your project is now wrong unless you correct it.

At the end of the run, the script prints a short block starting with "Paste this back into the chatbot so it knows what actually happened." Copy that block and paste it as your next message. It's short on purpose: things that went exactly as the chatbot expected are just counted, not repeated — only the parts that *didn't* go as expected (declined or failed changes) are spelled out, since those are the only ones that would otherwise mislead it.

You'll also find this same text saved as `sync_note.md` next to the archived package under `updates/applied/`, in case you close the terminal before copying it.

## 6. What happens next

- Every run adds a new dated entry to `CHANGELOG.md` at the project root, listing what was applied, deleted, or declined and why — this is what an engineering team can later use to reconstruct the project's history if it's ever handed off (see `docs/UPGRADE_PATH.md`).
- The package you dropped in gets moved into `updates/applied/<timestamp>-<slug>/` (not deleted), alongside a machine-readable `apply_log.json` and the `sync_note.md` mentioned above — so you always have a copy to go back to.
- If you declined a canonical-file change but you think the template really should adopt it, log it in `docs/TEMPLATE_BOUNDARY.md`'s proposal table.

## If something looks wrong

- **"unrecognized file"** — something in `updates/incoming/` isn't named `update_YYYYMMDD_HHMMSS.zip`. Rename it or remove it.
- **"older pending package, not applied"** — you have more than one update package waiting; only the newest (by its timestamp) gets applied. Review and remove the older one(s) once you're done with them.
- **"No update package found"** — nothing's waiting in `updates/incoming/`; nothing to do.
