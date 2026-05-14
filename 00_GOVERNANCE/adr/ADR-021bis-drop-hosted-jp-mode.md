# ADR-021bis — Drop "Hosted" from JP interface options

**Status:** Accepted
**Date:** 2026-05-14
**Decided by:** Ricardo + Claude (Batch 1 amendments per [`2026-05-14_amendments.md`](../../00_META/proposals/2026-05-14_amendments.md) §F27)
**Supersedes:** The unformalized "Hosted" option that appeared in prior brainstorming around JP's interface choice. There was no prior ADR establishing Hosted; this ADR closes the option explicitly so it cannot reappear by drift.

## Context

Earlier design conversations imagined three modes for JP to interact with Nexostrat: **Light** (Telegram + Gitea web only, zero install), **Hosted** (browser-based `code-server` running on HP, JP edits files in a web IDE), **Heavy** (full local clone + Claude Code + Gemini CLI + age key on JP's laptop). The 2026-05-13 founding spec carried "Hosted" as a passing reference (§5 Stage 2 triggers, §10 Open Items) without an ADR, design, or operational story.

The 2026-05-14 audit (Finding 27) flagged Hosted as a silently-dropped option: it appeared, it had no implementation plan, and no decision was on record to drop it. Walkthrough resolved that Hosted is not a real option for Stage 1.

## Options considered

1. **Drop Hosted entirely** (this ADR). JP's interface options are Light and Heavy only.
2. **Keep Hosted as a Stage 2 trigger** — host `code-server` if JP requests it. Cost: more bot/auth surface, age-key-on-server risk, no validated need.
3. **Defer the decision** — leave Hosted as a placeholder in §5/§10 until JP picks. Cost: drift; the spec carries a phantom option indefinitely.

## Decision

**Drop Hosted entirely.** JP chooses Light (default) or Heavy (when JP is ready). The upgrade path is one-way Light → Heavy; no intermediate hosted-IDE rung exists.

Spec changes (already applied in Batch 1):
- §5 Stage 2 triggers — removed the `code-server ← JP picks Hosted` row.
- §10 Open Items — JP interface choice listed as "(Heavy/Light — Hosted dropped per ADR-021bis)".
- ADR map — this row added.

`infra/machines/` will define only `jp-light.yaml` and `jp-heavy.yaml`; no `jp-hosted.yaml` profile exists.

## Consequences

**Positive:**
- One fewer interface surface to design, document, secure, and operate.
- No browser-based IDE means no age-key-on-server problem to solve (age keys live only on user machines, per ADR-003).
- The Heavy onboarding path stays the single articulated upgrade story; investment concentrates there.

**Negative:**
- If JP ever wants to edit code from a phone or borrowed machine, Light is read-only (Gitea web) and Heavy requires a fresh clone. That gap is acceptable: the firm's day-to-day editing is Ricardo's, and "borrowed-machine editing" is a real but vanishingly rare need.
- A future "managed code-server" decision would require a new ADR and a new threat model.

**Operational:**
- Plan 01c `STATUS.md` template removes any Hosted reference (per amendment plan §F27).
- The 2026-05-12 JP-readable presentations (v2/v3 cheatsheets and Aurora HTML when rebuilt) drop the Hosted column from the comparison.
