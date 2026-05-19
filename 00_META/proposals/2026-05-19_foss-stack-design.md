---
status: Accepted (design — execution is Plan 02 territory)
date: 2026-05-19
decided_by: Ricardo + Claude (Founder persona, /srv/Nexostrat/ session 6)
supersedes: ADR-038 § "Plan 02 brainstorm deferral" — this document is the brainstorm output
related:
  - 00_GOVERNANCE/adr/ADR-024-dual-meeting-capture.md
  - 00_GOVERNANCE/adr/ADR-026-ollama-local-summary.md
  - 00_GOVERNANCE/adr/ADR-027-intake-two-file-split.md
  - 00_GOVERNANCE/adr/ADR-029-no-n8n-python-systemd.md
  - 00_GOVERNANCE/adr/ADR-034-ambient-chat-extraction.md
  - 00_GOVERNANCE/adr/ADR-037-notion-canonical-role.md
  - 00_GOVERNANCE/adr/ADR-038-drop-notion-foss-tbd.md
  - 00_META/plans/README.md
  - 00_META/proposals/2026-05-13_nexostrat-system-design.md
unlocks:
  - Plan 02 (Documentation System — now expanded to include FOSS stack integration)
  - Plan 04 (Telegram bot — consumes Baserow API)
  - Plan 07 (Per-client production chain — Baserow rows track pipeline state)
  - Plan 08 (Meeting pipeline — meetings table is the canonical record)
---

# FOSS Stack Design — Baserow + BookStack

Brainstorm output for the FOSS stack decision deferred by ADR-038. This document is the design; Plan 02 is the execution.

## 1. Context & motivation

ADR-038 (2026-05-15) removed Notion from the Nexostrat architecture at the firm level and assigned four roles to a FOSS replacement to be decided at the start of Plan 02:

1. Meeting capture canonical
2. Summary generation
3. CRM
4. Collaborative docs workspace

ADR-038 also marked one role as implicit: JP's dashboard / window into Nexostrat (since JP-Light per ADR-021bis opts out of Gitea web).

Two of the four roles were effectively already decided by prior ADRs:
- **Meeting capture canonical:** Whisper.cpp + Jitsi (already shadow per ADR-024, promoted to canonical pending Plan 02 confirmation).
- **Summary generation:** Ollama (already in stack per ADR-026 + ADR-034).

This brainstorm closes the remaining two roles (CRM + collaborative docs workspace) and confirms how JP's dashboard role is fulfilled (Telegram bot consuming the CRM tool's API).

## 2. Decisions

| Role | Tool chosen | License | Cost |
|---|---|---|---|
| Meeting capture canonical | Whisper.cpp + Jitsi (confirmed) | already in stack | $0 |
| Summary generation | Ollama (confirmed) | already in stack | $0 |
| **State-store / CRM (metadata + relations)** | **Baserow Community Edition** | MIT | $0 forever |
| **Workspace docs (Ricardo-only, longform)** | **BookStack** | MIT | $0 forever |
| Dashboard / JP-facing | Telegram bot (Plan 04) queries Baserow REST | n/a | $0 |
| CRM artefacts (deliverable files) | filesystem `pipeline/clients/<slug>/` (unchanged) | n/a | $0 |

**Integration philosophy locked:** Intermediate — keep maximum existing infrastructure, add exactly one new collaborative-tool surface for Ricardo (BookStack), plus one state-store the Telegram bot can query reliably (Baserow). JP never accesses the GUI tools; his only surface is Telegram + email digests.

**Rationale for Baserow over AppFlowy / Twenty / NocoDB:**
1. API stability is non-negotiable — JP's only window is the Telegram bot, which queries the state-store. Baserow REST API has been stable since 2019; AppFlowy GraphQL is still maturing.
2. Pure MIT license — no BSL nuances, no dual-licensing premium features the firm needs, no fee structure ever.
3. Mature self-host with official Docker images, active maintainer team with commercial traction (revenue from cloud tier funds the FOSS work).

