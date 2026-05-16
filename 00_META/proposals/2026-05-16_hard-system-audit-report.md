# Hard system audit report — Nexostrat v0.1a-foundation

> **Audit date:** 2026-05-16
> **Auditor:** dispatched general-purpose agent with risk-auditor persona inlined (per `00_META/proposals/2026-05-17_hard-system-audit-brief.md`)
> **Audited against:** `v0.1a-foundation` tag (commit `acdcc4a`); HEAD `af6eb0a` (session-end commit after tagging)
> **Audit brief:** [`2026-05-17_hard-system-audit-brief.md`](2026-05-17_hard-system-audit-brief.md)
> **Verdict:** **YELLOW (small)**

## Verdict + counts

`v0.1a-foundation` is an honestly-tagged, architecturally-coherent milestone. The implementation matches Plan 01a's prescription, the C1/C2 fixes are demonstrably live (C1 fully; C2 at the artifact-encrypted-to-both-recipients level — JP-side decrypt confirmation is correctly deferred), the 7 HIGH patches from the 2026-05-14 re-audit are all still in place, and the seven non-interactive test scripts pass clean. **No CRITICAL findings** and no DESIGN-RETHINK FLAG; the architecture is sound.

What pulls the verdict to YELLOW (small) is **documentation staleness in load-bearing operator-facing files** (`CLAUDE.md`, the founding spec body, the 2026-05-14 presentation), driven by three post-spec/post-presentation decisions (ADR-038 Notion drop, JP onboarding closure, brothers-as-partners ceremony reduction) that have **not yet propagated** to those source-of-truth surfaces. The single-pass amendment task `t-spec-notion-removal-amendment` is queued for "between Plan 01c execution and Plan 02 writing" — moving it **before Plan 01b re-audit** (or at minimum before any external observer reads these files) closes the bulk of the YELLOW findings.

```
- 0 CRITICAL
- 5 HIGH
- 9 MEDIUM
- 6 LOW
```

**Severity definitions applied:**
- **CRITICAL** = mislead external observer / real data-loss-or-security risk in shipped artifact / fundamental contradiction between sources of truth someone is acting on. **None found.**
- **HIGH** = mislead internal operator (Ricardo or future-Claude) and produce wrong action; OR prior audit finding not actually closed; OR Stage 1 launch blocker not in any plan.
- **MEDIUM** = drift / documentation gap / pre-existing tracked debt grown in scope.
- **LOW** = stylistic / naming / future-installer note / rendering quirk.

---

## Findings table

