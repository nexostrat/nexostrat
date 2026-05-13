# Mejía, IA & CIA — Company System Design

> **Status:** PROPOSED — pending Founding Meeting ratification and JP review
> **Date:** 2026-05-11
> **Authors:** Ricardo Mejía + Claude (brainstorming session at `/srv/brain/01_VENTURES/04_MejiaIACia/`)
> **Audience:** Ricardo, Juan Pablo, future operators
> **Purpose:** Lock the architectural shape of the company brain BEFORE scaffolding any code or folders. Source of truth for the JP review-and-approval infographic.

---

## Executive Summary

This document specifies how Mejía, IA & CIA will operate as a 2-person AI consulting partnership: where the company brain lives, how it's structured, how AI agents run within it, and how humans (Ricardo + JP) interact with it through a Telegram bot. The substrate is a lightweight version of Ricardo's personal AI Brain pattern, intentionally separated from that personal brain, designed for multi-user collaboration from day 1, and supplemented by Notion (CRM + recordings), Drive (heavy assets), and a purpose-built Telegram bot (human interface).

The proposal is organized into five sub-systems: Foundation (where it lives, security, backups), Architecture (folder structure, personas, communication), Agents (automated work), Bot (human interface), and the JP-presentation infographic (output of this spec). Each sub-system contains explicit ADRs (Architecture Decision Records) that can be revisited and superseded over time.

The proposal is NOT implementation. It describes what we will build; the implementation plan is the next session's output.

---

## How to Read This Document

- **JP** — sections marked **[JP DECIDES]** are items that touch your personal setup and need your direct choice. Items marked **[JP VIEW]** are where you probably have strong input worth surfacing during review. Everything else is proposed by Ricardo + Claude; you can accept, edit, or veto any line.
- **Ricardo** — every decision below was discussed and locked during the 2026-05-11 brainstorming session. This document is the canonical record. Disagreements with JP at the Founding Meeting may amend specific items; supersession path is via new ADRs.
- **Future operators** — the system map and ADR index in `00_GOVERNANCE/` are the durable reference. This proposal is the moment those choices were first made.

---

## System Decomposition

Five sub-systems compose the company operating substrate. Earlier sub-systems gate later ones:

```
1. FOUNDATION ───── where the company brain lives, security, backups
   │
   ▼
2. ARCHITECTURE ─── folder structure + inter-folder communication
   │             ├── 3. AGENTS ────────── automated work, per-folder operators
   │             │
   ▼             ▼
   4. BOT ──────────── human interface (Telegram), capture + AI escalation
                 │
                 ▼
              5. JP INFOGRAPHIC ─── the deliverable derived from this spec
```

---

## [JP DECIDES] Your Interface to the System

This is the only decision in this proposal that's truly yours alone — because it determines what software runs on YOUR laptop and what credentials you hold. Pick one:

### Option A — Heavy (peer operator)
- Your laptop: Claude Code installed, Gemini CLI installed, full git clone, your own `.env`, SSH key to Gitea, your `age` private key.
- You operate at the same power level as Ricardo. You can open Claude Code at any folder and run agents directly.
- Onboarding: a few hours one-time + ongoing maintenance of your tooling.
- Secrets: live on your laptop too.
- Bus factor: zero. Independent of Ricardo's server.

### Option B — Hosted (browser into Ricardo's server)
- Your laptop: web browser + Tailscale client.
- On Ricardo's server: a per-user code-server (web IDE) running Claude Code on your behalf.
- Same powers as Heavy, but tools run on Ricardo's hardware.
- Onboarding: ~15 min (browser login).
- Secrets: only on Ricardo's server.
- Bus factor: 1 — depends on server uptime.

### Option C — Light (Telegram + Gitea web only)
- Your laptop: web browser + Telegram app.
- You use the Telegram bot for most interaction; Gitea web for reading markdown/PDFs.
- You don't install Claude Code or hold any operational credentials.
- Onboarding: zero — you already have both apps.
- Secrets: only on Ricardo's server.
- Bus factor: 1 — depends on Ricardo as operator.

**Ricardo's preferred default for you: Heavy.** Pick the one that fits your actual time commitment and tooling appetite.

---

## Foundation

### ADR-001 — System substrate
**Decision:** Lightweight Brain pattern as the company's intelligence layer, supplemented by Notion (CRM + recordings), Google Drive (heavy assets), and a purpose-built Telegram bot.

