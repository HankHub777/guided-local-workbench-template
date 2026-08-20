#!/usr/bin/env python3
"""Read-only inventory for deciding what belongs in a reusable public remote repo.

Run from anywhere inside the Git repository:

    python scripts/scan_repo_for_remote_review.py

Outputs:
    artifacts/remote_repo_review/repo_remote_review.md
    artifacts/remote_repo_review/repo_remote_review.json

The script NEVER modifies Git state, stages files, deletes files, resets files, or
edits ignore rules. It inventories repository structure and Git metadata so a
human/LLM can decide what is reusable template material versus instance state/data.

The report can contain local filenames and paths. Review it before sharing outside
an approved environment. Embedded credentials in URL-form Git remotes are redacted.
"""

from __future__ import annotations

import json
import os
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

OUTPUT_DIR_REL = Path("artifacts") / "remote_repo_review"
HEAVY_DIR_NAMES = {
    ".git", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".venv", "venv",
}
REVIEW_HINT_PREFIXES = (
    "data/", "updates/applied/", "updates/incoming/", "artifacts/",
    "logs/", "run/", "runtime/", "tmp/", "temp/",
)
REVIEW_HINT_NAMES = {
    ".env", ".env.local", ".env.production", "secrets.json", "credentials.json",
    ".npmrc", ".pypirc", "pip.ini", ".netrc", "id_rsa", "id_ed25519",
}


def run_git(root: Path, args: list[str], *, check: bool = True) -> bytes:
    proc = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def git_text(root: Path, args: list[str], *, check: bool = True) -> str:
    return run_git(root, args, check=check).decode("utf-8", errors="replace").strip()


def git_zlist(root: Path, args: list[str]) -> list[str]:
    raw = run_git(root, args)
    return [
        item.decode("utf-8", errors="replace").replace("\\", "/")
        for item in raw.split(b"\0")
        if item
    ]


def find_repo_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit("[blocked] Run this script inside a Git repository.")
    return Path(proc.stdout.decode("utf-8", errors="replace").strip()).resolve()


