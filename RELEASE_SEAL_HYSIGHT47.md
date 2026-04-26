# Hysight-47 Release Seal

**Release tag:** hysight-47
**Proved commit:** `f95086655d0810ccb279e15ce8cf7ffca342af8a` (6 test receipts)
**Seal commit:** `bb3fccb42cc6471a45b7dbed4bd0bf24d70f8fa0`
**Sealed at:** 2026-04-26T19:55:00Z
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

Validated by `python scripts/validate_release_seal.py` (full, no flags).

| Receipt | Proved At | Outcome | Passed |
|---------|-----------|---------|--------|
| `artifacts/proof/pipeline.json` | f9508665 | passed | 7 |
| `artifacts/proof/backend-baseline.json` | f9508665 | passed | 98 |
| `artifacts/proof/contract.json` | f9508665 | passed | 18 |
| `artifacts/proof/baseline.json` | f9508665 | passed | 123 |
| `artifacts/proof/autonomy-optional.json` | f9508665 | passed | 66 |
| `artifacts/proof/frontend.json` | f9508665 | passed | 71 |
| `artifacts/proof/current_tree_receipt.json` | bb3fccb4 | pass | — |

The tree receipt was generated at the seal commit (`bb3fccb4`) and provides a
reproducible source fingerprint of the release tree.

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
- **Python contract / Rust sidecar feature parity**: FIXED in Hysight-47. `user_id`, `embedding`, and `mode` fields are now present in `CandidateMemory` and `RetrievalQuery` in `memory_service/types.py` and `contract/schema.json`. Contract conformance proof: 18/0.