**Rationale for BookStack over Outline / AppFlowy / Wiki.js:**
1. Pure MIT license vs Outline's BSL 1.1 (which is free for internal use but has restrictions on competitive re-hosting).
2. Mature since 2015, simple PHP+MySQL stack, single-container deployment.
3. Hierarchical organization (shelves > books > chapters > pages) fits longform reference content well.

## 3. Architecture

### 3.1 Service topology

```
HP server (ricardo-hp-laptop, Linux Mint 22.2, Tailscale 100.64.121.80)
├── docker network: nexostrat_net
│   ├── baserow         :8090   (Postgres backend internal to container)
│   ├── bookstack       :8091   (MySQL backend internal to container)
│   ├── whisper-cpp     :8092   (already deployed)
│   ├── jitsi-meet      :8093   (already deployed)
│   ├── ollama          :11434  (already deployed)
│   ├── telegram-bot    :8094   (Plan 04 — consumes baserow:8090 via REST)
│   └── caddy-internal  :443    (reverse proxy, TLS, routing by subdomain)
│
└── filesystem (git tracked)
    └── pipeline/clients/<slug>/  (deliverable artefacts — unchanged)
```

### 3.2 Exposure model

- All services bind `0.0.0.0` inside the docker network.
- Caddy internal provides TLS + subdomain routing: `baserow.nexostrat.local`, `docs.nexostrat.local`, `meet.nexostrat.local`.
- HP firewall blocks WAN access to these ports. Only Tailscale peers reach the services.
- JP never accesses Baserow / BookStack UI. His only surface is Telegram bot (which runs server-side and queries Baserow API).

### 3.3 Cost envelope

- Software: $0/mo forever (MIT for both tools).
- Compute: incremental on existing HP. Baserow + BookStack add ~1-1.5 GB RAM + ~50 GB disk projected for Stage 1.
- Backup: included in Plan 01b warm-rsync timer (when warm-standby host arrives).

## 4. Data model — Baserow

**Stage 1 MVP: 4 tables.** YAGNI strict — only what the Telegram bot needs to answer real questions this week.

### 4.1 Table `clients`

| Field | Type | Notes |
|---|---|---|
| id | auto | Baserow PK |
| slug | text (unique) | Links to `pipeline/clients/<slug>/` folder |
| name | text | Legal entity name |
| display_name | text | Short name for display |
| country | single-select | `CO` / `MX` |
| rfc_nit | text | RFC (MX) or NIT (CO); nullable until obtained |
| sector | text | Descriptive |
| phase | single-select | `prospect` / `intake` / `diagnostico_in_progress` / `diagnostico_delivered` / `roadmap_offered` / `roadmap_in_progress` / `retainer_active` / `dormant` |
| pilot | bool | True for Stage 1 pilots |
| source | single-select | `inbound` / `outbound` / `referido` / `marketing` |
| decisor_name | text | Real decision-maker |
| decisor_role | text | Director / Founder / etc. |
| contact_name | text | Door-into-the-account (may differ from decisor) |
| contact_phone | text | WhatsApp / Telegram principal |
| contact_email | text | |
| folder_path | formula | Computed: `"pipeline/clients/" + slug + "/"` |
| created_at | created-on | Auto |
| updated_at | last-modified | Auto |

### 4.2 Table `meetings`

| Field | Type | Notes |
|---|---|---|
| id | auto | |
| client | link → clients | |
| date | date+time | TZ-aware |
| location | text | Physical address or Jitsi room URL |
| kind | single-select | `discovery` / `feedback` / `roadmap_kickoff` / `check_in` / `internal_r_jp` |
| attendees_text | long text | Names + roles (Stage 1 — no separate contacts table) |
| status | single-select | `planned` / `confirmed` / `recorded` / `transcribed` / `extracted` / `cancelled` |
| recording_path | text | `vault/clients/<slug>/meetings/<date>.age` |
| transcript_path | text | `pipeline/clients/<slug>/05_meetings/transcripts/...` |
| notes_path | text | Path to `.md` notes |
| duration_min | number | |
| created_at | created-on | |

