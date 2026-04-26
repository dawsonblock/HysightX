# Hysight-47 Optional Proof Summary

**Release tag:** hysight-47
**Commit:** `f95086655d0810ccb279e15ce8cf7ffca342af8a`
**Sealed at:** 2026-04-26

> Starting with Hysight-47, `RELEASE_SEAL_HYSIGHTNN.md` is the single
> authoritative release document. Optional proof summary files are supplementary
> human-readable companions; the seal is the source of truth.

---

## Autonomy Suite (Optional — Re-run and Passing)

| Metric | Value |
|--------|-------|
| Passed | 66 |
| Failed | 0 |
| Outcome | ✅ PASS |
| Commit | see seal |

The autonomy suite exercises the bounded operator-style control layer
(`hca/src/hca/autonomy/`), including `style_profile.py`,
`attention_controller.py`, and `supervisor.py`. Per the module's own docstring,
these profiles describe controllable work-style biases (prioritization, memory
emphasis, re-anchoring) and are not medical or diagnostic behavior models.

---

## Frontend Suite (Re-run and Passing)

| Metric | Value |
|--------|-------|
| Passed | 71 |
| Failed | 0 |
| Outcome | ✅ PASS |

Frontend proof passed all 5 stages via `scripts/run_tests.py --frontend`:

1. **Runtime verification** — backend endpoints callable, subsystems healthy
2. **Fixture drift gate** — `api.fixtures.generated.json` matches committed snapshot
3. **Lint** — ESLint clean
4. **Jest** — 71 tests passing across all suites
5. **Production build** — Vite build succeeded

---

## Live Sidecar Suite

| Metric | Value |
|--------|-------|
| Status | **CARRY-FORWARD** |
| Last proven | hysight-42, commit `10966b3bc57905b298563145dba8450d610f9c1c` |
| Last result | 13 passed, 0 failed, 2 skipped |
| Receipt | `artifacts/proof/release_live_sidecar_receipt_hysight42.json` |
| Subtree hash | `2ccc27c4c74694b733400110130c177dcef19c8bce1046ca1053abee9f93d99e` |
| Hash covers | 243 files under `memvid_service/` and `memvid/` (`.rs/.toml/.lock/.md`) |
| Recompute | `python scripts/hash_sidecar_subtree.py` |

Live Rust sidecar was not re-run in the hysight-47 sealing pass. No sidecar
source was modified between hysight-42 and hysight-47. The subtree hash above
is deterministic and reproducible; it proves the source tree is identical to
the last sidecar proof run.

---

## Known Limitations

- Python contract previously did not expose `user_id`, `embedding`, or `mode` fields
  supported by the Rust sidecar. **Fixed in Hysight-47**: all three fields are now in
  `CandidateMemory` and `RetrievalQuery` with matching defaults. Contract proof: 18/0.
- Live Mongo proof: not rerun; historical only.