def sanitize_remote_url(url: str) -> str:
    if "://" not in url:
        return url
    parts = urlsplit(url)
    host = parts.hostname or ""
    if parts.port:
        host = f"{host}:{parts.port}"
    return urlunsplit((parts.scheme, host, parts.path, parts.query, parts.fragment))


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def human_bytes(value: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{int(size)} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def top_component(rel: str) -> str:
    return rel.split("/", 1)[0] if "/" in rel else "(root)"


def review_hints(path: str) -> list[str]:
    low = path.lower()
    hints: list[str] = []
    if any(low.startswith(prefix.lower()) for prefix in REVIEW_HINT_PREFIXES):
        hints.append("instance/state/data-like path - review before publishing")
    if Path(low).name in REVIEW_HINT_NAMES:
        hints.append("environment/credential-like filename - review before publishing")
    if low.endswith((".xlsx", ".xls", ".csv", ".sqlite", ".db", ".parquet")):
        hints.append("data/database file type - review before publishing")
    if low.endswith((".log", ".png", ".jpg", ".jpeg", ".webp")):
        hints.append("runtime/evidence/media artifact - confirm whether reusable")
    return hints


def load_text_if_present(root: Path, rel: str) -> str | None:
    path = root / rel
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def build_tree(root: Path, max_depth: int = 4) -> list[str]:
    lines: list[str] = [f"{root.name}/"]

    def walk(directory: Path, prefix: str, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(
                [p for p in directory.iterdir() if p.name != ".git"],
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )
        except OSError:
            return

        for idx, entry in enumerate(entries):
            last = idx == len(entries) - 1
            branch = "└── " if last else "├── "
            if entry.is_dir():
                if entry.name in HEAVY_DIR_NAMES:
                    count = 0
                    total = 0
                    try:
                        for dirpath, _, filenames in os.walk(entry):
                            for name in filenames:
                                count += 1
                                total += file_size(Path(dirpath) / name)
                    except OSError:
                        pass
                    lines.append(
                        f"{prefix}{branch}{entry.name}/ "
                        f"[collapsed: {count} files, {human_bytes(total)}]"
                    )
                else:
                    lines.append(f"{prefix}{branch}{entry.name}/")
                    if depth < max_depth:
                        walk(entry, prefix + ("    " if last else "│   "), depth + 1)
                    else:
                        lines.append(f"{prefix}{'    ' if last else '│   '}└── … [depth limit]")
            else:
                lines.append(f"{prefix}{branch}{entry.name} [{human_bytes(file_size(entry))}]")

    walk(root, "", 1)
    return lines


def main() -> int:
    root = find_repo_root()
    output_dir = root / OUTPUT_DIR_REL
    output_dir.mkdir(parents=True, exist_ok=True)

    branch = git_text(root, ["branch", "--show-current"], check=False) or "(detached HEAD)"
    head = git_text(root, ["rev-parse", "--short", "HEAD"], check=False) or "(unknown)"

    remotes_raw = git_text(root, ["remote", "-v"], check=False)
    remotes: list[str] = []
    for line in remotes_raw.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            remotes.append(f"{parts[0]} {sanitize_remote_url(parts[1])} {parts[2]}")
        elif line.strip():
            remotes.append(line.strip())

    tracked = sorted(git_zlist(root, ["ls-files", "-z"]))
    untracked = sorted(git_zlist(root, ["ls-files", "--others", "--exclude-standard", "-z"]))
    ignored = sorted(git_zlist(root, ["ls-files", "--others", "--ignored", "--exclude-standard", "-z"]))
    status = git_text(root, ["status", "--short", "--untracked-files=all"], check=False)

    tracked_set = set(tracked)
    inventory = []
    for rel in sorted(tracked_set | set(untracked)):
        path = root / rel
        inventory.append({
            "path": rel,
            "git_state": "tracked" if rel in tracked_set else "untracked",
            "size_bytes": file_size(path),
            "review_hints": review_hints(rel),
        })

    ignored_summary = defaultdict(lambda: {"files": 0, "bytes": 0})
    for rel in ignored:
        top = top_component(rel)
        ignored_summary[top]["files"] += 1
        ignored_summary[top]["bytes"] += file_size(root / rel)

    tracked_by_top = Counter(top_component(p) for p in tracked)
    untracked_by_top = Counter(top_component(p) for p in untracked)
    flagged = [item for item in inventory if item["review_hints"]]
    gitignore = load_text_if_present(root, ".gitignore")
    gitattributes = load_text_if_present(root, ".gitattributes")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(root),
        "branch": branch,
        "head": head,
        "remotes_sanitized": remotes,
        "counts": {
            "tracked": len(tracked),
            "untracked": len(untracked),
            "ignored": len(ignored),
            "flagged_for_review": len(flagged),
        },
        "git_status_short": status.splitlines() if status else [],
        "tracked_by_top_level": dict(sorted(tracked_by_top.items())),
        "untracked_by_top_level": dict(sorted(untracked_by_top.items())),
        "ignored_by_top_level": {
            key: {"files": value["files"], "bytes": value["bytes"], "human_size": human_bytes(value["bytes"])}
            for key, value in sorted(ignored_summary.items())
        },
        "inventory_tracked_and_untracked": inventory,
        "review_flagged_items": flagged,
        "gitignore": gitignore,
        "gitattributes": gitattributes,
        "tree_max_depth_4": build_tree(root, max_depth=4),
    }

    json_path = output_dir / "repo_remote_review.json"
    md_path = output_dir / "repo_remote_review.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md: list[str] = [
        "# Remote Public Repo Review Inventory", "",
        "> Read-only inventory. No publish/delete decision is made by this report.", "",
        "> Review this report before sharing it outside the approved environment; local filenames and paths may be present.", "",
        "## Repository", "", f"- Root: `{root}`", f"- Branch: `{branch}`", f"- HEAD: `{head}`",
    ]
    if remotes:
        md.append("- Remotes (credentials redacted if embedded):")
        md.extend(f"  - `{item}`" for item in remotes)

    md += ["", "## Git state", "", f"- Tracked files: **{len(tracked)}**", f"- Untracked, not ignored: **{len(untracked)}**", f"- Ignored files: **{len(ignored)}**", f"- Review-flagged tracked/untracked items: **{len(flagged)}**", "", "### `git status --short`", "", "```text"]
    md.extend(status.splitlines() if status else ["(clean)"])
    md += ["```", "", "## Top-level Git inventory", "", "| Top level | Tracked | Untracked |", "|---|---:|---:|"]
    for key in sorted(set(tracked_by_top) | set(untracked_by_top)):
        md.append(f"| `{key}` | {tracked_by_top[key]} | {untracked_by_top[key]} |")

    md += ["", "## Ignored-content summary", "", "> Ignored files are summarized rather than dumped individually (e.g. node_modules).", "", "| Top level | Files | Approx size |", "|---|---:|---:|"]
    if ignored_summary:
        for key, value in sorted(ignored_summary.items()):
            md.append(f"| `{key}` | {value['files']} | {human_bytes(value['bytes'])} |")
    else:
        md.append("| _(none)_ | 0 | 0 B |")

    md += ["", "## Items flagged for human review", "", "> Flags are prompts only. They do not mean the file must be removed or kept.", ""]
    if flagged:
        for item in flagged:
            md.append(f"- `{item['path']}` — {item['git_state']}, {human_bytes(item['size_bytes'])} — {'; '.join(item['review_hints'])}")
    else:
        md.append("(none)")

    md += ["", "## Full tracked + untracked inventory", "", "| State | Size | Path |", "|---|---:|---|"]
    for item in inventory:
        md.append(f"| {item['git_state']} | {human_bytes(item['size_bytes'])} | `{item['path']}` |")

    md += ["", "## Repository tree (depth <= 4)", "", "```text"]
    md.extend(report["tree_max_depth_4"])
    md += ["```", "", "## `.gitignore`", "", "```gitignore", gitignore.rstrip() if gitignore is not None else "(missing)", "```", "", "## `.gitattributes`", "", "```text", gitattributes.rstrip() if gitattributes is not None else "(missing)", "```", "", "## Next review questions", "", "Use this inventory to decide, path by path:", "", "1. Is this reusable method/template infrastructure, or this project instance?", "2. Is the file source code/documentation, or generated/runtime/evidence state?", "3. Does the public template need the directory shape but not its current contents?", "4. Does any file contain business data, credentials, internal paths, host/network details, or project-specific evidence?", "5. If an instance file is currently tracked, should the public repo keep only a sample/example/placeholder instead?", ""]

    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("[done] Remote-repo inventory created.")
    print(f"[md]   {md_path}")
    print(f"[json] {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
