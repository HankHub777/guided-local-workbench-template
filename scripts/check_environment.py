#!/usr/bin/env python3
"""Read-only local capability preflight for the workbench template.

Usage:
    python scripts/check_environment.py
    python scripts/check_environment.py --json

This script does not install packages, make network requests, change proxy or
certificate settings, modify firewall rules, or print environment-variable values.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PROXY_VARS = (
    "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
    "http_proxy", "https_proxy", "no_proxy",
)
CA_VARS = (
    "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE", "NODE_EXTRA_CA_CERTS", "PIP_CERT",
)


def version_text(command: str, args: list[str]) -> str | None:
    exe = shutil.which(command)
    if not exe:
        return None
    try:
        proc = subprocess.run(
            [exe, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "present (version unavailable)"
    line = (proc.stdout or "").strip().splitlines()
    return line[0] if line else "present"


def browser_candidates() -> list[str]:
    found: list[Path] = []
    system = platform.system().lower()

    if system == "windows":
        roots = [
            os.environ.get("PROGRAMFILES"),
            os.environ.get("PROGRAMFILES(X86)"),
            os.environ.get("LOCALAPPDATA"),
        ]
        suffixes = [
            Path("Google/Chrome/Application/chrome.exe"),
            Path("Microsoft/Edge/Application/msedge.exe"),
            Path("Chromium/Application/chrome.exe"),
        ]
        for root in roots:
            if not root:
                continue
            for suffix in suffixes:
                candidate = Path(root) / suffix
                if candidate.is_file():
                    found.append(candidate)
    elif system == "darwin":
        for candidate in [
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        ]:
            if candidate.is_file():
                found.append(candidate)
    else:
        for name in ("google-chrome", "google-chrome-stable", "microsoft-edge", "chromium", "chromium-browser"):
            exe = shutil.which(name)
            if exe:
                found.append(Path(exe))

    seen: set[str] = set()
    result: list[str] = []
    for path in found:
        text = str(path)
        if text not in seen:
            seen.add(text)
            result.append(text)
    return result


def collect() -> dict:
    proxy_names = [name for name in PROXY_VARS if os.environ.get(name)]
    ca_names = [name for name in CA_VARS if os.environ.get(name)]
    git_version = version_text("git", ["--version"])
    node_version = version_text("node", ["--version"])
    npm_version = version_text("npm", ["--version"])
    browsers = browser_candidates()

    capabilities = {
        "git_repo_work": git_version is not None,
        "web_development": node_version is not None and npm_version is not None,
        "installed_browser_candidate": bool(browsers),
    }

    warnings: list[str] = []
    if not capabilities["git_repo_work"]:
        warnings.append("Git was not found on PATH; repository/PR work is blocked until Git is provided by an approved method.")
    if not capabilities["web_development"]:
        warnings.append("Node/npm are not both available; frontend install/build work is not ready on this machine.")
    if not capabilities["installed_browser_candidate"]:
        warnings.append("No common Chrome/Edge/Chromium executable was discovered; browser automation may need an approved browser or explicit path.")

    status = "BLOCKED" if not capabilities["git_repo_work"] else ("READY_WITH_LIMITATIONS" if warnings else "READY")

    return {
        "status": status,
        "os": platform.platform(),
        "python": sys.version.split()[0],
        "git": git_version,
        "node": node_version,
        "npm": npm_version,
        "browser_candidates": browsers,
        "detected_proxy_variable_names": proxy_names,
        "detected_ca_variable_names": ca_names,
        "capabilities": capabilities,
        "warnings": warnings,
        "notes": [
            "Proxy/CA values are intentionally not printed.",
            "No network request, dependency install, firewall change, or proxy/policy mutation was performed.",
        ],
    }


def print_text(report: dict) -> None:
    print(f"[status] {report['status']}")
    print(f"[os]     {report['os']}")
    print(f"[python] {report['python']}")
    print(f"[git]    {report['git'] or 'MISSING'}")
    print(f"[node]   {report['node'] or 'MISSING'}")
    print(f"[npm]    {report['npm'] or 'MISSING'}")
    if report["browser_candidates"]:
        print("[browser candidates]")
        for item in report["browser_candidates"]:
            print(f"  - {item}")
    else:
        print("[browser candidates] none discovered")

    proxy_names = report["detected_proxy_variable_names"]
    ca_names = report["detected_ca_variable_names"]
    print("[proxy vars] " + (", ".join(proxy_names) if proxy_names else "none detected"))
    print("[CA vars]    " + (", ".join(ca_names) if ca_names else "none detected"))

    if report["warnings"]:
        print("[warnings]")
        for item in report["warnings"]:
            print(f"  - {item}")
    print("[safety] No secret values printed; no environment or policy settings changed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    args = parser.parse_args()
    report = collect()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 2 if report["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