**Context:** The personal Brain pattern has proven value for methodology + skills + governance, but it doesn't scale-down well for operational data (active pipeline, who-was-contacted-when, contract states) — those belong in a CRM. Trying to make the Brain do everything would conflict with the partnership's pre-launch reality.

**Consequences:**
- Brain holds: methodology, prompts, skills, decisions, partnership rules, knowledge.
- Notion holds: client pipeline state, meeting recordings + transcripts, day-to-day CRM motion.
- Drive holds: heavy binary assets (recordings, large PDFs, image bundles).
- Telegram bot is the human-interface layer connecting everything.

### ADR-002 — Repository home
**Decision:** Standalone repo at `/srv/mejia-ia-cia/` on Ricardo's server. New Gitea organization `Mejia-IACia` with both Ricardo and JP as owners. Current stub at `/srv/brain/01_VENTURES/04_MejiaIACia/` becomes a one-file pointer.

**Why clean break:** the company brain must be readable/editable by JP without exposure to Ricardo's personal Brain (medical records, finances, family). Submodules / branch-permissions were considered and rejected as fragile.

### ADR-003 — Document vault encryption
**Decision:** `age` with per-user recipient keys. Each user generates an `age` private key, files are encrypted to BOTH public keys (envelope encryption). Either user can decrypt.

**Why per-user keys over shared password:** revocation is clean (drop a recipient, re-encrypt forward); each user's key never touches the other's machine; per-user audit possible. Slightly more setup than `gocryptfs`-shared-password; trivial relative to a forced re-encryption later.

**Future-proof:** works under any of the three JP-interface options (under Light/Hosted, JP's key lives on Ricardo's server only; under Heavy, on his laptop).

### ADR-004 — Secrets store
**Decision:** Single `secrets.env.age` file in git at root. Encrypted to the same two `age` recipient keys as ADR-003. A small wrapper script decrypts → exports env vars → runs the command → cleans up.

**Why git-tracked encrypted file over password manager:** majority of company secrets year 1 are machine-readable (API keys, bot tokens) — those want programmatic access. The few human-readable shared logins are rare enough to defer the password-manager investment (stage 2). One mental model for everything sensitive, fewer vendors.

### ADR-005 — Git discipline (PRs)
**Decision:** Trunk for non-protected paths. PRs required for protected paths: `skills/*/prompts/`, `clients/*/deliverables/`, `clients/*/proposals/`, `clients/*/contracts/`. At least one approval (either of you) before merge. AI agents always push to a branch on protected paths.

**Why selective:** "JP reviews before client" partnership rule becomes structural, not behavioral. Routine work (notes, journals, infrastructure code) doesn't tax review bandwidth. Agents have a clear lane.

### ADR-006 — Backup topology
**Decision:** Phased rollout.
- **Phase A (now):** Gitea origin on Ricardo's server + GitHub private mirror via post-receive hook.
- **Phase B (soon):** add Codeberg or GitLab as second mirror.
- **Phase C-prep (later):** weekly rclone snapshot of git tree.
- **Heavy assets:** Google Drive 2TB (your personal account) via dedicated OAuth credentials (refresh token managed by rclone), nightly `rclone copy` to your home NAS for local redundancy.
- **Recording format:** audio-only canonical (~30 MB/hour vs ~500 MB/hour for video). Video only when there's an explicit reason.

**Why phased:** earlier phases cost nothing and satisfy "have at least one off-site." Later phases trigger on actual durability concerns or asset volume growth.

### ADR-007 — AI vs human permissions
**Decision:** Layered model.
- Agents commit freely on non-protected paths.
- Destructive operations (delete, rename, file moves spanning folders, edits to settings/hooks/config, edits to protected paths) require a human signature.
- "Human signature" = a commit by a Telegram-authenticated user or a manual `git commit` by Ricardo/JP at terminal.

**Why layered over trunk-free or PR-everything:** matches Ricardo's existing "no destructive ops without approval" rule from the personal Brain. Doesn't bottleneck routine work; doesn't let agents accidentally cause irreversible harm.

### ADR-008 — Heavy assets storage
**Decision:** Google Drive 2TB (your personal Google account), accessed via dedicated OAuth client credentials with a long-lived refresh token (managed by rclone), stored only on Ricardo's server. Drive folder: `/Mejia-IACia/`, never mixed with personal Brain content. All sensitive heavy assets are `age`-encrypted before upload. Local rclone mirror to home NAS, nightly cron.

