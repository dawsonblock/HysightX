# Hysight-46 Release Seal

**Release tag:** hysight-46
**Commit:** `a3fdd9842e965ea3efaa709e5c5f1e29d1a754ac`
**Sealed at:** 2026-04-26T07:38:46Z
**Classification:** **sealed local-core release**

---

## Proof Counts

| Suite | Passed | Failed |
|-------|--------|--------|
| Baseline (pipeline + backend + contract) | 123 | 0 |
| Autonomy | 66 | 0 |
| Frontend | 71 | 0 |
| **Total (local-core)** | **260** | **0** |

Sidecar: **CARRY-FORWARD** — last proved at hysight-42 (13/0). No sidecar source changes since that proof.

---

## Evidence Files

All proof ran against the live repo at the exact commit listed above.

- `artifacts/proof/baseline.json`
- `artifacts/proof/backend-baseline.json`
- `artifacts/proof/contract.json`
- `artifacts/proof/autonomy-optional.json`
- `artifacts/proof/frontend.json`
- `artifacts/proof/current_tree_receipt.json`

All receipts carry `commit_sha: a3fdd9842e965ea3efaa709e5c5f1e29d1a754ac`.

---

## Environment

- Platform: macOS, local repo `.venv`
- Python: repo-local `.venv` bootstrap
- Node: system Node / Yarn (frontend proof via `scripts/run_tests.py --frontend`)

---

## Audit Fixes Applied (vs. Hysight-45)

| # | Finding | Resolution |
|---|---------|------------|
| 1 | `_effective_tool_policy()` silently overrode `run_command` to `requires_approval=False` / `ActionClass.low`, contradicting registry declaration (`requires_approval=True`, `ActionClass.high`) | Override block removed; registry declaration is now the single source of truth |
| 2 | `logs/*.log`, `logs/*.pid`, `artifacts/proof/sidecar-data/memory.mv2` tracked in git | Untracked via `git rm --cached`; `.gitignore` rules added |
| 3 | `frontend/craco.config.js` (CRA/CRACO residue) present despite Vite being used | File deleted |
| 4 | Proof receipts referenced stale commits; `artifacts/proof/frontend.json` missing | All receipts regenerated against `a3fdd984`; `frontend.json` now present |

---

## Known Carry-Forwards

- **Sidecar proof**: Rust sidecar last proved at hysight-42. Sidecar source unchanged.
- **Python contract / Rust sidecar feature parity**: `user_id`, `embedding`, `mode` fields are supported by the Rust sidecar but not yet exposed by the Python `ContractModel`. This is documented and tracked for a future proof tier.