### 4.3 Table `deliverables`

| Field | Type | Notes |
|---|---|---|
| id | auto | |
| client | link → clients | |
| skill | single-select | `company-analyst` / `industry-analyst` / `competitor-analyst` / `discovery-meeting` / `opportunity-report` |
| file_md | text | Path to `.md` |
| file_docx | text | Path to `.docx` |
| file_pdf | text | Path to `.pdf` (nullable until rendered) |
| status | single-select | `draft` / `internal_review` / `delivered` / `revised` |
| created_at | created-on | |
| delivered_at | date | Nullable |
| delivered_via | single-select | `email` / `whatsapp` / `in_person` / `not_yet` |

### 4.4 Table `financials`

| Field | Type | Notes |
|---|---|---|
| id | auto | |
| client | link → clients | Nullable (firm-level expenses have no client) |
| kind | single-select | `income` / `expense` |
| amount | number (decimal) | |
| currency | single-select | `MXN` / `COP` / `USD` |
| date | date | |
| status | single-select | `pending` / `received` / `paid` / `cancelled` |
| description | text | |
| invoice_path | text | Path to invoice (age-encrypted in `vault/accounting/`) |

### 4.5 Predefined views (Baserow Views)

Bot queries these directly by view ID instead of building filters at runtime.

- `clients`: **Pipeline activo** (phase ≠ dormant), **Pilotos** (pilot=true), **Por país**.
- `meetings`: **Próximas** (date >= today, sort asc), **Esta semana**, **Pendientes de transcripción** (status=recorded).
- `deliverables`: **Esta semana**, **En revisión interna** (status=internal_review), **Por skill**.
- `financials`: **Mes en curso**, **Por cobrar** (kind=income, status=pending).

### 4.6 Explicit non-goals for Stage 1 Baserow

- **Separate `contacts` table** — keep contacts as fields in `clients` + free text in `meetings.attendees_text`. Refactor when a client crosses 5+ active contacts.
- **`tasks_per_client` table** — root `tasks.json` remains source. Bot queries the JSON, not Baserow, for tasks.
- **`pipeline_events` log table** — `events.jsonl` (Plan 03) is the source. Baserow does not duplicate.
- **`service_offerings` catalog table** — lives in BookStack (one page per service). Stage 1 has 2 services (free Diagnóstico + future Hoja de Ruta).

## 5. Workspace docs — BookStack

### 5.1 Philosophy

BookStack is Ricardo's longform workspace. **JP never enters.** Git remains canonical for accepted ADRs, spec, plans, `tasks.json`, `calendar.json`. BookStack handles content that is too fluid for git OR too scattered to live in a single pipeline folder.

### 5.2 What lives in BookStack

- Operational playbooks (how to run X, how to handle Y)
- Accumulating sector knowledge (grows session by session)
- Drafts of ADRs / spec changes before git commitment
- Pricing experiments, service-model thinking, positioning
- Glossary / internal references / tooling notes

### 5.3 What does NOT live in BookStack

- Skill outputs (live in `pipeline/clients/<slug>/`)
- Accepted ADRs, spec, plans, `tasks.json`, `calendar.json` (live in git)
- Age-encrypted vault (lives in `vault/`)
- Cross-persona memos (live in `<scope>/00_META/inbox/`)
- Client / meeting / deliverable / financial metadata (lives in Baserow)

### 5.4 Initial structure

```
BookStack
├── Playbooks
│   ├── Book: Sales            (cold outbound, follow-up, objections, pricing-talk)
│   └── Book: Operations       (pre-meeting checklist, post-meeting, render workflow, brand)
│
├── Industries                  (sector knowledge accumulator)
│   └── Book: Logística-cross-border-MX  (seeded from Trixx, grows with future clients)
│
├── Drafts                      (sandbox before promotion to git)
│   ├── Book: ADRs-draft
│   ├── Book: Pricing
│   └── Book: Service-design
│
└── References
    ├── Book: Glossary
    ├── Book: Tooling
    └── Book: Templates
```

