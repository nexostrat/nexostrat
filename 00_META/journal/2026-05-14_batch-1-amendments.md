# 2026-05-14 — Batch 1 amendments executed

## Session shape

Single-purpose session: execute Batch 1 of the audit-amendment plan per `00_META/proposals/2026-05-14_amendments.md`. Ricardo's instruction was direct — "proceed with the next step" — and the CHECKPOINT from the terrain-prep session laid out the exact agenda: spec single-pass edit, ADR bodies, master plan index split, audit-request resolution.

Three commits landed on `main` and pushed to Gitea origin in roughly two hours of focused work. Working tree clean at session end.

## What we built

**Commit `dc5cbec` — Batch 1a spec single-pass amendment.** Edited `00_META/proposals/2026-05-13_nexostrat-system-design.md` in a coordinated pass touching ~14 distinct locations. ADR map: re-statused 005/013/018 to Amended with notes; added rows for ADR-021bis, ADR-036, ADR-037 in the right positions. Spec body: F6 per-user systemd timer pattern (with example `OnCalendar=` blocks for Ricardo and JP); F9 manifest.json schema with mandatory + mode-specific split; F10 persona table reallocation (Founder no longer owns `vault/clients/`; Client-Owner now owns it); F12 root file map `events.json → calendar.json`; F13 Linux Mint recommendation in §5 with explicit macOS-exception path; F17 chat capture rewritten to `/dev/shm` daytime + 23:59 encrypt cron pattern; F19 standardized "12 stations + 3 cross-cutting" everywhere; F22 REVISED — deleted all peripheral n8n references and rewrote ADR-029 to positive framing "Orchestration substrate: Python agents + systemd timers"; R4 CHECKPOINT.md concurrent-session protection note added to §4.10. Brain references stripped from `§1` heading, the path line, and §3 vault discipline. Gitea host port `:3001` made explicit in §1 Network and §5 docker stack listing.

