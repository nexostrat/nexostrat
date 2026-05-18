# Journal — Skill hygiene + DOCX renderer + test harness + .claude/skills registration

> **Date:** 2026-05-17 (second session of the day, started ~17:00 after Plan 01c session ended at 16:56)
> **Persona:** Founder
> **Operator:** Ricardo Mejía Caicedo (via Claude Code at `/srv/Nexostrat/`)
> **Session shape:** Start Session → discussion (test timing + ways to advance faster) → brainstorming on skill testing → audit of the four mature skills → execute (single arc, no sub-agent dispatch) → tests + docs → commit → mirror verification → session-end bookkeeping

## Narrative

This session started as a strategy conversation and turned into a concrete execution arc. The strategy question Ricardo opened with — *"How many sessions are missing from an actual test? Is there a way to advance faster?"* — surfaced that the four mature skills (`01_company_analyst`, `02_industry_analyst`, `03_competitor_analyst`, `06_discovery_meeting`) were probably runnable today rather than waiting for Plans 03/04/05. A `brainstorming` skill invocation against "test if skills are working / what the output is / if it's useful without breaking future architecture" produced a short approach-design (test the existing skills in `Mode A` only, output to canonical `pipeline/clients/<slug>/<stage>/runs/...` per spec §7, defer scoring + Mode B + judge to Plan 05) — at which point Ricardo cut through the design phase: *"We have a company analyst a industry analyst a competitor analyst and discovery meeting can we run them?"*

A quick audit of all four `SKILL.md` files showed they were 95% production-ready but had three classes of debt:
1. **Stale extraction paths.** Skills 02, 03, 06 referenced `/tmp/<skill>/scripts/...` and `/tmp/<skill>/assets/...` — leftovers from the original Anthropic-Skills zip extraction. Skill 01 used `<skill_dir>/scripts/...` placeholders.
2. **Skill 01 had no `generate_docx.py`.** Its `SKILL.md` referenced the Anthropic Skills DOCX bundle at `/var/folders/.../skills/docx/SKILL.md` — a macOS-specific path that doesn't exist on this Linux machine.
3. **No canonical output destination** documented in any of the four SKILL.md files. Outputs would land wherever the operator happened to invoke from, which would fight with `pipeline/clients/<slug>/<stage>/runs/...` later.

Ricardo's response set the standard for the rest of the session: *"Lets fix them once and for all. … Do the whole thing. Do it right. Do it with tests. Do it with documentation. Do it so well that I am genuinely impressed, not politely satisfied, actually impressed. Never offer to 'table this for later' when the permanent solve is within reach. Never leave a dangling thread when tying it off takes five more minutes. … The standard isn't 'good enough' it's 'holy shit, that's done.'"* I locked this verbatim as a permanent feedback memory at `~/.claude/projects/-srv-Nexostrat/memory/feedback_complete_or_nothing.md` so future sessions inherit the principle.

The 12-task plan came together immediately:

1. Read existing scripts to understand them (no edits yet).
2-5. Fix paths in Skills 01, 02, 03, 06 + add Skill 01's missing `generate_docx.py`.
6. Add canonical output-destination stanza (`## SETUP — Destino de outputs`) to all four `SKILL.md` files.
7. Register skills via `.claude/skills/<name>/` symlinks at repo root.
8. Write `infra/scripts/test_skills.sh` with 8 independent checks.
9. Run + iterate until clean.
10. Write `skills/README.md`.
11. Add per-skill `CHANGELOG.md`.
12. Final pass + commit.

The execution was linear (no sub-agent dispatches — this scope was tractable in one direct arc).

### Script analysis (Task 1)

All three `generate_docx.py` scripts (Skills 02, 03, 06) shared ~95% of their code — same brand palette (DARK_BLUE / ACCENT / MID_GRAY / BLACK), same heading typography, same table styling, same shade_cell helper. The differences were cosmetic: title-page default text, footer text, and (Skill 06 only) the blockquote color-coding logic for the meeting-script-specific colored boxes. The Anthropic Skills convention is for skills to be self-contained portable bundles; per-skill scripts match that. Deduping into `skills/shared/docx_renderer.py` would be cleaner architecturally but is out of scope here — explicitly noted in `skills/README.md` as deferred to Plan 02 or Plan 05.

`extract_financials.py` (in Skills 01 + 03) is the same file at both locations and self-locates via `Path(__file__).parent.parent / "assets"`, so it works regardless of the caller's CWD. No path changes needed inside the script — only in the SKILL.md commands that invoke it.