**Why dedicated OAuth credentials (not user OAuth, not service account):** decouples Drive access from any individual user's day-to-day Google session — both R and JP interact with assets through the system (CLI helper, Telegram bot), not directly via drive.google.com. Service accounts don't work cleanly with personal (non-Workspace) Drive accounts. Free, no Workspace upgrade required. Token can be rotated by re-running rclone's auth flow if compromised.

---

## Architecture

### ADR-009 — Top-level folder structure (Option B, function-based)

```
/srv/mejia-ia-cia/
├── 00_META/                 # system governance — changelog, BRAIN_STATUS equivalent, this proposal
├── 00_GOVERNANCE/           # decisions ledger (ADRs), system maps, proposals
├── 00_PARTNERSHIP/          # JP-co-owned: agreement, conflict protocol, KPIs, questionnaires, meeting notes
├── skills/                  # the 5 diagnostic skills (Skill 1 already built, in zipped form)
├── clients/                 # per-client folders — production chain inside each
├── prospects/               # pre-client tracking (qualified leads, not yet pilots)
├── operations/              # marketing / sales / accounting / legal / it
├── templates/               # branded DOCX, proposal templates, scope-doc, kickoff agenda
├── assets/                  # brand visuals (logo, deck PDF, public web material)
├── infra/                   # bot code, MCP server configs, agent definitions, scripts, hooks
├── knowledge/               # graduated reference (sector files, Quick Win library, RUES/SIEM caches)
└── vault/                   # encrypted catastrophic-loss material (IDs, signed contracts)
```

`00_` prefix keeps governance/system folders at the visual top of any file listing. Function names (no numbering elsewhere) make navigation discoverable for JP without a folder-numbering manual.

### ADR-010 — Per-client production chain

```
clients/<client-slug>/
├── README.md                       # name, sector, country, current phase, owner, last activity
├── state.json                      # phase, status, milestones, KPIs (machine-readable)
├── 00_intake/                      # Prospección — qualification form, initial contact
├── 01_company_analysis/            # Skill 1 output
├── 02_industry_analysis/           # Skill 2 output
├── 03_competitor_analysis/         # Skill 3 output
├── 04_meeting_script/              # Skill 4 output (PRIVATE — never to client)
├── 05_opportunity_report/          # Skill 5 output — the Diagnóstico deliverable
├── 06_proposal/                    # Fase D — modular commercial proposal
├── 07_contract_onboarding/         # Fase E — contract, scope doc, kickoff notes
├── 08_solution_design/             # Paso 10 — solution design (Diseño phase)
├── 09_implementation/              # Paso 11 — implementation artifacts
├── 10_followup/                    # Paso 12 — 30/60/90 reviews, KPI tracking
├── 11_retainer/                    # Paso 13 — ongoing retainer work
├── transcripts/                    # Whisper outputs of meetings (cuts across all phases)
├── communications/                 # email, WhatsApp, Telegram captures
└── archive/                        # superseded versions, withdrawn drafts
```

**Folders stay in place; never moved as phases advance.** Status tracked via `state.json`, not folder location. Moves would break git history.

**Inside each numbered station:** `report.md` (canonical), `report.docx` (Pandoc-rendered branded output), `report.pdf` (client-facing), `manifest.json` (provenance: who/when/what skill version/what prompt version/inputs consumed/sources cited), `inputs/` (snapshot of upstream data for reproducibility).

### ADR-011 — Persona model (3 personas only)

| Persona | Scope | What it does |
|---|---|---|
| **Founder** | root CLAUDE.md | Strategy, partnership, cross-cutting governance, operations functions (marketing, sales, accounting, legal, IT), prospects, knowledge curation. Default when no other persona applies. |
| **Skills-Master** | `skills/CLAUDE.md` | Designs, versions, tests, maintains the 5 diagnostic skills. Owns benchmark cases. |
| **Client-Owner** | `clients/CLAUDE.md` | Production-chain operator. The active client is a parameter, not a separate persona. |

Each persona has a matching `GEMINI.md` for the second-seat reviewer. **6 persona files total**, vs. the personal Brain's ~42.

**Complete CLAUDE.md inventory:**

| Has CLAUDE.md/GEMINI.md | Does NOT have CLAUDE.md/GEMINI.md (operated by Founder) |
|---|---|
| `/` (root) | `00_META/` |
| `skills/` | `00_GOVERNANCE/` |
| `clients/` | `00_PARTNERSHIP/` |
| | `prospects/` |
| | `operations/` (and ALL sub-folders: marketing, sales, accounting, legal, it) |
| | `templates/` |
| | `assets/` |
| | `infra/` |
| | `knowledge/` |
| | `vault/` |

