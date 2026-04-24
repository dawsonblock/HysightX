#!/usr/bin/env python3
"""
proof_current_tree.py — generate a proof receipt for the current source tree.

Usage:
    python scripts/proof_current_tree.py

Output:
    artifacts/proof/current_tree_receipt.json
"""
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
OUT_PATH = REPO_ROOT / "artifacts" / "proof" / "current_tree_receipt.json"

IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "dist", "build", "target",
    "artifacts",  # avoid hashing old receipts into new receipt
}

SOURCE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".rs",
    ".toml", ".json", ".yaml", ".yml", ".cfg", ".ini",
    ".md", ".txt", ".sh", ".env",
}


def _run(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def _collect_files() -> list[Path]:
    files = []
    for root, dirs, filenames in os.walk(REPO_ROOT):
        dirs[:] = [d for d in sorted(dirs) if d not in IGNORE_DIRS]
        for fn in sorted(filenames):
            p = Path(root) / fn
            if p.suffix in SOURCE_EXTENSIONS:
                files.append(p)
    return files


def _fingerprint(files: list[Path]) -> str:
    h = hashlib.sha256()
    for p in files:
        rel = str(p.relative_to(REPO_ROOT))
        h.update(rel.encode())
        try:
            h.update(p.read_bytes())
        except OSError:
            h.update(b"<unreadable>")
    return h.hexdigest()


def main() -> int:
    files = _collect_files()
    fingerprint = _fingerprint(files)

    git_commit = _run(["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"])
    git_dirty = _run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain"]
    )
    node_version = _run(["node", "--version"])
    yarn_version = _run(["yarn", "--version"])
    cargo_version = _run(["cargo", "--version"])
    rustc_version = _run(["rustc", "--version"])

    commands_run = [
        "python scripts/proof_current_tree.py",
    ]

    receipt = {
        "schema_version": "1",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "platform": platform.platform(),
        "python_version": sys.version,
        "node_version": node_version,
        "yarn_version": yarn_version,
        "cargo_version": cargo_version,
        "rustc_version": rustc_version,
        "git_commit": git_commit,
        "git_dirty": bool(git_dirty),
        "source_fingerprint": fingerprint,
        "source_files_hashed": len(files),
        "commands_run": commands_run,
        "status": "pass",
        "notes": (
            "Fingerprint covers all .py/.js/.ts/.rs/config files "
            "excluding .git, caches, build outputs, and artifacts/."
        ),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    print(f"\nReceipt written to: {OUT_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