### 5.5 Initial seeding (Plan 02 deliverable)

Create the structure + seed exactly 7 pages with content that **already exists** and clearly fits BookStack better than git:

| Shelf > Book | Initial page |
|---|---|
| Playbooks > Operations | "Pre-meeting checklist Trixx-derived" (extracted from session 5) |
| Playbooks > Operations | "Post-meeting protocol" (what to do with recording + notes) |
| Industries > Logística-cross-border-MX | "Términos clave + Reforma 2026" (extracted from Skill 02 Trixx) |
| Industries > Logística-cross-border-MX | "Mapa competitivo MX cross-border" (extracted from Skill 03 Trixx) |
| Drafts > Pricing | "Hoja de Ruta de IA — scope + pricing experiment" (placeholder) |
| References > Glossary | "Términos Nexostrat" (Diagnóstico, Hoja de Ruta, Skill 01-05) |
| References > Templates | "Checklist de session-end" (extracted from CLAUDE.md) |

All other pages are added organically by Ricardo as need arises.

### 5.6 Auth + access

- **Single user (Ricardo).** Email/password. JP never enters.
- Access via Tailscale only (Caddy routes `docs.nexostrat.local` to BookStack).
- Backup: MySQL dump nightly age-encrypted, included in warm-rsync.

### 5.7 BookStack non-goals for Stage 1

- **SSO** — single-user, email/password is sufficient. Add later if team grows.
- **Page versioning as source-of-truth** — git stays canonical for official docs. BookStack is scratchpad.
- **Auto-sync with git** — no automatic sync. When a BookStack page matures into an official doc, Ricardo manually copies it to `docs/` or `00_GOVERNANCE/`.
- **Public-facing pages** — everything is internal. Public docs (if ever) follow `docs/` Diátaxis tier-1/-2 in git.

## 6. Integration points

### 6.1 Telegram bot → Baserow (read queries)

| Bot command | Baserow query | Stage |
|---|---|---|
| `/status <slug>` | GET clients?filter=slug + recent meetings + latest deliverables | **Stage 1** |
| `/upcoming` | GET meetings?filter=date>=today&sort=date asc&limit=5 | **Stage 1** |
| `/this-week` | GET deliverables?filter=created_at>=-7d + meetings >= -7d | **Stage 1** |
| `/finanzas` | GET financials?filter=date>=start_of_month, aggregated | **Stage 1** |
| `/pipeline` | GET clients?view=Pipeline activo, grouped by phase | **Stage 1** |
| `/new-meeting <slug> <date>` | POST meetings | Stage 2 (Plan 04 write surface) |
| `/note <slug> <texto>` | POST BookStack page for client | Stage 2 (Plan 04) |

**Auth:** API token `nexostrat-internal` stored in `secrets.env.age`, consumed via `run-with-secrets.sh`. Read-heavy, narrow write surface (`meetings.notes_path`, `deliverables.status` only).

**Latency budget:** queries respond <500ms p95. Baserow on HP via Tailscale RTT <5ms; simple queries complete <50ms.

### 6.2 `new-client.sh` → Baserow (client creation)

`new-client.sh` is extended in Plan 02 to:

1. Create the folder scaffold (current behavior).
2. POST a row to Baserow `clients` table with initial fields (slug, name, country, sector, pilot, phase=prospect, source).
3. Return the Baserow `client_id` for downstream use.

**Idempotency:** if `slug` already exists in Baserow, skip with warning, do not error.

**Source-of-truth conflict between `state.json` and Baserow `clients` row:**
- Baserow = canonical source-of-truth for metadata.
- `state.json` = local cache + bootstrap (read by Claude Code at session start, updated by scripts/bot).
- Sync: explicit script `infra/scripts/sync-state-from-baserow.sh` reconciles on-demand. Plan 03 event-router automates the propagation when it lands.

