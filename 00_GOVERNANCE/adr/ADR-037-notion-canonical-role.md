# ADR-037 — Notion canonical role: Stage 2 review trigger

**Status:** Accepted
**Date:** 2026-05-14
**Decided by:** Ricardo + Claude (Batch 1 amendments per [`2026-05-14_amendments.md`](../../00_META/proposals/2026-05-14_amendments.md) §R5)
**Related:** ADR-024 (Dual meeting capture), ADR-034 (Ambient chat extraction)

## Context

Stage 1 makes **Notion AI the canonical source of meeting capture** for both internal R+JP meetings and client meetings (default), with Jitsi/Whisper as optional shadow for parity. The Stage 1 economics work because Notion's cost to the firm is **$0** — JP's personal Notion subscription absorbs the seat. Nexostrat pays nothing for what is effectively the firm's CRM + meeting brain.

This arrangement is sustainable as long as three conditions hold:
1. JP keeps the Notion subscription as a personal expense.
2. The cost of Notion + Notion AI add-on stays roughly stable.
3. The audit/data-residency risk of Notion holding client meeting transcripts stays acceptable.

If any of those conditions changes, the canonical-Notion decision deserves a fresh look. This ADR captures **what to look for and what the alternative would be**, so the review is concrete when it happens rather than freeform.

The 2026-05-14 audit (Recommendation 5) requested this artifact because the cost-flip alone (JP-personal vs firm-paid) is structurally fragile.

## Decision

**Notion remains canonical for Stage 1.** No infrastructure changes proposed at this time.

A Stage 2 review of this decision **must** be triggered by any of the following:

### Trigger A — Cost direction reverses

JP can no longer absorb the Notion subscription personally (he discontinues, hits a Notion price hike he won't eat, the cost-sharing arrangement renegotiates), **AND** the firm-paid cost would land above ~$50/mo. The Stage 1 cost envelope is $36-91/mo; a $50/mo Notion line item alone would consume more than half the headroom.

### Trigger B — Client data-residency risk surfaces

A signed client requires data residency guarantees Notion cannot meet (EU GDPR data-processing concern, sectoral compliance, contractual obligation to keep transcripts on-premise), **OR** a client-side audit flags Notion as an unacceptable processor for their meeting transcripts.

### Trigger C — JP workflow shift

JP's day-to-day workflow drifts away from Notion such that the firm is paying for (or freeloading on) a tool only Ricardo uses. The "canonical" status becomes operationally false even if technically true.

### Trigger D — Parity score reaches Whisper-canonical readiness

ADR-024 already names this trigger: parity score ≥ 0.9 for 4 consecutive internal meetings means Whisper.cpp transcripts are objectively as good as Notion AI for the firm's content. At that point, Whisper-canonical becomes a viable alternative on quality grounds alone.

## Alternative under review

The reviewable alternative is **Whisper.cpp on HP as canonical capture**, with Notion demoted to "personal use, JP only" or removed entirely. This means:

- **Pros:** $0/mo to the firm (Whisper.cpp is free, HP already runs it), full data ownership (audio + transcript live in `vault/clients/<slug>/meetings/`), no third-party processor, no JP-vs-firm cost coupling.
- **Cons:** Whisper.cpp Spanish transcripts at CPU speed take ~real-time to ~1.5x; Notion AI is faster and produces a polished summary out of the box. Whisper as canonical means the firm builds the summary layer (Ollama on desktop, per ADR-026 / ADR-034 patterns).
- **Migration cost:** when triggered, the migration is roughly Plan 08 + a chunk of Plan 09 work re-prioritized. Estimated 1-2 weeks elapsed if Plans 08-09 are already done; longer if they aren't.

## Review process when a trigger fires

1. Open a `00_META/proposals/<date>_notion-canonical-review.md` capturing which trigger fired and the evidence.
2. Run a fresh cost/risk analysis with current numbers.
3. If the review concludes "switch to Whisper-canonical," write a new ADR superseding the Notion-canonical posture in ADR-024 + this ADR.
4. If the review concludes "stay on Notion," append the rationale to this ADR.

## Consequences

**Positive:**
- The decision is explicit and reviewable. "We chose Notion" carries a list of conditions; future-us can check the list rather than re-arguing from scratch.
- JP's personal subscription absorbing the cost is acknowledged as a real-but-fragile arrangement rather than treated as permanent.
- The Whisper-canonical alternative is named, so when a trigger fires there is a concrete other-option to evaluate against.

**Negative:**
- No active monitoring — triggers fire when noticed, which may lag the actual condition. Quarterly partnership review explicitly asks "any ADR-037 triggers we should consider fired?"

**Operational:**
- ADR-024 stays Accepted (dual capture posture is correct for Stage 1).
- `infra/shadow/whisper/parity_score.md` rolling log feeds Trigger D directly.
