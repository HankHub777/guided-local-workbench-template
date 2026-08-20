#!/usr/bin/env python3
"""Apply an LLM-provided update package to this project.

Usage (see updates/README.md for the full non-technical guide):
    python scripts/apply_update.py [--source DIR] [--dry-run]

Stdlib only — no install step required.
"""

from __future__ import annotations

import argparse
import difflib
import filecmp
import json
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Keep in sync with docs/TEMPLATE_BOUNDARY.md's "Canonical files" list.
CANONICAL_PATHS = {
    "README.md",
    "README.zh-TW.md",
    "AGENTS.md",
    "ai/ARCHITECTURE_RULES.md",
    "ai/DESIGN_RULES.md",
    "docs/FILE_MANIFEST.md",
    "docs/UPGRADE_PATH.md",
    "docs/TEMPLATE_BOUNDARY.md",
    "docs/MIGRATION_FROM_SINGLE_FILE.md",
    "docs/MIGRATION_FROM_SINGLE_FILE.zh-TW.md",
    "docs/UPSTREAM_EXTRACTION.md",
    "docs/ENTERPRISE_ENVIRONMENT.md",
    "docs/WEB_DATA_APP_DESIGN_PLAYBOOK.md",
    ".gitignore",
    ".gitattributes",
    "LICENSE",
    "scripts/README.md",
    "scripts/apply_update.py",
    "scripts/build_context_bundle.py",
    "scripts/check_environment.py",
    "scripts/scan_repo_for_remote_review.py",
    "scripts/scan_public_candidates.py",
    "updates/README.md",
}

# Never overwritten by an incoming package; only this script's own append step touches it.
NEVER_TOUCH = {"CHANGELOG.md"}

PACKAGE_NAME_RE = re.compile(r"^update_(\d{8})_(\d{6})(\.zip)?$", re.IGNORECASE)
IGNORED_ENTRY_NAMES = {".gitkeep", "readme.md", ".ds_store"}
JUNK_NAMES = {"__macosx", ".ds_store", "thumbs.db"}


@dataclass
class Change:
    path: str  # project-root-relative, forward slashes
    type: str  # "added" | "modified" | "removed"
    reason: str
    source_file: Path | None  # None for "removed"


@dataclass
class Outcome:
    change: Change
    status: str
    detail: str = ""


def is_canonical(rel_path: str) -> bool:
    return rel_path in CANONICAL_PATHS


def normalize_rel_path(raw: str) -> str:
    """Normalize a manifest/package-relative path to project-root-relative posix form.

    Raises ValueError if the path escapes the project root.
    """
    posix = raw.replace("\\", "/").strip("/")
    candidate = (PROJECT_ROOT / posix).resolve()
    try:
        candidate.relative_to(PROJECT_ROOT)
    except ValueError:
        raise ValueError(f"path escapes project root: {raw!r}")
    return posix


def find_candidate_packages(source_dir: Path) -> tuple[list[tuple[Path, datetime]], list[Path]]:
    matched: list[tuple[Path, datetime]] = []
    unrecognized: list[Path] = []
    if not source_dir.exists():
        return matched, unrecognized
    for entry in sorted(source_dir.iterdir()):
        if entry.name.lower() in IGNORED_ENTRY_NAMES:
            continue
        m = PACKAGE_NAME_RE.match(entry.name)
        if not m:
            unrecognized.append(entry)
            continue
        try:
            ts = datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
        except ValueError:
            unrecognized.append(entry)
            continue
        matched.append((entry, ts))
    return matched, unrecognized


def safe_extract_zip(zip_path: Path, dest_dir: Path) -> None:
    resolved_dest = dest_dir.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.infolist():
            member_path = (dest_dir / member.filename).resolve()
            if resolved_dest not in member_path.parents and member_path != resolved_dest:
                raise ValueError(f"unsafe path in zip, refusing package: {member.filename!r}")
        zf.extractall(dest_dir)


def find_effective_root(extracted_dir: Path) -> Path:
    """If the package is wrapped in a single top-level folder, descend into it."""
    if (extracted_dir / "manifest.json").exists():
        return extracted_dir
    entries = [e for e in extracted_dir.iterdir() if e.name.lower() not in JUNK_NAMES]
    if len(entries) == 1 and entries[0].is_dir():
        return entries[0]
    return extracted_dir


def load_manifest(pkg_root: Path) -> dict | None:
    manifest_path = pkg_root / "manifest.json"
    if not manifest_path.exists():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"warning: manifest.json present but unreadable ({exc}); falling back to raw diff")
        return None
    if not isinstance(data, dict) or not isinstance(data.get("changes"), list):
        print("warning: manifest.json missing a valid 'changes' list; falling back to raw diff")
        return None
    return data


def is_binary(data: bytes) -> bool:
    return b"\x00" in data[:8192]


