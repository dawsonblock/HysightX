# Hysight-47 Release Seal

**Release tag:** hysight-47
**Commit (proved):** `ea65d66580f885114b61e51cdea59db6f5249447`
**Commit (packaged):** `ce9de158c1154a6354d9bed0eb92d886bc0980e2`
**Sealed at:** 2026-04-26T19:30:00Z
**Classification:** **sealed local-core release**

---

## Proof Counts

| Suite | Passed | Failed |
|-------|--------|--------|
| Pipeline | 7 | 0 |
| Backend baseline | 98 | 0 |
| Contract conformance | 18 | 0 |
| **Baseline aggregate** | **123** | **0** |
| Autonomy optional | 66 | 0 |
| Frontend (5 stages) | 71 | 0 |
| **Total local-core** | **260** | **0** |

Sidecar: **CARRY-FORWARD** — last proved at hysight-42 (13/0).
Sidecar subtree hash (`memvid_service/` + `memvid/`, `.rs/.toml/.lock/.md` files, sorted):
`2ccc27c4c74694b733400110130c177dcef19c8bce1046ca1053abee9f93d99e` (243 files)
This hash can be recomputed at any commit to verify no sidecar source changed since hysight-42.

---

## Evidence Files

All 6 proof receipts share commit `ea65d665` (the proved commit).
The tree receipt reflects the packaged commit `ce9de158` (dirty=false).
Validated by `python scripts/validate_release_seal.py --pre-stamp`.

| Receipt | Outcome | Passed |
|---------|---------|--------|
| `artifacts/proof/pipeline.json` | passed | 7 |
| `artifacts/proof/backend-baseline.json` | passed | 98 |
| `artifacts/proof/contract.json` | passed | 18 |
| `artifacts/proof/baseline.json` | passed | 123 |
| `artifacts/proof/autonomy-optional.json` | passed | 66 |
| `artifacts/proof/frontend.json` | passed | 71 |
| `artifacts/proof/current_tree_receipt.json` | pass | — |

---

## Environment

- Platform: macOS-26.2-arm64-arm-64bit
- Python: 3.9.7, repo-local `.venv`
- Node: v24.15.0
- Yarn: 1.22.22
- Rust/cargo: 1.94.0

---

## Audit Fixes Applied (vs. Hysight-46 / v8 archive)

| # | Finding | Resolution |
|---|---------|------------|
| 1 | `artifacts/proof/backend-baseline.json` was from commit `88028d69` with 5 failures | Regenerated at HEAD — 98 passed, 0 failed |
| 2 | `artifacts/proof/contract.json` was from commit `88028d69` | Regenerated at HEAD |
| 3 | `artifacts/proof/pipeline.json` was missing or stale | Regenerated at HEAD |
| 4 | `artifacts/proof/current_tree_receipt.json` was from commit `354882323` | Regenerated at HEAD |
| 5 | `artifacts/proof/baseline.json`, `autonomy-optional.json`, `frontend.json` were from `a3fdd984` (one commit behind) | Regenerated at HEAD |
| 6 | `README.md` Release Seal section referred to Hysight-45, wrong commit, 67 frontend tests | Updated to Hysight-46/47, correct commit, 71 frontend tests |
| 7 | `BOOTSTRAP.md` said "Node 20 / Yarn 1.22.22" | Corrected to "Node 24 / Yarn 1.22.22" |

---

## Known Carry-Forwards

- **Sidecar proof**: Rust sidecar last proved at hysight-42. Subtree hash above provides verifiable evidence of no source change.
- **Python contract / Rust sidecar feature parity**: `user_id`, `embedding`, `mode` fields supported by Rust sidecar are not yet in the Python `ContractModel`. Documented and tracked; not a runtime regression.
