# Nexostrat — Skills (Skills-Master bucket)

> **Scope:** the 5 reusable, versioned skills that produce the firm's deliverables.
> **Source of truth:** spec §6 (skills + intake + multi-model), §7 (per-client chain), and JP's pipeline diagram at `00_META/proposals/2026-05-18_jp-diagrama-pipeline.html`.
> **Status (2026-05-18):** all 5 skills are mature and runnable. JP delivered updated content + the new Skill 05 in `SKills updated.zip` on 2026-05-18; integrated into production same day. Test harness: 32 PASS · 0 SKIP · 0 FAIL.

---

## Layout

```
skills/
├── 01_company_analyst/        ← mature · CO (NIT) + MX (RFC) support
├── 02_industry_analyst/       ← mature · reusable per sector · CO + MX
├── 03_competitor_analyst/     ← mature · CO + MX
├── 04_discovery_meeting/      ← mature · "PrepLlamada" / Guía de Preparación · consumes 01+02+03
├── 05_opportunity_report/     ← mature · client-facing deliverable · consumes 01+02+03+meeting-notes
├── shared/                    ← future shared lib (Plan 02/05): scoring.py, judge_prompt.md, anti_hallucination.md
├── 00_META/                   ← persona inbox + journal for Skills-Master
├── CLAUDE.md                  ← Skills-Master persona (Claude)
├── GEMINI.md                  ← Skills-Master persona (Gemini)
└── CHECKPOINT.md              ← session baton
```

