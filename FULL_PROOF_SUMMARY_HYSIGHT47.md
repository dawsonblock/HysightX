# Hysight-47 Full Proof Summary

**Release tag:** hysight-47
**Proved commit:** `f95086655d0810ccb279e15ce8cf7ffca342af8a` (6 test receipts)
**Seal commit:** `bb3fccb42cc6471a45b7dbed4bd0bf24d70f8fa0`
**Sealed at:** 2026-04-26T19:55:00Z
**Platform:** macOS, local repo `.venv`
**Classification:** **sealed local-core release**

> Starting with Hysight-47, `RELEASE_SEAL_HYSIGHTNN.md` is the single
> authoritative release document. Full and optional proof summary files are
> supplementary human-readable companions; the seal is the source of truth.
>
> The 6 test receipts were generated at the proved commit. The tree receipt
> was generated at the seal commit and provides a reproducible source fingerprint.

---

## Proof Matrix

| Suite | Passed | Failed | Skipped | Notes |
|-------|--------|--------|---------|-------|
| Pipeline | 7 | 0 | — | included in baseline total |
| Backend baseline | 98 | 0 | 1 deselected | included in baseline total |
| Contract | 18 | 0 | — | included in baseline total |
| **Baseline total** | **123** | **0** | — | ✅ |
| Autonomy (optional) | 66 | 0 | — | ✅ |
| Frontend | 71 | 0 | — | ✅ all 5 stages |
| Live sidecar | **CARRY-FORWARD** | — | — | last proved hysight-42 (13/0) |

**Total proven passing tests: 260** (123 baseline + 66 autonomy + 71 frontend)

---

## What Was Verified

The 6 test receipts were generated at the proved commit (`f9508665`).
The following surfaces were confirmed:

- Canonical baseline proof: pipeline 7 + backend-baseline 98 + contract 18 = 123/0
- Autonomy suite: 66/0 (bounded operator-style control layer)
- Frontend (runtime-verification + fixture-drift + lint + Jest + production build): 71/0

## What Was Not Verified

- Live Rust sidecar (`memvid-sidecar`) — not re-run in this pass
  Last proven: hysight-42, commit `10966b3bc57905b298563145dba8450d610f9c1c`, 13/0
  Carry-forward verified via reproducible subtree hash:
  `2ccc27c4c74694b733400110130c177dcef19c8bce1046ca1053abee9f93d99e` (243 files)
  Recompute: `python scripts/hash_sidecar_subtree.py`

---

## Environment

- Python: repo-local `.venv`
- Node: v24.15.0
- Yarn: 1.22.22
- Rust/cargo: carry-forward, not invoked

---

## What Materially Changed vs hysight-46

### Contract expansion (Python ↔ Rust parity)

`memory_service/types.py`:
- `CandidateMemory` — added `user_id: str = "default"` and `embedding: Optional[List[float]] = None`
- `RetrievalQuery` — added `user_id: str = "default"`, `embedding: Optional[List[float]] = None`, `mode: Literal["bm25", "semantic", "hybrid"] = "bm25"`

`contract/schema.json`:
- `CandidateMemory` definition — added `user_id` and `embedding`
- `RetrievalQuery` definition — added `user_id`, `embedding`, and `mode`

All new fields are optional with defaults matching the Rust sidecar. Zero breaking change to existing callers. Contract conformance proof still passes 18/0.

### Release tooling

- `scripts/validate_release_seal.py` — validates that 6 test receipts match the proved commit and tree receipt has git_dirty=false
- `scripts/hash_sidecar_subtree.py` — deterministic SHA-256 of sidecar source tree for reproducible carry-forward verification

---

## Classification Rationale

Baseline, autonomy, and frontend proofs ran locally at the proved commit (`f9508665`).
The tree receipt was generated at the seal commit (`bb3fccb4`) and provides a
reproducible source fingerprint (git_dirty=false). Live Rust sidecar was not
re-run; last proof stands from hysight-42 and is verified via reproducible
subtree hash. Classification is "sealed local-core release".