def read_bytes_or_none(path: Path) -> bytes | None:
    return path.read_bytes() if path.is_file() else None


def build_changes_from_manifest(manifest: dict, pkg_root: Path) -> list[Change]:
    changes: list[Change] = []
    for raw in manifest.get("changes", []):
        raw_path = raw.get("path") if isinstance(raw, dict) else None
        change_type = raw.get("type") if isinstance(raw, dict) else None
        reason = (raw.get("reason") if isinstance(raw, dict) else None) or "(no reason provided)"
        if not raw_path or change_type not in {"added", "modified", "removed"}:
            print(f"warning: skipping malformed manifest entry: {raw!r}")
            continue
        try:
            rel_path = normalize_rel_path(raw_path)
        except ValueError as exc:
            print(f"warning: skipping manifest entry ({exc})")
            continue
        if rel_path in NEVER_TOUCH:
            print(f"warning: manifest lists {rel_path!r}; this file is managed only by this script, skipping")
            continue
        if change_type == "removed":
            changes.append(Change(rel_path, "removed", reason, None))
            continue
        source_file = pkg_root / rel_path
        if not source_file.is_file():
            print(f"warning: manifest lists {rel_path!r} as {change_type} but it isn't in the package; skipping")
            continue
        live_path = PROJECT_ROOT / rel_path
        if live_path.is_file() and live_path.read_bytes() == source_file.read_bytes():
            continue  # no-op
        changes.append(Change(rel_path, change_type, reason, source_file))
    return changes


def build_changes_from_diff(pkg_root: Path) -> list[Change]:
    changes: list[Change] = []
    for source_file in sorted(pkg_root.rglob("*")):
        if source_file.is_dir():
            continue
        if source_file.name == "manifest.json" and source_file.parent == pkg_root:
            continue
        rel_parts = source_file.relative_to(pkg_root).parts
        if any(part.lower() in JUNK_NAMES for part in rel_parts):
            continue
        rel_path = source_file.relative_to(pkg_root).as_posix()
        if rel_path in NEVER_TOUCH:
            continue
        live_path = PROJECT_ROOT / rel_path
        if live_path.is_file() and filecmp.cmp(live_path, source_file, shallow=False):
            continue  # no-op
        change_type = "modified" if live_path.exists() else "added"
        changes.append(
            Change(rel_path, change_type, "(no reason provided — no manifest.json in package)", source_file)
        )
    return changes


def diff_preview(live_path: Path, source_file: Path | None, cap: int | None) -> str:
    old_bytes = read_bytes_or_none(live_path)
    new_bytes = source_file.read_bytes() if source_file else None
    if (old_bytes and is_binary(old_bytes)) or (new_bytes and is_binary(new_bytes)):
        old_size = len(old_bytes) if old_bytes else 0
        new_size = len(new_bytes) if new_bytes else 0
        return f"binary file, cannot preview: {old_size} bytes -> {new_size} bytes"
    old_lines = old_bytes.decode("utf-8", errors="replace").splitlines(keepends=True) if old_bytes else []
    new_lines = new_bytes.decode("utf-8", errors="replace").splitlines(keepends=True) if new_bytes else []
    diff_lines = list(difflib.unified_diff(old_lines, new_lines, fromfile="current", tofile="incoming"))
    if not diff_lines:
        return "(no textual difference)"
    if cap is not None and len(diff_lines) > cap:
        remaining = len(diff_lines) - cap
        return "".join(diff_lines[:cap]) + f"... (truncated, {remaining} more lines — press d for full diff)\n"
    return "".join(diff_lines)


def confirm(change: Change, live_path: Path) -> bool:
    label = "CANONICAL" if is_canonical(change.path) else "INSTANCE"
    if change.type == "removed":
        print(f"\n[{label}] {change.path} (removed)")
        print(f"Reason: {change.reason}")
        try:
            answer = input(f"Delete local file {change.path}? This was marked removed in the update. [y/N] ")
        except EOFError:
            print("warning: no interactive input available; declining. Re-run in a terminal to confirm.")
            return False
        return answer.strip().lower() == "y"

    cap: int | None = 60
    while True:
        print(f"\n[{label}] {change.path} ({change.type})")
        print(f"Reason: {change.reason}")
        print(diff_preview(live_path, change.source_file, cap))
        try:
            answer = input("Apply this change? [y/N/d] ").strip().lower()
        except EOFError:
            print("warning: no interactive input available; declining. Re-run in a terminal to confirm.")
            return False
        if answer == "d" and cap is not None:
            cap = None
            continue
        return answer == "y"