F14-REVISED resolved to a no-op on the spec body: the original §5 cost table already showed Notion at `$0 to firm` (JP's personal subscription absorbing the seat). Saved an edit. Stage 1 envelope stays at $36-91/mo.

**Commit `5f126a7` — Batch 1b new ADR bodies.** Created `00_GOVERNANCE/adr/` (which Plan 01a will populate the rest of) and wrote three ADR bodies:
- **ADR-021bis** — Drop "Hosted" from JP interface options. Closes F27. Explicit supersede of the unformalized "Hosted" option that had appeared in earlier brainstorming without an ADR. JP's interface options are now Heavy and Light only.
- **ADR-036** — Stage 1 surface area: v0 vs v1 fidelity. Closes R3. Enumerates seven features deliberately shipping at v0 fidelity (per-user TZ group briefs, ambient chat extraction, two-tier docs hook automation, parity diff, backup verification, observability, multi-language) with the explicit trigger that moves each to v1. This artifact prevents future-us from re-deriving "is this a v0 or v1 commitment?" every time.
- **ADR-037** — Notion canonical role: Stage 2 review trigger. Closes R5. Records four trigger conditions (cost reversal, client data-residency, JP workflow shift, Whisper parity readiness) and names Whisper.cpp-canonical as the alternative under review. ADR-024 stays Accepted; this ADR sits alongside it as the "when to revisit" anchor.

Each ADR follows the spec-mandated format: Status · Date · Decided by · Context · Options · Decision · Consequences.

**Commit `d5ebbf9` — Batch 1c master plan index split.** Rewrote `00_META/plans/README.md`. Status table reorganized: 01a (due 2026-05-27), 01b (due 2026-06-03), 01c (due 2026-06-10), with a SUPERSEDED row pointing at the original Plan 01 file. Per-plan headers (Goal · Deliverables · Dependencies · Success criteria · Spec references) drafted for 01a/01b/01c reflecting locked audit-amendment decisions — every audit C/F/R item is tagged to one of the three plans. Dependency graph updated: Plan 01c (which tags `v0.1-foundation`, the original Plan 01 milestone) is the new entry-point dependency for Plans 02-04. Original Plan 01 file (`2026-05-13_plan-01-repository-foundation.md`) got a SUPERSEDED banner with do-not-execute warning and pointer to the three replacement plans + replacement-milestones list.

## What the audit-walkthrough work looked like in practice

The amendment plan was already very specific about what to change and where — the walkthrough did the heavy lifting two days earlier. This session was disciplined execution rather than design. The main judgment calls during execution:

1. **ADR-029 reframing.** The original ADR-029 title was "Drop n8n from Nexostrat critical path" and the body contrasted Python+systemd against n8n. Per the no-n8n directive, even peripheral mentions die. Solution: keep the ADR (it documents the substrate decision), rename to "Orchestration substrate: Python agents + systemd timers", and rewrite the body in positive framing — listing why Python is the chosen substrate without contrastive reference. F22 closure mentioned explicitly so the historical record stays traceable.
2. **ADR-021bis naming.** The amendment plan called for "ADR-021bis" but the content (drop Hosted) has nothing to do with ADR-021 (3-bucket grouping). The "bis" name is a placeholder, not a semantic supersede. Placed it in the ADR map immediately after ADR-021 for adjacency; the body explicitly states it supersedes "the unformalized Hosted option, never an ADR" so the record is honest about what's being replaced.
3. **F14-REVISED no-op.** The original F14 amendment direction was to ADD a $10-30/mo Notion AI line to §5 and bump Stage 1 envelope to $46-121/mo. The REVISED direction (per Ricardo's clarification during terrain prep) was the opposite: Notion cost stays $0 to firm because JP's personal subscription absorbs it. When I went to make the F14 edit, I noticed the spec already showed `$0 to firm` and `$36-91/mo` envelope. Original spec was correct; the amendment plan's F14 line was the part that needed to be reversed, not the spec. Saved an edit, captured the no-op explicitly in the spec changelog entry.
4. **`00_GOVERNANCE/adr/` premature creation.** The folder didn't exist yet (it's a Plan 01a deliverable). The three new ADR bodies need to live *somewhere*. Two options: stage in `00_META/proposals/` and move during Plan 01a, or create the final folder now and put them in their final destination. Chose the latter — three files in a folder that Plan 01a will then fill out further is cleaner than a move-later operation that risks broken links.

## Surface-area discoveries

- **Audit-request was already marked RESOLVED.** When I went to apply Batch 1 Step 1e (resolve `2026-05-13_audit-request.md` status), I found the file already carried `Status: RESOLVED 2026-05-14` in its frontmatter from a prior session pass. One less commit. Noted in the task tracker and moved on.
- **The plan's three-commit cadence held.** Spec edit, ADR bodies, master plan index — three commits, each tightly scoped, each independently understandable. The amendment plan's commit cadence (Batch 1 = three commits with one collapsed for the already-done rename) translated cleanly to three actual commits.
- **Per-plan headers replaced the original Plan 01 detail.** The original Plan 01 file had ~28 tasks with ~120 atomic steps. The master plan index now carries three per-plan headers (one per replacement plan) that the writing-plans skill will expand into full task-by-task plans in Batch 2. The original Plan 01 file is retained for historical reference but explicitly marked do-not-execute.

## What's queued for next session (per Ricardo's directive)

**Aurora-styled HTML presentation of the AMENDED design.** Same pedagogical voice as the 2026-05-12 JP v3 cheatsheet. Clean "this is the architecture" doc reflecting all Batch 1 changes — not a diff-style "what changed" doc. Aurora palette (Midnight, Ocean Deep, Sky Blue, Emerald, Amber Gold, Arctic White), Space Grotesk + Manrope + JetBrains Mono typography. Lands at `00_META/proposals/2026-05-XX_nexostrat-presentation.html`. ~2-3 hours focused build.

Batch 2 (write Plans 01a/01b/01c) is also unblocked but queued behind the presentation per Ricardo's sequencing.

## Memory hygiene

No new durable memory entries this session. Existing memories (no Brain refs, drop n8n entirely, Notion via JP personal, user role) were active throughout and informed the spec edits — none needed updating; the spec is now the durable record of those policies.