### 6.3 Skill renderers → Baserow (`deliverables`)

When a skill produces a `.docx` / `.pdf`:

1. The renderer writes the file to `pipeline/clients/<slug>/<station>/runs/<date>_mode-a/<filename>` (current behavior).
2. The renderer calls `skills/shared/baserow.py:post_deliverable(client_slug, skill_name, paths)` which POSTs a `deliverables` row.
3. **Idempotency:** dedupe by `(client_slug, skill, file_md path)`. If a row matches, UPDATE in place rather than INSERT.

**Helper module `skills/shared/baserow.py`:** ~50 LOC. Exposes `post_client(...)`, `post_meeting(...)`, `post_deliverable(...)`, `update_status(...)`. Loads token from `secrets.env.age` via `run-with-secrets.sh` wrapper.

### 6.4 Meeting capture → Baserow

**Stage 1 — manual.** Ricardo creates the `meetings` row in Baserow UI before the meeting. After the meeting:
1. Upload recording to `vault/clients/<slug>/meetings/<date>.age`.
2. Paste the path into `recording_path` field.
3. Update `status` to `recorded`.

**Stage 2 (Plan 08):** Whisper transcribes → script updates `transcript_path` + `status=transcribed`. Ollama extracts → `status=extracted`.

### 6.5 events.jsonl → Baserow (Plan 03 event-router)

Plan 03's event-router daemon translates `events.jsonl` events into Baserow mutations:

| Event | Baserow effect |
|---|---|
| `client.created` | INSERT clients |
| `client.phase_changed` | UPDATE clients.phase |
| `meeting.recorded` | UPDATE meetings.status=recorded, recording_path |
| `meeting.transcribed` | UPDATE meetings.status=transcribed, transcript_path |
| `meeting.extracted` | UPDATE meetings.status=extracted |
| `deliverable.created` | INSERT deliverables |
| `deliverable.delivered` | UPDATE deliverables.status=delivered, delivered_at, delivered_via |
| `financial.recorded` | INSERT financials |

**Stage 1 does NOT include event-router.** Stage 1 paths are direct (script → Baserow REST). When Plan 03 lands, event-router consolidates and becomes the single write channel.

### 6.6 Daily brief → Baserow

Plan 03 deliverable `daily_brief.py` runs 07:00 in each user's TZ. Compiles:
- Next 24h: meetings (Baserow query), tasks due (`tasks.json`), open inbox memos.
- Last 24h: deliverables created, phases changed, relevant events.

Output: Telegram message per user.

### 6.7 BookStack — minimal automated integration

BookStack is Ricardo-only longform. Stage 1 has no significant automated integration.

- **Outbound links:** BookStack pages may link to filesystem paths (`file:///srv/Nexostrat/...`) or Gitea URLs. Manual.
- **Backups:** nightly MySQL dump age-encrypted, included in warm-rsync.
- **Search:** native BookStack full-text search. Sufficient for Stage 1.
- **Stage 2+ optional:** BookStack webhook → `events.jsonl` when a page publishes. YAGNI for now.

### 6.8 Stage 1 vs Stage 2 summary

**Stage 1 (Plan 02 delivers):**
- Baserow + BookStack hosted, schema loaded, initial seeding done
- `new-client.sh` extended with Baserow POST
- 5 skill renderers extended with `deliverables` POST
- Common helper `skills/shared/baserow.py` (~50 LOC)
- `infra/scripts/baserow-reconcile.sh` nightly
- Meetings: manual UI in Baserow

**Stage 2+ (Plans 03, 04, 08):**
- Event-router → Baserow propagation (Plan 03)
- Telegram bot read + write commands (Plan 04)
- Whisper auto-updates `meetings.status` (Plan 08)

## 7. Failure modes, backup, recovery

### 7.1 Backup strategy