| ID | Title | Source A (authority) | Source B (drift) | Reality | Severity | Recommendation |
|---|---|---|---|---|---|---|
| H1 | CLAUDE.md says "JP pubkey pending" | repo: `infra/age-recipients.txt:28` (JP pubkey present since 2026-05-15 commit `b7e39bf`) | `CLAUDE.md:148` | JP pubkey in recipients file; CLAUDE.md still cites `t-jp-age-keypair` and "JP pubkey pending" | HIGH | Patch `CLAUDE.md:148` to reflect both recipients on file; remove `t-jp-age-keypair` reference (task closed 2026-05-15). |
| H2 | CLAUDE.md says spec has "ADRs 001-035" | spec `00_META/proposals/2026-05-13_nexostrat-system-design.md:34-71` (ADR map has 001-037 + 021bis = 37 entries; ADR-038 exists in `00_GOVERNANCE/adr/` but not yet in spec body) | `CLAUDE.md:7`, `CLAUDE.md:85` | Spec body has 37 ADRs; ADR-038 exists as separate file but is not in the spec body's ADR map | HIGH | Patch `CLAUDE.md:7` and `:85` to "ADRs 001-038 (ADR-038 in `00_GOVERNANCE/adr/` pending spec-body integration via `t-spec-notion-removal-amendment`)". Same correction in any `-explicado.md` partner. |
| H3 | Spec §5 cost table contradicts `cost-sharing-agreement.md` and the build-side reality | spec `2026-05-13_nexostrat-system-design.md:431-438` ("Anthropic API $20-60 / Ricardo"; "Notion $0 to firm / JP") | `00_PARTNERSHIP/cost-sharing-agreement.md:13-31` (Claude MAX $200 each; Notion still listed as JP-personal at $30-50/mo, but per ADR-038 Notion should be removed entirely) | Spec table: 6 line items, ~$36-91 envelope. cost-sharing-agreement.md: Claude MAX $200×2 + Notion + Drive + Grok + email + domain. Per ADR-038: Notion should be $0/removed entirely. Three sources of truth disagree. | HIGH | Bundle into `t-spec-notion-removal-amendment` (already scoped) — **move sweep before Plan 01b re-audit** rather than between Plan 01c and Plan 02. cost-sharing-agreement.md JP total `$237-257/mo` must drop the Notion line. Spec §5 needs the same edit + the Claude-MAX reality reflected. |
| H4 | Presentation HTML asserts Notion as canonical infrastructure across multiple cards + ADR popovers | repo: `00_GOVERNANCE/adr/ADR-038-drop-notion-foss-tbd.md` (Notion exits firm-level, 2026-05-15) | `00_META/proposals/2026-05-14_nexostrat-presentation.html:868, 877, 917, 1322, 2566-2607, 2693, 2696, 2895, 2989, 3090, 3195, 3260` (16 Notion references; ADR-001 popover says "markdown-in-git + Notion + Telegram"; ADR-024 popover says "Notion AI canonical"; ADR-037 popover unchanged; cost-table card has "Notion + Notion AI $10-18/mo · JP") | Presentation written 2026-05-14, ADR-038 landed 2026-05-15. No regeneration since. External observer reading the presentation gets a wrong picture of the firm's stack. | HIGH | Add **regenerate-presentation** as an explicit deliverable inside `t-spec-notion-removal-amendment`. Or split into `t-presentation-refresh-post-adr-038` so the deliverable doesn't fall off when the spec-only sweep runs. The presentation footer explicitly says "regeneration is supported by reading current spec + ADRs + STATUS"; the mechanism exists, the trigger is missing. |
| H5 | Direction A sentinel still committed at HEAD; `v0.1a-foundation` tag points at a tree containing unencrypted-roundtrip-fixture artifact | `vault/keys/sentinel-ricardo-to-jp.age` (tracked, 346 bytes) | Plan 01a Task 13 Step 4 ("Remove both sentinels after bidirectional confirmation"; `git rm` was supposed to remove both); plan re-audit Finding 11 also flagged `vault/keys/` is a production-recovery namespace not a test-fixture namespace | The sentinel was correctly deferred (per the 2026-05-16 directive: build now, JP downloads later) and the deferral is tracked in `t-plan-01a-jp-and-tty-deferred`. But: the tag's published tree contains a non-recovery file in `vault/keys/`, and the file's git presence is the verification surface JP will eventually use to confirm Direction A. Plan 01b re-audit and any future cross-bucket consistency check will see this. | HIGH | Either (a) accept the file is in `vault/keys/` for now (status-quo; tracked in deferred task); or (b) **before Plan 01b execution starts**, finish the JP-side Direction A confirmation + Direction B + cleanup commit so the tag's next-milestone successor is clean. The current state is honest (tag annotation documents it) but the hygiene/discipline regression Finding 11 of the Plan 01a re-audit predicted is now live. |
| M1 | Spec body still contains 19 Notion references; ADRs 001/024/037 all defend Notion canonical | spec `2026-05-13_nexostrat-system-design.md` (19 occurrences of "Notion"); ADR-024/037 status "Accepted" in ADR map | `ADR-038-drop-notion-foss-tbd.md` (Notion exits; ADR-024 and ADR-037 are "Superseded" per ADR-038 §"Supersession scope") | Spec body has not been touched since ADR-038. ADR-024/037 still read as Accepted in the spec ADR map (lines 58, 71). | MEDIUM | Tracked in `t-spec-notion-removal-amendment` — confirm it covers: ADR-024 status flip to Superseded, ADR-037 status flip to Superseded, ADR map row for ADR-038 added, §5 cost table re-written, §6 storage hierarchy, §8 meeting-capture defaults, §10 failure modes. (The task's existing scope covers most of these.) |
| M2 | `infra/secrets/MANIFEST.md` lists `NOTION_API_KEY` row with active Plan 04/08 use; `secrets.env.age` still has the variable | repo: `infra/secrets/MANIFEST.md:13` (NOTION row with `Used by`: "Meeting transcription watcher (Plan 08), `/note` plugin (Plan 04)") | `ADR-038-drop-notion-foss-tbd.md` (no Notion API surface in Nexostrat) | The MANIFEST row reads as active future-use even though no future use is planned. Already in `t-spec-notion-removal-amendment` scope (per STATUS.md). | MEDIUM | When the sweep runs: strike or remove the NOTION_API_KEY row, decrypt `secrets.env.age` → strip the line → re-encrypt → commit both files atomically. |
| M3 | `00_PARTNERSHIP/ROLES.md:23,25` lists "Notion canonical workspace ownership" and "Notion" in default communication for JP | repo: `00_PARTNERSHIP/ROLES.md:23,25` | `ADR-038-drop-notion-foss-tbd.md`; STATUS.md "Notion removal spec touchups" line 69 catalogs this exact file | Pre-existing tracked drift, scoped into sweep. | MEDIUM | Same sweep — strike the Notion line items from ROLES.md when `t-spec-notion-removal-amendment` runs. |
| M4 | `pipeline/clients/_template/README.md:30` says "transcripts canonical = Notion AI per ADR-024" | repo: `pipeline/clients/_template/README.md:30` | `ADR-038-drop-notion-foss-tbd.md`; STATUS.md catalogs this. | Same as M3. | MEDIUM | Same sweep. |
| M5 | `00_PARTNERSHIP/REVENUE_DISTRIBUTION.md:38` references "Shared infrastructure (Notion, hosting, domain — see cost-sharing-agreement.md)" | repo: `00_PARTNERSHIP/REVENUE_DISTRIBUTION.md:38` | ADR-038 | Same shape — pre-existing tracked drift. Not currently catalogued in STATUS.md's sweep list (cost-sharing-agreement.md and ROLES.md are; REVENUE_DISTRIBUTION.md is not). | MEDIUM | Add to `t-spec-notion-removal-amendment` scope. (Trivial: strip the parenthetical "Notion, ".) |
| M6 | CLAUDE.md describes JP's interface as "Telegram + Gitea web only", but per 2026-05-15 JP-Light variant decision JP opted out of Gitea web | repo: `ADR-038-drop-notion-foss-tbd.md` §"JP-Light variant"; `STATUS.md:84` ("JP picked Light mode … no Gitea web") | `CLAUDE.md:21, :100`; `00_PARTNERSHIP/ROLES.md:25`; `infra/machines/jp-light.yaml:14-16` (declares `chrome  # or any browser — for Gitea web`) | JP's actual interface = Telegram + email/digests + future FOSS dashboard (Plan 02 chooses). The "Telegram + Gitea web" string is from pre-2026-05-15 design. | MEDIUM | Patch `CLAUDE.md:21` + `:100` to "Telegram + future FOSS dashboard (Plan 02)". Patch ROLES.md:25 similarly. Patch jp-light.yaml comment or note that browser is optional for ad-hoc reading, not the canonical surface. Bundle into the sweep. |
| M7 | Founding spec §2 file map (`2026-05-13_nexostrat-system-design.md:169-171`) shows `00_META/inbox/` and `00_META/shared/` as part of the canonical tree at root; neither directory exists in the repo | spec `2026-05-13_nexostrat-system-design.md:163-171` | `find /srv/Nexostrat/00_META -maxdepth 1 -type d` returns `handoff, journal, plans, proposals, scripts` only | Correctly deferred — `00_META/shared/` is Plan 01c territory; per-bucket inboxes are Plan 04 territory (Telegram bot writes to `<scope>/00_META/inbox/`). But the spec file map shows them at root as if they exist now. The audit brief flagged this kind of thing: "If the spec implies any of these is DONE, that's a finding. If they correctly label them as planned/future, no finding." The spec file map does NOT label these as future. | MEDIUM | Add inline notes in the spec file map: `inbox/ (Plan 04)` and `shared/ (Plan 01c)`. One-line annotation, no architectural change. Bundle into `t-spec-notion-removal-amendment` sweep since the auditor is touching the file. |
| M8 | Master plan README `00_META/plans/README.md:18-20` "Due" column shows hard dates (2026-05-27 / 06-03 / 06-10) that no longer reflect reality given the audit-cycle slip + JP-and-TTY deferral | master-index `00_META/plans/README.md:18-20` (Plan 01a Due 2026-05-27) | tasks.json `t-plan-01a-execute`: due 2026-05-27, completed 2026-05-16 (ahead of schedule on artifact side; deferred items don't have a corresponding Due column in README) | The 2026-05-14 amendment plan (§R6) explicitly called for "calendar honesty." The dates are stale (artifacts side complete; the "Due" column is now ambiguous given the deferred-but-tracked items). | MEDIUM | Update master-index README to reflect 01a status `DONE` (artifacts) + `t-plan-01a-jp-and-tty-deferred` parallel track. Keep 01b/01c dates but acknowledge audit-cycle insertion before 01b. Minor edit; could land in the next session-end commit or in the next sweep. |
| M9 | `infra/machines/jp-light.yaml:8` has `tailscale_ip: null` and `os: <TBD>` even though OS is known (macOS Sequoia 15.7.3 per STATUS.md:50) | repo: `infra/machines/jp-light.yaml` | `STATUS.md:50` (JP OS confirmed 2026-05-15) | The YAML is a stale template. macOS-confirmed; Light mode doesn't require the cross-platform tooling, so this is documentation-only, but the file is meant to be machine-readable. | MEDIUM | Patch `infra/machines/jp-light.yaml`: `os: macos`, `os_version: "15.7.3"`. Note that bootstrap-machine.sh is Linux-only, so Light-mode (no docker, no cli_tools) doesn't fail on macOS — but the data should be accurate. Optional: include a comment that `bootstrap-machine.sh` is skipped for Light-mode JP. |
| L1 | Spec body header (`2026-05-13_nexostrat-system-design.md:1-7`) labels itself "Status: PROPOSED — pending Ricardo's review" | spec self-header | The spec has been actively-amended (Batch 1, then ADR-038), 6 prior audits + walkthroughs have driven changes; presentation is built from it; plans 01a/01b/01c all reference it; v0.1a-foundation built from it | Status should be "ACTIVE — amended via Batch 1 and ADR-038; further single-pass amendment pending" or similar. Trivial. | LOW | One-line edit. Bundle into sweep. |
| L2 | Spec §10 (Open Items) header date claims still reference 2026-05-14 / 2026-05-15 / 2026-05-16 as future ("**JP brand top-5 vote** (t-006, due 2026-05-14)") | spec `2026-05-13_nexostrat-system-design.md:980-985` | Tasks are completed (per tasks.json + STATUS.md) | Spec narrative-time hasn't moved since 2026-05-14. Items 1-5 are all done. | LOW | Either strike Section 10 Open Items entirely (move to STATUS.md / journal) or add inline `(DONE 2026-05-XX)` annotations. Sweep candidate. |
| L3 | Presentation `Plan_Maestro_MejiaIACia` references in archive (`00_PARTNERSHIP/questionnaires/archive/*.docx`) preserve the old brand name for forensic record | `00_PARTNERSHIP/questionnaires/archive/Plan_Maestro_MejiaIACia_{Ricardo,JP}.docx` + `.backup-2026-05-07.docx` | spec uses "Nexostrat" exclusively | This is correct (archival; never to be renamed). Flag only as "auditor confirmed this is intentional" so future audits don't waste cycles re-discovering it. | LOW | None — confirm in this report as intentional. |
| L4 | `00_META/CHANGELOG.md:5-6` opening lines reference "Brain Architect" and `/srv/brain/` | repo: `00_META/CHANGELOG.md:5-6` | CLAUDE.md Strict Rule #3 (no `/srv/brain` references) | The CHANGELOG is historical narrative; the references describe what existed before the no-Brain rule was locked. Per the audit brief: "pre-ADR-038 references are catalogued debt awaiting the sweep" — historical CHANGELOG entries are arguably even more locked-down. | LOW | Confirm intentional historical record; no action. Could add a one-line header note ("Entries before 2026-05-14 describe the pre-rewrite state.") to make this explicit. |
| L5 | `00_GOVERNANCE/` is mostly empty — only the 4 ADRs (021bis/036/037/038) exist; spec §"ADR ledger" says ADRs 001-035 will be drafted "during scaffold" | repo: `00_GOVERNANCE/adr/` (4 ADR files) | spec `2026-05-13_nexostrat-system-design.md:367-369` ("Full ADRs (Context · Options · Decision · Consequences) are drafted into `00_GOVERNANCE/adr/` during scaffold") + `00_META/plans/README.md:192` (Plan 02 deliverable: "All 15 new ADRs (021-035) drafted as `00_GOVERNANCE/adr/ADR-NNN-<slug>.md` with `-explicado.md` partners") | Correctly deferred to Plan 02. Plan 01a/01b/01c don't require the ADR bodies. The 4 ADRs that exist are the new ones not in the spec. The audit brief explicitly says "Plan 02-10 artifacts: all of them … correctly absent." | LOW | None — correctly absent. Note in report. |
| L6 | Plan-01c master-index entry (`00_META/plans/README.md:165`) lists "`00_META/shared/STATUS.md` template" as a deliverable; but `STATUS.md` lives at repo root, not under `00_META/shared/` | repo: `STATUS.md` at root | `00_META/plans/README.md:165` (Plan 01c Deliverable) | Minor wording issue — Plan 01c likely meant "shared stanzas that reference STATUS.md (replacing the old `BRAIN_STATUS.md` reference)". | LOW | Re-word the Plan 01c README entry: "shared stanza referencing `STATUS.md` at repo root (replaces old `BRAIN_STATUS.md` reference per F20)". Trivial; can land during Plan 01c re-audit. |

---

## Detailed findings — HIGH

## Finding H1 (HIGH) — `CLAUDE.md` says "JP pubkey pending" but JP pubkey landed 2026-05-15

### What's wrong

`CLAUDE.md` is the Founder persona's operating contract. Line 148 reads:

```
**Recipients file:** [`infra/age-recipients.txt`](infra/age-recipients.txt) — public file, safe to commit. Contains pubkeys of everyone who can decrypt firm secrets/vault. Currently: Ricardo. JP pubkey pending (per `t-jp-age-keypair`).
```

JP's pubkey was added 2026-05-15 in commit `b7e39bf` and is currently present in `infra/age-recipients.txt:28`:

```
# Juan Pablo Mejia (founder, jp-mac, macOS Sequoia 15.7.3, received 2026-05-15)
age10k4rzha64ykqtjrjkqut6dyzxy5qexu2038lpe6gqk58l7rx4p4qrupv79
```

The task `t-jp-age-keypair` is also closed (`tasks.json` shows `status: done, completed: 2026-05-15`).

### Evidence

```
$ grep -c "^age1" /srv/Nexostrat/infra/age-recipients.txt
2
$ grep -n 't-jp-age-keypair' /srv/Nexostrat/tasks.json | head -1
67:      "id": "t-jp-age-keypair",
$ grep -nA1 't-jp-age-keypair' /srv/Nexostrat/tasks.json | head -4
67:      "id": "t-jp-age-keypair",
68:      "subject": "JP age keypair generation — awaiting Signal reply",
69:      "status": "done",
```

### Why it matters

A future-Claude reading CLAUDE.md at session start gets the wrong picture of the firm's crypto posture: they would assume JP can't decrypt anything yet, would not encrypt new artifacts to both recipients, and might re-raise the C2 escalation. The C2 audit finding is closed at the artifacts level (every encrypted artifact since 2026-05-15 has two X25519 stanzas; verified via `file secrets.env.age` and `file vault/keys/sentinel-ricardo-to-jp.age`). The decrypt-roundtrip is the only thing still deferred (correctly tracked in `t-plan-01a-jp-and-tty-deferred`).

Per the source-of-truth hierarchy: ADR > spec > Plan > **CLAUDE.md** > presentation > repo. The repo state is *more recent* than CLAUDE.md, which violates the hierarchy unless CLAUDE.md is patched.

### Recommendation

Patch `CLAUDE.md:148`. Proposed replacement:

```
**Recipients file:** [`infra/age-recipients.txt`](infra/age-recipients.txt) — public file, safe to commit. Contains pubkeys of everyone who can decrypt firm secrets/vault. **Currently: Ricardo + JP** (both pubkeys on file since 2026-05-15). Bidirectional decrypt roundtrip is partially verified (Direction A sentinel encrypted + pushed; JP-side decrypt confirmation + Direction B + sentinel cleanup tracked in `t-plan-01a-jp-and-tty-deferred`).
```

### Effort estimate

5 minutes. Single-line edit. No re-encryption / no tag impact / no cross-doc cascade.

---

## Finding H2 (HIGH) — `CLAUDE.md` cites "ADRs 001-035" but spec has 001-037 + 021bis (and ADR-038 exists outside spec body)

### What's wrong

`CLAUDE.md:7` and `CLAUDE.md:85` both say the spec has "ADRs 001-035":

```
> - **Founding spec:** [`00_META/proposals/2026-05-13_nexostrat-system-design.md`] — 10 sections, ADRs 001-035 (Batch 1 amendments pending; see [`00_META/proposals/2026-05-14_amendments.md`])
```

The actual ADR map (`2026-05-13_nexostrat-system-design.md:34-71`) now contains:
- ADRs 001-020 (Accepted / Amended / Superseded per Batch 1)
- ADR-021, ADR-021bis (new in 2026-05-14)
- ADRs 022-037 (new)

That's **37 ADR entries** (38 if you count 021bis). Plus **ADR-038** (Notion drop, 2026-05-15) exists as `00_GOVERNANCE/adr/ADR-038-drop-notion-foss-tbd.md` but is **not yet listed in the spec body's ADR map**.

The qualifier "(Batch 1 amendments pending)" in CLAUDE.md is itself stale — Batch 1 amendments were applied 2026-05-14 (commits `dc5cbec`, `5f126a7`, `d5ebbf9`).

### Evidence

```
$ grep -cE "^\| ADR-" /srv/Nexostrat/00_META/proposals/2026-05-13_nexostrat-system-design.md
37
$ ls /srv/Nexostrat/00_GOVERNANCE/adr/
ADR-021bis-drop-hosted-jp-mode.md
ADR-036-stage-1-surface-area.md
ADR-037-notion-canonical-role.md
ADR-038-drop-notion-foss-tbd.md
$ grep -c "ADR-038" /srv/Nexostrat/00_META/proposals/2026-05-13_nexostrat-system-design.md
0
```

### Why it matters

The hierarchy makes ADRs and the spec body higher authority than CLAUDE.md. So strictly speaking, CLAUDE.md is the one that's wrong and must be patched. But the consequence for operators is: a Claude or Gemini session reading CLAUDE.md will think the firm has 35 ADRs when it actually has 37 + a 38th out-of-spec; this affects how the agent reasons about "what's decided" vs "what's open."

The compounding issue: ADR-038's spec-body integration is deliberately scheduled into `t-spec-notion-removal-amendment` (a single-pass sweep). Until that sweep runs, the spec body says one thing and the ADR file says another. The current state is internally inconsistent across the ADR layer.

### Recommendation

Two-step fix:

1. **Immediate** (5 min, no sweep dependency): Patch `CLAUDE.md:7` and `:85` to read:
   > **Founding spec:** [`...`] — 10 sections, **ADRs 001-038** (ADR-038 in `00_GOVERNANCE/adr/`; spec-body integration via `t-spec-notion-removal-amendment` sweep). Batch 1 amendments applied 2026-05-14 (commits dc5cbec/5f126a7/d5ebbf9).

2. **Sweep** (already tracked in `t-spec-notion-removal-amendment`): integrate ADR-038 into the spec body's ADR map; flip ADR-024 + ADR-037 to "Superseded by ADR-038"; update all spec text mentioning Notion as canonical.

Recommend **pulling the sweep forward** to run **before Plan 01b re-audit**, not between Plan 01c execute and Plan 02 write. Rationale below in § Recommended actions.

### Effort estimate

Immediate fix: 5 minutes. Sweep: ~half-day (already scoped).

---

## Finding H3 (HIGH) — Spec §5 cost table, `cost-sharing-agreement.md`, and ADR-038 disagree on Notion + costs

### What's wrong

Three sources of truth describe the firm's Stage 1 cost structure and they don't match:

**Spec §5 cost table (`2026-05-13_nexostrat-system-design.md:431-438`):**
```
| Anthropic API | $20-60 | Ricardo | Claude judge, /ask, automation |
| Google Drive 2TB | ~$10 | Ricardo | Heavy assets |
| xAI Grok API | $5-15 | Ricardo | 3rd-model parallel research |
| Notion | $0 to firm | JP (his account) | CRM + client meeting notes |
| Domain | ~$1 amortized | Compartido | nexostrat.com |
| Super Grok (web, optional) | $30 | Ricardo | Interactive Grok (NOT pipeline) |
```
Envelope per the same spec: "USD ~$36-91/month."

**`cost-sharing-agreement.md` (`00_PARTNERSHIP/cost-sharing-agreement.md:13-31`):**
- Claude MAX (Ricardo) $200/mo
- Claude MAX (JP) $200/mo
- Gemini API $0 (free until ~Oct 2026)
- Grok API $5-15
- Notion + AI add-on $30-50/mo
- Domain ~$1
- Email ~$6/mo
- Drive 2TB ~$10
- Total Ricardo personal: ~$215-225 + Claude MAX $200
- Total JP personal: ~$237-257
- Total firm: $0

**ADR-038 (`00_GOVERNANCE/adr/ADR-038-drop-notion-foss-tbd.md` § Supersession scope):**
> Spec §5 cost table: Notion line item removed. Amendment F14 ... is reversed; the Stage 1 envelope returns to the pre-F14 figure or lower (FOSS + existing self-hosted infra is approximately $0 incremental for Stage 1).

### Evidence

The three numbers don't even share a denominator:
- Spec uses **Anthropic API ($20-60)** — pay-per-use model.
- cost-sharing uses **Claude MAX ($200×2)** — flat subscription.
- ADR-038 says **Notion line removed**, which neither of the other two has acted on.

This is the kind of contradiction the audit brief calls out for severity HIGH ("a divergence between two sources of truth that would mislead an INTERNAL operator (Ricardo or future-Claude) and produce wrong action").

### Why it matters

An operator reading the spec sees a Stage 1 cost envelope of $36-91/mo. An operator reading cost-sharing-agreement.md sees ~$452-482/mo of personal spend. An operator who reads ADR-038 sees Notion removed (which neither doc reflects). Any cost-related decision — Stage 2 trigger evaluation, reimbursement planning, "can we afford to add X?" — runs from a wrong baseline depending on which doc the operator read first.

This compounds across artifacts: the presentation HTML (line 2588) lists Notion + Notion AI at $10-18/mo from JP-personal; the spec table says Notion $0 to firm (no number for JP); cost-sharing says $30-50/mo. All three contradict ADR-038's "removed entirely."

### Recommendation

Two actions, both within the existing `t-spec-notion-removal-amendment` sweep scope (STATUS.md line 69 confirms scope includes cost-sharing-agreement.md JP cost + PARTNERSHIP_AGREEMENT.md range):

1. **Sweep edits the spec §5 cost table** to match the reality:
   - Remove the Notion row entirely (per ADR-038).
   - Replace "Anthropic API $20-60" with "Claude MAX (Ricardo + JP) $200×2" reflecting the actual subscription model, with a note "Anthropic API charges deprecated as primary; reserved for non-Claude-Code use cases."
   - Either move all founder-personal-spend lines into a separate "Pre-revenue personal spend" subsection, or keep §5 as "firm-paid only ($0 Stage 1)" with a pointer to `cost-sharing-agreement.md` for the personal-spend reality.
   - Restate envelope: "Stage 1 firm pays $0/mo; pre-revenue personal spend per cost-sharing-agreement.md, reimbursable at first revenue."

2. **Sweep edits cost-sharing-agreement.md** to remove the Notion row + recalculate JP's "237-257" total → drop the Notion 30-50 line → JP total becomes ~$207-218 (Claude MAX 200 + Domain ~1 + Email 6).

   This also requires touching `PARTNERSHIP_AGREEMENT.md:61` which currently cites "JP ~USD 237-257/mo".

3. **Sweep regenerates the presentation cost-card** to match (see Finding H4 for the full presentation refresh recommendation).

### Effort estimate

Half-day for the full sweep (already scoped). Each individual edit is small; the discipline is making sure every dependent number is updated in lockstep so the next audit doesn't find a different layer still stale.

---

## Finding H4 (HIGH) — Presentation HTML is materially out of date post-ADR-038; external observer would get wrong picture

### What's wrong

`00_META/proposals/2026-05-14_nexostrat-presentation.html` was written 2026-05-14 (the day before ADR-038 landed). It carries 16 references to Notion across multiple cards, the ADR popover database, and the cost-share card. Sample evidence:

- **Line 868** (operating cards): "el sistema le reporta automáticamente vía Telegram **y Notion**"
- **Line 877**: "cost-sharing-agreement.md · pre-revenue: Ricardo cubre Claude+Drive+hardware; **JP cubre Notion**"
- **Line 917**: "Captura de reuniones (**Notion canonical** + shadow opcional)"
- **Line 2588** (cost table card): "**Notion + Notion AI** | ~$10–18 | JP · personal | CRM + meeting notes"
- **Line 2696** (ADR badges list): "<span class='adr-badge' data-adr='037'>ADR-037</span> · **Notion canonical** + Stage 2 review trigger"
- **Line 2895** (SVG diagram label): "**Notion AI canonical** + Jitsi/Whisper shadow."
- **Line 3090** (ADR-001 popover decision text): "El sistema operativo de Nexostrat se construye sobre markdown en git ..., **Notion** (vista CRM + meeting notes para JP) y Telegram."
- **Line 3195** (ADR-024 popover): "**Internal R+JP: Notion AI canonical** + Jitsi/Whisper shadow ..."
- **Line 3261** (ADR-037 popover): "**Notion AI permanece canonical** para meeting capture en Stage 1."

Per ADR-038 (2026-05-15): Notion exits the firm-level architecture. ADR-024 and ADR-037 are explicitly superseded.

Also: the presentation's ADR database **omits ADR-038 entirely** (not in the JS `ADR` object at lines 3088-3263). The presentation footer claims "Total ADRs referenciadas: 37" — but ADR-038 doesn't exist in the presentation at all.

Separately: the presentation **omits ADR-009** (correctly — it's Superseded), **ADR-016** (operations sub-tree — Amended, not Superseded, should be in the popover db), and **ADR-018** (agent inventory — Amended). So the popover database is missing ADRs 009, 016, 018, and 038. Of these, only ADR-038 is a current-relevance miss; 009/016/018 are minor completeness issues.

### Evidence

```
$ grep -ciE 'notion' /srv/Nexostrat/00_META/proposals/2026-05-14_nexostrat-presentation.html
16
$ grep -cE "ADR-038|adr-038|'038'" /srv/Nexostrat/00_META/proposals/2026-05-14_nexostrat-presentation.html
0
$ grep -oE "'[0-9]{3}(bis)?'" /srv/Nexostrat/00_META/proposals/2026-05-14_nexostrat-presentation.html | sort -u
'001' '002' '003' '004' '005' '006' '007' '008' '010' '011' '012' '013' '014' '015' '017' '019' '020'
'021' '021bis' '022' '023' '024' '025' '026' '027' '028' '029' '030' '031' '032' '033' '034' '035' '036' '037'
```

(Note: ADRs 009/016/018/038 absent from the popover JS database; 9/16/18 also absent from the spec ADR map → no, 016/018 ARE in the spec map, only 009 is Superseded. So the presentation database is missing 016, 018, 038.)

### Why it matters

The audit brief lists the presentation as source-of-truth tier 5 (above repo state, below CLAUDE.md). It's also the **first artifact** a non-technical reader (JP, a future hire, a regulator who asks "what does Nexostrat actually do") will see. If the presentation says "Notion AI canonical" and ADR-038 says "Notion exits," the presentation misleads.

The audit brief explicitly flagged this risk area:
> **D. Presentation fidelity** ... If a card claims "X is built" and X is in Plan 01b, that's a finding.

The presentation's Notion claims aren't even "X is in Plan 01b" — they're "X is canonical right now" while the ADR ledger says X is removed. Higher severity than the v0/v1 fidelity check the brief described.

This is the largest-readership artifact in the repo. Per the CRITICAL definition ("the system in its current state would mislead an external observer"), this nearly qualifies as CRITICAL — held back from CRITICAL because:
- The presentation has a clear "2026-05-14 snapshot" disclaimer in the footer (`line 3063-3065`).
- The presentation is not currently being shown to external parties (per STATUS.md and journals, JP saw v2 before ADR-038 landed; no external observer is in the loop right now).

Treating it as HIGH not CRITICAL on the grounds that it's a known-stale snapshot. If Ricardo plans to share this with anyone external before Plan 02, it elevates to CRITICAL.

### Recommendation

Three options ordered by quality:

1. **(Preferred) Regenerate the presentation.** The footer explicitly says "Para regenerar: abrir Claude Code en `/srv/Nexostrat/`, leer spec + ADRs + CHECKPOINT + STATUS actuales, escribir nueva versión con timestamp actualizado en filename." The mechanism exists. Do it after `t-spec-notion-removal-amendment` runs, so the regenerated presentation reads from a clean spec.
   - New filename: `2026-05-XX_nexostrat-presentation.html` (post-sweep date).
   - Old file moved to `00_META/proposals/archive/2026-05-14_nexostrat-presentation.html` (snapshot).

2. **(Acceptable) Patch in place.** Add a banner at top: "⚠️ Esta presentación es un snapshot 2026-05-14 PRE-ADR-038. Notion ya no es canonical — ver ADR-038. Para versión actualizada, regenerar." Less effort, but every reader has to do the mental substitution.

3. **(Worst) Leave as-is.** Acceptable only if no one external reads it and Ricardo + JP know to disregard the Notion sections.

Create a new task `t-presentation-refresh-post-adr-038` (high, due 2026-06-01) that gates on `t-spec-notion-removal-amendment` completing, then regenerates the HTML.

### Effort estimate

~1 day to regenerate (matching the 2026-05-14 effort: brainstorm + write + iterate). Reduces if the prompt asks for "minimal diff from prior version, applying ADR-038 supersessions only."

---

## Finding H5 (HIGH) — `vault/keys/sentinel-ricardo-to-jp.age` is committed in the `v0.1a-foundation` tree and is a known hygiene regression

### What's wrong

Plan 01a Task 13 prescribed: encrypt sentinel → commit Direction A → JP decrypts → JP sends back Direction B → commit Direction B → cleanup both sentinels in one commit (`git rm`). The current state stops at "commit Direction A pushed to Gitea" because the 2026-05-16 directive said "build now; JP downloads on his schedule." Plan 01a's own re-audit Finding 11 flagged the choice of `vault/keys/` as a test-fixture location: "vault/keys/ is a folder semantically reserved for production recovery material."

So the tag `v0.1a-foundation` (`acdcc4a`) points at a tree whose `vault/keys/` directory contains:
- `.gitkeep` (folder marker)
- `sentinel-ricardo-to-jp.age` (test fixture, 346 bytes)

The tag annotation is honest about the deferral (the message explicitly says "C2 Direction A: sentinel encrypted to both recipients + pushed to Gitea, awaiting JP-side decrypt confirmation — Task 13 (partial)") so this is not a misleading-tag issue. But it IS the kind of "we know about it; we're not sure when it gets fixed" debt that grows quietly.

### Evidence

```
$ file /srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age
/srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age: age encrypted file, X25519 recipient, among others

$ git log --oneline -- /srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age
ff01d52 Plan 01a Task 13 Direction A · sentinel from Ricardo

$ git log --all --oneline -- /srv/Nexostrat/vault/keys/sentinel-jp-to-ricardo.age
(empty — Direction B never committed)
```

The `vault/keys/sentinel-jp-to-ricardo.age` was never created. Step 4 cleanup in the patched plan uses `git rm` for BOTH files (which is the desired "loud failure if Direction B was skipped") — so the cleanup can't run until Direction B lands.

Task `t-plan-01a-jp-and-tty-deferred` (`tasks.json` line 166) explicitly tracks this with due 2026-06-30 and `priority: medium`, non-blocking for Plan 01b.

### Why it matters

Three concerns of escalating severity:

1. **Discipline:** the Plan 01a re-audit flagged exactly this. Predicted defect is now live.
2. **Tag cleanliness:** `v0.1a-foundation` is the canonical reference point for "what shipped." Anyone checking out the tag for forensic reasons (incident response, "what was in the foundation at milestone N?") sees an out-of-place file in `vault/keys/`. Recoverable from the tag annotation, but it's a foot-note.
3. **Plan 01b dependency:** Plan 01b's warm-rsync step will rsync the entire `/srv/Nexostrat/` tree (per spec backup table). Sentinel-ricardo-to-jp.age will replicate to warm-standby. By the time it gets cleaned up, it'll exist in HP + Gitea + warm-standby + GitHub mirror + Codeberg mirror. Trivial to clean later (it's just a file), but the multiplication is real.

### Recommendation

Two options, ordered by quality:

1. **(Preferred) Close `t-plan-01a-jp-and-tty-deferred` before Plan 01b execution starts.** Specifically:
   - JP downloads `sentinel-ricardo-to-jp.age` (Gitea web → raw link, or one-time clone).
   - JP decrypts with his key → confirms via Signal.
   - JP encrypts a Direction B sentinel → Signal-attaches.
   - Ricardo saves attachment to `vault/keys/sentinel-jp-to-ricardo.age` → decrypts → confirms back.
   - Single cleanup commit: `git rm vault/keys/sentinel-{ricardo-to-jp,jp-to-ricardo}.age` + push.
   - Updates STATUS.md confirming bidirectional C2 closure.
   - Estimated effort: ~30 min Ricardo + ~30 min JP, async over Signal. The 2026-05-15 turnaround pattern (JP responsive in hours) suggests this is realistic before Plan 01b starts.

2. **(Acceptable) Accept the deferral, let Plan 01b absorb the replication cost, clean later.** Status quo. The tracked task `t-plan-01a-jp-and-tty-deferred` already has it.

If option 1 is taken, the new Plan 01b re-audit can verify C2 is fully closed; option 2 carries the C2-not-quite-closed footnote into Plan 01b and beyond.

### Effort estimate

Option 1: ~1 hour async. Option 2: zero now, ~30 min cleanup later.

---

## Production-readiness gap

### Gating items for Stage 1 launch (2026-06-30 to 2026-07-15)

| # | Plan | Status | Elapsed estimate | Notes |
|---|---|---|---|---|
| 1 | Plan 01a | **DONE (artifacts side)** + `t-plan-01a-jp-and-tty-deferred` parallel | — | Tagged `v0.1a-foundation` 2026-05-16. JP-side + TTY tests due 2026-06-30. |
| 2 | This audit's HIGH findings + `t-spec-notion-removal-amendment` sweep | not started | 0.5-1 day | Recommend running BEFORE Plan 01b re-audit (see § Recommended actions). |
| 3 | Plan 01b mirrors + warm-standby | READY (written, audited not yet) | ~1 day re-audit + ~3-5 days execute | Tasks 1-6 unblocked; Tasks 7-12 gate on physical second host (Linux Mint 22.2 + Tailscale-joined). Realistic completion: 2026-06-05 to 2026-06-08. |
| 4 | Plan 01c personas + hooks + smoke test | READY (written, audited not yet) | ~1 day re-audit + ~3-5 days execute | No coordination gates within the plan. Realistic: 2026-06-10 to 2026-06-13. |
| 5 | Plan 02 documentation + FOSS docs stack decision | DRAFT-PENDING (not written) | ~1 day brainstorm + ~1 day write + ~1 day audit + ~3 days execute | **Load-bearing per ADR-038** — FOSS replacements for Notion's four roles are decided here. Realistic: 2026-06-15 to 2026-06-22. |
| 6 | Plan 03 events.jsonl spine + Python agent framework | DRAFT-PENDING | ~1 day write + 1 day audit + ~1 week execute | Required before Plans 04-10. Critical-path. |
| 7 | Plan 04 Telegram bot + Unified Inbox | DRAFT-PENDING | ~1 day write + 1 day audit + ~1 week execute | First user-facing surface for Ricardo + JP. |
| 8 | Plan 05 Skill 1 end-to-end | DRAFT-PENDING | ~1 day write + 1 day audit + ~1 week execute | First Diagnóstico-eligible chain. Quality bar (Bodai benchmark) lands here. |
| 9 | Plan 06 Skills 2-5 | DRAFT-PENDING | ~1 day write + 1 day audit + ~2 weeks execute | Parallel-fan-out work; some can run concurrently with Plan 04. |
| 10 | Plan 07 Per-client chain + orchestrator | DRAFT-PENDING | ~1 day write + 1 day audit + ~1 week execute | First income-eligible Diagnóstico after this. |
| 11 | Plan 08 Meeting Pipeline | DRAFT-PENDING | ~1 day write + 1 day audit + ~1.5 weeks execute | Brief, parity, extraction — major build. |
| 12 | Plan 10 Observability + Go-Live | DRAFT-PENDING | ~3 days execute | Smoke tests + runbooks + Stage 1 checklist. |

**Plans deferrable to post-Stage-1 (depending on first-paying-client timeline):**
- Plan 08 meeting pipeline can ship at minimum-viable fidelity (manual `/note` capture; per ADR-036 v0 fidelity allows this).
- Plan 09 ambient chat extraction is v0-deferrable per ADR-036.
- Plan 03 events.jsonl router can ship at v0 fidelity (file-tail loop; v1 Python daemon later).

### Critical-path narrative

**Realistic Stage 1 launch:** 2026-07-15 to 2026-07-30 (slipping ~2-4 weeks from the original 2026-06-30-to-2026-07-15 target, but within the brief's stated range).

Drivers of slip:
- Plan 02's FOSS docs stack decision is now load-bearing (per ADR-038); previously Notion absorbed the role. Plan 02 brainstorm + decisions + initial deployment is ~5 days of new work vs the pre-ADR-038 estimate.
- The audit-before-each-plan-execution discipline (locked per the 2026-05-15 do-it-right-do-it-once memory) adds ~1 day per plan ×  ~7 plans ≈ 7 days vs pre-discipline estimate.
- `t-plan-01a-jp-and-tty-deferred` is non-blocking but consumes coordinator attention.

**What could go wrong:**
1. **Physical second host availability** — Plan 01b Tasks 7-12 gate on this. If procurement slips, the warm-standby + recovery story is partial. Mitigation: Tasks 1-6 (mirrors) ship without it; warm-standby ships when host lands.
2. **FOSS stack quality lag** — ADR-038 acknowledges this explicitly: "Whisper.cpp Spanish transcripts at CPU speed take real-time to ~1.5x; self-hosted summary pipelines (Ollama, etc.) are less polished than Notion AI's default output. Plan 02 onwards must close this gap or accept it." If the gap is wider than expected, Stage 1 ships with degraded meeting capture quality (acceptable per ADR-036 v0/v1 trade-offs).
3. **JP bandwidth** — JP-Light + 10h/wk = limited JP-availability for coordination items (Signal turnarounds, Direction A confirmation, FOSS dashboard sign-off). Mitigation: per `feedback_prefer_architecture_over_ceremony.md`, Ricardo+Claude build autonomously; JP downloads/responds when convenient.
4. **Unaudited deferred items compound** — every plan now has a "deferred to next sweep" list (Plan 01a has `t-plan-01a-jp-and-tty-deferred` + `t-plan-01a-text-amendments` + this audit's findings). If the sweep cadence slips, the next audit will find a larger backlog. Discipline mitigation: pull `t-spec-notion-removal-amendment` forward to **before** Plan 01b re-audit (not between Plan 01c and Plan 02).

**Flexibility we have:**
- Per ADR-036, several v1 features can ship as v0 in Stage 1 (per-user TZ briefs at v0 = single firm TZ; chat extraction at v0 = manual; docs drift audit at v0 = manual; parity diff at v0 = manual).
- Plans 02-10 are all written just-in-time per the master-index discipline; nothing is over-committed up front.
- The "tag at every milestone" discipline (v0.1a / v0.1b / v0.1-foundation / v1.0) means every milestone is checkpoint-able; rollback to a known-good state is cheap.

**What's not yet planned but Stage 1 needs:**

Nothing critical. The audit brief listed possible Stage 1 gaps:
- Plan 03 (events.jsonl router) — planned, JIT.
- Plan 08 (Drive heavy-asset upload) — planned, JIT.

Both are in the master-index, neither slips Stage 1 in the worst case (v0 fidelity acceptable per ADR-036).

---

## Recommended actions

### Before Plan 01b re-audit (must close before continuing)

**These five items are the H1-H5 findings consolidated; each has a concrete one-or-two-paragraph patch.**

1. **Patch `CLAUDE.md:148`** to reflect both age recipients on file (H1). 5 minutes; one-line edit.

2. **Patch `CLAUDE.md:7` and `:85`** to "ADRs 001-038" with ADR-038 note (H2). 5 minutes.

3. **Patch `CLAUDE.md:21` and `:100`** + `00_PARTNERSHIP/ROLES.md:25` to remove "Gitea web" from JP's interface description, replace with "Telegram + email + future FOSS dashboard (Plan 02)" (M6 — same edit, do it in the same pass). 10 minutes.

4. **Patch `infra/machines/jp-light.yaml`** to set `os: macos`, `os_version: "15.7.3"`, and add a comment that `bootstrap-machine.sh` is skipped for Light mode (M9). 5 minutes.

5. **Pull `t-spec-notion-removal-amendment` forward** to run **immediately, before Plan 01b re-audit** rather than between Plan 01c and Plan 02. Rationale: the audit found that Notion staleness is the single largest source of finding-count (M1-M5 + parts of H3-H4 are all Notion-related). Bundling the sweep upfront cleans the spec/plans/presentation in one focused pass and Plan 01b's re-audit starts from a verified baseline.
   - Scope additions surfaced this session (not in the existing task's notes):
     - `00_PARTNERSHIP/REVENUE_DISTRIBUTION.md:38` (M5).
     - Spec §2 file map `inbox/` and `shared/` annotations (M7).
     - Master plan README dates calibration (M8).
     - Presentation regeneration as a follow-on task (H4 — new task `t-presentation-refresh-post-adr-038`).
     - ADR-038 spec-body integration: add as ADR-038 row to spec ADR map; flip ADR-024 + ADR-037 to Superseded status.

6. **Resolve Finding H5 by closing `t-plan-01a-jp-and-tty-deferred`** (or at least the bidirectional sentinel + cleanup portion). Coordinate one async exchange with JP via Signal. Realistic effort: ~1 hour over a half-day. If JP unavailable in the window before Plan 01b execution starts, accept option 2 (status quo) and document the decision.

### Bundle into next single-pass amendment (the now-pulled-forward `t-spec-notion-removal-amendment`)

The existing task's scope plus the additions from this audit. Concretely:

1. Spec body: ADR-024 + ADR-037 → Superseded by ADR-038. Add ADR-038 row to ADR map.
2. Spec §5 cost table: remove Notion line; replace Anthropic API with Claude MAX reality; add pointer to `cost-sharing-agreement.md` for personal-spend reality.
3. Spec §6, §8, §10: every "Notion AI canonical" / "notion.*" reference re-pointed at FOSS-TBD per ADR-038 Supersession scope.
4. Spec §2 file map: annotate `00_META/inbox/` (Plan 04) and `00_META/shared/` (Plan 01c) (M7).
5. Spec §10 Open Items: mark items 1-5 done with dates (L2).
6. Spec header: status PROPOSED → ACTIVE (L1).
7. `00_PARTNERSHIP/cost-sharing-agreement.md`: strike Notion row; recalculate JP total.
8. `00_PARTNERSHIP/ROLES.md`: strike Notion lines.
9. `00_PARTNERSHIP/REVENUE_DISTRIBUTION.md:38`: drop "Notion," from parenthetical.
10. `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md:61`: recalculate JP cost range to match cost-sharing-agreement.md post-Notion-removal.
11. `pipeline/clients/_template/README.md:30`: re-point transcripts source from "Notion AI per ADR-024" to "TBD per Plan 02 FOSS stack decision."
12. `infra/secrets/MANIFEST.md:13`: strike or remove NOTION_API_KEY row.
13. `secrets.env.age`: decrypt → strip NOTION_API_KEY line → re-encrypt to both recipients → commit (requires Ricardo TTY).
14. Add Plan-01a-text-amendments per `t-plan-01a-text-amendments` (process-substitution → direct `-i` pattern across Tasks 11/13/14/15/16/17/18).

### Track as new tasks

1. **`t-presentation-refresh-post-adr-038`** (high, due 2026-06-01) — gates on `t-spec-notion-removal-amendment` completing. Regenerate `00_META/proposals/<date>_nexostrat-presentation.html`. Archive the 2026-05-14 version to `00_META/proposals/archive/`. Update ADR popover database to include ADR-038 and the missing ADR-016 + ADR-018.

2. **`t-plan-01b-amendment-await-baseline`** (note, not a task per se but a procedural reminder) — Plan 01b re-audit should re-read this audit's report and confirm none of the findings introduce new constraints on Plan 01b's task list. (Most likely none do; Plan 01b is mirrors + warm-standby and only tangentially related to the Notion/CLAUDE.md/presentation drift.)

### Polish-pass material (post-Plan-01c)

1. **`00_META/CHANGELOG.md:5-6`** — add a one-line header note that pre-2026-05-14 entries describe the pre-rewrite state (L4).
2. **`00_META/plans/README.md:165`** — re-word Plan 01c README entry on "00_META/shared/STATUS.md template" (L6).
3. **Spec §10 Open Items section** — consider whether to keep this as a static section or migrate to STATUS.md going forward (L2).
4. **Plan-01a-deferred-Minor findings** from the original re-audit (`AGE_ERR` not in cleanup trap, `vault/keys/` namespace for test fixtures) — collect into a single polish-pass commit.
5. **Presentation popover database missing ADRs 009 (correctly), 016, 018** — adding the two missing ones during the H4 regeneration.

---

## What this audit did NOT cover

Per the audit brief's hard constraint ("be honest about what you cannot verify"):

1. **TTY-required tests.** `infra/scripts/test_run_with_secrets_no_leak.sh` reads `/dev/tty` for the age passphrase; this audit ran via tool-driven Bash so the test was not exercised. The plan-level success criterion #2 ("`run-with-secrets.sh sleep 60 &` followed by 2s `ls /dev/shm/nexostrat-secrets-*` returns no files") is **not verified by this audit**. The wrapper script itself is correctly written (`set -uo pipefail`, trap on EXIT/INT/TERM/HUP, no `exec`, AGE_ERR captured per Finding 7 of prior audit) per static read. The patch-verification-trail's Finding 2 verification steps would catch a regression. **Recommend Ricardo run the test at TTY at his convenience.**

2. **`secrets.env.age` decrypt verification.** This audit confirmed `file secrets.env.age` reports `age encrypted file, X25519 recipient, among others` (the "among others" implies ≥2 stanzas, consistent with both-recipients encryption). But the **decrypt round-trip to confirm the 8 plaintext variable names match the plan prescription** is TTY-required. Tracked in `t-plan-01a-jp-and-tty-deferred`.

3. **JP-side state.** Per the JP-Light + no-Gitea + macOS reality: JP's private key passphrase, his Bitwarden backup status, his ability to receive Signal attachments — all are JP-side and unverifiable from this end. The C2 audit-finding "bidirectional roundtrip" is therefore confirmed only at the artifacts-encrypted-to-two-recipients level; JP-side decrypt remains untested. **Recommend the coordination loop in Finding H5's recommendation.**

4. **Plan 01b and Plan 01c plan-text coherence.** This audit read Plan 01a in full (3523 lines) and spot-checked Plans 01b/01c via the master-index README (which summarizes their deliverables). A line-by-line Plan 01b/01c audit is the responsibility of the dedicated re-audit cycle for each plan (`t-plan-01b-reaudit` / `t-plan-01c-reaudit`). This audit does not preempt those.

5. **Subagent-driven-development execution quality.** Plan 01a's Tasks 12-18 ran via the subagent skill with the two-stage review loop. The journal documents the pattern (1 cross-cutting reviewer pass, 1 hardening commit for `age`+`shred` data-loss path). This audit took the journal at face value — did not re-read every subagent dispatch transcript to verify each subagent's spec-compliance + code-quality reviewer actually caught what they claimed.

6. **External-mirror functionality.** Plan 01b builds the GitHub + Codeberg mirrors. They don't exist yet (per master-index README + the audit brief's "what's not yet built"). This audit confirms they're correctly absent in the v0.1a-foundation state; the mirror functionality is unverified because it doesn't exist yet.

7. **The presentation's 5 SVG diagrams' accuracy.** Spot-checked text labels (caught the "Notion AI canonical" one in line 2895). The geometric / topological correctness of the diagrams against current architecture was not exhaustively verified.

---

## Auditor's overall assessment

The system at `v0.1a-foundation` is **substantively healthy**. The 7 HIGH patches from the 2026-05-14 re-audit are live and verified by spot-checks. The C1 fix (run-with-secrets.sh no-exec-leak) is correctly implemented per static read. The C2 fix is structurally complete (both recipients on file, every artifact encrypted to both per `file` inspection); only JP-side decrypt confirmation is deferred, honestly tracked, and non-blocking. The `00_PARTNERSHIP/` policy files are coherent and the brothers-as-partners markdown agreement is a sound resolution to F5.

The YELLOW verdict comes from **documentation staleness driven by post-2026-05-14 decisions not yet propagated**. None of the staleness is in code or in encryption posture; it's in operator-facing context files (CLAUDE.md), the spec body, the presentation, and a handful of policy-doc cross-references. All of it is **scoped into existing tasks** (`t-spec-notion-removal-amendment`, `t-plan-01a-text-amendments`, `t-plan-01a-jp-and-tty-deferred`). The single biggest leverage point: **pull `t-spec-notion-removal-amendment` forward to before Plan 01b re-audit**, run it in a focused half-day, and Plan 01b's re-audit starts from a verified baseline.

The discipline patterns from the 2026-05-14 → 2026-05-16 sessions are **paying off measurably**:
- Honest tag annotations document what's deferred.
- The `do-it-right-do-it-once` memory prevented several "let's just ship and patch later" shortcuts.
- The subagent two-stage review loop caught a genuine data-loss path (age + shred newline-separated → `&&`-chained in Task 16 hardening commit `ed9a596`).
- The patch-verification-trail (`2026-05-14_plan-01a-patch-verification-trail.md`) survived two sessions (2026-05-15 Tasks 1-11 + 2026-05-16 Tasks 12-18) with zero intersessional drift.

**Verdict: YELLOW (small).** Patches are surgical, fit in one session, and unblock Plan 01b re-audit. No architectural changes needed. No DESIGN-RETHINK FLAG. The foundation is solid; the words around it need a half-day refresh.

---

*Audit completed 2026-05-16. Auditor recommends walking the HIGH findings paragraph-by-paragraph with Ricardo, deciding the H5 close-vs-defer question, then running the consolidated `t-spec-notion-removal-amendment` sweep with the expanded scope above. Plan 01b re-audit can start the session after.*