For Skill 01's missing `generate_docx.py`, I modeled it on Skill 02's renderer (most comprehensive) with title page tuned to "Análisis de Compañía" and footer "Análisis Empresarial Interno". The four mature skills now produce a coherent set of outputs with shared brand palette.

### Path corrections (Tasks 2-5)

Mechanical Edit calls:
- **Skill 01:** replaced two `<skill_dir>/scripts/extract_financials.py` references with `skills/01_company_analyst/scripts/extract_financials.py`; replaced both `/var/folders/.../skills/docx/SKILL.md` references (PASO 4b + NOTAS OPERATIVAS) with calls to the new local `scripts/generate_docx.py`.
- **Skill 02:** replaced `/tmp/industry-analyst/scripts/generate_docx.py` with `skills/02_industry_analyst/scripts/generate_docx.py`.
- **Skill 03:** replaced four `/tmp/competitor-analyst/...` references. Also simplified the `extract_financials.py` invocation — the previous SKILL.md passed three explicit args (query + 2 XLSX paths), but the script auto-locates the XLSX files via its self-positioning logic, so only the query arg is needed. SKILL.md updated accordingly.
- **Skill 06:** replaced bare relative `scripts/generate_docx.py` (CWD-fragile — only worked if operator ran from inside the skill folder) with absolute repo-relative `skills/06_discovery_meeting/scripts/generate_docx.py`.

### Canonical output destination (Task 6)

Added a `## SETUP — Destino de outputs` workflow section near the top of each `SKILL.md` (after `## REGLA ANTI-ALUCINACIÓN`, before the first PASO). The stanza documents the spec-§7 canonical destination:

```
pipeline/clients/<slug>/<STAGE>/runs/<YYYY-MM-DD_HHMM>_mode-a/
├── final_report.md
├── final_report.docx
└── notes.md
```