def apply_change(change: Change, dry_run: bool) -> Outcome:
    live_path = PROJECT_ROOT / change.path
    canonical = is_canonical(change.path)
    needs_confirm = canonical or change.type == "removed"

    if needs_confirm:
        if dry_run:
            action = "delete" if change.type == "removed" else "apply"
            return Outcome(change, f"would-{action}-confirmed")
        if not confirm(change, live_path):
            note = (
                "Consider logging in docs/TEMPLATE_BOUNDARY.md's proposal table if this is a genuine "
                "template-level need."
                if canonical
                else ""
            )
            return Outcome(change, "declined", note)

    # From here: either a non-canonical add/modify, or a needs-confirm change the user approved.
    if change.type == "removed":
        try:
            if live_path.is_file():
                live_path.unlink()
            return Outcome(change, "deleted")
        except OSError as exc:
            return Outcome(change, "skipped-error", str(exc))

    if dry_run:
        return Outcome(change, "would-apply")

    try:
        live_path.parent.mkdir(parents=True, exist_ok=True)
        assert change.source_file is not None
        shutil.copy2(change.source_file, live_path)
        return Outcome(change, "applied")
    except OSError as exc:
        return Outcome(change, "skipped-error", str(exc))


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug[:40] or "update"


def archive_package(selected_path: Path, slug: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = PROJECT_ROOT / "updates" / "applied" / f"{timestamp}-{slug}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / selected_path.name
    shutil.move(str(selected_path), str(dest))
    return archive_dir


def write_apply_log(archive_dir: Path, outcomes: list[Outcome], mode: str, source_name: str) -> None:
    record = {
        "source": source_name,
        "mode": mode,
        "applied_at": datetime.now().isoformat(timespec="seconds"),
        "changes": [
            {
                "path": o.change.path,
                "type": o.change.type,
                "reason": o.change.reason,
                "canonical": is_canonical(o.change.path),
                "status": o.status,
                "detail": o.detail,
            }
            for o in outcomes
        ],
    }
    (archive_dir / "apply_log.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_changelog(outcomes: list[Outcome], summary: str, source_name: str, mode: str, archive_dir: Path) -> None:
    reportable = [o for o in outcomes if o.status in {"applied", "deleted", "declined", "skipped-error"}]
    if not reportable:
        return

    changelog_path = PROJECT_ROOT / "CHANGELOG.md"
    existing = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else "# Changelog\n"
    if existing.startswith("# Changelog"):
        header_line, _, rest = existing.partition("\n")
        rest = rest.lstrip("\n")
    else:
        header_line, rest = "# Changelog", existing

    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [f"## {date_str}: {summary}", ""]
    for outcome in reportable:
        change = outcome.change
        if outcome.status == "applied":
            lines.append(f"- **Applied** `{change.path}` ({change.type}) — {change.reason}")
        elif outcome.status == "deleted":
            lines.append(f"- **Deleted** `{change.path}` — {change.reason}")
        elif outcome.status == "declined":
            tag = "canonical" if is_canonical(change.path) else "instance"
            suffix = f" {outcome.detail}" if outcome.detail else ""
            lines.append(f"- **Declined** `{change.path}` ({change.type}, {tag}) — {change.reason}.{suffix}")
        elif outcome.status == "skipped-error":
            lines.append(f"- **Error** `{change.path}` ({change.type}) — {outcome.detail}")
    lines.append("")
    lines.append(
        f"Source: `{source_name}` ({mode}). Archived to `{archive_dir.relative_to(PROJECT_ROOT).as_posix()}/`."
    )
    lines.append("")
    new_section = "\n".join(lines) + "\n"

    new_content = header_line + "\n\n" + new_section + ("\n" + rest if rest else "")
    tmp_path = changelog_path.with_suffix(".md.tmp")
    tmp_path.write_text(new_content, encoding="utf-8")
    tmp_path.replace(changelog_path)


def build_sync_note(outcomes: list[Outcome]) -> str:
    """A short, copy-paste-back-to-the-chatbot summary of this run.

    Deliberately asymmetric: changes that landed exactly as proposed get one
    line total (the chatbot already assumes those happened — repeating them
    file-by-file adds no new information). Anything that differs from what
    the chatbot proposed — declined or failed changes — gets full detail,
    because that's the part the chatbot doesn't already know and will act on
    incorrectly if it isn't told.
    """
    as_proposed = [o for o in outcomes if o.status in {"applied", "deleted"}]
    declined = [o for o in outcomes if o.status == "declined"]
    errors = [o for o in outcomes if o.status == "skipped-error"]

    lines = ["Paste this back into the chatbot so it knows what actually happened:", ""]
    if as_proposed:
        lines.append(f"- {len(as_proposed)} change(s) were applied exactly as proposed.")
    else:
        lines.append("- Nothing was applied as proposed.")

    if declined:
        lines.append("")
        lines.append(f"- {len(declined)} change(s) were NOT applied — do not assume these took effect:")
        for outcome in declined:
            change = outcome.change
            tag = "template contract file" if is_canonical(change.path) else "deletion"
            lines.append(f"  - `{change.path}` ({change.type}, {tag}) — user declined this one.")

    if errors:
        lines.append("")
        lines.append(f"- {len(errors)} change(s) failed to apply:")
        for outcome in errors:
            lines.append(f"  - `{outcome.change.path}` — {outcome.detail}")

    if not declined and not errors:
        lines.append("- Nothing else to report; the plan went through unchanged.")

    return "\n".join(lines) + "\n"


def check_boundary_drift() -> None:
    boundary_path = PROJECT_ROOT / "docs" / "TEMPLATE_BOUNDARY.md"
    if not boundary_path.exists():
        return
    text = boundary_path.read_text(encoding="utf-8")
    match = re.search(r"## Canonical files.*?\n(.*?)\n## ", text, re.DOTALL)
    if not match:
        return
    doc_paths = set(re.findall(r"^- `([^`]+)`", match.group(1), re.MULTILINE))
    if not doc_paths:
        return
    if doc_paths != CANONICAL_PATHS:
        missing_in_script = doc_paths - CANONICAL_PATHS
        missing_in_doc = CANONICAL_PATHS - doc_paths
        print("warning: scripts/apply_update.py's CANONICAL_PATHS looks out of sync with docs/TEMPLATE_BOUNDARY.md:")
        if missing_in_script:
            print(f"  in doc but not script: {sorted(missing_in_script)}")
        if missing_in_doc:
            print(f"  in script but not doc: {sorted(missing_in_doc)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply an LLM-provided update package. See updates/README.md.")
    parser.add_argument("--source", type=Path, default=PROJECT_ROOT / "updates" / "incoming")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without changing anything.")
    args = parser.parse_args(argv)

    check_boundary_drift()

    matched, unrecognized = find_candidate_packages(args.source)
    for entry in unrecognized:
        print(
            f"warning: unrecognized file in {args.source}: {entry.name} "
            "(expected update_YYYYMMDD_HHMMSS.zip) — rename or remove it"
        )

    if not matched:
        print("No update package found.")
        return 0

    matched.sort(key=lambda item: item[1])
    selected_path, _ = matched[-1]
    for older_path, _ in matched[:-1]:
        print(
            f"note: {older_path.name} is an older pending package, not applied — "
            "review or delete it from updates/incoming/"
        )

    print(f"Selected package: {selected_path.name}")

    with tempfile.TemporaryDirectory(prefix="apply_update_") as work_dir_str:
        work_dir = Path(work_dir_str)
        if selected_path.is_file():
            try:
                safe_extract_zip(selected_path, work_dir)
            except (zipfile.BadZipFile, ValueError) as exc:
                print(f"error: could not read {selected_path.name}: {exc}")
                return 1
            pkg_root = find_effective_root(work_dir)
        else:
            pkg_root = find_effective_root(selected_path)

        manifest = load_manifest(pkg_root)
        if manifest is not None:
            changes = build_changes_from_manifest(manifest, pkg_root)
            mode = "manifest"
            summary = manifest.get("summary") or f"Local update ({len(changes)} file(s))"
        else:
            changes = build_changes_from_diff(pkg_root)
            mode = "raw diff (no manifest.json)"
            summary = f"Local update ({len(changes)} file(s))"

        if not changes:
            print("No differences found between the package and the current project.")
            if not args.dry_run:
                archive_dir = archive_package(selected_path, slugify(summary))
                print(f"Archived (no changes) to {archive_dir.relative_to(PROJECT_ROOT)}")
            return 0

        outcomes = [apply_change(change, args.dry_run) for change in changes]
        had_error = any(o.status == "skipped-error" for o in outcomes)

        if args.dry_run:
            print("\n--dry-run: plan only, nothing written.\n")
            for o in outcomes:
                print(f"  [{o.status}] {o.change.path} ({o.change.type}) — {o.change.reason}")
            return 2 if had_error else 0

        archive_dir = archive_package(selected_path, slugify(summary))
        write_apply_log(archive_dir, outcomes, mode, selected_path.name)
        write_changelog(outcomes, summary, selected_path.name, mode, archive_dir)

        sync_note = build_sync_note(outcomes)
        (archive_dir / "sync_note.md").write_text(sync_note, encoding="utf-8")

        applied = sum(1 for o in outcomes if o.status in {"applied", "deleted"})
        declined = sum(1 for o in outcomes if o.status == "declined")
        print(
            f"\nDone: {applied} applied, {declined} declined. "
            f"See CHANGELOG.md and {archive_dir.relative_to(PROJECT_ROOT)}."
        )
        print(f"\n----- {archive_dir.relative_to(PROJECT_ROOT) / 'sync_note.md'} -----")
        print(sync_note, end="")
        print("-----")
        return 2 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