**Why operations sub-folders (marketing, IT, etc.) don't get personas:**
- Specialized voice (marketing tone, accounting strictness, legal precision) belongs in **skills**, not personas. Example: when you want a LinkedIn post, you'd build/invoke `skills/linkedin_post_generator/` whose prompts encode the brand voice — the Founder persona orchestrates the call. **Persona = WHO is operating; Skill = WHAT capability is being used.**
- Adding 5 personas for operations sub-folders alone would put us back on the personal Brain's heavy-persona path that ADR-011 explicitly avoids.
- Path to add a function-specific persona later (if a specialization is so different from "Founder running operations" that the indirection helps): new ADR superseding this one, scoped to the specific function. Not at v0.

**Other folders are data stores**, operated by whichever persona is active. Personas attach to FUNCTION, not LOCATION.

### ADR-012 — Per-skill folder template

```
skills/01_company_analyst/
├── SKILL.md                   # Claude Skill manifest
├── README.md                  # human-readable usage
├── STATUS.md                  # current version, benchmark score, known issues
├── prompts/                   # v1.md, v2.md, v3.md, ... — versioned prompts
├── scripts/                   # extract_financials.py and any other helpers
├── references/                # source guides (RUES/SIEM URL maps), schemas
├── assets/                    # data files (Supersociedades XLSX, sector caches)
├── tests/                     # benchmark cases — the "fixed test company" from Plan Maestro
└── versions/                  # archived prior SKILL.md + prompt versions
```

**Existing `company-analyst.skill.zip` migrates into `skills/01_company_analyst/` at scaffold time** — Day 1 of Plan Maestro Paso 2 is effectively done.

**Per-skill benchmark fixture:** pick one Colombian company (recommend Bodai) as permanent benchmark. Every prompt change re-runs against it. Regression detection without a real client.

### ADR-013 — Inter-folder communication

**Decision:** Replace memo system as the default channel with an append-only `00_META/events.jsonl` log. Memos persist only for genuine "I need a human decision" cases.

Event schema:
```json
{"ts":"2026-05-15T14:23:00-07:00","id":"evt-001","actor":"skill-1-agent","type":"skill.completed","scope":"clients/ascenso","subject":"Skill 1 done for Ascenso","data":{"skill":"01_company_analysis","output":"...","next":"skill_2"}}
```

- Single global file. POSIX atomic append.
- Agents subscribe by filter (`type=skill.completed AND data.skill=01_company_analysis`) and act.
- Humans `tail -f` or use a helper script to see live narrative.
- Telegram bot watches selected event types and pushes to the right channel.
- Log is durable history — never pruned.

**When memos still apply:** human-to-human "I need your explicit decision on X" cases. Frequency drops from weekly (personal Brain) to monthly (company).

### ADR-014 — `00_GOVERNANCE/` shape

```
00_GOVERNANCE/
├── README.md
├── DECISIONS.md                  # one-line index of all ADRs with status
├── adr/                          # ADR-001 through ADR-NNN, one .md per decision
├── system_map.md                 # the architecture diagram
└── proposals/                    # design proposals (this file moves here at scaffold)
```

ADR format: Status · Date · Decided by · Context · Options considered · Decision · Consequences.

### ADR-015 — `00_PARTNERSHIP/` shape

```
00_PARTNERSHIP/
├── README.md
├── PARTNERSHIP_AGREEMENT.md      # founding terms (equity, KPIs, deal-breakers)
├── CONFLICT_PROTOCOL.md          # 15-min raised-hand + 12-24h written-reply (JP's mechanism)
├── REVENUE_DISTRIBUTION.md       # 20/20/20/40 split logic, worked examples
├── ROLES.md                      # Ricardo (ops + BD) · JP (strategy + review)
├── KPIs.md                       # 12-month milestones (3 clients/mo, ≥$5k/mo avg, 85% replicable)
├── questionnaires/
│   ├── 2026-05-07_Ricardo.md     # converted from .docx
│   ├── 2026-05-07_JP.md          # converted from .docx
│   └── 2026-MM-DD_founding_meeting.md   # outcome doc, post-meeting
├── meetings/
│   ├── weekly/                   # Mon planning + Fri retrospective
│   └── decisions/                # ad-hoc decision meetings
├── raised_hand_log.md            # append-only
└── reviews/                      # quarterly partnership reviews
```

