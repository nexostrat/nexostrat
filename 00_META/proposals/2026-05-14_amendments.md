# Amendment Plan — Nexostrat Foundation 2026-05-14

> **Status:** APPROVED (decisions locked) — pending amendment execution
> **Source audit:** [`2026-05-14_audit-report.md`](2026-05-14_audit-report.md) (verdict: RED, 28 findings, 15 HIGH+, DESIGN-RETHINK FLAG triggered)
> **Walkthrough completed:** 2026-05-14, joint pass by Ricardo + Claude through all 28 findings + 6 auditor recommendations
> **Output of:** in-session triage producing per-finding accept/reject/defer decisions

## Summary

The audit returned **RED with DESIGN-RETHINK FLAG** because 15 findings hit HIGH severity or above. The walkthrough resolved every finding to a concrete position. The major structural change: **Plan 01 splits into 01a / 01b / 01c** (auditor recommendation 1). Every other finding either (a) becomes a spec/ADR/Plan amendment captured below, (b) gets folded into the 01a/01b/01c rewrite, or (c) is deferred with explicit rationale.

**Outcome counts:**
- 28 findings → 28 decisions (0 deferred without action; 0 rejected)
- 6 recommendations → 6 decisions (1 structural — split Plan 01; 5 small ADR/spec adds)
- 5 new ADRs to write: ADR-021bis (drop Hosted), ADR-036 (Stage 1 surface area), ADR-037 (deferred Notion review), plus amendments to ADR-005/013/018 (re-status with notes), plus optionally a "Stage 2 escrow vault recipient" ADR (filed, not built)
- 1 master plan index update (Plan 01 → 01a/b/c)
- 3 new plans to write (01a, 01b, 01c) replacing the current Plan 01

## New canonical sequence (replaces the one in `2026-05-13_audit-request.md`)

```
1. APPLY AMENDMENTS (this session or next):
   1a. Spec amendments — single edit pass to 2026-05-13_nexostrat-system-design.md
       covering: per-user TZ pattern, Mode A/B manifest schema, persona
       ownership reallocation, Notion AI cost, Linux-Mint JP recommendation,
       12-station+3-cross-cutting standardization, station counts.
   1b. ADR ledger pass — re-status ADRs 001-020 (Accepted/Amended/Superseded);
       write ADR-021bis (drop Hosted); write ADR-036 (Stage 1 surface area);
       write ADR-037 (deferred Notion review).
   1c. Rename root events.json → calendar.json (single git mv + reference
       updates; touches existing file content + spec).
   1d. Master plan index — replace Plan 01 entry with 01a/b/c entries; renumber
       downstream Plans 02-10 if needed (most likely keep numbering, new plans
       slot before current Plan 02).
   1e. Resolve audit-request.md status to RESOLVED (cross-link to this doc).

2. WRITE PLAN 01a using superpowers:writing-plans skill.
   Scope: foundation. Folder scaffold, identity, JP key coordination + age
   recipients, vault recovery decision, secrets (with C1 fix), questionnaires
   migration, partnership doc commit, root governance files, comprehensive
   .gitignore, basic tasks.json/calendar.json. ~15 tasks.

3. RE-AUDIT Plan 01a (independent risk-auditor pass; same dispatch pattern
   as today's audit). Target: GREEN. If YELLOW with ≤3 amendments, apply
   inline and proceed; if more, re-rewrite the affected tasks.

4. EXECUTE Plan 01a via superpowers:subagent-driven-development.
   Tag v0.1a-foundation on completion.

5. WRITE Plan 01b. Scope: GitHub mirror via systemd path-watcher (C4),
   Codeberg mirror (F7), warm-rsync timer + service, ADR ledger cleanup,
   00_GOVERNANCE/system_map.md (Plan 01 Task 14 work). ~10 tasks.

6. RE-AUDIT, EXECUTE, tag v0.1b-mirrors.

7. WRITE Plan 01c. Scope: shared stanzas with leak audit (F20), inliner
   script (C3) + memos script (F8) + nexostrat-tasks-v1 schema (F21),
   persona CLAUDE.md/GEMINI.md generation (F10 reallocation), pre-commit
   hooks, rich integration smoke test (R2 — real decrypt round-trip + push-
   and-verify-GitHub-HEAD-changed + rsync dry-run). ~10 tasks.

8. RE-AUDIT, EXECUTE, tag v0.1-foundation (the original Plan 01 milestone).

9. Continue with Plans 02-10 from the master index (per-plan re-audit before
   execution becomes the new norm).
```