| Component | Mechanism | Cadence | Local path | Off-site |
|---|---|---|---|---|
| Baserow Postgres | `pg_dump` → age-encrypt | nightly 02:30 TZ | `vault/backups/baserow/YYYY-MM-DD.sql.age` | warm-rsync (Plan 01b) |
| BookStack MySQL | `mysqldump` → age-encrypt | nightly 02:30 TZ | `vault/backups/bookstack/YYYY-MM-DD.sql.age` | warm-rsync |
| Baserow uploads | `tar.gz` → age-encrypt | nightly 02:30 TZ | `vault/backups/baserow-uploads/YYYY-MM-DD.tar.gz.age` | warm-rsync |
| BookStack uploads | `tar.gz` → age-encrypt | nightly 02:30 TZ | `vault/backups/bookstack-uploads/YYYY-MM-DD.tar.gz.age` | warm-rsync |
| Baserow schema snapshot | export schema JSON | weekly + on schema change | `infra/baserow/schema/YYYY-MM-DD.json` (git tracked) | git origin + mirrors |

**Retention:** 30 days local (cron purge), 90 days warm-standby.

**RPO target:** 24h max (nightly cadence). Acceptable Stage 1 given low write volume (1-2 clients touch/day, 0-1 meeting/day, 0-2 deliverables/day). 24h loss recovery: ~10 min manual repopulation from filesystem (skill outputs remain).

**RTO target:** 30 min for Baserow + 30 min BookStack (parallelizable) = 30 min wallclock total.

### 7.2 Failure modes

| # | Mode | Detection | Response | RTO |
|---|---|---|---|---|
| F1 | Baserow container crash | systemctl / `/health` fails | `docker compose restart baserow` | 1-2 min |
| F2 | Baserow Postgres corruption | restart loops / pg logs | `infra/recovery/restore-baserow.sh <date>` | 15-20 min |
| F3 | Baserow total data loss | volume corrupt / disk failure | F2 path + warm-standby failover if HP disk | 30 min |
| F4 | BookStack container crash | systemctl / `/health` fails | `docker compose restart bookstack` | 1-2 min |
| F5 | BookStack MySQL corruption | restart loops / mysql logs | `infra/recovery/restore-bookstack.sh <date>` | 15-20 min |
| F6 | BookStack total data loss | volume corrupt / disk failure | F5 path + warm-standby failover | 30 min |
| F7 | HP server total down | Tailscale ping fails | `docs/runbooks/hp_down.md` (Plan 01b) — failover to warm-standby | 15-30 min |
| F8 | API token leak / compromise | unauthorized requests in logs | revoke in tool UI + regenerate + re-encrypt `secrets.env.age` + restart services | 10 min |
| F9 | Schema drift (UI edit accidental) | weekly schema-check diff fails | `baserow-schema-check.sh` alerts Telegram. Recover by applying canonical schema | 20 min |
| F10 | Bot Telegram queries fail (Baserow unreachable) | bot health check fails | Bot fallback: read `state.json` cache + disclaimer "data may be stale" | 0 min |
| F11 | Skill renderer POST fails (network blip) | logs show 5xx/timeout | Renderer logs error to `<run-dir>/.baserow-post-error.log`. File still produced. Nightly `baserow-reconcile.sh` detects orphan deliverables and creates rows retroactively | 24h |
| F12 | Disk full on HP | `df` watch alert | Purge backups >30 days + alert Ricardo | 5 min |

### 7.3 Recovery scripts (Plan 02 deliverable)

Under `infra/recovery/`:

- `restore-baserow.sh <date>` — decrypt + pg_restore + restart container, validates health.
- `restore-bookstack.sh <date>` — equivalent for MySQL.
- `baserow-schema-check.sh` — weekly, diff current schema vs `infra/baserow/schema/canonical.json`, alert on drift.
- `baserow-reconcile.sh` — nightly, scan filesystem for orphan deliverables, create rows retroactively.
- `baserow-rotate-token.sh` — semi-manual playbook (requires Baserow UI for revoke + regenerate).

### 7.4 Runbooks (Plan 02 deliverable)