**Seeded at scaffold from existing material:**
- `Plan_Maestro_MejiaIACia_Ricardo.docx` → `questionnaires/2026-05-07_Ricardo.md`
- `Plan_Maestro_MejiaIACia_JP.docx` → `questionnaires/2026-05-07_JP.md`
- `Plan_Maestro_MejiaIACia.backup-2026-05-07.docx` → `questionnaires/archive/`
- `Consultoria_IA_PYMEs_v1.pdf` → `assets/` (brand asset)

### ADR-016 — `operations/` sub-tree

```
operations/
├── marketing/                   # brand.md, linkedin.md, content/
├── sales/                       # pipeline.md (Notion snapshot), outreach.md, playbooks/
├── accounting/                  # invoices/ (*.docx.age once PII), expenses.md, tax/
├── legal/                       # entity.md, templates/, compliance.md
└── it/                          # STACK.md, accounts.md (account ownership, NOT credentials)
```

**Distinction:**
- `infra/` = CODE we build (Telegram bot, MCP configs, agent definitions)
- `operations/it/` = SERVICES we subscribe to (Notion, Drive, Gitea, Cal.com, eventually Stripe/DocuSign)

**Sensitive content rule:** anything with PII (invoices once they ship, entity formation docs) is `age`-encrypted in place (`.age` extension). The central vault is for catastrophic-loss material (signed contracts, IDs); routine sensitive operational files live with their function.

---

## Agent Framework

### ADR-017 — Agent framework shape

**Lightweight, multi-path invocation.** Each agent in `infra/agents/<name>/`:

```
infra/agents/skill_1_company_analyst/
├── manifest.json                 # name, version, inputs/outputs, triggers, persona, skill dependency
├── run.py                        # invocation logic
├── README.md
└── tests/
```

`manifest.json` example:
```json
{
  "name": "skill_1_company_analyst",
  "version": "1.0",
  "description": "Run company analysis (Skill 1) on a target company",
  "inputs": ["client_slug", "company_name", "nit?", "sector?"],
  "outputs": ["clients/<client_slug>/01_company_analysis/report.md", "report.docx", "manifest.json"],
  "triggers": [
    {"type": "command", "pattern": "/skill1 <client_slug>"},
    {"type": "event", "match": {"type": "client.created"}},
    {"type": "cli", "name": "skill1"}
  ],
  "persona": "skills_master",
  "skill_dependency": "skills/01_company_analyst",
  "protected_output": true
}
```

**Single dispatcher** at `infra/agents/dispatch.py`. Bot, cron, event watcher, CLI all invoke through it.

**Distinction:**
- **Skills** (`skills/`) = methodology + prompts (the WHAT). Versioned, testable, swappable.
- **Agents** (`infra/agents/`) = thin runtime wrappers that invoke skills with specific inputs (the HOW TO RUN).
- **Claude Code sessions** = interactive human-in-the-loop work. NOT in the agent framework — those are how humans engage directly.

**Four invocation paths, one runtime:**

| Path | Trigger |
|---|---|
| Bot command | `/skill1 ascenso` typed in Telegram |
| Event subscription | `events.jsonl` row matching agent's filter |
| Cron / scheduled | systemd timer (daily 8am pipeline digest) |
| Direct CLI | `mejia agent run skill1 --client ascenso` |

### ADR-018 — Agent inventory

**Day 1:**
1. `skill_1_company_analyst` — wraps existing company-analyst skill
2. `event_notifier` — watches `events.jsonl`, pushes filtered events to Telegram

**Built per skill at Paso 2 progress:**
3. `skill_2_industry_analyst`
4. `skill_3_competitor_analyst`
5. `skill_4_meeting_script`
6. `skill_5_opportunity_report`

**Built when triggered (skeleton manifests at scaffold so the slot exists):**
7. `transcript_processor` (first meeting recorded)
8. `pipeline_orchestrator` (multi-skill chain run)
9. `pipeline_daily_digest` (3+ active clients)

**Planned, documented but not built:**
10. `weekly_review` (Sunday digest)
11. `memo_triager` (incoming memo classification)
12. `client_state_reporter` (one-shot status query)
13. `prospect_classifier` (qualifies inbound prospects against the 5-question pre-filter — JP proposed)

---

## Telegram Bot

### ADR-019 — Bot design