with per-skill `<STAGE>` mapping (01→01_company_analysis, 02→02_industry_analysis, 03→03_competitor_analysis, 06→04_meeting_script — note the 06→04 mapping since the discovery meeting's pipeline-station role is `04_meeting_script`). For standalone invocations the existing per-skill naming conventions (`Empresa_AnalisisCompania_YYYYMMDD.md`, etc.) are preserved. The stanza also documents prompt-version capture via git commit SHA per ADR-022, and (where relevant) flags input dependencies — Skill 03 needs company-analyst output; Skill 06 needs all three prior reports.

### Registration via .claude/skills/ (Task 7)

Created `.claude/skills/` at repo root with four symlinks mapping each skill's frontmatter `name:` to its source folder:

```
.claude/skills/company-analyst    → ../../skills/01_company_analyst
.claude/skills/industry-analyst   → ../../skills/02_industry_analyst
.claude/skills/competitor-analyst → ../../skills/03_competitor_analyst
.claude/skills/discovery-meeting  → ../../skills/06_discovery_meeting
```

Project-scoped (not user-global) — these skills are Nexostrat-specific and shouldn't leak to other projects. `.gitignore` was checked: only `.claude/cache/` is gitignored, so the new symlinks commit cleanly and travel with the repo. Verified each `.claude/skills/<name>/SKILL.md` resolves before moving on.

Effect: a Claude Code session opened at `/srv/Nexostrat/` now auto-discovers all four skills via their `name:` and `description:` frontmatter. Operators trigger naturally — *"analiza la empresa Bodai"* should activate `company-analyst` per its description's "Activar SIEMPRE ante" patterns.

### Test harness (Tasks 8-9)

`infra/scripts/test_skills.sh` — 320 lines, 8 independent checks, layer-aware SKIP for missing deps (matching the `smoke-test.sh` R2 convention):

1. YAML frontmatter parses cleanly + has `name` + `description` + name matches the symlink target.
2. `.claude/skills/<name>/` symlinks resolve to the right source folder.
3. Every Python script in `skills/<NN>/scripts/` compiles via `python3 -m py_compile`.
4. Every `skills/<NN>/scripts/*.py` path referenced in `SKILL.md` exists on disk (regex extracts paths and stats each).
5. Asset XLSX files present where `extract_financials.py` expects them (Skills 01 + 03).
6. No stale `/tmp/<skill>/` or `/var/folders/` paths in any `SKILL.md` (scoped to SKILL.md only — CHANGELOG and README can legitimately reference old paths when documenting fixes).
7. `generate_docx.py` smoke test per skill — renders a minimal MD with h1/h2/h3/bullets/table/bold to a >1 KB DOCX.
8. `extract_financials.py` not-found smoke test for Skills 01 + 03 — queries with a deliberately impossible string and confirms the documented "NO ENCONTRADO EN SUPERSOCIEDADES" path returns.

First run: **27 PASS · 1 SKIP · 0 FAIL.** The SKIP was check [8] gated on `pandas + openpyxl` missing. Per the locked complete-or-nothing standard, that SKIP was a dangling thread — `pip install pandas openpyxl --break-system-packages` (30 seconds) converts it to PASS. Re-run: **27 PASS · 0 SKIP · 0 FAIL.**

Then I caught a regression on the third run: 1 FAIL on check [6]. Cause: the per-skill `CHANGELOG.md` entries I had just written legitimately reference the OLD `/tmp/<skill>/` paths in their descriptions of what was changed, and the grep pattern was scanning all of `skills/` rather than `SKILL.md` only. False positive. Fix: scope check [6] to `skills/*/SKILL.md` and add an inline comment explaining why CHANGELOG + README are excluded. Final result: **27 PASS · 0 SKIP · 0 FAIL.**

### Documentation (Tasks 10-11)

- `skills/README.md` (182 lines): layout map, the two invocation paths (registered via `.claude/skills/` auto-discovery vs direct SKILL.md read), canonical output destination + per-skill stage mapping, the Diagnóstico dependency chain (01 → {02, 03} → 06), anti-hallucination discipline, test command, and the explicit list of what's deferred to Plans 02/05/06/07. The "What's NOT here yet" table is load-bearing — it makes the boundaries between this commit and future plan work explicit so nothing dangles invisible.

- Per-skill `CHANGELOG.md` (4 files): v0.1 entries documenting exactly what changed in this commit. Per ADR-022 the git commit SHA is the authoritative artifact; these files are the human-readable index pointing at it.

### Commit + mirror (Task 12)

Single atomic commit `ab24a0d`: 15 files (4 symlinks + 1 new script + 4 SKILL.md edits + 4 new CHANGELOG.md + 1 README + 1 test harness), 1045 insertions, 24 deletions. Commit message includes verification details + the full deferred-to-future-plans list. Pushed to Gitea origin; mirror cluster (per Plan 01b commit `d38e865`'s systemd path-watcher pattern) propagated to GitHub + Codeberg within 15 seconds. Confirmed via `git ls-remote` against both remotes.

### What did NOT change (the discipline)

I had to resist a few temptations:
- **Touching prompt content.** The 13/10/8/8-section templates and the anti-hallucination blocks are LOCKED — they're what we're testing, not what we're tweaking. Path hygiene only.
- **Building Skill 05.** Tempting to write the opportunity_report prompt while in the zone — but that's Plan 06 work, not skill-hygiene scope. Deferred explicitly.
- **Deduping `generate_docx.py` into `skills/shared/`.** ~95% of the code is identical across 4 skills. The architecturally clean answer is a shared library. But that's a new architectural decision (per-skill self-contained vs shared lib) that deserves its own thinking + the `skills/shared/` folder convention isn't established yet. Deferred to Plan 02 or Plan 05 with an explicit note in README.

## Decisions locked

1. **Per-skill self-contained scripts.** Anthropic Skills convention preserved. `skills/shared/` dedup deferred. Trade-off accepted: ~95% code duplication across 4 `generate_docx.py` variants.

2. **Project-scoped registration (`.claude/skills/`)** rather than user-global (`~/.claude/skills/`). Nexostrat-specific skills shouldn't leak to other projects on Ricardo's machine.

3. **Canonical output destination = `pipeline/clients/<slug>/<STAGE>/runs/<TIMESTAMP>_mode-a/final_report.{md,docx}`** for pipeline runs; per-skill conventional naming for standalone runs. Documented in the `## SETUP — Destino de outputs` stanza in each SKILL.md.

4. **`SKILL.md` is the runtime artifact** — that's where stale paths bite. CHANGELOG + README can legitimately reference old paths when documenting fixes. Test check [6] scoped accordingly.

5. **Complete-or-nothing standard locked permanently** as `~/.claude/projects/-srv-Nexostrat/memory/feedback_complete_or_nothing.md`. The memory cites the exact phrasing Ricardo used so future sessions inherit the principle without paraphrase drift.

## What this unlocks

The four mature skills are now production-runnable today. The natural next concrete step — *test them on a real Colombian company* — has nothing structural in its way. Ricardo just needs to pick a target (Bodai is the architectural placeholder name with no real data loaded; alternatives include a real prospect or a random Supersociedades pick that becomes the permanent benchmark fixture).

This also opens a path-choice for the next session that wasn't on the table this morning:
- **Path A:** Plan 02 brainstorm (documented default, FOSS docs stack picks, load-bearing per ADR-038).
- **Path B:** Skill-chain test on a real company (newly unblocked, answers the "are the skills useful?" question with ground truth before more infrastructure investment).

Both paths are open. Plan 02 doesn't gate on the skill-chain test, and the skill-chain test doesn't gate on Plan 02 — they're parallel. The decision is whether to validate the skills' output quality before investing in the docs stack, or build the docs stack while skills sit untested. Ricardo picks at next session start.

## Side-effects worth noting

- `pip install pandas openpyxl --break-system-packages` was run on `ricardo-hp-laptop` to enable check [8] of the test harness. Both packages are now system-installable (broken into the OS Python by `--break-system-packages`). This is consistent with the per-skill `pip install python-docx --break-system-packages -q` patterns documented in SKILL.md files; the deps are runtime requirements for the skills' scripts.

- The brainstorming skill was invoked early in the session for "test design" but didn't reach its terminal state (writing a design doc + invoking writing-plans). Ricardo's mid-flow direction ("can we run them? … fix them once and for all") superseded the brainstorming flow's HARD-GATE per CLAUDE.md priority order: user's explicit instructions > skill defaults. The brainstorm's intermediate outputs (the audit + three-approach analysis + recommended path) fed directly into the execution plan, so nothing was wasted.

- This is the SECOND session of the day. The first (Plan 01c execute) ended at 16:56 with `CHECKPOINT.md` rewritten for Plan 02 brainstorm-next. This session's CHECKPOINT.md will rewrite that baton to reflect today's new state.

## Files changed (this session)

- `.claude/skills/company-analyst` (new symlink → `../../skills/01_company_analyst`)
- `.claude/skills/industry-analyst` (new symlink → `../../skills/02_industry_analyst`)
- `.claude/skills/competitor-analyst` (new symlink → `../../skills/03_competitor_analyst`)
- `.claude/skills/discovery-meeting` (new symlink → `../../skills/06_discovery_meeting`)
- `infra/scripts/test_skills.sh` (new, 320 lines, executable)
- `skills/01_company_analyst/SKILL.md` (path fixes + SETUP stanza + DOCX call corrected)
- `skills/01_company_analyst/scripts/generate_docx.py` (new, 339 lines, executable, modeled on Skill 02's renderer)
- `skills/01_company_analyst/CHANGELOG.md` (new, v0.1 entry)
- `skills/02_industry_analyst/SKILL.md` (path fix + SETUP stanza)
- `skills/02_industry_analyst/CHANGELOG.md` (new, v0.1 entry)
- `skills/03_competitor_analyst/SKILL.md` (path fixes + simplified extract_financials call + SETUP stanza)
- `skills/03_competitor_analyst/CHANGELOG.md` (new, v0.1 entry)
- `skills/06_discovery_meeting/SKILL.md` (path fix + SETUP stanza)
- `skills/06_discovery_meeting/CHANGELOG.md` (new, v0.1 entry)
- `skills/README.md` (new, 182 lines)
- `~/.claude/projects/-srv-Nexostrat/memory/feedback_complete_or_nothing.md` (new feedback memory, also linked in MEMORY.md index)

Plus session-end bookkeeping (this commit):
- `STATUS.md`
- `tasks.json`
- `CHECKPOINT.md`
- `00_META/journal/2026-05-17_skill-hygiene.md` (this file)
- `00_META/CHANGELOG.md`

## For a future auditor

If you're reading this trying to understand the state of the skills as of `v0.1-foundation` + commit `ab24a0d`: the four mature skills are runnable today via Claude Code, with outputs landing at the canonical pipeline destination per spec §7. The contract is documented in `skills/README.md` and validated by `infra/scripts/test_skills.sh`. Path hygiene is the only thing fixed; prompt content is unchanged. Mode B / judge.py / scoring.py / Aurora render / benchmark fixtures all land in Plan 05. Skills 04 + 05 prompts land in Plan 06.

The complete-or-nothing standard locked this session applies to all future work unless explicitly scoped down — see `~/.claude/projects/-srv-Nexostrat/memory/feedback_complete_or_nothing.md`.