**Calendar honesty (R6):** 01a/b/c each ~5 days execute + 1-2 days write + 1 day re-audit. Plus JP-coordination latency (he has 10h/wk). Foundation milestone realistic by **2026-06-03 to 2026-06-10**, not 2026-05-20 as Plan 01 currently lists.

---

## Decisions — CRITICAL (4)

### C1 — `run-with-secrets.sh` leaks plaintext to /dev/shm
**Chosen:** Option A — drop `exec`, add explicit cleanup.
**Where the fix lands:** Plan 01a (when secrets task is rewritten). Replace `exec "$@"` with:
```bash
"$@"
RC=$?
cleanup
exit $RC
```
Plus: rich smoke test in 01c — wrap `sleep 60 &`, verify no leftover `/dev/shm/nexostrat-secrets-*` after 2s.
**Rejected:** Option B (source via process substitution) — not Stage 1; tracked as future hardening idea.
**Why:** 4-line patch, fully addresses leak, keeps existing wrapper pattern intact. Option B requires rewriting the consumer pattern (Docker `--env-file` etc) — not justified at Plan 01 scope.

### C2 — Vault encrypted to Ricardo only is unrecoverable SPOF
**Chosen:** Option 1 — block Plan 01a on JP age keypair + symmetric passphrase posture.
**Where the fix lands:** Plan 01a Task 6 (or earlier) grows: "JP coordination — JP runs `age-keygen` on his machine, sends pubkey via Signal, Ricardo adds to `infra/age-recipients.txt` BEFORE any encryption. JP key requires passphrase (symmetric with Ricardo's)." Plan 01a Definition of Done requires recovery path is testable.
**Future:** ADR for Stage 2 escrow recipient + Shamir split (for if/when firm scale justifies it).
**Why:** Cheapest fix (~10 min elapsed); honors spec's "either holder can decrypt" promise; founding meeting is done so JP coordination is socially cheap. Symmetric passphrase posture matches the security model.

### C3 — Persona files ship with literal `{{include: ...}}` placeholders
**Chosen:** Option A — write inliner script as Plan 01c Task 17.5; Task 18 invokes it.
**Where the fix lands:** Plan 01c. New script `infra/scripts/inline_includes.py` (~30 lines Python: read CLAUDE.md template, replace `{{include: path}}` with file contents, write final). Task 18 invokes it for each of the 6 persona files. Plan 02's drift hook becomes a wrapper around the same script in `--check` mode.
**Why:** Strictly dominates manual copy-paste — lower error rate, re-runnable, doubles as Plan 02's drift-hook foundation, fits ADR-029's "Python over n8n" reasoning. Adds one small Plan 01c task; reduces Plan 02 scope by more.