**Channels & auth:** 3 channels (group R+JP, DM-Ricardo, DM-JP). Telegram user-ID allowlist of exactly 2 IDs. Anyone else → silent drop + log entry.

**Capture plugins** (slash commands that file information):

| Command | Lands in | Notes |
|---|---|---|
| `/note <text>` | User's personal inbox (DM) or shared inbox (group) | General note |
| `/idea <text>` | `operations/marketing/ideas.md` or personal | Business ideas |
| `/decision <text>` | `00_GOVERNANCE/proposals/` as ADR draft | Triggers JP-review event |
| `/expense <amt> <cat> <desc>` | `operations/accounting/expenses.md` | Always shared |
| `/photo` | Drive heavy assets + manifest in `00_META/captures/` | Age-encrypt if flagged sensitive |
| `/client <slug> <text>` | `clients/<slug>/communications/<ts>.md` | Always shared (client-scoped) |
| `/meeting <slug>` | Meeting metadata + triggers transcript-processor agent | |
| `/marketing <text>` | `operations/marketing/inbox.md` | Always shared |
| `/prospect <name> <details>` | `prospects/<slug>/intake/` | Always shared, fires `prospect_classifier` when built |
| `/legal <text>` | `operations/legal/inbox.md` | Always shared |
| `/task <description>` | Personal tasks (DM) or shared (group) | |

**Operation plugins:**
- `/status` (all clients) / `/status <client>` (one)
- `/skill1 <client>` ... `/skill5 <client>` — fire skill agents
- `/pipeline run <client>` — fire orchestrator
- `/digest` — manual pipeline digest
- `/list [scope]` — recent captures
- `/ask <question>` — force AI-brain escalation
- `/help` — sectioned command list, Spanish default
- `/whoami` — identity + permissions
- `/done <task-id>` / `/snooze <task-id>`

**AI-brain escalation rules:** default behavior is canned (acknowledge, queue, return status). Escalation only when:
- Explicit `/ask <question>`
- Long natural-language message (>200 chars) without slash command
- Question mark + no command (bot prompts "are you asking me something?")
- Critical events per `00_PARTNERSHIP/CONFLICT_PROTOCOL.md` auto-escalate to both DMs

Cost control: rate-limit AI escalations to 20/hour per user.

**Notification routing:** declarative rules in `infra/telegram/routing.yaml`:
```yaml
- match: {type: skill.completed}
  channels: [group]
- match: {type: client.advanced}
  channels: [group]
- match: {type: meeting.recorded}
  channels: [group]
- match: {type: memo.posted, priority: high}
  channels: [group, dm-ricardo, dm-jp]
- match: {type: agent.failed}
  channels: [dm-ricardo]
- match: {type: pipeline.digest, schedule: morning}
  channels: [group]
- match: {type: capture.acknowledged}
  channels: [originating]
- match: {type: deal_breaker.triggered}
  channels: [dm-ricardo, dm-jp, group]
```

Editing this file = an ADR moment (architecture decision affecting notification flow).

**Standardized message templates:** Jinja2 templates in `infra/telegram/templates/es/<key>.j2`. Spanish default. English variants for legal/tax docs later.

**Implementation stack:** `python-telegram-bot` library + systemd service + SQLite state at `infra/telegram/bot.db` + event-watcher loop polling `events.jsonl` every 5s.

### ADR-020 — Independent codebase

**Decision:** Build the company Telegram bot from scratch in `infra/telegram/bot/`. Personal Brain Telegram Hub at `/srv/brain/12_INITIATIVES/02_BrainTelegramHub/` is **read-only reference**, never imported, never linked.

**Why:**
- Consistent with ADR-002 clean-break decision.
- Multi-user / multi-channel from day 1 is structurally different from single-user personal Hub; retrofitting would cost more than starting fresh.
- JP can audit the company bot codebase in isolation.
- No version coupling, no behavioral drift confusion.

