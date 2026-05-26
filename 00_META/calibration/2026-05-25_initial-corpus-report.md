# Initial calibration-corpus report

**Date:** 2026-05-25
**Author:** Nexostrat Founder session (session 18)
**Tracks:** Phase 0a P-N3 in meetings-pipeline overhaul master plan §6.2 · same line item as `t-confidence-calibration-corpus` (B17, due 2026-06-22)
**Corpus file:** [`auto_task_extraction.jsonl`](auto_task_extraction.jsonl)
**Rubric source:** [`README.md`](README.md)

---

## 1. Row count

| Block | Rows |
|---|---:|
| `_comment` guard (retuner skips) | 1 |
| Meeting-derived ratings | 20 |
| Synthetic edge cases | 30 |
| **Total rated rows** | **50** |
| **File line count** | **51** |

Hand-rated floor (≥50) met. The master plan §6.2 P-N3 done-criterion ("≥ 50 valid NDJSON rows, each carrying `model_score`, `ground_truth_score`, `ground_truth_should_write`, `rater`, `rated_at`") is satisfied — see schema validation below.

## 2. Schema validation

All 50 rated rows carry every required field (`meeting_id`, `extracted_text`, `owner`, `model_score`, `ground_truth_score`, `ground_truth_should_write`, `auto_written`, `rater`, `rated_at`). Optional fields (`due`, `notes`) present where applicable.

`model_score` is **`null` for every row by design** — the field exists so the future P-H6 DeepSeek-vs-OpenAI calibration pass can backfill real model scores without a schema migration. The retuner script (`/srv/brain-hub/hub/router/calibration.py` per README) must therefore skip `null`-score rows until P-H6 completes; recommend adding a `--require-model-score` guard or filtering in `recommend_threshold()` before next bi-weekly retune attempt.

## 3. Tier distribution

| Tier | Score range | Rubric meaning | Meeting | Synthetic | Total |
|---|---|---|---:|---:|---:|
| T1 | 0.90–1.00 | Direct quote, explicit commit + owner + when | 2 | 8 | **10** |
| T2 | 0.70–0.89 | Paraphrased commit, clear owner + intent | 13 | 7 | **20** |
| T3 | 0.40–0.69 | Inferred from context, no explicit commit | 5 | 8 | **13** |
| T4 | 0.00–0.39 | Speculation / aspirational / small-talk FPs | 0 | 7 | **7** |
| | | **Total** | **20** | **30** | **50** |

**Notes on the distribution:**

- T4 is 0 from real meetings because the source files are `summary.md` — they already filter small-talk before reaching the calibration corpus. Synthetic Tier 4 rows cover that gap (false-positive triggers like `voy al baño`, `algún día deberíamos abrir oficina`, etc.).
- T2 is intentionally the largest tier (20/50 = 40%) because that's where the auto-write threshold actually bites; the bulk of real-world action items live in this band.
- `ground_truth_should_write = true` for 19 / 50 rows (38%). All 19 sit at `ground_truth_score ≥ 0.82`; everything below 0.82 routes to review. The boundary aligns cleanly with the rubric: T2 paraphrased commits with clear owner *and* a crisp deliverable get auto-written; T2 commits with multi-assignee / external-party / vague-verb signals don't.

## 4. Edge-case coverage check

Per the master plan §6.2 P-N3 + contribution doc §3 P-N3 mandate, the synthetic 30 cover:

- ✅ **Ambiguous "we should do X someday"** — Tier 3 (S16–S23) + Tier 4 (S25, S30).
- ✅ **Multi-assignee phrasings** — meeting rows #5, #10, #11, #13, #17; synthetic S11 (`Ricardo y JP coordinarán…`).
- ✅ **Dates given only in relative form** — synthetic S1 (`el lunes`), S2 (`mañana`), S3 (`esta semana`), S4 (`hoy en la tarde`), S5 (`el viernes`), S6 (`el miércoles a las 3pm`), S7 (`hoy mismo`).
- ✅ **JP-language quirks** — S3 (`yo me encargo`), S4 (`te paso`), S5 (`te tengo lista`), S8 (`confirmo`). These are JP's canonical I-own-it phrases; the extractor must recognize them as Tier 1 commits, not Tier 2.
- ✅ **False-positive triggers** (small-talk an LLM might mis-extract) — S24 (`eventualmente podríamos`), S27 (`voy al baño`), S28 (`déjame buscar el cargador`), S29 (`luego te cuento del fin de semana`).
- ✅ **External-party owner** (should not auto-write) — meeting #16 (Neo+Ricardo), #17 (Neo+Ricardo+JP), synthetic S15 (Andrea).
- ✅ **Chained / dependent tasks** — meeting #7 (JP consolidates AFTER Ricardo+JP fill their cuestionarios).
- ✅ **Compound actions needing split** — meeting #10 (`por separado`), #11 (two pilots conflated), #14 (`abrir cuentas` ≠ `publicación gradual`).

## 5. Threshold recommendation

The README rubric proposes `auto_task_threshold = 0.85` as the starting value. Since `model_score` is `null` for every row in this initial corpus, the retuner cannot compute real precision/recall — but a **perfect-calibration upper-bound sweep** (assuming `model_score == ground_truth_score`) gives a useful sanity check:

| Threshold | TP | FP | FN | TN | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.70 | 19 | 11 | 0 | 20 | 0.633 | 1.000 | 0.776 |
| 0.75 | 19 |  8 | 0 | 23 | 0.704 | 1.000 | 0.826 |
| 0.80 | 19 |  2 | 0 | 29 | 0.905 | 1.000 | 0.950 |
| 0.82 | 19 |  1 | 0 | 30 | 0.950 | 1.000 | **0.974** |
| **0.85** | **17** | **0** | **2** | **31** | **1.000** | **0.895** | **0.944** |
| 0.88 | 12 |  0 | 7 | 31 | 1.000 | 0.632 | 0.774 |
| 0.90 | 10 |  0 | 9 | 31 | 1.000 | 0.526 | 0.690 |

**Recommendation: hold at `auto_task_threshold = 0.85` for Stage 1 launch.**

The upper-bound sweep suggests F1 peaks at 0.82 (0.974), and 0.85 (0.944) is also strong. But:

1. **The sweep is an upper bound, not reality.** Once P-H6 backfills real DeepSeek `model_score` values, calibration noise will widen the band. A 0.85 threshold leaves precision headroom for that noise; 0.82 would not.
2. **`should_write = true` posture is partnership-sensitive.** Audit B17 framed this explicitly: in a JP-shared partnership the cost of an auto-write false positive (a junk task appearing in JP's ledger) is higher than the cost of a false negative (a real task routed to one extra confirmation click). Precision-favoring posture matches that asymmetry.
3. **Corpus is biased toward action-rich content.** Real raw-transcript extraction will see far more T3/T4 noise than this `summary.md`-sourced corpus suggests. The 0.85 threshold's "0 FP" property on this corpus is the right starting posture; widening to 0.80–0.82 should happen only after P-H6 + 2 bi-weekly retune cycles confirm real-world calibration matches.
4. **Stage 1 launch already commits to 0.85** in the README rubric and routing.yaml-template default. Changing the threshold before the corpus has real `model_score` data would be premature optimization on a perfect-calibration toy.

**Re-evaluation triggers** for raising/lowering `auto_task_threshold`:

- After P-H6 lands (DeepSeek + OpenAI both backfill `model_score` for all 50 rows), re-run this sweep with real scores; expected delta from upper bound is precision drop of 0.05–0.10 and possibly a different F1 peak.
- After 2 full bi-weekly retune cycles post-Phase-4-launch (i.e., 4 weeks of auto-written rows accumulating with their `model_score` recorded), the retuner has enough live data to recommend a non-arbitrary value.
- Until then, **do not change the threshold from 0.85**. The retuner's output is high-variance noise per the README cautionary note ("F1 on a 5-row corpus is high-variance noise"; this corpus is 50 rows but still synthetic-skewed).

## 6. Known gaps and follow-ups

1. **No `jp`-rated rows.** All 50 are `rater: ricardo`. JP-rated comparison rows are the natural next pass (audit B17 deliverable 3 cron: "bi-weekly re-rating of 20 auto-written tasks" — JP should rate a subset for inter-rater agreement). Defer to first bi-weekly cycle post-Phase-4-launch.
2. **No live `auto_written: true` rows.** All 50 are historical/synthetic (`auto_written: false`). The first live auto-write from Phase 4 will set `auto_written: true` and populate `model_score` from the extractor's confidence; that row joins the corpus on the next bi-weekly retune.
3. **`model_score: null` shortcut.** Until P-H6 backfills, the retuner script must skip these rows or treat null as un-evaluable. Recommend documenting this in the retuner's `recommend_threshold()` docstring before P-H6 runs.
4. **Synthetic Tier 2 (0.78–0.85) under-sampled.** Only 4 of 30 synthetic rows sit in the 0.78–0.85 boundary band (S9 0.85, S10 0.78, S13 0.82, S15 0.78). This is the exact band where the 0.85 threshold lives — future labelling passes should over-sample here for sharper threshold tuning.
5. **No Spanish-vs-English mixing.** All rated rows are in Spanish (matches Nexostrat's bilingual rule that JP-facing content is Spanish). If future English-only meetings ship (Ricardo solo notes, external customer calls in English), expand corpus with English rows.

## 7. Retuner usage (post-P-H6)

Per README:

```bash
cd /srv/brain-hub
source venv/bin/activate
python -c "from pathlib import Path; from hub.router.calibration import recommend_threshold; \
  print(recommend_threshold(Path('/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl')))"
```

Expected output once `model_score` is backfilled:

```
Recommendation(threshold=0.XX, precision=0.YY, recall=0.ZZ, f1=0.WW)
```

If the recommended threshold differs from the active `auto_task_threshold` in `routing.yaml` by ≥ 0.05, open a memo to Ricardo per the README bi-weekly retune protocol.

---

**Done-criterion check (master plan §6.2 P-N3):**

- ✅ ≥ 50 valid NDJSON rows in the corpus file (50 rated rows + 1 `_comment` guard = 51 lines).
- ✅ Each row carries `model_score`, `ground_truth_score`, `ground_truth_should_write`, `rater`, `rated_at`.
- ✅ Initial-corpus report file exists with precision/recall numbers (under perfect-calibration assumption since `model_score: null`) + recommended threshold (0.85, hold).

P-N3 → DONE.