New runbooks under `docs/runbooks/`:

- `baserow_down.md` — F1-F3
- `bookstack_down.md` — F4-F6
- `baserow_token_compromise.md` — F8
- `baserow_schema_drift.md` — F9
- `baserow_reconcile.md` — F11 manual trigger + output interpretation

`docs/runbooks/hp_down.md` (Plan 01b) extends to include Baserow + BookStack in the warm-standby boot sequence.

### 7.5 Non-obvious decisions

- **Source-of-truth during recovery:** if Baserow restore leaves pre-incident state and filesystem has post-incident artefacts, **filesystem wins.** Skill outputs always write to filesystem first. `baserow-reconcile.sh` aligns Baserow to filesystem post-restore.
- **Canonical schema:** lives in git (`infra/baserow/schema/canonical.json`). UI edits by Ricardo must be intentional — if they break canonical, weekly check alerts and Ricardo decides commit-new vs revert.
- **Token rotation is not zero-downtime Stage 1:** restart of bot + skill renderers during rotation = ~30s of failed queries. Acceptable Stage 1 (manual, off-hours). Plan 10 may improve.
- **No active streaming replication Stage 1:** rsync nightly only. Active replication is Stage 2 if throughput justifies. RPO 24h is fine for Stage 1 volume.

## 8. Plan 02 MVP scope, deferrals, dependencies

### 8.1 Plan 02 deliverables (Stage 1 MVP)

**Deployment:**
- `infra/docker/foss-stack/docker-compose.yml` with `baserow`, `bookstack`, `caddy-internal`
- systemd unit `nexostrat-foss-stack.service` (boot-on-start)
- Tailscale-only exposure verified (positive test from Tailscale peer, negative test from WAN)
- Backup systemd timers (nightly 02:30) installed + dry-run validated

**Baserow:**
- 4 tables (clients, meetings, deliverables, financials) per Section 4 schema
- Predefined views installed
- API token `nexostrat-internal` generated, stored in `secrets.env.age`
- Schema snapshot committed to `infra/baserow/schema/canonical.json`

**BookStack:**
- 4 shelves + books per Section 5
- 7 initial pages seeded
- Ricardo email/password auth configured
- Backup unit for MySQL dump included

**Integrations:**
- `infra/scripts/new-client.sh` extended with Baserow POST (idempotent)
- 5 skill renderers extended via `skills/shared/baserow.py` helper
- `infra/scripts/baserow-reconcile.sh` installed + nightly timer

**Recovery:**
- 5 scripts under `infra/recovery/`
- 5 runbooks under `docs/runbooks/`
- Weekly schema-check timer + Telegram alert on drift

**Tests:**
- `infra/scripts/smoke-test.sh` extended with Baserow + BookStack health checks + reconcile dry-run
- Integration test: scaffold test client → verify Baserow row → drop → verify clean
- Recovery test: pg_dump + pg_restore round-trip end-to-end

### 8.2 Explicitly DEFERRED (not in Plan 02)

| Item | Lands in |
|---|---|
| Event-router → Baserow propagation | Plan 03 |
| `events.jsonl` schemas for Baserow operations | Plan 03 |
| Telegram bot read commands (`/status`, `/upcoming`, etc.) | Plan 04 |
| Telegram bot write commands (`/new-meeting`, `/note`) | Plan 04 (optional Stage 1) |
| Auto-update `meetings.status` post-Whisper | Plan 08 |
| Auto-extract decisions/actions/dates → `tasks.json` | Plan 08 |
| Ambient chat → propose Baserow updates | Plan 09 |
| BookStack SSO | Post-Stage-1 if team grows |
| BookStack page versioning as source-of-truth | Never (git stays canonical) |
| BookStack webhook → `events.jsonl` | YAGNI / Plan 09+ if justifies |
| Baserow active streaming replication | Post-Stage-1 if throughput justifies |
| Public-facing docs/sites | Stays in git+Diátaxis tier-1/-2 (not BookStack) |

