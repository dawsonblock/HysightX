#!/usr/bin/env python3
"""
hash_sidecar_subtree.py — compute a deterministic SHA-256 fingerprint of the
Rust sidecar source tree (memvid_service/ + memvid/) for carry-forward
verification.

Usage:
    python scripts/hash_sidecar_subtree.py
    python scripts/hash_sidecar_subtree.py --verify EXPECTED_HASH

Algorithm:
    1. Collect all files under memvid_service/ and memvid/ whose suffix is in
       {.rs, .toml, .lock, .md}, excluding build artefacts (target/).
    2. Sort paths lexicographically (repo-root-relative).
    3. For each path (in sorted order): update SHA-256 with the UTF-8 path
       bytes, then with the raw file bytes.
    4. Output the hex digest.

Exit codes:
    0 — success (or --verify match)
    1 — --verify mismatch
    2 — usage / IO error
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SIDECAR_DIRS = ["memvid_service", "memvid"]
SIDECAR_EXTENSIONS = {".rs", ".toml", ".lock", ".md"}
EXCLUDE_DIRS = {"target", ".git"}


def collect_files() -> list[Path]:
    files: list[Path] = []
    for dir_name in SIDECAR_DIRS:
        base = REPO_ROOT / dir_name
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            if path.suffix in SIDECAR_EXTENSIONS:
                files.append(path)
    return sorted(files, key=lambda p: str(p.relative_to(REPO_ROOT)))


def compute_hash(files: list[Path]) -> str:
    h = hashlib.sha256()
    for path in files:
        rel = str(path.relative_to(REPO_ROOT))
        h.update(rel.encode("utf-8"))
        h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute deterministic SHA-256 fingerprint of sidecar source tree."
    )
    parser.add_argument(
        "--verify",
        metavar="HASH",
        help="Expected hex digest; exits 1 if mismatch.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only the hash (no labels).",
    )
    args = parser.parse_args()

    try:
        files = collect_files()
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    digest = compute_hash(files)

    if args.quiet:
        print(digest)
    else:
        print("algorithm:  sha256")
        print(f"file_count: {len(files)}")
        print(f"hash:       {digest}")
        print()
        print("included paths:")
        for path in files:
            print(f"  {path.relative_to(REPO_ROOT)}")

    if args.verify:
        expected = args.verify.strip().lower()
        actual = digest.lower()
        if actual != expected:
            print(
                f"\nVERIFY FAILED\n  expected: {expected}\n  actual:   {actual}",
                file=sys.stderr,
            )
            return 1
        if not args.quiet:
            print("\nVERIFY OK")

    return 0


if __name__ == "__main__":
    sys.exit(main())
