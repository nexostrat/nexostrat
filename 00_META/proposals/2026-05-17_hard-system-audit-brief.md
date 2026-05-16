# Hard system audit — Nexostrat v0.1a-foundation

> **Status:** BRIEF — written 2026-05-16 at Ricardo's request to set up the next session's auditor.
> **Auditor scope:** end-to-end gap audit of the built system against every "source of truth" we have. Verify that what we PLANNED/PROMISED is what we BUILT. Pinpoint divergences. Recommend fixes.
> **Audit run target:** 2026-05-17 / 2026-05-18 / 2026-05-19 (whenever Ricardo opens the next session).
> **Auditor identity:** dispatched general-purpose agent with risk-auditor persona inlined (same pattern as the 2026-05-13 founding-spec audit and the 2026-05-14 Plan 01a re-audit).
> **Auditor's deliverable:** report at `00_META/proposals/2026-05-17_hard-system-audit-report.md` (this filename whatever date the run happens — adjust the YYYY-MM-DD prefix accordingly).

---

## Why this audit exists

We have just landed `v0.1a-foundation` (commit `acdcc4a`, 2026-05-16). Plan 01a built scaffold + identity + crypto + machine profiles + partnership + JSON schemas. Plans 01b (mirrors + warm-standby) and 01c (personas + hooks + integration test) are written but not executed. Plans 02-10 are master-index headers only.

Before charging into Plan 01b execution, Ricardo wants an **independent gap audit** to verify:

1. **Documentation ↔ implementation match.** The founding spec, ADRs, Plan 01a, and the 2026-05-14 presentation say a lot of things. The repo state on disk is the reality. Where do the words and the bytes disagree?

2. **Cross-document coherence.** Spec vs Plan 01a vs presentation vs ADRs — do they tell the same story, or has drift accumulated across the rewrites and amendments?

3. **Honest production-readiness.** What would actually need to happen for Stage 1 launch (2026-06-30 to 2026-07-15)? Are we tracking toward that, or are there gaps we have not surfaced?

4. **Specific risk areas.** Calibrate against the deferred items from this session, the ADR-038 Notion drop, the brothers-as-partners ceremony reduction, and the JP-Light mode default.

The goal is **decision-grade evidence** for what to fix, what to amend, what to accept. The previous audits (2026-05-14 founding-spec, 2026-05-14 Plan 01a) followed this pattern and shipped patches inline; this one is broader and may surface architectural-level adjustments.

---

## Sources of truth (in authority order)

When two sources disagree, the auditor uses this hierarchy to decide which one is authoritative — and the OTHER one needs to be patched, NOT the source of truth.

1. **ADRs** (`00_META/proposals/2026-05-13_nexostrat-system-design.md` § ADRs 001-037 + ADRs 021bis / 036 / 037 / 038 if referenced in the spec body). These are the load-bearing architectural decisions; if the spec body contradicts an ADR, the ADR wins.
   - Note: ADR-038 (Notion drop, 2026-05-15) is currently captured in `MEMORY.md` (auto-memory) and in feedback files at `/home/ricardo/.claude/projects/-srv-Nexostrat/memory/`, NOT yet in the spec body. The single-pass amendment `t-spec-notion-removal-amendment` is the scheduled fix.

2. **Founding spec body** (`00_META/proposals/2026-05-13_nexostrat-system-design.md` — the 10-section design doc). Architecture decisions, deliverables, success criteria, failure modes. Amendments documented in `00_META/proposals/2026-05-14_amendments.md`.

3. **Plan 01a** (`00_META/plans/2026-05-14_plan-01a-foundation.md`). The execution plan that produced v0.1a-foundation. Patched 2026-05-14 by the re-audit; verified by `00_META/proposals/2026-05-14_plan-01a-patch-verification-trail.md`.

4. **CLAUDE.md** (`/srv/Nexostrat/CLAUDE.md`). The Founder persona's operating contract. References spec, plans, and CHECKPOINT.md.

