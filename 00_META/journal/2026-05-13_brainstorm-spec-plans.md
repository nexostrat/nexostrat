# 2026-05-13 — Founding spec + master plan index + Plan 01 in detail

**Session type:** brainstorm + design + plan writing (no execution)
**Duration:** long; multi-turn brainstorming with sequential clarifying questions
**Agent:** Claude Code (Opus 4.7, 1M context) launched from `/srv/brain/`
**Output location:** `/srv/Nexostrat/` (own repo, separate from personal Brain)
**Working tree at session end:** clean; all changes committed

## What was done

Took Nexostrat from "a folder with founding docs + proposals from prior sessions" to "fully designed system with the first plan ready to execute, gated on a hard audit."

The full arc of the session:

### Phase 1 — discovery + scope confirmation (early turns)

- Found the Nexostrat folder on /srv (capital N), inspected its existing content (Plan Maestro × 3, Consultoria PDF, brand pivot artifacts, 20-ADR system design from 2026-05-11, JP v3 presentation HTML).
- Cleaned up the working tree from the prior session: unzipped Files.zip and company-analyst.skill.zip, verified MD5 duplicates, deleted them, extracted skill bundles to `00_META/skills/`, moved logo to dated naming convention. Committed as `20af199`.
- Verified the JP-approved architecture from the 2026-05-11 spec and the 2026-05-12 v3 HTML cheatsheet.
- Confirmed brand: Nexostrat (Ricardo's pick, 8/10), Aurora palette (Midnight / Ocean Deep / Sky Blue / Emerald / Amber Gold / Arctic White).
- Email: `contacto@nexostrat.com`. Configured per-repo git author for the Nexostrat repo (no impact on personal Brain).

### Phase 2 — brainstorming (the 5 clarifying questions + 4 cross-cutting additions)

Per the `superpowers:brainstorming` skill, one question at a time:

1. **Replication topology** — Warm-standby chosen. HP stays the live server; a second laptop holds idle docker-compose + nightly rsync of `/srv/Nexostrat/`; manual SSH failover 15-30 min via Tailscale routing flip. Data redundancy already triple-mirrored via git (Gitea origin + GitHub mirror + Codeberg mirror).

2. **Meeting capture** — Dual capture for internal R+JP meetings (Notion AI = canonical + Jitsi/Whisper shadow with n8n-style parity diff). Single canonical (Notion AI) for client meetings. Ricardo's call validated by the dual-tools shadow eat-your-own-dogfood strategy already adopted for everything else.

3. **Multi-model investigation** — Parallel-then-judge. Three models (Claude API + Gemini API + xAI Grok API) get same prompt + intake; three raw outputs land in `runs/<date>_<mode>_v<N>/raw_outputs/`; Claude-as-Judge synthesizes a final report flagging disagreements explicitly + comparing to hypotheses. Same pattern that worked for the brand tournament.

4. **Intake isolation** — 2-file split: `research_input.md` (slices 1+2 — public facts + private context, both fed to research) + `our_hypotheses.md` (slice 3 — sealed during research, read only at synthesis). The "people opinion" question Ricardo raised got resolved by slicing: factual people-context goes into research_input.md (feeds the AI's understanding), judgment-about-people goes into our_hypotheses.md (sealed until synthesis). Insight unlocked: the opinion section is VERY valuable when sliced; the bias problem only exists when you lump factual context with judgment.

5. **Two-tier documentation format** — Paired files (`X.md` technical + `X-explicado.md` plain) with tiered scope (only JP-facing docs get pairs; code-level CLAUDE/GEMINI/SKILL.md stay single-file). Gitea pre-receive hook flags drift. Later in the session Ricardo confirmed JP reads English fine, so both versions stay English (the "easier" tier is shorter and plainer, not Spanish-translated).

### Phase 3 — cross-cutting additions (driven by Ricardo's catches)

Mid-design, Ricardo surfaced four additional concerns that demanded their own design:

- **CHECKPOINT.md per persona** (Section 4.10) — closes the session-continuity gap. Bigger than STATUS.md / journal / tasks.json because it answers "where exactly did I leave off" at the level of "which command to run next." Required at session end; read first at session start. Mode B writes it automatically when a pipeline pauses awaiting review.

- **Unified inbox** (Section 4.11) — Telegram capture + manual memos converge to a single primitive at `<scope>/00_META/inbox/`. Bot writes; personas read at session start; Ollama auto-resolves simple questions during office hours; API fallback when desktop asleep.

- **Per-user timezone-aware delivery scheduling** (Section 10.8) — JP in Bogotá, Ricardo in Tijuana. Each user has `infra/telegram/users/<userid>.yaml` with TZ, working hours, quiet hours per tier, morning-brief time. `delivery_flush.py` daemon (every 5 min) routes deferred messages. Tier 1 (critical) overrides all preferences; `/emergency` lets either founder force-escalate.

- **Ambient chat extraction** (Section 8.10) — bot saves every Telegram message (encrypted), Ollama on desktop (every 4h office hours) extracts tasks/dates/decisions, threaded confirmation loop, wake-on-LAN for queued jobs. Sensitive-content filter skips secrets / PII / medical content.

Plus one substantive architectural revision mid-design when Ricardo asked **"why n8n and not a Python script made by Claude?"**:

- **ADR-029 — Drop n8n from Nexostrat critical path.** The n8n choice was a reflex (already running for AttenBot). On reflection, Python + systemd timers is meaningfully better for: maintainability, AI-authorship, testing, debugging, version control, no vendor lock-in, no UI-vs-JSON drift. The two n8n advantages (visual UI for non-coders, prebuilt integrations) collapse because (a) JP doesn't open the n8n UI, (b) the 4-5 APIs we call are ~30 lines of SDK each. n8n keeps running for AttenBot at `/srv/atten-bot/`; Nexostrat doesn't add new dependencies on it. This was the most important course-correction of the day.

### Phase 4 — founding spec written

10 sections covering every aspect of the architecture, 15 new ADRs (021-035), 60 KB, zero placeholders. Self-reviewed for placeholders / consistency / cross-references / contradictions. Committed as `493d0b4` to Nexostrat repo.

### Phase 5 — master plan index + Plan 01 in detail

Per `superpowers:writing-plans` skill, decomposed the spec into 10 implementation plans:

1. Repository Foundation (~1 week)
2. Documentation System (~3 days)
3. events.jsonl + Python agent framework (~1 week)
4. Telegram Bot + Unified Inbox (~1 week)
5. Skill 1 End-to-End (~1 week)
6. Skills 2-5 (~2 weeks)
7. Per-Client Chain + Pipeline Orchestrator (~1 week)
8. Meeting Pipeline (~1.5 weeks)
9. Ambient Chat Extraction (~3 days)
10. Observability + Go-Live (~3 days)

Total ~7-9 weeks of one-operator effort. Plans 02-10 are written just-in-time (not pre-written today) because tool versions and lessons learned will invalidate any plan written 8 weeks before execution.

Plan 01 written in full task-by-task TDD detail: 28 tasks across 12 phases (~120 atomic steps each 2-5 min). Self-reviewed, one fix applied (removed dangling `hp_down_failover.sh` from file map — it's Plan 04 deliverable). Committed as `05ee016`.

### Phase 6 — session-end discipline

When the moment came to either execute Plan 01 in this session OR end cleanly, Ricardo chose to end cleanly. **This validates the CHECKPOINT pattern as more than an abstract design — it's now the first thing the next session will read.**

Then Ricardo added a strong improvement: before executing Plan 01, do a **hard architectural audit** of today's work. Discipline: audit catches design issues cheaply (~30 min); same issue caught mid-Plan-01 execution is hours of rework or, worse, silently propagates into Plans 02-10. Ricardo's proposed order — audit → presentation → Plan 01 — is the correct sequence.

The audit request brief lives at `00_META/proposals/2026-05-13_audit-request.md` with the full scope, two methodologies (risk-auditor agent vs fresh adversarial Claude session), and the required output format.

## Decisions made

| Decision | Source |
|---|---|
| Warm-standby (not hot-standby; not git-only) | Q1 |
| Dual meeting capture for internal; single canonical for client | Q2 |
| Parallel-then-judge multi-model | Q3 |
| 2-file intake (sealed hypotheses) | Q4 |
| Paired-file docs, English/English, tiered scope | Q5 |
| Ollama on desktop (hybrid), HP for orchestration | Topology revision |
| 3-bucket grouping (Skills/Pipeline/Operations) | Ricardo's catch — ADR-021 supersedes ADR-009 |
| Dual-mode pipeline (Manual + API, same contract) | Ricardo's parallel-modes ask — ADR-022 |
| Drop n8n; Python + systemd | Ricardo's sharpest question — ADR-029 |
| CHECKPOINT pattern per persona | Ricardo's continuity ask — ADR-031 |
| Unified inbox | Ricardo's inbox ask — ADR-032 |
| Per-user TZ scheduling | Ricardo's TZ ask — ADR-030 |
| Plans 02-10 just-in-time | session-continuity reasoning |
| Hard audit before Plan 01 execution | Ricardo's final ask |
| Aurora palette + Space Grotesk/Manrope/JBM typography | locked per ADR-033 |

## Open items

- **Hard audit** of today's three artifacts before Plan 01 execution (CRITICAL — gates everything).
- **Aurora-styled user-friendly presentation** of the design after audit passes (HIGH — JP-readable reference).
- **Execute Plan 01** after audit + presentation done (CRITICAL — gated).
- **Write Plan 02 in full detail** after Plan 01 done (HIGH — via writing-plans skill).
- 3 decision points for Plan 01 to be answered at next-but-one session (when Plan 01 actually starts executing): standby host hostname/IP, GitHub username (recommend `<your-handle>/nexostrat` private), age key passphrase yes/no (recommend yes per spec).

## Files written this session

To `/srv/Nexostrat/` (own repo):

**Commit 20af199** — Session cleanup:
- 22 files: extracted 4 skill bundles to `00_META/skills/`, moved logo, added `.gitignore`, deleted Files.zip + company-analyst.skill.zip + excalidraw.log, appended CHANGELOG entry.

**Commit 493d0b4** — Founding spec:
- 1 file (954 lines, 60 KB): `00_META/proposals/2026-05-13_nexostrat-system-design.md`

**Commit 05ee016** — Master plan index + Plan 01:
- 4 files (4069 lines total):
  - `00_META/plans/README.md` (master index, 440 lines)
  - `00_META/plans/README-explicado.md` (67 lines)
  - `00_META/plans/2026-05-13_plan-01-repository-foundation.md` (3462 lines, Plan 01 full detail)
  - `00_META/plans/2026-05-13_plan-01-repository-foundation-explicado.md` (100 lines)

**Commit at session end** — Session wrap:
- `00_META/proposals/2026-05-13_audit-request.md` (audit brief for next session)
- `00_META/journal/2026-05-13_brainstorm-spec-plans.md` (this file)
- `CLAUDE.md` (rewritten as Nexostrat Founder per Plan 01 Task 18, done early to give next session correct persona context)
- `STATUS.md` (rewritten — pre-audit state)
- `tasks.json` (rewritten — removed completed JP vote + Founding Meeting; added audit/presentation/Plan-01 tasks)
- `00_META/CHANGELOG.md` (session entry appended)
- `CHECKPOINT.md` (created — Founder baton with audit-first sequence)

Zero commits to `/srv/brain/`. Clean repo separation maintained throughout.

## Notes for next session

- Open Claude Code AT `/srv/Nexostrat/` (not `/srv/brain/`). The CHECKPOINT.md baton fires the safety net.
- Sequence is locked: **audit first**. Don't skip. The audit-request brief (`00_META/proposals/2026-05-13_audit-request.md`) has the full scope + methodology + output format.
- After audit verdict:
  - GREEN → presentation session, then Plan 01.
  - YELLOW → apply amendments first, then re-audit if many, then presentation, then Plan 01.
  - RED → stop, surface to Ricardo, possibly redesign.
- The architecture intentionally biases toward completeness over minimalism (per Ricardo's "marginal cost of completeness near zero with AI" principle). Don't let the auditor mis-flag this as over-engineering.
- The single biggest risk surface in today's work is probably the **per-user TZ scheduling** (lots of edge cases) and the **CHECKPOINT pattern enforcement** (the hook needs to refuse empty checkpoints — does the schema validator catch all corruption modes?). Audit those harder than others.

## What I'd do differently

Nothing material. The sequence "brainstorm → spec → plans → audit → execute" is the right discipline. The hard-audit gate before execution was Ricardo's catch and it elevates the rigor meaningfully.

One small thing: the founding spec is 60 KB. It's at the upper limit of what's comfortable to re-read end-to-end in a single session. Future foundational sessions should aim for spec ≤ 40 KB by being more decisive in cuts. Not changing today's spec — it's appropriate for what it covers — just a discipline note for future similar work.