**Patterns to carry over** (read, don't import): python-telegram-bot library choice, systemd service shape, auth-middleware-as-allowlist, plugin framework, BotFather setup, inbox-writer atomic-write pattern, the 113-test suite as a curriculum.

**Cost:** ~1-2 weeks of dev (vs. ~2-3 from pure scratch) with personal Hub as learning shortcut. Worth the isolation.

---

## Stack Inventory

### Stage 1 — deploy now
- **Gitea** (your home server) — git origin
- **GitHub private mirror** — Phase A off-site
- **`age`** — vault + secrets encryption (per-user keys for R + JP)
- **rclone + Drive 2TB (service account)** — heavy assets primary
- **NAS rclone mirror** — heavy assets local secondary
- **Obsidian** — markdown UX + mobile + graph view (with wikilink protocol from day 1)
- **Whisper.cpp** — local audio transcription (Spanish-strong)
- **Pandoc** — markdown → branded DOCX/PDF
- **MCP servers** (filesystem-scoped to company, time, fetch) — agent tool access
- **Cal.com self-hosted** — scheduling
- **Telegram bot** — primary human interface
- **Claude Code + Gemini CLI** — primary + second-seat agents
- **Notion** — CRM + native call recording + meeting docs
- **Zoom Free** — meeting recording (40-min limit, audio → Whisper)

### Stage 1 — investigation queue
- **Odoo** [JP VIEW] — **HIGH PRIORITY**
  - Free Community Edition, self-hostable.
  - PyMEs in target markets (CO/MX) often use it — touching it is unavoidable.
  - Service-line opportunity: "Odoo + IA consulting" can be a billable category.
  - Deployable for clients — sell what you use.
  - Action: Claude+Gemini deep-dive on scope, install effort, learning curve, Brain↔Odoo integration, service-line viability. Decision deferred to post-investigation.

### Stage 2 — deploy on trigger
| Tool | Trigger |
|---|---|
| Codeberg mirror | Phase B (within a few weeks) |
| rclone snapshot of git tree | Phase C-prep |
| Backblaze B2 or Cloudflare R2 | Drive 2TB fills |
| Bitwarden / 1Password org | Shared-login phone access gets routine |
| code-server | JP picks Hosted interface |
| Notion AI | When native Notion-recorded transcripts integration is worth $10/user/mo |
| DocuSign / HelloSign | First contract signed |
| Stripe | First invoice issued |
| Real CRM upgrade | Pipeline > 15 active clients |
| Static-site generator (Astro / Eleventy) | Public website becomes priority |

---

## Roadmap — Spec to First Paying Client

1. **JP review of this proposal** — Ricardo presents the infographic (next deliverable), JP accepts / edits / vetoes per section.
2. **Founding Meeting (Plan Maestro Paso 1)** — must happen before any scaffolding. Ricardo + JP sit down (in-person or video), compare questionnaire answers, ratify the partnership agreement that gets saved to `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md`.
3. **Scaffolding** — Ricardo (with Claude) creates `/srv/mejia-ia-cia/` per this spec, seeds `00_PARTNERSHIP/` from existing material, migrates `company-analyst.skill.zip` into `skills/01_company_analyst/`, sets up Gitea repo + GitHub mirror, generates `age` keys, provisions vault, initializes secrets store, configures rclone for Drive + NAS.
4. **JP's interface chosen and provisioned** — once JP picks Heavy/Hosted/Light, his side gets set up (install or browser-login or Telegram-only).
5. **Telegram bot v0** — independent codebase, builds capture plugins + minimum operation plugins, deploys as systemd service. ~1-2 weeks.
6. **Skills 2-5 built** (Plan Maestro Paso 2 continues from Day 2) — JP proposes initial prompts, Ricardo reviews and refines. 5-6 days.
7. **Three pilot clients run end-to-end** (Plan Maestro Paso 3-4) — diagnostic complete, JP reviews each output, refinements logged.
8. **First paid Diagnóstico** — once quality is consistently 8/10 and at least 1 case study documented. Trigger transition to paid model per Plan Maestro.

---

## [JP VIEW] Items Where Your Input Probably Matters

These are not "JP DECIDES" — Ricardo+Claude have a position. They're items where you may push back hard and we want to hear it BEFORE scaffold.

1. **Odoo positioning** — embrace as service-line bet, or stay focused on the 5-skill diagnostic system as the primary offering? (Ricardo's lean: embrace, because free Community Edition + service-line opportunity is a strong combination.)
2. **Recording / transcription privacy** — we plan to record every client call (audio-only) and run it through Whisper locally for transcript. Clients should know via the scope document. Are you comfortable with the privacy posture, or do you want NDA-by-default first?
3. **Partnership protocol formalization** — your 15-min raised-hand mechanism, Mon+Fri meetings, and Telegram channel are codified in `00_PARTNERSHIP/CONFLICT_PROTOCOL.md`. Sign off on the written form?
4. **First service-line beyond Diagnóstico** — Plan Maestro mentions Diseño / Implementación / Seguimiento / Retainer. Which is the realistic first paid product after Diagnóstico — Diseño, or jump direct to Implementación for satisfied pilots?
5. **Prospect classifier criteria** — JP proposed the 5-question pre-qualification form in the Plan. When we build the `prospect_classifier` agent, what does "qualified" mean? (Minimum revenue threshold? Sector fit? Disposition?)

---

## Decision Ledger — One-Line Index

| ID | Decision | Status |
|---|---|---|
| ADR-001 | System substrate: lightweight Brain + Notion + Telegram | Proposed |
| ADR-002 | Repository home: `/srv/mejia-ia-cia/`, org `Mejia-IACia` | Proposed |
| ADR-003 | Document vault: `age` + per-user keys | Proposed |
| ADR-004 | Secrets: `secrets.env.age` in git | Proposed |
| ADR-005 | Git discipline: PRs on protected paths | Proposed |
| ADR-006 | Backup topology: phased A→B→C + Drive heavy assets | Proposed |
| ADR-007 | AI-vs-human permissions: Layered | Proposed |
| ADR-008 | Heavy assets: Drive 2TB via service account | Proposed |
| ADR-009 | Top-level folder structure: function-based | Proposed |
| ADR-010 | Per-client production chain (13-station) | Proposed |
| ADR-011 | Persona model: 3 personas | Proposed |
| ADR-012 | Per-skill folder template | Proposed |
| ADR-013 | Inter-folder communication: events.jsonl | Proposed |
| ADR-014 | `00_GOVERNANCE/` shape | Proposed |
| ADR-015 | `00_PARTNERSHIP/` shape | Proposed |
| ADR-016 | `operations/` sub-tree | Proposed |
| ADR-017 | Agent framework: lightweight, multi-path | Proposed |
| ADR-018 | Agent inventory | Proposed |
| ADR-019 | Telegram bot design | Proposed |
| ADR-020 | Independent bot codebase | Proposed |

All transition from "Proposed" to "Accepted" when JP has reviewed the infographic and ratified the framework. Specific items he edits become amended ADRs; specific items he vetoes are marked "Rejected" with rationale.

---

## What This Document Does NOT Cover

- **Founding Meeting outcomes.** Plan Maestro Paso 1 must happen separately before scaffold. Outcomes seed `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md`.
- **Full ADR contents.** This file references ADR-001 through ADR-020 in compact form. Full ADRs (Context · Options Considered · Decision · Consequences for each) get written into `00_GOVERNANCE/adr/` at scaffold.
- **Implementation plan.** Next session's deliverable, via the `writing-plans` skill — step-by-step "how do we actually scaffold this" with reviewable checkpoints.
- **The JP infographic.** Separate visual deliverable derived from this spec — what JP actually reviews. Tracked as a follow-up task.
- **Specific Telegram bot copy/UX.** Wireframes for the help menu, exact wording of error messages, etc. — implementation detail.

---

## Glossary

- **Skill** — methodology + prompts + assets for an analytical task. Lives in `skills/`. Versioned, testable. Example: `skills/01_company_analyst/` (already built).
- **Agent** — thin runtime wrapper that invokes a skill with specific inputs and emits events. Lives in `infra/agents/`. Example: `skill_1_company_analyst` agent wraps the `01_company_analyst` skill.
- **Persona** — scope-attached identity defined by CLAUDE.md (Founder, Skills-Master, Client-Owner). Determines how Claude operates in that scope.
- **ADR** — Architecture Decision Record. Lightweight markdown file capturing one decision: status, date, context, options, decision, consequences. Lives in `00_GOVERNANCE/adr/`.
- **Production chain** — the 13-station per-client folder pipeline (`00_intake/` through `11_retainer/` plus `transcripts/` and `communications/`).
- **events.jsonl** — append-only log at `00_META/events.jsonl` capturing every cross-folder action. Default inter-folder communication channel; memos rare.
- **Vault** — `age`-encrypted store in `vault/` for catastrophic-loss material (signed contracts, IDs). Routine sensitive operational files (invoices, entity docs) live `.age`-encrypted with their function.
- **Protected paths** — files requiring PR review per ADR-005: `skills/*/prompts/`, `clients/*/deliverables/`, `clients/*/proposals/`, `clients/*/contracts/`.
- **Stage 1 / Stage 2** — tools we deploy now vs. tools deferred until a specific trigger fires.