5. **2026-05-14 presentation** (`00_META/proposals/2026-05-14_nexostrat-presentation.html`). The public-facing communication of what we're building. Test companion at `2026-05-14_nexostrat-presentation.tests.md` documents validation checks.

6. **Repo state on disk** (everything in `/srv/Nexostrat/`). The reality. What's actually built, what's tracked in git, what's running.

7. **Auto-memory** (`/home/ricardo/.claude/projects/-srv-Nexostrat/memory/`). Locked feedback principles, project facts, references. Lives outside the repo but governs how Claude operates.

---

## What's NOT yet built (calibrate expectations)

This is the realistic state at v0.1a-foundation. The auditor should NOT flag these as defects unless the spec/plan/presentation MISLEADS about their existence. They are correctly absent.

- **Plan 01b artifacts:** GitHub mirror + Codeberg mirror + warm-standby clone + Drive 2TB heavy-asset upload flow.
- **Plan 01c artifacts:** Skills-Master + Client-Owner personas (`skills/CLAUDE.md`, `pipeline/CLAUDE.md`), SessionStart hook, Stop hook, events.jsonl router daemon, integration smoke test.
- **Plan 02-10 artifacts:** all of them. Documentation system (Plan 02), event router (Plan 03), Telegram bot (Plan 04), Mode B Skills (Plan 05), Client-Owner flow (Plan 06), Bodai benchmark (Plan 07), heavy-asset Drive integration (Plan 08), Plan 09 / Plan 10.
- **JP-side roundtrip + sentinel cleanup** (tracked in `t-plan-01a-jp-and-tty-deferred`).
- **TTY-required tests** (run-with-secrets.sh leak test, secrets.env.age decrypt verify, full Plan 01a Task 18 rerun).
- **Single-pass amendments** (`t-spec-notion-removal-amendment`, `t-plan-01a-text-amendments`, `t-spec-cost-table-amendment`).

If the presentation or spec implies any of these is DONE, that's a finding. If they correctly label them as planned/future, no finding.

---

## Specific risk areas to probe

These are concrete things the auditor should check. Not exhaustive — the auditor is encouraged to find issues beyond this list.

### A. Cross-document coherence

- **Personas (ADR-011):** spec says 3 personas — Founder, Skills-Master, Client-Owner. Currently only the Founder `CLAUDE.md` exists. Does Plan 01a correctly defer the other two to Plan 01c? Does the presentation correctly label personas as planned vs implemented? Does CLAUDE.md mention the gap?

- **events.jsonl (ADR-013):** spec says append-only event log is THE cross-persona primitive. Currently does not exist (Plan 03 territory). Does Plan 01a / 01b / 01c reference it correctly? Does the presentation imply it exists?

- **No-n8n rule (ADR-029 + 2026-05-14 directive).** Any residual n8n reference anywhere? In spec, plans, ADRs, presentation, machine YAMLs?

- **No-Brain-references rule (2026-05-14 directive).** Any residual `/srv/brain` mention? Any pointers to Brain templates, scripts, or paths? Brain is a completely separate entity.

- **Notion drop (ADR-038, 2026-05-15).** Notion references should be PRESERVED in plan-prescribed slots awaiting the single-pass amendment, but should NOT appear in NEW artifacts. Confirm: `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md` (Task 17 reframed, this session) introduces ZERO new Notion references. Confirm the existing references in `cost-sharing-agreement.md`, `ROLES.md`, `_template/README.md`, `MANIFEST.md`, `secrets.env.age`, `infra/machines/hp-server.yaml` are documented for the upcoming sweep but not silently growing.

- **Brothers-as-partners ceremony reduction (`feedback_prefer_architecture_over_ceremony.md`, 2026-05-16).** Task 17 reframed dropped the signed PDF + sensitive_index row. Confirm the markdown PARTNERSHIP_AGREEMENT.md captures the substantive terms faithfully. Confirm `vault/sensitive_index.md` is still a valid template (it should remain as-is for future external-need artifacts). Confirm the F5 audit finding is now closed via "alternate satisfaction" in a way the spec body acknowledges or will acknowledge.