### C4 — Gitea post-receive hook can't decrypt; mirror silently dies
**Chosen:** Option 1 — host-side systemd path-watcher.
**Where the fix lands:** Plan 01b. Drop the Gitea-internal hook from Plan 01. Add `nexostrat-mirror.path` (watches Gitea's bare repo refs/heads/main) + `nexostrat-mirror.service` running as `ricardo` (has the age key). Same pattern as warm-rsync timer.
**Sub-task:** Confirm Gitea's actual bare-repo path (resolves Finding 22 too). Write into `00_GOVERNANCE/system_map.md`.
**Smoke test:** Plan 01c rich smoke test does real `git push origin main`, waits 30s, verifies GitHub HEAD changed.
**Why:** Cleaner separation; doesn't require editing the AttenBot/Gitea compose stack (governance overhead); decouples Gitea from firm secrets. Reuses warm-rsync's pattern.

---

## Decisions — HIGH (11)

### F5 — Founding Meeting ordering
**Chosen:** Founding Meeting was **DONE 2026-05-12**; agreement signed.
**Where the fix lands:** Plan 01a commits the real signed PDF (lands in `vault/partnership/` per F10 namespace split) plus markdown summary at `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md`. Plan 01a's embedded tasks.json sets Founding Meeting `status: done, completed: 2026-05-12`.
**Tactical detail:** Where signed PDF currently lives → confirm at execution time; stage into vault.

### F6 — Per-user TZ "07:00 each user's TZ" needs per-user timers
**Chosen:** Auto-amend to per-user systemd timer pattern; group-brief TZ deferred to Plan 08.
**Where the fix lands:** Spec §9.4 + ADR-030 amended: timer-per-user pattern with `OnCalendar=America/Tijuana 07:00:00` etc. (systemd 248+). Plan 08 (when it's written) inherits this pattern; group-brief TZ choice (earlier-of-two / send-twice / nominal-firm-TZ) resolved in Plan 08 design.

### F7 — Codeberg mirror missing
**Chosen:** Auto-amend; fold into Plan 01b alongside GitHub mirror.
**Where the fix lands:** Plan 01b. Same systemd path-watcher pattern as GitHub (different remote, different PAT).

### F8 — `nexostrat-memos.py` referenced but never created
**Chosen:** Auto-amend; bundle with C3's inliner-script task.
**Where the fix lands:** Plan 01c Task 17.5 cluster. ~40 lines Python reading `**/00_META/inbox/*.md` frontmatter, filtering by `to:` field, output formatted summary.

### F9 — Mode A/B manifest schema doesn't match
**Chosen:** Define schema with mandatory/mode-specific split; accept Mode A multi-turn as documented asymmetry.
**Where the fix lands:** Spec §6 amended to define `runs/<id>/manifest.json` schema. MANDATORY fields (both modes): `mode`, `model`, `prompt_version`, `inputs_hash`, `final_report_hash`. MODE-B-SPECIFIC: `tokens_in`, `tokens_out`, `latency_ms`, `stop_reason`, `id`. MODE-A-OPTIONAL: `turn_count`. comparison.md diffs only mandatory fields + final_report content. Plan 05 ships test asserting both modes write mandatory schema.

### F10 — `prospects/` and `vault/clients/` ownership conflicts
**Chosen:** Reallocate per auditor's main path.
**Where the fix lands:** Spec §4.1 persona table amended:
- **Client-Owner** owns `pipeline/{clients,prospects}/` AND `vault/clients/<slug>/`
- **Founder** owns `vault/{partnership,legal,accounting,keys}/` (but NOT `vault/clients/`)
- **Skills-Master** owns no vault content
- Founder routes prospects to Client-Owner via memo
shared/vault_access.md stanza updated to match. Persona CLAUDE.md scope sections (Plan 01c Task 18-21 work) updated.

### F11 — ADR ledger drift (ADR-005, 008, 013, 018 marked Accepted but changed)
**Chosen:** Auto-amend; full audit of ADRs 001-020.
**Where the fix lands:** Single-pass spec edit during amendment-execution work. Each ADR reviewed against current spec, marked one of {Accepted | Amended (with note) | Superseded by ADR-N}. Specifically known: ADR-005 (path naming → Amended), ADR-013 (events.jsonl path → Amended), ADR-018 (agent inventory → Amended).

### F12 — `events.json` (calendar) vs `events.jsonl` (event spine) name collision
**Chosen:** Rename root file to `calendar.json`; spine stays `infra/events/events.jsonl`.
**Where the fix lands:** Spec §1 file map + Plan 01a Task 5 (creates calendar.json instead of events.json) + shared/session_*.md stanzas all updated. `git mv events.json calendar.json` during amendment-execution. Note: SessionStart hook in /srv/brain reads /srv/Nexostrat events.json — that hook gets a small update OR Nexostrat's own session-start safety net (Plan 06 territory) handles it independently.

### F13 — `bootstrap-machine.sh` has no macOS support
**Chosen:** Bootstrap stays Linux-only. Recommend JP install Linux Mint for heavy setup.
**Where the fix lands:** Spec + Plan 01a explicitly document Linux Mint as the JP-side recommended baseline. `jp-heavy.yaml` OS field set to `linux-mint` (no longer placeholder). Spec adds note: "Mac/Windows support handled as exceptions in Plan 02 if JP pushes back."
**Sub-question still open:** JP's actual OS — to be confirmed before Plan 01a execution. If JP can install Linux Mint, no macOS work needed.

### F14 — Notion AI cost not in budget
**Chosen:** Pay the cost; Notion stays canonical for Stage 1.
**Where the fix lands:** Spec §5 cost table updated: "Notion AI add-on | $10-30/mo | JP/firm | Meeting transcription". Stage 1 envelope updated from $36-91/mo to **$46-121/mo**.
**Linked:** R5 (deferred Notion review ADR) captures the Stage 2 reconsideration trigger.

### F15 — Questionnaires conversion missing from Plan 01 tasks
**Chosen:** Auto-amend; add Plan 01a Task 5.5.
**Where the fix lands:** Plan 01a Task 5.5 — `pandoc Plan_Maestro_MejiaIACia_Ricardo.docx -o 00_PARTNERSHIP/questionnaires/2026-05-07_ricardo.md`; same for JP; move originals to `00_PARTNERSHIP/questionnaires/archive/`; move `.backup-2026-05-07.docx` to archive; move `Consultoria_IA_PYMEs_v1.pdf` to `operations/assets/`.

---

## Decisions — MEDIUM (9)

### F16 — `_template/` ordering between Plans 01/05/07
**Chosen:** Move template definition to Plan 01.
**Where the fix lands:** Plan 01a Task 3 (or 21.5 equivalent) creates `pipeline/clients/_template/` with all 12 stations + 3 cross-cutting folders + `state.json` schema file. Plan 05's Bodai work then clones a real template instead of defining it post-hoc.

### F17 — Encrypted ambient chat log race condition
**Chosen:** Option A — plaintext on /dev/shm during day; daily 23:59 encrypt.
**Where the fix lands:** Spec §8.10 amended: chat capture writes plaintext JSONL to `/dev/shm/chat_log/{group,dm-ricardo,dm-jp}/YYYY-MM-DD.jsonl` (atomic append works). Daily 23:59 cron `chat_log_encrypt.py` reads /dev/shm files, encrypts to `infra/telegram/chat_log/.../YYYY-MM-DD.jsonl.age`, shreds plaintext. Plan 09 inherits this design.
**Trade-off documented:** plaintext on RAM tmpfs for up to 24h is the cost of single-process append-safety.

### F18 — Persona ownership table inconsistent for vault writes
**Chosen:** Resolved by F10's namespace split. No additional work.

### F19 — Station count drift (13 vs 12 vs 15)
**Chosen:** Standardize on "12-station chain plus 3 cross-cutting folders."
**Where the fix lands:** Spec §2 + §4 + §7 wording all aligned to "12 stations + 3 cross-cutting" everywhere. Single grep-and-replace pass during amendment execution.

### F20 — `BRAIN_STATUS.md` reference is a /srv/brain leak
**Chosen:** Replace with `STATUS.md`; full audit of shared stanzas.
**Where the fix lands:** Plan 01c shared stanzas pass — replace `BRAIN_STATUS.md` reference in `shared/session_output_format.md` with `STATUS.md`. Audit all 9 shared stanzas for `/srv/brain/`, `BRAIN_STATUS`, `00_TEMPLATES/` leaks. The `00_META/00_TEMPLATES/memo_template.md` reference in `shared/memo_protocol.md` either gets created in Plan 01a or the stanza updated to point at a Nexostrat-local template.

### F21 — `tasks.json $schema = brain-tasks-v1` is /srv/brain coupling
**Chosen:** Define `nexostrat-tasks-v1` schema.
**Where the fix lands:** Plan 01a creates `infra/schemas/tasks.schema.json` (~20 lines JSON Schema) and `infra/schemas/events.schema.json` for calendar.json. Update tasks.json `$schema` field to `nexostrat-tasks-v1`. Plan 03 adds pre-commit validation against the schemas.

### F22 — n8n location inconsistency (`/srv/atten-bot` vs `/home/ricardo/n8n`)
**Chosen:** Resolved by C4 sub-task (path verification).
**Where the fix lands:** Bundle Gitea + n8n path verification into Plan 01b. Result documented in `00_GOVERNANCE/system_map.md` (Plan 01 Task 14 work). Spec line 461 + Plan 01 line 525 both updated to actual paths.

### F23 — `.gitignore` not updated by Plan 01
**Chosen:** Auto-amend; comprehensive .gitignore in Plan 01a.
**Where the fix lands:** Plan 01a Task 4 Step 4.5. Cover: Python (`__pycache__/`, `.pyc`, `.venv/`, `*.egg-info/`), Node (`node_modules/`, `npm-debug.log`), IDE (`.idea/`, `.vscode/`, `*.swp`), OS (`.DS_Store`, `Thumbs.db`), Docker (`docker-compose.override.yml`), age private keys (`*.key`), shm dumps, `*.log`. Belt-and-suspenders with the pre-commit hook.

### F24 — warm-rsync false positive smoke test
**Chosen:** Auto-amend; real start-and-verify check.
**Where the fix lands:** Plan 01b Task 27-equivalent (or Plan 01c integration test): `systemctl start nexostrat-warm-rsync.service && systemctl status ... | grep 'status=0/SUCCESS'`. Or rsync `--dry-run` exit-zero verification.

---

## Decisions — LOW (4)

### F25 — Gitea repo owner: org or personal?
**Chosen:** Org `nexostrat` (equal-owner posture).
**Where the fix lands:** Plan 01b paths updated to `nexostrat/nexostrat.git` (not `RicardoMejiaCaicedo/nexostrat.git`). Sub-prereq: org exists in Gitea (verify; create if missing; add JP as member).
**Why:** Aligns with ADR-002. Future-proof for JP committer access. Slightly more Gitea admin (one-time).

### F26 — `phones.yaml` no platform field
**Chosen:** Auto-amend; add `platform: ios|android` field.
**Where the fix lands:** Plan 01a (when phones.yaml is written) — per-user `platform` field. No code change needed at Plan 01.

### F27 — JP `Hosted` option silently dropped
**Chosen:** Kill it; write ADR-021bis.
**Where the fix lands:** New ADR-021bis "Drop Hosted from JP options" — explicit supersede of the original Hosted option. Spec §3 references to Hosted updated. Plan 01c STATUS.md update removes Hosted reference.

### F28 — Plan 01 task count drift (`~40` vs 28)
**Chosen:** Auto-amend; pure search/replace.
**Where the fix lands:** Resolved automatically when Plan 01 splits into 01a/b/c — old "~40" references don't survive the rewrite.

---

## Decisions — Recommendations (6)

### R1 — Right-size Plan 01
**Chosen:** Split into 01a / 01b / 01c.
**Where the fix lands:** Master plan index updated; three new plan files written via writing-plans skill; current Plan 01 file archived (kept for reference, marked superseded). See "New canonical sequence" above.

### R2 — Pre-flight test harness
**Chosen:** Auto-approved; folds into Plan 01c integration test.
**Where the fix lands:** Plan 01c "rich smoke test" task (~2-3 hours Python). Real decrypt round-trip + real `git push` + real GitHub HEAD verification + warm-rsync `--dry-run`.

### R3 — Stage 1 surface area ADR
**Chosen:** Auto-approved; new ADR-036.
**Where the fix lands:** New ADR-036 "Stage 1 surface area — v0 vs v1 fidelity" — explicitly lists features that ship at v0 fidelity for Stage 1 with v1 deferred (e.g., per-user TZ → v0 single firm TZ acceptable until 3+ users; chat extraction → v0 manual paste acceptable until volume justifies).

### R4 — CHECKPOINT.md concurrent-session protection
**Chosen:** Auto-approved.
**Where the fix lands:** Spec §4.10 (CHECKPOINT pattern) amended: SessionStart hook check — if CHECKPOINT.md modified within last N minutes by a different process, warn. Plan 06 (when it's written) implements the hook.

### R5 — Reconsider Notion's role (deferred review)
**Chosen:** Auto-approved; new ADR-037 capturing the Stage 2 review trigger.
**Where the fix lands:** New ADR-037 "Notion canonical role — Stage 2 review trigger" — captures the trigger conditions (cost climbs past $X, audit risk increases, JP workflow shifts) and the Whisper-canonical alternative as the reviewable choice.

### R6 — Plan 01 calendar honesty
**Chosen:** Auto-approved.
**Where the fix lands:** Master plan index + new Plans 01a/b/c due dates spread realistically across 2-3 weeks (foundation milestone v0.1-foundation by 2026-06-03 to 2026-06-10 instead of 2026-05-20).

---

## Work breakdown for amendment execution

Three concrete batches of work. Each batch is a candidate session.

### Batch 1 — Spec + ADR + master index amendments (~2-3 hours)
- Spec single-pass edit covering: F6, F9, F10, F11 (full ADR audit), F12 (calendar.json rename), F13 (Linux Mint recommendation), F14 (cost table), F17 (chat log /dev/shm pattern), F19 (station count), F22 (paths after path verification), R3 (ADR-036), R4 (CHECKPOINT race), R5 (ADR-037), R6 (calendar honesty in master index).
- Write ADR-021bis (drop Hosted), ADR-036 (Stage 1 surface), ADR-037 (deferred Notion review).
- Re-status ADRs 001-020 with notes (F11 audit).
- `git mv events.json calendar.json` + reference updates (F12).
- Master plan index update: replace Plan 01 entry with 01a/b/c entries; renumber if needed; update due dates (R6).
- Resolve `2026-05-13_audit-request.md` status to RESOLVED with cross-link.

### Batch 2 — Write Plans 01a / 01b / 01c (~3-4 hours)
- Use superpowers:writing-plans skill three times.
- 01a (~15 tasks): foundation. C1 fix, C2 JP key, F5 partnership doc, F15 questionnaires, F23 .gitignore, F21 schemas, F26 phones platform field, F16 _template structure.
- 01b (~10 tasks): mirrors + warm-standby. C4 path-watcher, F7 Codeberg, F22 path verification + system_map.md, F24 real warm-rsync test.
- 01c (~10 tasks): personas + hooks + integration test. C3 inliner script + F8 memos script + F20 leak audit, F10 reallocation in persona scope sections, R2 rich smoke test, F27 ADR follow-through in STATUS.md.

### Batch 3 — Re-audit + execute 01a → 01b → 01c (~3-4 weeks elapsed)
- Per the new canonical sequence above. Re-audit each plan before execution. GREEN-or-quick-amend gate.
- Each execute uses superpowers:subagent-driven-development.
- Tags: v0.1a-foundation, v0.1b-mirrors, v0.1-foundation (final foundation milestone replaces the original Plan 01 v0.1-foundation).

---

## Items NOT in this amendment plan

- **Future hardening (post-Stage-1):** Option B for C1 (process substitution secrets), Stage 2 escrow vault recipient (C2 Option 2), per-user TZ DST monitoring details. Filed as "future" — not Stage 1 work.
- **Notion deferred review:** ADR-037 captures it but the actual revisit happens at Stage 2.
- **Group-brief TZ choice:** Deferred to Plan 08 design.
- **macOS bootstrap support:** Deferred unless JP can't install Linux Mint.
- **JP committer access in Gitea org:** Filed as Plan 02+ task once JP onboards.

---

*This amendment plan is the canonical record of audit walkthrough decisions. Amendment-execution sessions read it as their brief. Once Batches 1-3 are complete, this file moves to `00_META/proposals/archive/`.*
