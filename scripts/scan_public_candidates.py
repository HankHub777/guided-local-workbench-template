#!/usr/bin/env python3
"""Read-only second-stage audit for explicit upstream-candidate paths.

Examples:
    python scripts/scan_public_candidates.py docs/example.md scripts/example.py
    python scripts/scan_public_candidates.py --paths-file artifacts/remote_repo_review/candidates.txt

The script gathers current content plus Git diffs for tracked files. It does not
decide what should be published and never stages, resets, deletes, or edits files.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("artifacts") / "remote_repo_review"
DEFAULT_BOUNDARY_PATHS = [
    "data/input", "data/generated", "data/fixtures",
    "updates/applied", "updates/incoming", "artifacts",
    "web", "server", "shared", "tests",
]
MAX_TEXT_BYTES = 250_000
MAX_DIFF_BYTES = 300_000


def run_git(root: Path, args: list[str], check: bool = True) -> bytes:
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


def git_text(root: Path, args: list[str], check: bool = True) -> str:
    return run_git(root, args, check=check).decode("utf-8", errors="replace")


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


def normalize_rel(root: Path, raw: str) -> str:
    text = raw.strip().replace("\\", "/")
    if not text or text.startswith("#"):
        return ""
    path = (root / text).resolve()
    try:
        rel = path.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"[blocked] Candidate path escapes repository root: {raw!r}") from exc
    return rel.as_posix()


def load_candidate_paths(root: Path, direct: list[str], files: list[str]) -> list[str]:
    raw_items = list(direct)
    for item in files:
        source = Path(item)
        if not source.is_absolute():
            source = root / source
        if not source.is_file():
            raise SystemExit(f"[blocked] Candidate path file not found: {source}")
        raw_items.extend(source.read_text(encoding="utf-8").splitlines())

    result: list[str] = []
    seen: set[str] = set()
    for raw in raw_items:
        rel = normalize_rel(root, raw)
        if rel and rel not in seen:
            seen.add(rel)
            result.append(rel)
    if not result:
        raise SystemExit(
            "[blocked] No candidate paths supplied. Pass repository-relative paths directly "
            "or use --paths-file. The script intentionally does not guess what should be public."
        )
    return result


def tracked_set(root: Path) -> set[str]:
    raw = run_git(root, ["ls-files", "-z"])
    return {item.decode("utf-8", errors="replace").replace("\\", "/") for item in raw.split(b"\0") if item}


def ignored_status(root: Path, rel: str) -> bool:
    proc = subprocess.run(
        ["git", "check-ignore", "-q", "--", rel],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.returncode == 0


def read_text(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "kind": "missing", "bytes": 0, "text": None, "truncated": False}
    if path.is_dir():
        return {"exists": True, "kind": "directory", "bytes": 0, "text": None, "truncated": False}

    size = path.stat().st_size
    raw = path.read_bytes()
    truncated = len(raw) > MAX_TEXT_BYTES
    if truncated:
        raw = raw[:MAX_TEXT_BYTES]
    try:
        text = raw.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        encoding = "utf-8-with-replacement"
    return {"exists": True, "kind": "file", "bytes": size, "text": text, "encoding": encoding, "truncated": truncated}


def file_state(root: Path, rel: str, tracked: set[str]) -> str:
    if rel in tracked:
        return "tracked"
    path = root / rel
    if path.exists() and ignored_status(root, rel):
        return "ignored"
    if path.exists():
        return "untracked"
    return "missing"


def get_diff(root: Path, rel: str, tracked: set[str]) -> dict:
    if rel not in tracked:
        return {"available": False, "text": None, "truncated": False}
    raw = run_git(root, ["diff", "--", rel], check=False)
    truncated = len(raw) > MAX_DIFF_BYTES
    if truncated:
        raw = raw[:MAX_DIFF_BYTES]
    return {"available": True, "text": raw.decode("utf-8", errors="replace"), "truncated": truncated}


def list_boundary(root: Path, rel: str, tracked: set[str]) -> dict:
    path = root / rel
    if not path.exists():
        return {"path": rel, "exists": False, "tracked_count": 0, "untracked_count": 0, "ignored_count": 0, "sample_entries": []}
    files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
    counts = {"tracked": 0, "untracked": 0, "ignored": 0}
    samples: list[dict] = []
    for p in sorted(files):
        rp = p.relative_to(root).as_posix()
        state = file_state(root, rp, tracked)
        counts[state] = counts.get(state, 0) + 1
        if len(samples) < 30:
            samples.append({"path": rp, "state": state, "bytes": p.stat().st_size})
    return {"path": rel, "exists": True, "tracked_count": counts.get("tracked", 0), "untracked_count": counts.get("untracked", 0), "ignored_count": counts.get("ignored", 0), "sample_entries": samples}


def fence_for(rel: str) -> str:
    suffix = Path(rel).suffix.lower()
    return {".md": "markdown", ".py": "python", ".cmd": "bat", ".bat": "bat", ".json": "json", ".toml": "toml", ".yml": "yaml", ".yaml": "yaml", ".ts": "typescript", ".tsx": "tsx"}.get(suffix, "text")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Repository-relative candidate paths.")
    parser.add_argument("--paths-file", action="append", default=[], help="UTF-8 text file containing one candidate path per line; repeatable.")
    parser.add_argument("--boundary", action="append", default=[], help="Additional boundary path to summarize; repeatable.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Repository-relative output directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = find_repo_root()
    candidates = load_candidate_paths(root, args.paths, args.paths_file)
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    tracked = tracked_set(root)
    status = git_text(root, ["status", "--short", "--untracked-files=all"], check=False).strip()
    branch = git_text(root, ["branch", "--show-current"], check=False).strip() or "(detached HEAD)"
    head = git_text(root, ["rev-parse", "--short", "HEAD"], check=False).strip() or "(unknown)"

    candidate_records = [
        {"path": rel, "git_state": file_state(root, rel, tracked), "content": read_text(root / rel), "diff": get_diff(root, rel, tracked)}
        for rel in candidates
    ]
    boundaries = list(dict.fromkeys(DEFAULT_BOUNDARY_PATHS + args.boundary))
    boundary_records = [list_boundary(root, rel, tracked) for rel in boundaries]

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(root), "branch": branch, "head": head,
        "git_status_short": status.splitlines() if status else [],
        "candidate_paths": candidate_records,
        "boundary_paths": boundary_records,
    }

    json_path = output_dir / "public_candidate_review.json"
    md_path = output_dir / "public_candidate_review.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md: list[str] = [
        "# Public Candidate Content Review", "",
        "> Read-only second-stage audit. No keep/remove decision is made automatically.", "",
        "## Repository", "", f"- Root: `{root}`", f"- Branch: `{branch}`", f"- HEAD: `{head}`", "",
        "## Current Git status", "", "```text",
    ]
    md.extend(status.splitlines() if status else ["(clean)"])
    md += ["```", "", "## Boundary-path summary", "", "> These paths are not automatically public candidates.", "", "| Path | Exists | Tracked | Untracked | Ignored |", "|---|---:|---:|---:|---:|"]
    for item in boundary_records:
        md.append(f"| `{item['path']}` | {'yes' if item['exists'] else 'no'} | {item['tracked_count']} | {item['untracked_count']} | {item['ignored_count']} |")
    md.append("")

    md += ["## Candidate file contents and tracked diffs", ""]
    for record in candidate_records:
        rel, content, diff = record["path"], record["content"], record["diff"]
        md += [f"### `{rel}`", "", f"- Git state: **{record['git_state']}**"]
        if content["exists"] and content["kind"] == "file":
            md += [f"- Size: **{content['bytes']} bytes**", f"- Decoding: `{content.get('encoding', 'n/a')}`"]
        else:
            md.append(f"- State on disk: **{content['kind']}**")
        md.append("")
        if diff["available"]:
            md += ["#### Git diff against HEAD", ""]
            if diff["text"]:
                md += ["```diff", diff["text"].rstrip()]
                if diff["truncated"]:
                    md.append("... [diff truncated by scanner] ...")
                md += ["```", ""]
            else:
                md += ["(no tracked diff)", ""]
        md += ["#### Current file content", ""]
        if not content["exists"]:
            md.append("(missing)")
        elif content["kind"] == "directory":
            md.append("(directory; content not inlined)")
        else:
            md += [f"```{fence_for(rel)}", (content["text"] or "").rstrip()]
            if content["truncated"]:
                md.append("... [content truncated by scanner] ...")
            md.append("```")
        md.append("")

    md += ["## Classification worksheet", "", "| Path | Decision | Notes |", "|---|---|---|"]
    for record in candidate_records:
        md.append(f"| `{record['path']}` | _TBD_ | |")
    md += ["", "Recommended decision vocabulary:", "", "- `PUSH AS-IS`", "- `GENERICIZE THEN PUSH`", "- `RESET / DON'T PUSH`", "- `LOCAL ONLY`", ""]

    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("[done] Public-candidate content review created.")
    print(f"[md]   {md_path}")
    print(f"[json] {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