- **JP-Light vs JP-Heavy (ADR-038-adjacent, 2026-05-15).** Plan 01a Task 6 has `jp-heavy.yaml` as a future-state stub. Does the spec correctly mark JP-Heavy as a flip event, not a Stage 1 deliverable? Does the presentation match? Does any artifact assume JP-Heavy when he's Light?

### B. Implementation correctness

- **Recipients file (`infra/age-recipients.txt`).** 2 pubkeys present. Cross-check against the founding spec §3 + ADR-003. Both pubkeys are valid age1 format.

- **secrets.env.age structure.** Verify it decrypts to ONLY the 8 plan-prescribed variables. (Requires TTY for passphrase — flag if you cannot verify directly; recommend Ricardo run a verify command.)

- **run-with-secrets.sh logic.** Read top-to-bottom. C1 fix (no exec leak) confirmed by per-task review. Cross-cutting question: does the wrapper's behavior under signals (SIGTERM mid-`source`, SIGKILL during the wrapped command) match the spec's "shred on every exit path" guarantee?

- **Pre-commit secret-scan hook.** Live at `.git/hooks/pre-commit` → symlinks to `infra/hooks/pre-commit-secret-scan.sh`. Cross-check the false-positive patterns the hook ignores (.age, etc.) against the spec's secrets-discipline contract. Are there real-world patterns the hook would miss? (E.g., Stripe keys, OAuth tokens beyond Anthropic/OpenAI/Google formats.)

- **JSON schemas (`infra/schemas/`).** `nexostrat-tasks-v1` + `nexostrat-calendar-v1`. Do they enforce what the spec requires (e.g., status enum, priority enum, ISO-8601 dates)?

- **Machine profiles (`infra/machines/*.yaml`).** 7 files exist (hp-server, hp-standby, ricardo-desktop, ricardo-travel, jp-light, jp-heavy, phones). Cross-check against spec §5 — does each declare the services its CLAUDE.md / persona contract expects?

- **Folder scaffold.** 3-bucket structure: `00_PARTNERSHIP/`, `00_META/`, `00_GOVERNANCE/`, `docs/`, `vault/`, `knowledge/`, `skills/`, `pipeline/`, `operations/`, `infra/`. Cross-check spec §4.1 + §5. Any missing folders? Any unexpected folders?

- **`pipeline/clients/_template/`.** Spec says 12 stations + 3 cross-cutting. Audit them.

- **`00_PARTNERSHIP/` policy files.** 7 files from Task 9 (CONFLICT_PROTOCOL, REVENUE_DISTRIBUTION, ROLES, KPIs, cost-sharing-agreement, qualified-prospect-definition, raised_hand_log) + PARTNERSHIP_AGREEMENT.md from Task 17. Cross-check against spec §4.5 + the presentation's partnership cards.

### C. Process / audit-trail integrity

- **Git history coherence.** Read commit messages in order from `952cf2d` (pre-Tasks-1-11 baseline) to HEAD. Are they self-contained? Do hardening commits clearly reference the original task commit they extend? Are there commits that bypass the discipline (force-pushed, amended, `--no-verify`)?

- **Tag `v0.1a-foundation`.** Annotated tag with honest message. Confirm the deferred items list matches `t-plan-01a-jp-and-tty-deferred`'s scope. Confirm the message doesn't overclaim.

- **`tasks.json` integrity.** Validates against `infra/schemas/tasks.schema.json`. Status transitions sensible. No orphan `blocked_by` references.

- **`STATUS.md` accuracy.** Current state matches HEAD; Recent activity entries match git log.

- **`CHECKPOINT.md` accuracy.** Last session's CHECKPOINT pointed at this session; this session's CHECKPOINT (after session end) should point at the audit. Verify.

