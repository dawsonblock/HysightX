#!/usr/bin/env python3
"""
validate_release_seal.py — assert that every proof receipt in the current
tree is consistent with the active release seal.

Usage:
    python scripts/validate_release_seal.py
    python scripts/validate_release_seal.py --seal RELEASE_SEAL_HYSIGHT47.md
    python scripts/validate_release_seal.py --pre-stamp  # outcomes only, no commit check

Seal format understood:
    **Commit:** `<40-hex>`                  (single-commit seals — preferred)
    **Commit (proved):** `<40-hex>`         (split-commit seals — legacy)

Exit codes:
    0 — all checks passed
    1 — one or more checks failed (diff table printed to stderr)
    2 — usage / IO error

Checks performed by default (full validation):
    1. Seal proved-commit == every receipt commit_sha
    2. Seal proved-commit == current_tree_receipt.json git_commit
    3. current_tree_receipt.json git_dirty == false
    4. Every receipt outcome == "passed"
    5. Every receipt failed_test_count == 0

--pre-stamp skips checks 1-3 (outcomes only). Use only during the stamping
workflow, never cite it as final release validation.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = REPO_ROOT / "artifacts" / "proof"

RECEIPT_NAMES = [
    "pipeline",
    "backend-baseline",
    "contract",
    "baseline",
    "autonomy-optional",
    "frontend",
]

# Matches **Commit:** or **Commit (proved):** followed by a 40-hex SHA.
SEAL_COMMIT_RE = re.compile(
    r"\*\*Commit(?:\s*\(proved\))?:\*\*\s*`([0-9a-f]{40})`", re.IGNORECASE
)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR reading {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def _extract_seal_commit(seal_path: Path) -> str:
    text = seal_path.read_text(encoding="utf-8")
    match = SEAL_COMMIT_RE.search(text)
    if not match:
        print(
            "ERROR: could not find a commit SHA in seal file.\n"
            "  Expected: **Commit:** `<40-hex>`\n"
            "       or: **Commit (proved):** `<40-hex>`\n"
            f"  File: {seal_path}",
            file=sys.stderr,
        )
        sys.exit(2)
    return match.group(1)


def _find_seal_file(explicit: Optional[str]) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = REPO_ROOT / p
        if not p.exists():
            print(f"ERROR: seal file not found: {p}", file=sys.stderr)
            sys.exit(2)
        return p
    candidates = sorted(REPO_ROOT.glob("RELEASE_SEAL_HYSIGHT*.md"), reverse=True)
    if not candidates:
        print("ERROR: no RELEASE_SEAL_HYSIGHT*.md found in repo root", file=sys.stderr)
        sys.exit(2)
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate proof receipts against the active release seal."
    )
    parser.add_argument(
        "--seal",
        metavar="FILE",
        help="Path to release seal .md (default: latest RELEASE_SEAL_HYSIGHT*.md)",
    )
    parser.add_argument(
        "--pre-stamp",
        action="store_true",
        help=(
            "Skip commit-identity checks. "
            "Use before the stamp commit to verify outcomes only."
        ),
    )
    args = parser.parse_args()

    seal_path = _find_seal_file(args.seal)
    seal_commit = _extract_seal_commit(seal_path)

    failures: list[str] = []  # type: ignore[type-arg]

    print(f"Seal file:   {seal_path.name}")
    print(f"Seal commit: {seal_commit}")
    print()

    for name in RECEIPT_NAMES:
        receipt_path = PROOF_DIR / f"{name}.json"
        if not receipt_path.exists():
            failures.append(f"MISSING  {name}.json")
            continue
        data = _load_json(receipt_path)
        commit = data.get("commit_sha", "")
        outcome = data.get("outcome", "")
        failed = data.get("failed_test_count", -1)
        passed = data.get("passed_test_count", 0)

        row_ok = True
        notes = []

        if not args.pre_stamp and commit != seal_commit:
            notes.append(f"commit {commit[:12]} != seal {seal_commit[:12]}")
            row_ok = False
        if outcome != "passed":
            notes.append(f"outcome={outcome!r}")
            row_ok = False
        if failed != 0:
            notes.append(f"failed_test_count={failed}")
            row_ok = False

        status = "OK  " if row_ok else "FAIL"
        note_str = "; ".join(notes) if notes else ""
        print(f"  [{status}] {name:25s}  {commit[:12]}  {passed}p/{failed}f  {note_str}")
        if not row_ok:
            failures.append(f"{name}: {note_str}")

    tree_path = PROOF_DIR / "current_tree_receipt.json"
    if not tree_path.exists():
        failures.append("MISSING  current_tree_receipt.json")
    else:
        tree = _load_json(tree_path)
        tree_commit = tree.get("git_commit", "")
        tree_dirty = tree.get("git_dirty", True)
        tree_status = tree.get("status", "")

        row_ok = True
        notes = []
        if not args.pre_stamp and tree_commit != seal_commit:
            notes.append(f"git_commit {tree_commit[:12]} != seal {seal_commit[:12]}")
            row_ok = False
        if tree_dirty:
            notes.append("git_dirty=true")
            row_ok = False
        if tree_status != "pass":
            notes.append(f"status={tree_status!r}")
            row_ok = False

        status = "OK  " if row_ok else "FAIL"
        note_str = "; ".join(notes) if notes else ""
        print(
            f"  [{status}] {'current_tree_receipt':25s}  {tree_commit[:12]}"
            f"  dirty={tree_dirty}  {note_str}"
        )
        if not row_ok:
            failures.append(f"current_tree_receipt: {note_str}")

    print()
    if failures:
        print(f"RESULT: FAIL — {len(failures)} check(s) failed:", file=sys.stderr)
        for f in failures:
            print(f"  ✗ {f}", file=sys.stderr)
        return 1

    mode = "(pre-stamp)" if args.pre_stamp else ""
    print(f"RESULT: PASS — all checks OK {mode}".strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
