# Proof Receipts

## Current proof

Current proof receipts must be regenerated from the current source tree by running:

```bash
python scripts/proof_current_tree.py
```

The output receipt is written to `artifacts/proof/current_tree_receipt.json`.

**Proof receipts are valid only when their `git_commit` and `source_fingerprint` fields match the source tree being released.**

## Historical receipts

All historical receipts (from previous release cycles) are stored under `artifacts/proof/history/`.
They are retained for audit purposes but **do not prove the current source tree**.

Do not reference files under `history/` as proof of the current build.

## Generating a fresh receipt

```bash
# from repo root
python scripts/proof_current_tree.py
```

The script hashes all relevant source and config files (ignoring caches, generated output,
and the history directory) and records tool versions and git state at the time of invocation.