- **Journal coverage.** `00_META/journal/` — every working session has a journal entry. Spot-check 2-3 entries for accuracy against their corresponding commits.

### D. Presentation fidelity

The presentation HTML has 22 ADR badges, 34 cards, 5 SVG diagrams. Verify:

- Every ADR badge in the presentation refers to an ADR that EXISTS in the spec.
- Every card's "ELI5" + "Técnico" pair tells the same story (no contradiction between the two columns).
- The "what's implemented" vs "what's planned" framing in the presentation matches reality. If a card claims "X is built" and X is in Plan 01b, that's a finding.
- The cost numbers in the presentation match `cost-sharing-agreement.md` (Ricardo USD 215-225/mo, JP USD 237-257/mo, firm $0/mo Stage 1). Note: JP's number depends on the still-pending Notion sweep; if the presentation already excludes Notion from JP's total, flag the consistency to chase.

### E. Production-readiness gap

The auditor should produce an honest assessment of what's left for Stage 1 launch (2026-06-30 to 2026-07-15):

- **Required (gating Stage 1):** Plan 01b artifacts (mirrors + warm-standby — the backup posture is unwalked without these), Plan 01c (personas + hooks + integration test), Plan 02 (documentation system FOSS replacement choices), Plan 04 (Telegram bot + meeting capture), Plan 05 (Mode B Skills + judge agent), Plan 06 (Client-Owner flow), Plan 07 (Bodai benchmark — quality bar mechanism).

- **Possibly required (depends on whether first paying client lands before Stage 2):** Plan 08 (Drive heavy-asset), Plan 03 (events.jsonl router).

- **Stage 2 / deferred:** the rest.

If the auditor sees a CRITICAL gap that would block Stage 1 launch and is NOT tracked in any plan, that's a finding. If the auditor sees something the spec says is required but no plan owns it, that's a finding.

---

## Methodology

The auditor should follow this structure to keep the scope tractable:

### Phase 1 — Inventory (1 hour)

Walk the repo. List every meaningful artifact (file, folder, hook, script, config). Cross-reference against the spec's expected deliverables. Produce a coverage matrix: spec deliverable → planned in which Plan → built (yes/no) → location.

### Phase 2 — Coherence probes (1-2 hours)

For each of the risk areas in section "Specific risk areas to probe" above, run the explicit check. Document evidence (file paths, line numbers, grep output) for each finding.

### Phase 3 — Document-vs-reality diff (1-2 hours)

For each "source of truth" file (spec, plans, presentation, ADRs), spot-check 5-10 specific claims against the repo state. Anything that doesn't match → finding.

### Phase 4 — Production-readiness gap (1 hour)

Apply the section E framework. Produce the gap list. Estimate elapsed time to close each gap based on plan size + execution velocity (Plan 01a took ~6 hours/session for Tasks 1-11 and ~6 hours/session for Tasks 12-18 autonomous portions, so Plan 01b's 12 tasks should land in ~1.5 sessions, Plan 01c's 11 tasks in ~1 session, etc.).

### Phase 5 — Report (1 hour)

Write the report. Format below.

---

## Report format

Write to `/srv/Nexostrat/00_META/proposals/YYYY-MM-DD_hard-system-audit-report.md` (use the date the audit actually runs).

### Header

```markdown
# Hard system audit report — Nexostrat v0.1a-foundation

> **Audit date:** YYYY-MM-DD
> **Auditor:** [dispatched agent persona]
> **Audited against:** v0.1a-foundation tag (commit acdcc4a)
> **Audit brief:** 00_META/proposals/2026-05-17_hard-system-audit-brief.md
> **Verdict:** RED | YELLOW | GREEN
```

### Verdict + counts

State the verdict with a 2-3 sentence justification. Then a count summary.

```
- 0 CRITICAL
- N HIGH
- M MEDIUM
- L LOW
```

**Severity definitions** (use these exactly):