### 8.3 Dependencies

**Hard prerequisites (satisfied):**
- ✅ Foundation milestone `v0.1-foundation` reached (Plan 01c done)
- ✅ `vault/` working + age keys configured (Plan 01a done)
- ✅ Docker stack base installed on HP

**Soft prerequisites (not blocking):**
- Plan 01b warm-standby Tasks 7-12 — for rsync destination. Plan 02 can land without; backups stay local until second host arrives.
- Plan 04 Telegram bot — Plan 02 leaves API token + schema ready; bot consumes when it lands.
- Plan 03 event-router — Plan 02 writes directly to Baserow from scripts; event-router is later optimization.

### 8.4 Effort estimate

| Component | Days |
|---|---|
| Deploy compose + Caddy + backup timers | 1 |
| Baserow schema + seeding + views | 0.5 |
| BookStack setup + 7 seeded pages | 0.5 |
| `new-client.sh` extension + `skills/shared/baserow.py` + 5 renderer extensions | 1 |
| Recovery scripts + runbooks (5 + 5) | 1 |
| Tests + smoke-test extension | 0.5 |
| **Docs Diátaxis original Plan 02 scope** (auto-gens, drift hook, 15 ADRs, 10 how-tos) | 2 |
| Buffer | 0.5-1 |
| **Total** | **7-7.5 days execute** |

**Note:** this brainstorm expands Plan 02 beyond the original master-index estimate (~3 days). The original 3-day scope was only "Docs Diátaxis." The FOSS stack adds ~4-4.5 days.

### 8.5 Success criteria (Plan 02 done)

- `docker compose up` in `infra/docker/foss-stack/` brings stack up in <60s
- `https://baserow.nexostrat.local` and `https://docs.nexostrat.local` return 200 from Tailscale, fail from WAN
- `infra/scripts/smoke-test.sh` extended passes all checks
- `new-client.sh` creating test client → folder + Baserow row + `state.json` synchronized
- Skill 01 on test client → file + `deliverables` row in Baserow
- Backup nightly produces valid `.age` file, decrypt verifies
- Recovery: `restore-baserow.sh <date>` round-trip passes
- 7 pages visible in BookStack via web
- Canonical schema snapshot committed
- Repo tagged `v0.2-foss-stack` (or equivalent set in Plan 02)

## 9. Open questions / decisions for later

These are intentionally deferred — listed here so they do not get lost.

1. **Baserow vs NocoDB final pick re-evaluation.** Stage 1 ships Baserow. If after 6+ months a specific Baserow limitation hurts, swap is straightforward (both have import/export). Re-evaluate at Stage 2 review.
2. **BookStack vs Outline re-evaluation.** Same shape — if Outline matures licensing or BookStack proves limiting, swap is feasible.
3. **Stage 2 trigger for active streaming replication of Baserow.** Currently nightly rsync. Trigger: if data write volume crosses ~50 writes/hour sustained OR client SLA requires <1h RPO.
4. **JP-Heavy flip implications.** If JP flips from Light to Heavy (per ADR-021bis), he gets a Gitea web account and may want BookStack access. Plan 02 leaves the door open by not committing single-user-forever.
5. **Tailscale subnet routing for client viewing.** Currently Tailscale is internal-only. If a client ever needs read access to a specific BookStack page or Baserow view, a different mechanism is required (read-only proxy, signed URL, manual export). Not Stage 1.

## 10. Change log

| Date | Agent | Description |
|---|---|---|
| 2026-05-19 | Claude (Opus 4.7 1M, Founder persona, session 6) | Initial design from brainstorm. Sections 1-8 approved by Ricardo incrementally before write. Tooling locked: Baserow Community Edition (MIT) + BookStack (MIT). Confirms Whisper.cpp + Jitsi (already in stack per ADR-024). Confirms Ollama (already in stack per ADR-026/034). Plan 02 scope expanded to include FOSS stack integration alongside original Docs Diátaxis work — estimate 6-7 days vs original 3. |
