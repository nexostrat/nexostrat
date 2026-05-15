# ADR-038 — Drop Notion at firm level; FOSS self-hosted replacement deferred to Plan 02 brainstorm

**Status:** Accepted
**Date:** 2026-05-15
**Decided by:** Ricardo + Claude (this session, in the JP-Light onboarding refinement that followed JP's Signal confirmation of macOS Sequoia + Light-mode preference)
**Supersedes:** Notion-canonical posture in ADR-024 (Dual meeting capture); Stage 2 review framing in ADR-037 (Notion canonical role) — see § Supersession scope.

## Context

The 2026-05-13 founding spec wove Notion into the architecture in four roles:

1. **Meeting capture canonical** (ADR-024) — Notion AI for both internal R+JP meetings and client meetings; Jitsi/Whisper as parity shadow.
2. **CRM** (spec §6) — `clients/` database with phase tracking, KPIs, contact history, recording preferences.
3. **Shared collaborative docs workspace** for Ricardo + JP — content too dynamic for git but accessible to both founders.
4. **Cost arrangement** — $0 to the firm: JP's personal Notion AI subscription absorbed the seat (per amendment F14 + project memory `notion-via-jp-personal`).

The 2026-05-14 audit's Recommendation 5 surfaced fragility: cost-flip is structurally weak; data-residency posture has client-audit risk; JP-personal coupling is operationally unsound at scale. ADR-037 captured the fragility as a Stage 2 review trigger with four named conditions (cost reversal, residency risk, JP workflow drift, parity-score-meeting-readiness).

This session: Ricardo elected to **act on the fragility now rather than wait for Stage 2**, and additionally elected to **lean heavily on self-hosted free-open-source solutions** in place of any SaaS alternative. This ADR records that decision and scopes the consequent re-design.

## Decision

**Notion exits the Nexostrat architecture at the firm level.**

- No firm-paid Notion subscription, ever.
- No firm-canonical reliance on JP's personal Notion subscription. If JP keeps Notion personally for his own use, that is his choice and outside the firm's scope.
- The previously-issued invite from JP's "Nexostrat" Notion workspace to `contacto@nexostrat.com` will not be accepted; the workspace is JP-personal going forward.

**All four roles Notion was filling get reassigned to FOSS self-hosted solutions.** The specific tooling choices are **deferred to a brainstorm at the start of Plan 02 (Documentation System)**, with the explicit constraint: **all options open** — no pre-commit to a specific FOSS stack at this time.

Candidate FOSS solutions to be evaluated during the Plan 02 brainstorm (non-exhaustive, no preference implied):

| Notion role | Candidate FOSS replacements |
|---|---|
| Meeting capture / transcription | Whisper.cpp (already in stack as shadow per ADR-024), Jitsi local recording, self-hosted Meet, etc. |
| Summary generation | Ollama (already in stack per ADR-026/034) with local LLMs, or external-cheap-API fallback |
| CRM | EspoCRM, SuiteCRM, Krayin, Twenty (FOSS+self-host), Vikunja+custom, or build minimal on top of SQLite + Gitea Issues |
| Collaborative docs workspace | AppFlowy, Outline, BookStack, AFFiNE, Wiki.js, Logseq, Trilium, HedgeDoc, or Gitea Wiki (already in stack) |
| Dashboard / reports for JP | Grafana, Metabase, custom HTML+Telegram digest, or whatever the docs-workspace tool can render |

The Plan 02 brainstorm will select one or several (or others not listed) to cover the four roles. It will also decide whether one tool covers multiple roles (e.g. AppFlowy for both docs + meeting summaries) or whether specialized tools are preferable.

## Supersession scope

- **ADR-024 (Dual meeting capture: Notion AI canonical + Jitsi/Whisper shadow):** Notion-canonical posture is superseded. The shadow-capture infrastructure (Jitsi + Whisper) is **promoted to canonical pending Plan 02 brainstorm.** If Plan 02 elects a different capture solution, a new ADR will supersede this interim posture.
- **ADR-037 (Notion canonical role: Stage 2 review trigger):** Superseded. The review the ADR scheduled is happening now (Stage 1 immediate) rather than at Stage 2. The triggers ADR-037 named (cost flip, data residency, JP workflow, parity score) become irrelevant because the canonical-Notion posture they were defending is itself withdrawn.
- **Spec §5 cost table:** Notion line item removed. Amendment F14 (which budgeted $10-30/mo for Notion AI add-on) and its memory companion (`notion-via-jp-personal`) are reversed; the Stage 1 envelope returns to the pre-F14 figure or lower (FOSS + existing self-hosted infra is approximately $0 incremental for Stage 1).
- **Spec §6 storage hierarchy + client CRM, §8 service contracts (`notion.*` references), §10 failure modes (Notion API down):** Pending re-pass via `t-spec-notion-removal-amendment` — a single-pass spec/plan touchup commit scheduled between Plan 01c execution and Plan 02 writing.
- **Project memory `notion-via-jp-personal`:** Invalidated; replaced by `project_no_notion.md` recording this decision.

## JP-Light variant (companion decision, same session)

Folded in for memorialization without promoting to its own ADR (config decision, not architectural):

JP's specific Light-mode configuration **opts out of Gitea web access** (he wants results, not architecture browsing). His interface is therefore strictly: Telegram bot + email/report digests + the FOSS dashboard chosen in Plan 02. Spec's generic Light-mode definition ("Telegram + Gitea web only") is unchanged — this is a JP-specific config variant. If JP's posture shifts later, his Gitea user can be created in ~10 minutes server-side; no architectural change required.

## Consequences

**Positive:**
- No firm-paid SaaS subscriptions. Stage 1 cost envelope returns to its lower bound (or below).
- No structural dependency on JP's personal Notion subscription.
- No third-party data processor holding client meeting transcripts — data residency posture improves materially.
- Full architectural sovereignty: all infrastructure FOSS + self-hosted; no vendor lock-in.

**Negative:**
- **Build cost increases.** Notion AI provided polished summaries + database UI + collaborative editing out of the box. The FOSS replacements require self-hosting infra, more configuration, more glue code. Plan 02 onwards absorbs this work.
- **Quality lag risk.** Whisper.cpp Spanish transcripts at CPU speed take real-time to ~1.5x; self-hosted summary pipelines (Ollama, etc.) are less polished than Notion AI's default output. Plan 02 onwards must close this gap or accept it.
- **JP-onboarding simplifies** (one less account, no Notion invite, no Gitea web) but **the architecture work to build the Notion-role replacements is non-trivial** — Plan 02 scope increases materially.

**Operational (immediate, this session):**
- `t-ricardo-jp-onboarding-actions` — closed (Gitea postponed indefinitely; Notion cancelled; GitHub already done).
- `t-foss-docs-stack-decision` — opened, deferred to Plan 02 brainstorm.
- `t-spec-notion-removal-amendment` — opened, single-pass touchup scheduled between Plan 01c and Plan 02.
- `t-macos-deviation-decision` — closed (JP-Light moots the Heavy-on-macOS adaptation work).
- Memory `notion-via-jp-personal` deleted; replaced with `no-notion`.

**Operational (downstream):**
- Plan 02 brainstorm becomes load-bearing — its outcome unlocks meeting capture, CRM, and collaborative docs as built capability. Plan 02 cannot be skipped or compressed.
- ADR-024 + ADR-037 carry "superseded by ADR-038" status notes during the spec touchup pass.
- The `t-spec-notion-removal-amendment` commit will produce a single coherent diff against spec + plans, similar in shape to the Batch 1a single-pass amendment commit (`dc5cbec`).

## Reviewable

This decision is not reviewable in the same conditional sense as ADR-037. Notion is structurally out. A future "bring Notion back" decision would require a new ADR superseding this one with the same level of justification (specific incident + cost-benefit + alternative-cost analysis showing FOSS gap).

If a Plan 02 brainstorm concludes "no FOSS stack adequately covers Notion's role for X reason," the response is to **either accept that gap or pay for a non-Notion paid alternative** (e.g. a different SaaS or a paid FOSS-hosting service), not to revert this decision quietly.