- **CRITICAL** = the system in its current state would mislead an external observer (paying client, regulator, hire) about what exists, OR there is a real data-loss / security risk in something already shipped, OR there is a fundamental contradiction between two sources of truth that someone is acting on. CRITICAL findings block continuing to Plan 01b.

- **HIGH** = a divergence between two sources of truth that would mislead an INTERNAL operator (Ricardo or future-Claude) and produce wrong action; OR a missing audit finding from the prior audits not actually closed; OR a Stage 1 launch blocker not tracked in any plan. HIGH findings should be patched before Plan 01b execution but do not block writing/auditing Plan 01b.

- **MEDIUM** = drift between spec/plans/presentation; documentation gap; pre-existing tracked debt that has grown in scope. MEDIUM findings get logged for the next single-pass amendment cycle.

- **LOW** = stylistic, naming, or minor inconsistency; future-installer notes; rendering quirks. LOW findings collected for a post-Plan-01c polish pass.

### Findings table

```markdown
| ID | Title | Source A | Source B | Reality | Severity | Recommendation |
|---|---|---|---|---|---|---|
| F1 | [short title] | [doc + line] | [other doc + line] | [what's actually in repo] | CRITICAL/HIGH/MEDIUM/LOW | [concrete action] |
| ... |
```

### Detailed findings

For each HIGH and CRITICAL finding, dedicate a full section:

```markdown
## Finding N (SEVERITY) — Title

### What's wrong

[Paragraph: the discrepancy, with file paths and line numbers]

### Evidence

[grep output, file excerpts, diff between what spec says and what's built]

### Why it matters

[Who would be misled, what wrong action they'd take, what's at stake]

### Recommendation

[Concrete: amend file X line Y to read Z, OR add task t-foo, OR re-execute step N of Plan 01a, etc.]

### Effort estimate

[How long to fix: minutes / hours / a session / multiple sessions]
```

MEDIUM and LOW findings can be one-paragraph each in a "Deferred findings" appendix.

### Production-readiness assessment

```markdown
## Production-readiness gap

### Gating items for Stage 1 launch (2026-06-30 to 2026-07-15)

| # | Plan | Status | Elapsed estimate | Notes |
|---|---|---|---|---|
| 1 | Plan 01b mirrors + warm-standby | [written / not executed] | [X days] | [Tasks 7-12 gate on physical second host] |
| 2 | Plan 01c personas + hooks + smoke test | ... | ... | ... |
| ... |

### Critical-path narrative

[2-3 paragraphs: realistic timeline; what could go wrong; what flexibility we have]
```

### Recommended action list

```markdown
## Recommended actions

### Before Plan 01b re-audit (must close before continuing)

1. [Specific patch — file:line, exact change]
2. ...

### Bundle into next single-pass amendment

1. ...
2. ...

### Track as new tasks

1. New task `t-...` — [description]
2. ...

### Polish-pass material (post-Plan-01c)

1. ...
```

---

## Auditor's hard constraints

- **Do NOT edit any source-of-truth file during the audit.** Patches are the controller's job after reviewing your report. You write findings, not commits.
- **Use file paths + line numbers in every finding.** Vague findings ("the spec is inconsistent") are unactionable.
- **Cite the source-of-truth hierarchy when calling something a defect.** "The ADR says X; the spec body says Y; the implementation matches Y; per the hierarchy the ADR wins, so the spec body needs to be patched to match X."
- **Be honest about what you cannot verify.** TTY-required decrypts, JP-side state, future-state plans — flag them and recommend who can verify.
- **Read at least the entire founding spec and Plan 01a.** Don't audit from summary; the value of the audit is the careful reading.
- **Run real commands, don't trust file timestamps.** `git log`, `git show`, `grep -r`, `find` — verify what's actually in the tree.
- **No DESIGN-RETHINK FLAG without justification.** The prior audits used this only when a load-bearing architectural assumption was wrong. If you raise it, dedicate a full section explaining the rethink.

---

## Decision Ricardo will make on the audit report