**Pipeline order** (per JP's 2026-05-18 diagram — skills run **serially**, with mandatory human review between each):

```
Skill 01 → review → Skill 02 → review → Skill 03 → review → Skill 04 (PrepLlamada)
                                                                  │
                                                                  ▼
                                                      30-min discovery call (recorded)
                                                                  │
                                                                  ▼
                                                          meeting notes
                                                                  │
                                                                  ▼
                                                       Skill 05 (Reporte de Oportunidades)
                                                                  │
                                                                  ▼
                                                  Internal review (Ricardo + JP, mandatory)
                                                                  │
                                                                  ▼
                                                       Manual send to client
                                                                  │
                                                                  ▼
                                                  D+4 business days: auto-follow-up
```

Each mature skill follows the Anthropic Skills convention plus Nexostrat extensions:

```
skills/<NN>_<name>/
├── SKILL.md                   ← prompt + frontmatter (name, description), Anthropic-spec compatible
├── CHANGELOG.md               ← version log per spec §6.3
├── scripts/                   ← extract_financials.py + generate_docx.py (skill-specific)
├── references/                ← sources_guide.md, sector_associations.md, competitor_research_guide.md
└── assets/                    ← Supersociedades XLSX files (01 + 03 only)
```

---

## How to run a skill (Stage 1 — Mode A only)

The five mature skills can be invoked **two ways**. The model is the same; the difference is discoverability.

### Path A — Registered via `.claude/skills/` (auto-discovered by Claude Code)

`.claude/skills/` at the repo root contains symlinks that map each skill's frontmatter `name:` to its source folder:

```
.claude/skills/
├── company-analyst    → ../../skills/01_company_analyst
├── industry-analyst   → ../../skills/02_industry_analyst
├── competitor-analyst → ../../skills/03_competitor_analyst
├── discovery-meeting  → ../../skills/04_discovery_meeting
└── opportunity-report → ../../skills/05_opportunity_report
```

A Claude Code session opened at `/srv/Nexostrat/` auto-discovers these and surfaces them by their frontmatter description. Ricardo invokes naturally:

> *"Analiza la empresa Bodai SAS"* → Claude triggers `company-analyst` skill.
> *"Prepárame para la reunión con Bodai"* → Claude triggers `discovery-meeting` (which validates that 01+02+03 outputs exist).

The description fields use SIEMPRE/Activar phrasing so the trigger surface is broad — see each `SKILL.md` frontmatter for exact activation patterns.

### Path B — Direct invocation (read the SKILL.md and execute)

If you want to run a skill outside an interactive Claude Code session — or you want to invoke from a script — read `skills/<NN>_<name>/SKILL.md` and follow the workflow. The `SKILL.md` is the prompt + runbook; everything needed is in there. Useful for:
- Sub-agent dispatches (the parent passes the SKILL.md path)
- Cron-driven runs (Plan 05's Mode B)
- Debugging a specific run with a controlled prompt version

---

## Canonical output destination (per spec §7)

When running a skill **inside the pipeline of a client**, outputs land at:

```
pipeline/clients/<slug>/<STAGE>/runs/<YYYY-MM-DD_HHMM>_mode-a/
├── final_report.md      ← the report (canonical name)
├── final_report.docx    ← Word version (generated by scripts/generate_docx.py)
└── notes.md             ← optional: operator's qualitative judgment, used for prompt iteration
```

Stage mapping:

| Skill | `<STAGE>` |
|---|---|
| `01_company_analyst` | `01_company_analysis` |
| `02_industry_analyst` | `02_industry_analysis` |
| `03_competitor_analyst` | `03_competitor_analysis` |
| `04_discovery_meeting` | `04_prep_llamada` |
| `05_opportunity_report` | `05_opportunity_report` |

When running **standalone** (no client context), save to the working directory with the skill's documented naming convention (e.g., `Bodai_AnalisisCompania_20260517.md`). Each skill's `SKILL.md` documents its standalone naming in the `SETUP` section.

**Prompt version capture:** the git commit SHA at the time of a run identifies the exact `SKILL.md` version used (ADR-022). Edit `SKILL.md` → commit → run → and the run is permanently traceable. For deliberate prompt iteration, commit the `SKILL.md` change *before* re-running.

---

## The dependency chain (Diagnóstico path)

```
                ┌─► 02 industry_analyst ─┐
01 company_analyst                        ├─► 06 discovery_meeting
                └─► 03 competitor_analyst ┘
                                          │
                                          └─► (Plan 06 → Skill 05 opportunity_report)
```

- **01 company_analyst** reads nothing; pulls financials from `assets/supersociedades_*.xlsx` + does web research; produces 13-section report.
- **02 industry_analyst** can read 01's output to auto-identify the sector; produces 10-section sector report. **Reusable per sector** (~6-12 month vigencia) — cache reports for re-use across multiple prospects in the same sector.
- **03 competitor_analyst** reads 01's output (mandatory); produces 8-section competitive analysis.
- **06 discovery_meeting** reads ALL THREE (01 + 02 + 03); produces a 60-minute meeting script with color-coded sections. **Private — only for Ricardo's use.**

The four together make Ricardo "the most prepared person in the room" before any exploratory call. The pipeline gap is **Plan 06** (Skills 04 + 05) which then convert the discovery-call output into the actual Diagnóstico deliverable.

---

## Anti-hallucination discipline (non-negotiable)

Every `SKILL.md` carries an `## REGLA ANTI-ALUCINACIÓN` block near the top, enforcing:

- If a source is unavailable or returns nothing → write **"No se encontró información en [source name]"** explicitly. Never omit the section.
- Never invent financial figures, market sizes, employee counts, founder names, dates, or competitor data.
- Always cite the source of each datum.
- When data is partial or estimated, mark it explicitly ("se estima entre X y Y según [fuente]").

This block is **required** in every prompt under `skills/<NN>_*/`. A future pre-commit hook (Plan 02) will enforce its presence. The Bodai regression benchmark (Plan 05) measures factual-accuracy drift — a drop blocks commits unconditionally per ADR-022.

---

## Testing

```bash
bash infra/scripts/test_skills.sh
```

8 checks across all 4 mature skills:

| # | Check |
|---|---|
| 1 | YAML frontmatter parses + has `name` + `description` |
| 2 | `.claude/skills/<name>/` symlinks resolve correctly |
| 3 | Every Python script in `scripts/` compiles |
| 4 | Every script path referenced in `SKILL.md` exists on disk |
| 5 | Asset XLSX files present (extract_financials.py dependency) |
| 6 | No stale `/tmp/<skill>/` or `/var/folders/` paths anywhere |
| 7 | `generate_docx.py` smoke test (renders minimal MD → DOCX) per skill |
| 8 | `extract_financials.py` smoke test (not-found path) for 01 + 03 |

Expected output: **27 PASS · 0 SKIP · 0 FAIL** when all deps are installed. Checks gated on `python-docx`, `pandas`, `openpyxl` SKIP-not-FAIL when deps are missing.

**To install all deps:**
```bash
pip install python-docx pandas openpyxl --break-system-packages
```

---

## What's NOT here yet (deferred to later plans)

| Capability | Lands in |
|---|---|
| Mode B (parallel-then-judge via Python agent) | Plan 05 |
| `judge.py` synthesizer (Claude-as-Judge) | Plan 05 |
| Aurora-branded pandoc rendering | Plan 05 |
| `tests/benchmark_input.md` + `benchmark_expected.md` per skill | Plan 05 |
| `skills/shared/scoring.py` regression formula | Plan 05 |
| Bodai benchmark fixture data | Plan 05 |
| Skills 04 (meeting_script) + 05 (opportunity_report) prompts | Plan 06 |
| Pre-commit hook enforcing anti-hallucination block presence | Plan 02 |
| Auto-discovery via `events.jsonl` + skill orchestrator | Plan 07 |
| `/intake`, `/go`, `/stop` Telegram plugins around skills | Plan 04 + Plan 07 |
| `skills/shared/` dedup of generate_docx.py boilerplate | Plan 02 or Plan 05 |

The current scope (post-2026-05-18 JP delivery) makes all 5 skills cleanly runnable today via manual Claude Code invocation. The rest builds on top — none of the deferred items invalidate what's here.

---

## References

- **Founding spec:** [`../00_META/proposals/2026-05-13_nexostrat-system-design.md`](../00_META/proposals/2026-05-13_nexostrat-system-design.md) — §6 (skills), §7 (per-client chain).
- **Master plan index:** [`../00_META/plans/README.md`](../00_META/plans/README.md) — Plans 05 + 06 (skill rollout).
- **Skills-Master persona:** [`CLAUDE.md`](CLAUDE.md) — folder-scope discipline + anti-hallucination rule.
- **ADRs:** 010 (skill model), 012 (folder template), 022 (versioning + benchmark gate), 026 (Mode A/B), 027 (anti-hallucination), 033 (intake 2-file split).
