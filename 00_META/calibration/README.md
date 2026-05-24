# Auto-task extraction — calibration corpus

Per audit B17. Hybrid-by-confidence (B6) only works if the LLM's `confidence` scores are calibrated against reality. This corpus is the ground truth used to (a) hand-rate the rubric prompt's quality, and (b) retune the per-tenant `auto_task_threshold` bi-weekly.

## Rubric the extractor prompt uses

| Score range | Meaning | Example |
|---|---|---|
| 0.90 – 1.00 | Direct quote from a participant saying "I'll do X by Y" | "JP: voy a mandar la propuesta a Trixx el lunes" |
| 0.70 – 0.89 | Paraphrased commitment with clear owner + intent | "JP dijo que la propuesta queda lista esta semana" |
| 0.40 – 0.69 | Inferred from context, no explicit commitment | "Sería bueno avanzar con Trixx pronto" |
| 0.00 – 0.39 | Speculation / aspirational | "Eventualmente podríamos contactar Trixx" |

## Schema

NDJSON, one row per rated example:

```json
{"meeting_id": "2026-05-19_08-00_nexostrat-weekly",
 "extracted_text": "JP: mando propuesta Trixx el lunes",
 "owner": "jp", "due": "2026-05-26",
 "model_score": 0.92,
 "ground_truth_score": 0.95,
 "ground_truth_should_write": true,
 "auto_written": true,
 "rater": "ricardo", "rated_at": "2026-05-21T18:00:00-07:00",
 "notes": "Direct quote. Owner explicit."}
```

### Field meanings

| Field | Required | Meaning |
|---|---|---|
| `meeting_id` | yes | Source meeting slug (matches `/srv/meetings/<id>/`) |
| `extracted_text` | yes | The action text the LLM proposed |
| `owner` | yes | LLM's inferred owner |
| `due` | no | LLM's inferred due date, or null |
| `model_score` | yes | The LLM's `confidence` for this action |
| `ground_truth_score` | yes | Human rater's score on the same rubric (calibration check) |
| `ground_truth_should_write` | yes | Boolean — should this have been auto-written or routed to review? Drives the retuner's F1 calculation. |
| `auto_written` | yes | Whether the live system actually wrote it (depends on the threshold at the time) |
| `rater` | yes | `ricardo` or `jp` |
| `rated_at` | yes | ISO-8601 timestamp |
| `notes` | no | Free-text rater notes |

## Retuning script

`/srv/brain-hub/hub/router/calibration.py` reads this corpus, computes the F1 score of "auto-write" decisions at candidate thresholds, recommends the threshold with the highest F1. Bi-weekly Brain Architect pass runs the script and updates `routing.yaml extras.auto_task_threshold`.

```bash
cd /srv/brain-hub
source venv/bin/activate
python -c "from pathlib import Path; from hub.router.calibration import recommend_threshold; \
  print(recommend_threshold(Path('/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl')))"
```

Output:
```
Recommendation(threshold=0.87, precision=0.93, recall=0.88, f1=0.90)
```

## Seeding

Ricardo and JP rate the first 50 examples by hand during Phase 6 dry-run (target: 2-3 sample meetings × ~20 actions each). This is **not** the engineer's work — the value of the corpus is that the raters are the actual stakeholders whose judgment the system is approximating.

**Until the corpus has ≥50 rated examples, the retuner script's output is unreliable** (F1 on a 5-row corpus is high-variance noise). Do not update `auto_task_threshold` from a sparse corpus.

## Bi-weekly retune protocol

1. Brain Architect runs the retuner on the current corpus.
2. If recommended threshold differs from `auto_task_threshold` by ≥ 0.05: open a memo to Ricardo with the recommendation + precision/recall trade-off.
3. Ricardo decides; merges the routing.yaml change if approved.
4. New auto-tasks accumulate at the new threshold; next bi-weekly cycle adds their ratings to the corpus.

## Audit

This file ratifies audit B17. The corpus is **append-only** in normal operation — historical ratings stay even if the rubric is later refined (so the retuner can chart drift over time).