After reading the audit report, Ricardo will (per his typical pattern):

1. **Walk the report with Claude** — joint reading, paragraph-by-paragraph for HIGH+ findings.
2. **Decide on patches** — either inline (small surgical) or via amendment plan (large).
3. **Re-run if needed** — sometimes a re-audit pass after patches lands.
4. **Update tasks.json** to mark resolved findings and create follow-up tasks for deferred items.
5. **Then green-light Plan 01b re-audit.**

The audit should make all 5 of those steps easy. If the report is so long Ricardo can't walk it in one sitting, it's too long — prefer concise findings with file:line refs over verbose prose.

---

## Why this is worth doing

The prior audits caught real defects:
- 2026-05-14 founding-spec audit (28 findings + DESIGN-RETHINK FLAG) led to Plan 01 splitting into 01a/01b/01c.
- 2026-05-14 Plan 01a audit (7 HIGH findings) led to surgical patches across the plan body that the patch-verification-trail proved are still live.

This audit is upstream of Plan 01b's re-audit. If we go into Plan 01b with stale assumptions about v0.1a-foundation's state, the re-audit will be working from a corrupted baseline. Catching coherence problems NOW saves cycles downstream.

---

## Files the auditor will read (minimum)

```
00_META/proposals/2026-05-13_nexostrat-system-design.md           # founding spec + ADRs 001-035
00_META/proposals/2026-05-14_amendments.md                         # Batch 1 amendments
00_META/proposals/2026-05-14_audit-report.md                       # founding-spec audit report (prior context)
00_META/proposals/2026-05-14_plan-01a-audit-report.md              # Plan 01a audit report
00_META/proposals/2026-05-14_plan-01a-patch-verification-trail.md  # patch trail for Plan 01a HIGH fixes
00_META/proposals/2026-05-14_nexostrat-presentation.html           # the public-facing presentation
00_META/proposals/2026-05-14_nexostrat-presentation.tests.md       # validation companion
00_META/plans/README.md                                            # master plan index
00_META/plans/2026-05-14_plan-01a-foundation.md                    # the plan that produced v0.1a
00_META/plans/2026-05-14_plan-01b-mirrors.md                       # next plan (audit it for coherence too)
00_META/plans/2026-05-14_plan-01c-personas.md                      # plan after that
CLAUDE.md                                                          # Founder persona contract
STATUS.md                                                          # current state
CHECKPOINT.md                                                      # last session's baton
tasks.json                                                         # task tracker
00_META/journal/2026-05-15_plan-01a-tasks-1-11.md                  # session journal (1-11)
00_META/journal/2026-05-16_plan-01a-tasks-12-18.md                 # session journal (12-18 — will exist by audit time)
infra/age-recipients.txt                                           # the recipients
infra/scripts/run-with-secrets.sh                                  # C1 implementation
infra/scripts/test_run_with_secrets_no_leak.sh                     # C1 test
infra/secrets/MANIFEST.md                                          # secrets manifest
infra/hooks/pre-commit-secret-scan.sh                              # secret-scan hook
infra/schemas/                                                     # JSON schemas
infra/machines/                                                    # machine profiles (7 YAMLs)
00_PARTNERSHIP/*.md                                                # 8 policy files
vault/README.md + vault/sensitive_index.md                         # vault model
.gitignore                                                         # secrets discipline
```

Plus run:
```
git -C /srv/Nexostrat log --oneline --all
git -C /srv/Nexostrat tag -l -n10
git -C /srv/Nexostrat status
bash /srv/Nexostrat/infra/scripts/validate_schemas.sh
ls -la /srv/Nexostrat/vault/keys/
file /srv/Nexostrat/secrets.env.age
file /srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age
```

---

*This brief is self-contained. Open the next session, type "Start Session" → "Run the hard system audit per `00_META/proposals/2026-05-17_hard-system-audit-brief.md`" → dispatch the auditor. Report should land within one focused session (~5-7 hours elapsed).*
