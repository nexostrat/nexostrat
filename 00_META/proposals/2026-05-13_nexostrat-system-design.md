# Nexostrat — System Design (Founding Spec v1)

> **Status:** ACTIVE — Batch 1 amendments applied 2026-05-14 (commits `dc5cbec`/`5f126a7`/`d5ebbf9`); ADR-038 (Notion drop) spec-body integration applied 2026-05-16 via `t-spec-notion-removal-amendment` sweep post-hard-system-audit. Plan 01a tagged `v0.1a-foundation` 2026-05-16.
> **Date:** 2026-05-13 (initial draft) · 2026-05-14 (Batch 1 amendments) · 2026-05-16 (ADR-038 sweep)
> **Authors:** Ricardo Mejía Caicedo + Claude (Opus 4.7, 1M context)
> **Audience:** Ricardo, Juan Pablo, future operators (hires, contractors, AI personas)
> **Supersedes:** [`2026-05-11_company-system-design.md`](2026-05-11_company-system-design.md) (extends; ADRs 001-020 retained with amendments per ADRs 021-028)
> **Purpose:** Lock the architectural shape of Nexostrat before scaffolding. Single source of truth for what gets built in Stage 1.

---

## Executive Summary

Nexostrat is Ricardo and JP's AI consulting firm for small and medium businesses ("PyMEs") in Mexico, Colombia, and Latin America. The architectural goal of this document is to make the system **bulletproof, replicable, AI-first, and JP-readable**. Same artifacts every time, same locations, same protocols, same recovery paths.

The system runs on three machines today (HP server live, second laptop warm-standby, Ricardo's desktop for GPU work) plus Telegram on phones, with a clean upgrade path for JP's eventual Heavy mode. Documentation is paired (technical + plain English) so both founders understand every piece. Pipelines support **two modes that produce identical artifacts**: manual (CLI session, zero API spend) and automated (Python agents calling APIs, with explicit human gates). Both modes write to the same folders so we can run them in parallel during the trial phase and compare outputs.

All decisions in this document were reached during the 2026-05-13 brainstorming session and represent ratified architecture. ADRs 021-028 are new in this session; ADRs 001-020 carry forward from the prior spec with amendments noted inline.

---

## How to Read This Document

- **Ricardo, JP** — every numbered section maps to one operational concern. Skim section headers first; drill into anything that affects daily work. The `Open Items` list at the end shows what's pending your input.
- **Future operators (hires, contractors)** — the 10 sections are the canonical architecture. `docs/` is the user manual built from this spec. ADRs in `00_GOVERNANCE/adr/` are the durable record of why each decision was made.
- **AI personas** — read this in full before any session at Nexostrat root. Cross-reference with the canonical `00_META/shared/` stanzas in CLAUDE.md per persona.

---

## ADR Map

| ADR | Title | Status | Source |
|---|---|---|---|
| ADR-001 | System substrate: markdown-in-git + Telegram + FOSS workspace (Plan 02 TBD) | **Amended** | 2026-05-11 spec (rebranded). Amended 2026-05-16 per ADR-038: Notion removed from substrate; FOSS replacement decided in Plan 02 brainstorm. |
| ADR-002 | Repository home: `/srv/Nexostrat/`, Gitea org `nexostrat` | Amended | 2026-05-11 spec (path updated for brand) |
| ADR-003 | Document vault: `age` per-user keys | Accepted | 2026-05-11 |
| ADR-004 | Secrets: `secrets.env.age` in git | Accepted | 2026-05-11 |
| ADR-005 | Git discipline: PRs on protected paths | Amended | 2026-05-11 (protected-path list updated for 3-bucket layout per ADR-021) |
| ADR-006 | Backup topology: phased A→B→C + Drive heavy assets | Amended | 2026-05-11 (warm-standby added per ADR-023) |
| ADR-007 | AI-vs-human permissions: layered | Accepted | 2026-05-11 |
| ADR-008 | Heavy assets: Drive 2TB via OAuth | Accepted | 2026-05-11 |
| ADR-009 | Top-level folder structure | **Superseded** | replaced by ADR-021 |
| ADR-010 | Per-client production chain (12 stations + 3 cross-cutting) | Accepted | 2026-05-11 |
| ADR-011 | Persona model: 3 personas | Accepted | 2026-05-11 |
| ADR-012 | Per-skill folder template | Accepted | 2026-05-11 |
| ADR-013 | Inter-folder communication: events.jsonl | Amended | 2026-05-11 (spine path locked at `infra/events/events.jsonl`; root `calendar.json` is the disjoint calendar file — see F12) |
| ADR-014 | `00_GOVERNANCE/` shape | Accepted | 2026-05-11 |
| ADR-015 | `00_PARTNERSHIP/` shape | Amended | 2026-05-11 (cost-share + qualified-prospect docs added) |
| ADR-016 | `operations/` sub-tree | Amended | 2026-05-11 (lives under `operations/` bucket per ADR-021) |
| ADR-017 | Agent framework: Python multi-path invocation | **Amended** | 2026-05-11 (Python in-house — see ADR-029) |
| ADR-018 | Agent inventory | Amended | 2026-05-11 (inventory expanded by ADRs 029-035; canonical list lives in §9) |
| ADR-019 | Telegram bot design | Accepted | 2026-05-11 |
| ADR-020 | Independent bot codebase | Accepted | 2026-05-11 |
| **ADR-021** | **3-bucket top-level grouping (Skills/Pipeline/Operations)** | **New** | this session |
| **ADR-021bis** | **Drop "Hosted" from JP interface options (Heavy/Light only)** | **New** | 2026-05-14 amendment (supersedes the original Hosted option, never formalized; see F27) |
| **ADR-022** | **Dual-mode pipeline (Manual + API), same contract** | **New** | this session |
| **ADR-023** | **Warm-standby service redundancy** | **New** | this session |
| **ADR-024** | **Dual meeting capture (Notion AI canonical + Jitsi/Whisper shadow) for internal; single canonical for client** | **Superseded by ADR-038** (2026-05-15) | this session. Notion-canonical posture withdrawn 2026-05-15; Jitsi/Whisper promoted to canonical pending Plan 02. |
| **ADR-025** | **Paired-file two-tier documentation (English/English)** | **New** | this session |
| **ADR-026** | **Multi-model investigation: parallel-then-judge** | **New** | this session |
| **ADR-027** | **Intake: 2-file split, hypotheses sealed during research** | **New** | this session |
| **ADR-028** | **Ollama on Desktop (hybrid): HP for orchestration, Desktop for GPU during office hours** | **New** | this session |
| **ADR-029** | **Drop n8n from Nexostrat critical path: Python agents + systemd timers** | **New** | this session |
| **ADR-030** | **Per-user timezone-aware delivery scheduling** | **New** | this session |
| **ADR-031** | **CHECKPOINT.md per persona + per-client for session continuity** | **New** | this session |
| **ADR-032** | **Unified inbox: Telegram captures + manual memos converge to single primitive** | **New** | this session |
| **ADR-033** | **Aurora brand palette + Space Grotesk/Manrope/JBM typography** | **New** | this session |
| **ADR-034** | **Ambient chat extraction with Ollama (sensitive-content filtered)** | **New** | this session |
| **ADR-035** | **Meeting lifecycle protocol (start/pause/resume/end/recover/override)** | **New** | this session |
| **ADR-036** | **Stage 1 surface area — v0 vs v1 fidelity (deliberate trade-offs)** | **New** | 2026-05-14 amendment (R3; lists features shipping at v0 fidelity with v1 deferred) |
| **ADR-037** | **Notion canonical role — Stage 2 review trigger** | **Superseded by ADR-038** (2026-05-15) | 2026-05-14 amendment (R5). Stage-2 review brought forward to immediate (2026-05-15); ADR-038 supersedes the canonical-Notion posture this ADR was defending. |
| **ADR-038** | **Drop Notion at firm level; FOSS self-hosted replacement deferred to Plan 02 brainstorm** | **Accepted** | 2026-05-15. Notion exits the firm-level architecture. All four Notion roles (meeting capture canonical, summary generation, CRM, collaborative docs workspace) reassigned to FOSS self-hosted solutions — specific tools chosen during Plan 02 brainstorm with all options open. Full ADR body at [`00_GOVERNANCE/adr/ADR-038-drop-notion-foss-tbd.md`](../../00_GOVERNANCE/adr/ADR-038-drop-notion-foss-tbd.md). Supersedes ADR-024 + ADR-037. Reverses amendment F14. Mooted memory `notion-via-jp-personal`. |

Full ADRs (Context · Options · Decision · Consequences) are drafted into `00_GOVERNANCE/adr/` during scaffold. ADRs 021bis / 036 / 037 / 038 already exist as full ADR bodies in `00_GOVERNANCE/adr/`; ADRs 001-020 + 022-035 are scheduled for Plan 02 to draft.

---

# Section 1 — Topology & Brand

## Where Nexostrat lives

Path: `/srv/Nexostrat/` on the HP laptop (Linux Mint 22.2, `ricardo-hp-laptop`, Tailscale `100.64.121.80`). Standalone git repo. Git author per-repo: `Nexostrat <contacto@nexostrat.com>` — every commit carries this email as the firm's auditable signature.

## Brand identity (locked)

| Element | Value |
|---|---|
| Name | **Nexostrat** |
| Domain | `nexostrat.com` (Hostinger-registered) |
| Email | `contacto@nexostrat.com` |
| Palette (Aurora) | Midnight `#0C1A2E` · Ocean Deep `#0D4A6B` · Sky Blue `#0EA5E9` · Emerald `#10B981` · Amber Gold `#F59E0B` · Arctic White `#F0FBFF` |
| Typography | Space Grotesk (display), Manrope (body), JetBrains Mono (code). Fraunces banned. |
| Logo | Final pick pending; 5 monogram proposals exist |

## Replication topology (warm-standby)

```
                              GitHub private (mirror, off-site)
                                    ▲
                                    │ post-receive → mirror push
                                    │
HP LAPTOP (LIVE, primary)  ─────────┼──────────► Codeberg (mirror, off-site)
ricardo-hp-laptop                   │
Docker stack live:                  │
  • gitea (origin)                  │
  • nexostrat-bot (Telegram)        │
  • jitsi (video shadow)            │
  • nextcloud (file shadow)         │
  • whisper-cpp (CPU transcript)    │ nightly rsync (data only)
  • mcp servers                     │
  • event-router daemon (Python)    ▼
  • delivery-flush daemon (Python)   SECOND LAPTOP (WARM-STANDBY, idle)
                                       /srv/Nexostrat/ data clone
                                       Same docker-compose.yml, services stopped
                                       Failover RTO 15-30 min via SSH + compose up
```

**Backup ladder (7 layers):** working tree on HP → Gitea origin → GitHub mirror → Codeberg mirror → warm-standby clone → Drive 2TB (heavy assets, age-encrypted before upload) → NAS rclone mirror.

## Machine roles

```
HP server (always-on, low-power, orchestration)
  Power: ~25W idle, ~55W active. Hosts: Gitea, bot, Jitsi, Nextcloud, Whisper.cpp,
  event-router daemon, systemd timers. NEVER runs Ollama (no useful GPU; flicker-issue dGPU
  remains unloaded).

Desktop (office hours, GPU-accelerated, LLM-heavy)
  Specs: Ryzen 5 5600X, 32 GB RAM, RTX 3060 Ti / 8 GB VRAM, NVMe 2TB + 2.7TB ext4.
  Hosts: Ollama (Llama 3.1 8B Q5, Qwen 2.5 14B Q4, Mistral 7B). Awake 08:00-20:00 local
  with systemd suspend after; wake-on-LAN from HP for queued jobs. Power ~80-250W active.

Ricardo travel laptop / other workstations
  Git clones. Claude Code, Gemini CLI for hands-on sessions. Hold Ricardo's age key.
  Tailscale members.

JP laptop (Light mode default, Heavy mode whenever JP chooses)
  Light: Telegram + Gitea web only, zero install.
  Heavy: full clone + Claude Code + Gemini CLI + age key. ~1h onboarding.

Phones (R + JP)
  Telegram clients only. Allowlisted chat_ids. Never hold keys, never run code.
```

## Network

Tailscale mesh is the VPN. HP exposes Gitea (host port `:3001`), Jitsi, Nextcloud only on Tailscale IP — no public port forward. DNS via Tailscale split-DNS: `gitea.nexostrat.internal`, `jitsi.nexostrat.internal`, etc.

---

# Section 2 — Repository Structure (3-Bucket Grouping)

**ADR-021:** Top-level layout follows the firm's three operational concerns: **Skills**, **Pipeline**, **Operations**. Cross-cutting concerns (governance, docs, infra, vault, knowledge) stay at root. This makes the filesystem tree match the presentation JP just approved, and makes the 3-persona model visible at the filesystem level.

```
/srv/Nexostrat/
│
├─ CLAUDE.md  GEMINI.md  README.md  STATUS.md
├─ CHECKPOINT.md           ← Founder's session-handoff baton (Section 4.10)
├─ tasks.json  calendar.json
├─ docker-compose.yml  .env.example
├─ .gitignore  .gitattributes
│
├─ 00_META/                ← system meta-governance
│   ├─ CHANGELOG.md
│   ├─ proposals/          ← design docs (THIS FILE lives here)
│   ├─ journal/            ← session-end entries
│   ├─ handoff/            ← Claude ↔ Gemini handoff + archive
│   │   └─ checkpoints/    ← archived CHECKPOINT.md history
│   ├─ inbox/              ← Founder's cross-folder memo inbox (PLAN 04 — Telegram bot writes here)
│   │   └─ archive/
│   └─ shared/             ← canonical short-form stanzas (rule1, session_start, etc.) (PLAN 01c)
│
├─ 00_GOVERNANCE/          ← decisions ledger + protocols
│   ├─ adr/                ← ADR-001 .. ADR-035, one .md per decision
│   ├─ DECISIONS.md        ← one-line index of ADRs (auto-generated)
│   ├─ system_map.md
│   ├─ key-rotation-protocol.md
│   ├─ meeting-protocol.md
│   ├─ compliance-checklist.md
│   └─ each canonical doc + -explicado.md
│
├─ 00_PARTNERSHIP/         ← R + JP co-owned
│   ├─ PARTNERSHIP_AGREEMENT.md         (50/50 equity; 20/20/20/40 revenue split)
│   ├─ CONFLICT_PROTOCOL.md             (15-min raised-hand)
│   ├─ REVENUE_DISTRIBUTION.md
│   ├─ ROLES.md  KPIs.md
│   ├─ cost-sharing-agreement.md        (pre-revenue: R covers Claude+Grok+Drive+hw; JP covers Claude+domain+email — Notion line removed per ADR-038)
│   ├─ qualified-prospect-definition.md (>= USD 50K/yr client revenue, per Q6)
│   ├─ questionnaires/                  (from Plan_Maestro docx → migrated)
│   ├─ meetings/weekly/  meetings/decisions/
│   ├─ raised_hand_log.md
│   └─ reviews/                          (quarterly)
│
├─ docs/                   ← user manual (Diátaxis structure)
│   ├─ README.md
│   ├─ tutorials/  how-to/  reference/  explanation/  runbooks/
│   └─ (each doc + -explicado.md pair where it's JP/operator facing)
│
├─ infra/                  ← code we build (cross-cutting)
│   ├─ agents/             ← Python agents (orchestration substrate — ADR-029)
│   ├─ telegram/           ← bot source + plugins + users/ + delivery_queue/
│   ├─ events/             ← events.jsonl + schemas/ + taxonomy.md (auto-gen)
│   ├─ shadow/             ← dual-tools configs (jitsi, nextcloud, ollama, whisper, anytype)
│   ├─ machines/           ← per-machine YAML profiles
│   ├─ systemd/            ← .service + .timer unit files (committed)
│   ├─ hooks/              ← pre-commit + pre-receive
│   ├─ recovery/           ← runbook-aligned scripts
│   ├─ secrets/            ← MANIFEST.md (values in secrets.env.age at root)
│   ├─ scripts/            ← doc generators, smoke tests, bootstrap
│   └─ observability/      ← prometheus config + grafana dashboards (Stage 2)
│
├─ vault/                  ← encrypted catastrophic-loss material (age)
│   ├─ sensitive_index.md
│   └─ .encrypted/         ← ciphertext (decrypt to /dev/shm at use time)
│
├─ knowledge/              ← graduated reference (cross-bucket)
│   ├─ sectors/  quick_wins/  source_caches/
│
├─ skills/                 ← SKILLS bucket — Skills-Master persona
│   ├─ CLAUDE.md  GEMINI.md  CHECKPOINT.md
│   ├─ 01_company_analyst/      ← already built (extracted from zipped skill)
│   ├─ 02_industry_analyst/     ← to build
│   ├─ 03_competitor_analyst/   ← to build
│   ├─ 04_meeting_script/       ← to build (PRIVATE)
│   ├─ 05_opportunity_report/   ← to build (Diagnóstico deliverable)
│   ├─ 06_discovery_meeting/    ← existing (facilitation)
│   └─ shared/                  ← judge_prompt.md, research_input_template.md, anti_hallucination.md
│
├─ pipeline/               ← PIPELINE bucket — Client-Owner persona
│   ├─ CLAUDE.md  GEMINI.md  CHECKPOINT.md
│   ├─ clients/
│   │   ├─ _template/      ← canonical empty client folder
│   │   ├─ bodai/          ← permanent benchmark
│   │   └─ alfa-bitcoin/   ← first pilot (JP's company per Plan Maestro)
│   │       (12-station chain inside — see Section 7)
│   └─ prospects/
│       └─ <slug>/intake/  qualification.md
│
└─ operations/             ← OPERATIONS bucket — Founder back office
    ├─ marketing/  sales/  accounting/  legal/  it/
    ├─ templates/          (Aurora docx, proposal/scope/kickoff templates)
    └─ assets/             (logo/, palette/, fonts/, public/)
```

**Naming conventions:**
- Ordered folders: `NN_name/` (e.g., `01_company_analyst/`, `00_intake/`)
- Unordered: lowercase descriptive (e.g., `clients/`, `infra/`)
- Files: `snake_case.py` for code; `kebab-case.md` or `YYYY-MM-DD_topic.md` for docs
- Per-skill runs: `runs/YYYY-MM-DD_<mode>_v<N>/` so multiple runs coexist
- Paired docs: `X.md` (technical) + `X-explicado.md` (plain English partner) for JP-facing folders

---

# Section 3 — Foundation Layer (Security & Durability)

## Identities — per-user `age` keys (ADR-003)

`age` for vault + secrets. Each user generates a keypair locally; private key (passphrase-protected) never leaves their machines; public keys live in `infra/age-recipients.txt` (committed). Files encrypted to ALL recipients. Either holder can decrypt. Revocation = drop a pubkey + re-encrypt forward.

## Vault — rare-access pattern (no persistent mount)

```
vault/
├─ README.md  sensitive_index.md
├─ partnership/   (signed agreement, revenue receipts)
├─ clients/<slug>/   (NDAs, contracts, invoices — .age ciphertext)
├─ legal/   (entity, tax filings when constituted)
├─ accounting/   (bank statements monthly)
└─ keys/   (recovery codes, key-rotation log)
```

Decrypt to `/dev/shm` (RAM tmpfs) at use time → use → shred. **No persistent mounted plaintext.** Heavy assets (audio, large PDFs) age-encrypted before Drive upload; index lives in `sensitive_index.md`.

## Secrets — runtime injection (ADR-004)

`secrets.env.age` at repo root, encrypted to both keys. Services start via `infra/scripts/run-with-secrets.sh` which decrypts to `/dev/shm/secrets.env`, sources env, execs the service, shreds on exit. `infra/secrets/MANIFEST.md` is the plaintext index (no values) listing every secret, what uses it, where to rotate, last rotation date.

**Hard caps** configured at each provider (Anthropic monthly cap, etc.) so blast radius of any leak is bounded.

## Backup ladder (ADR-006 + ADR-023)

| # | Layer | Contains | Frequency | Encryption |
|---|---|---|---|---|
| 1 | HP working tree | Live | Continuous | Mixed |
| 2 | Gitea origin | Same | Per commit | Same |
| 3 | GitHub private mirror | Same | Per push (hook) | Same; sensitive = ciphertext |
| 4 | Codeberg mirror | Same | Per push (Phase B) | Same |
| 5 | Warm-standby clone | `/srv/Nexostrat/` rsync | Nightly 03:00 | Same |
| 6 | Drive 2TB | Heavy assets only | Continuous (rclone) | All ciphertext |
| 7 | NAS local | Mirror of Drive | Nightly 04:00 | All ciphertext |

Weekly verification cron (Sunday 02:00): sample mirrors for hash match, count Drive heavy-assets vs `sensitive_index.md`.

## Recovery procedures

Each maps to a runbook (`docs/runbooks/`) + script (`infra/recovery/`):

| Incident | RTO | Runbook |
|---|---|---|
| HP down | 15-30 min | `hp_down.md` |
| HP + standby down | 4-8h | `total_outage.md` |
| Ricardo laptop stolen | 1h block + 24h rotate | `key_compromise.md` |
| JP laptop stolen | Same | `key_compromise.md` |
| Server compromised | 24-48h | `server_compromise.md` |
| Secret committed plaintext | Immediate | `secret_leak.md` |
| age key compromised | 24h | `key_rotation_routine.md` |
| Pipeline stuck | 15 min | `pipeline_stuck.md` |

## Guards (hooks)

**Pre-commit** (client-side, `infra/hooks/`):
1. Secret-scan (regex for `sk-ant-`, `sk-`, `AKIA`, `ghp_`, `eyJ`...)
2. File-pattern block (refuse `.env`, `*.pem`, `*.key`, `*_secret*`, etc.)
3. Docs-pair check (X.md modified → X-explicado.md must also be staged)
4. Age-encrypt reminder (vault/ accepts only `.age` files)
5. CHECKPOINT.md validation

**Pre-receive** (server-side in Gitea): same checks + branch protection on `skills/*/prompts/`, `pipeline/clients/*/{06_proposal,07_contract_onboarding}/`, `00_GOVERNANCE/`, `secrets.env.age`, `infra/age-recipients.txt`.

---

# Section 4 — Personas & Governance

## The three personas (ADR-011)

| Persona | Lives at | Owns |
|---|---|---|
| **Founder** | `/CLAUDE.md` | Root governance, `operations/*`, `infra/`, `docs/`, `knowledge/`, `vault/{partnership,legal,accounting,keys}/` (NOT `vault/clients/`) |
| **Skills-Master** | `/skills/CLAUDE.md` | The 5+1 reusable skills, prompts, versions, benchmark tests (no vault content) |
| **Client-Owner** | `/pipeline/CLAUDE.md` | Active client work (the 12-station chain + 3 cross-cutting), `pipeline/{clients,prospects}/`, AND `vault/clients/<slug>/` |

6 persona files total (3 CLAUDE.md + 3 GEMINI.md). Operations sub-folders (marketing, sales, etc.) don't get personas — they get **skills**. Persona = WHO operates; Skill = WHAT capability.

## Each CLAUDE.md / GEMINI.md skeleton

```
1. Role
2. About Ricardo + JP
3. Strict Rules (operator-driven scope)
4. Scope
5. Session Start Protocol
6. Session End Protocol
7. Session Output Format (5-bullet brief)
8. Architecture / Context
9. Cross-Folder Memo Protocol
10. Gemini Handoff Protocol (Claude file only)
11. Vault / Sensitive Discipline
12. Backup Posture
13. Change Log
```

Shared stanzas at `00_META/shared/*.md` are inlined into each persona file; an audit script catches drift.

## Strict rules

1. **Operator-driven scope.** When Ricardo or JP is in-session driving, any persona may edit any folder. Memos remain for specialist requests / paper trails / autonomous async work. Vault namespaces stay strictly isolated.
2. Project content owned by the bucket's persona; defer to them when their session is active.
3. **Claude authors all GEMINI.md files.** Gemini may NOT edit any CLAUDE.md.
4. **New top-level folders require Founder approval** (ADR). Sub-folders inside a bucket can be added by the owning persona.
5. No destructive operations without explicit per-action approval.
6. Sensitive content goes in the vault. Never plaintext.

## Gemini handoff (file-based)

`00_META/handoff/claude_to_gemini.md` ↔ `gemini_to_claude.md` + archive. Claude raises `OPEN`; Gemini flips `IN_PROGRESS` → writes response `RESPONSE_READY` → Claude integrates → archives both.

## ADR ledger

`00_GOVERNANCE/adr/ADR-NNN-<slug>.md` per decision. Format: Status · Date · Decided by · Context · Options · Decision · Consequences. `DECISIONS.md` is the auto-generated one-line index.

## 00_PARTNERSHIP/ contents

Partnership agreement (50/50, fully vested), conflict protocol (JP's 15-min raised-hand), revenue distribution (20% company / 20% originator / 20% closer / 40% executor), roles, KPIs (≥10 paying clients, ≥USD 20K revenue at month 12), cost-sharing agreement, qualified-prospect definition (>USD 50K/yr client revenue), questionnaires migrated from Plan Maestro, meetings (weekly + decisions), raised_hand_log, quarterly reviews.

## Two-tier docs hook (ADR-025)

Pre-commit refuses if `X.md` in a tier-1 folder (`docs/`, `00_PARTNERSHIP/`, `00_GOVERNANCE/`, root README) is modified without its `X-explicado.md` partner. Escape hatch: `docs-skip-pair` in commit message. Weekly drift audit (Sunday 06:00) flags partners more than 14 days stale.

## Cross-folder memo protocol (simplified for 3 inboxes)

`<bucket>/00_META/inbox/` + `archive/`. Each persona scans its inbox at session start (`infra/scripts/nexostrat-memos.py`). Standard YAML frontmatter (`status`, `from`, `to`, `type`, `priority`, `subject`, `due?`).

## Session continuity — CHECKPOINT.md (ADR-031)

**The gap closed:** prior session's exact stopping point, to the level of "which file to open and which command to run next." One CHECKPOINT.md per persona (`/CHECKPOINT.md`, `/skills/CHECKPOINT.md`, `/pipeline/CHECKPOINT.md`) + optional per-client `pipeline/clients/<slug>/checkpoint.md`.

Required fields: timestamp, persona, "what I just did," "in flight — concrete next action," "blocked on," "open questions," "files modified but not committed," "estimated time to finish," "after this, what's next."

Empty CHECKPOINT.md commits refused unless explicitly written as `CHECKPOINT_NO_ACTIVE_WORK`. SessionStart hook reads it first; Session End Protocol Step 3.0 writes it. Mode B Python agents write CHECKPOINT.md automatically when a pipeline pauses awaiting review. Telegram `/handoff [scope]` posts current CHECKPOINT to group.

**Concurrent-session protection (R4):** the SessionStart hook (Plan 06 territory) checks `CHECKPOINT.md`'s mtime — if it was modified within the last 10 minutes by a process other than the current session, the hook warns loudly before allowing the session to proceed. This catches the "Ricardo opened a second Claude Code session by mistake" failure mode without forcing a hard lock.

## Unified inbox — Telegram + manual converge (ADR-032)

Same primitive, two write paths. Telegram bot is a write-only client to `<scope>/00_META/inbox/`.

**Capture commands route to scope's inbox:**

| Command | Lands in |
|---|---|
| `/note <text>` | root inbox |
| `/note pipeline <text>` | pipeline inbox |
| `/note <client-slug> <text>` | client's inbox |
| `/idea <text>` | `operations/marketing/00_META/inbox/` |
| `/question <text>` | current scope inbox |
| `/request <scope> <text>` | target scope inbox |
| `/observation <client> <text>` | client inbox |
| `/decision <text>` | `00_GOVERNANCE/proposals/` |
| `/expense <amt> <text>` | `operations/accounting/expenses.md` (append) |
| `/voice` (attachment) | Whisper transcribes → text → inbox |
| `/photo` | Drive heavy + manifest in inbox |
| (no slash, free text) | personal DM catch-all inbox |

**File format** (one .md per item with YAML frontmatter: `status`, `from`, `to`, `source`, `type`, `created`, `priority`, `subject`, `related`).

**Resolution layers:**
1. Human at session start — reads inbox, replies, archives.
2. Ollama auto-resolver — every 4h during office hours, scans for `type=question` with `confidence≥0.6`, posts answer + archives. Never touches `type=request` or `type=decision`.
3. API fallback — when desktop asleep or Ollama low-confidence, Anthropic API answers.

**`/inbox` family** for inspection: `/inbox`, `/inbox <scope>`, `/inbox all`, `/resolve <id> <reply>`, `/defer <id> <date>`, `/promote <id> <target>`.

Session-start hook surfaces inbox count + top-3 unresolved alongside CHECKPOINT.md.

---

# Section 5 — Stack & Tools

## Stage 1 — paid / reserved services

The firm-as-entity pays **USD $0/mo** at Stage 1; pre-revenue founder personal-spend is documented in [`00_PARTNERSHIP/cost-sharing-agreement.md`](../../00_PARTNERSHIP/cost-sharing-agreement.md) and reimbursed at first-revenue. The table below describes services that have a non-zero firm-bearing cost component reserved for future stages plus optional personal interactive tools.

| Service | Stage 1 cost (firm) | Personal-spend equivalent (per cost-sharing-agreement.md) | Purpose |
|---|---|---|---|
| Claude MAX (Ricardo + JP) | $0 firm | ~$200/mo each (Anthropic personal) | Mode A skill execution + judge synthesis + /ask + automation. **Replaces the pay-per-use Anthropic API line from earlier draft** — at MAX usage volumes the subscription is cheaper. |
| Google Drive 2TB | $0 firm | ~$10/mo (Ricardo personal) | Heavy assets (audio, large PDFs) — age-encrypted before upload |
| xAI Grok API | $0 firm | ~$5-15/mo (Ricardo personal) | 3rd-model parallel research |
| Domain `nexostrat.com` | $0 firm | ~$12/yr amortized (JP personal Hostinger) | Brand DNS |
| Email `contacto@nexostrat.com` | $0 firm | ~$6/mo (JP personal hosting) | Outbound firm email |
| Super Grok (web, optional) | $0 firm | $30/mo (Ricardo personal, optional) | Interactive Grok web (NOT pipeline) |

**~~Notion~~** — REMOVED 2026-05-15 per ADR-038. Notion exits Nexostrat at firm level; JP's personal Notion subscription, if retained, is outside firm scope and non-reimbursable. FOSS replacement for meeting capture / summary generation / CRM / collaborative docs chosen during Plan 02 brainstorm — candidates include Whisper.cpp + Ollama + EspoCRM/AppFlowy/Outline/etc.

**Stage 2 firm-bearing services** (when reserve target met OR cumulative revenue ≥ USD 5,000 — see ADR-019): DocuSign/Documenso, Stripe, Backblaze B2 (when Drive 2TB > 80%), CRM upgrade (when pipeline > 15 clients), Bitwarden org sub, WAHA-Nexostrat (when first WhatsApp client).

## Stage 1 — self-hosted (free)

Gitea, Telegram bot (custom), Tailscale, age, rclone, pandoc, Whisper.cpp (CPU on HP), Jitsi Meet, Nextcloud, MCP servers, GitHub free mirror, Codeberg mirror (Phase B), Cal.com (Stage 2).

## Stage 1 — GPU (Desktop, office hours)

Ollama with Llama 3.1 8B Q5, Qwen 2.5 14B Q4, Mistral 7B. Awake 08:00-20:00 local; systemd suspend + wake-on-LAN from HP.

## Workstation tools

Claude Code + Gemini CLI on Ricardo's workstations, eventually on JP's Heavy. Obsidian for markdown UX. VS Code/Cursor as editor. Telegram desktop + mobile per machine profile.

## Per-machine profiles (`infra/machines/*.yaml`)

One YAML file per machine declares hostname, role, Docker services, CLI tools, desktop apps, schedule, gpu config, hooks, crons. The bootstrap script (`infra/scripts/bootstrap-machine.sh <profile>`) reads the profile and installs accordingly. Idempotent. Re-runnable.

Profiles: `hp-server`, `hp-standby`, `ricardo-desktop`, `ricardo-travel`, `jp-light`, `jp-heavy`, `phones`.

**JP-side OS baseline (F13):** `bootstrap-machine.sh` is Linux-only. **Linux Mint** is the recommended baseline for JP's Heavy machine — same family as Ricardo's HP, well-trodden install path, no surprises. macOS support is out of Stage 1 scope and handled as an explicit exception in Plan 02 only if JP cannot install Linux Mint. `jp-heavy.yaml` declares `os: linux-mint`; if the exception path is taken, Plan 02 produces an `os: macos` variant alongside.

**JP Light onboarding: 5 minutes.** Telegram + Tailscale (optional). Heavy onboarding: ~1 hour additive when JP chooses.

## Docker stack on HP

Single `/srv/Nexostrat/docker-compose.yml`. All versions pinned (no `:latest`). All ports bound to Tailscale IP. Secrets via wrapper script.

Services: gitea (1.22, host port `:3001`), nexostrat-bot (custom Python), jitsi-web/prosody/jicofo/jvb (stable-9457), nextcloud (29-apache), whisper-cpp (custom build with Spanish model), mcp-filesystem/time/fetch, cal-com (Stage 2 — disabled until trigger).

## Dual-tools shadow — 4-week cronograma

| Week | Tools | Where |
|---|---|---|
| 1 | Nextcloud + Jitsi | HP |
| 2 | Ollama + 3 models | Desktop |
| 3 | Whisper.cpp pipeline | HP (CPU baseline) |
| 4 | Anytype or AppFlowy | HP |

Each shadow tool gets `infra/shadow/<tool>/` with compose snippet, configs, README documenting purpose + canonical it shadows + parity score.

## Stage 2 triggers

DocuSign/Documenso ← first contract signed. Stripe ← first invoice issued. Backblaze B2 ← Drive 2TB > 80%. CRM upgrade ← pipeline > 15 clients. Static site ← public web prioritized. Bitwarden org ← shared logins routine. WAHA-Nexostrat ← first client via WhatsApp.

## Upgrade discipline

Renovate-cli weekly report. Each version bump → ADR → test on warm-standby 7 days → promote to HP-live. No silent latest-pull. Rollback procedure per service documented at `docs/runbooks/rollback_<service>.md`.

## Cost summary

**Stage 1 firm pays: USD $0/month** (amended 2026-05-16 per ADR-038). Pre-revenue founder personal-spend per [`cost-sharing-agreement.md`](../../00_PARTNERSHIP/cost-sharing-agreement.md): Ricardo ~$215-225/mo (Claude MAX 200 + Grok 5-15 + Drive 10); JP ~$207/mo (Claude MAX 200 + Domain ~1 + Email 6) — Notion line removed. Reimbursement triggers at firm cumulative revenue ≥ USD 1,000. Per-Diagnóstico marginal cost in Mode B: ~$1.25 (5 skills × ~$0.25) covered by Claude MAX subscription headroom. Pricing baseline USD 1500-3000 → API cost is rounding error.

---

# Section 6 — Skills, Intake & Multi-Model Investigation

## The 5 + 1 skills

| # | Name | Built? | Input | Output | Notes |
|---|---|---|---|---|---|
| 1 | Análisis de Compañía | ✅ already built | research_input.md | DOCX 15-25 pp, 13 sections | Anti-hallucination strict |
| 2 | Análisis de Industria | to build | research_input.md | DOCX 10-15 pp | DANE/INEGI sources |
| 3 | Análisis de Competencia | to build | research_input.md | DOCX 10-15 pp | 3-5 direct + 2-3 indirect |
| 4 | Guión de Reunión | to build | Skills 1-3 + our_hypotheses | Private MD 6-10 pp | **NEVER to client** |
| 5 | Reporte de Oportunidades | to build | Skills 1-3 + meeting notes + our_hypotheses | DOCX 20-30 pp Aurora | THE Diagnóstico deliverable |
| 6 | Discovery Meeting | existing | Live | Facilitation flow | Different category |

## Per-skill folder template (ADR-012)

`skills/01_company_analyst/`: `SKILL.md`, `README.md`, `STATUS.md`, `prompts/v1.md` + `versions/` + `CHANGELOG.md`, `scripts/`, `references/`, `assets/`, `tests/{benchmark.md, benchmark_input.md, benchmark_expected.md, results/}`.

## Versioning + benchmark (Bodai)

Every prompt edit = new version. Commit triggers regression test against Bodai fixture. Score drop > 10% blocks commit; factual-accuracy drop blocks unconditionally. Quality bar: 7/10 to start pilots; 8/10 to go paid. Score formula at `skills/shared/scoring.py`.

## Intake — 2-file split (ADR-027)

`pipeline/clients/<slug>/00_intake/research_input.md` (slices 1+2: public facts + private factual context) + `our_hypotheses.md` (slice 3: judgment + people-judgments, **SEALED** during research, read by Claude-as-Judge at synthesis).

Templates at `skills/shared/{research_input_template.md, our_hypotheses_template.md}`.

Input mechanisms (all produce the same 2 files):
- Telegram `/intake <slug>` (guided)
- Spreadsheet template → script
- Manual markdown edit

## Multi-model — parallel-then-judge (ADR-026)

Same prompt + research_input.md → Claude + Gemini + Grok in parallel → 3 raw_outputs → Claude-as-Judge reads all 3 + our_hypotheses + research_input → unified final_report.md flagging disagreements + "What we expected vs. what research found."

Per-run folder: `runs/YYYY-MM-DD_<mode>_v<N>/{raw_outputs/, final_report.md, manifest.json}`. `canonical.md` symlink at station root points to the chosen run. `comparison.md` auto-generated when 2+ runs exist. `thread.jsonl` per skill captures `/ask` continuity.

## `manifest.json` schema (ADR-022 + F9)

Both modes write the same `manifest.json` so Mode-A and Mode-B runs are diffable. Schema:

**Mandatory (both modes):**
- `mode` — `"manual" | "api"`
- `model` — primary model identifier (e.g., `"claude-opus-4-7"`; for Mode B, the synthesizer model; for Mode A, the model that drove the session)
- `prompt_version` — semver-ish (e.g., `"v1"`, `"v1.2"`)
- `inputs_hash` — sha256 of `research_input.md` + `our_hypotheses.md` at run time
- `final_report_hash` — sha256 of `final_report.md`

**Mode-B-specific (required when `mode == "api"`):**
- `tokens_in`, `tokens_out` — int totals across the run
- `latency_ms` — wall-clock duration int
- `stop_reason` — `"end_turn" | "max_tokens" | "stop_sequence" | "error"`
- `id` — provider run id (per provider)

**Mode-A-optional:**
- `turn_count` — int turn count if the session naturally maps to discrete turns (CLI conversation); else omitted

`comparison.md` auto-diffs the **mandatory fields + final_report content** between any two runs; mode-specific fields are reported alongside but not used to score diff. Plan 05 ships `test_manifest_schema_both_modes.py` asserting both modes produce mandatory fields.

## Judge prompt — `skills/shared/judge_prompt.md`

Standardized 5-section output: Synthesis, Where models agreed, Where models disagreed (no silent averaging), What we expected vs. what research found, Reviewer notes (initially empty; `/note` populates).

## Anti-hallucination rule — `skills/shared/anti_hallucination.md`

Inlined into every skill prompt via marker block. "If you cannot verify a fact via a citable source, write 'No se encontró información en [source]'. NEVER invent revenues, employee counts, dates, founder names, addresses, contract amounts, market share figures. NEVER omit a section because you lack data. Mark each claim: verified / inferred / best guess."

Pre-commit hook validates the marker block exists in every skill prompt.

## Mode A and Mode B (ADR-022) — same contract, two backends

**Mode A — Manual** (`infra/runbooks/manual/skill_<N>_manual.md` per skill):
Claude Code walks Ricardo through: read research_input.md → produce Claude output → prepare Gemini prompt for paste into Gemini CLI → user saves Gemini output → prepare Grok prompt → user pastes into grok.com → user saves Grok output → Claude synthesizes via judge prompt → pandoc render → commit. 30-60 min per skill, $0.

**Mode B — API** (Python agent at `infra/agents/skill_<N>_<name>/run_api.py`):
Concurrent HTTP calls to Anthropic + Gemini + Grok APIs → 3 raw_outputs → judge call → pandoc → commit → Telegram digest with gates `[/go /stop /note /ask]`. 3-6 min per skill, ~$0.20-0.40.

**Both modes write to the same `runs/` folder so they can run in parallel during the trial phase. `comparison.md` auto-diffs the two runs.**

**Mode B human gates:**
- `/go` advances pipeline; `/stop` halts; `/note <text>` annotates without advancing; `/ask <q>` opens a thread (`thread.jsonl`) with Claude API answering, posted to Telegram; pipeline waits for `/go`.
- `/switch <client> mode={manual,api}` flips mid-pipeline; `/rerun <skill> mode=...` re-runs.

## Cost + time per skill per mode

| Skill | Mode A | Mode B |
|---|---|---|
| 1 Company | 45-60 min, $0 | ~5 min, ~$0.25 |
| 2 Industry | 30-45 min, $0 | ~4 min, ~$0.20 |
| 3 Competitor | 30-45 min, $0 | ~5 min, ~$0.25 |
| 4 Meeting script | 20-30 min, $0 | ~3 min, ~$0.15 |
| 5 Opportunity | 60-90 min, $0 | ~8 min, ~$0.40 |
| **Full Diagnóstico** | **3-5 h, $0** | **~25 min, ~$1.25** |

---

# Section 7 — Per-Client Production Chain

## 12 stations + 3 cross-cutting (ADR-010)

```
pipeline/clients/<slug>/
├─ README.md  state.json  checkpoint.md
├─ 00_intake/                  ← Plan Maestro Pasos 1-3
├─ 01_company_analysis/        ← Skill 1 (Fase B)
├─ 02_industry_analysis/       ← Skill 2 (Fase B)
├─ 03_competitor_analysis/     ← Skill 3 (Fase B)
├─ 04_meeting_script/          ← Skill 4 PRIVATE (Fase B)
├─ 05_opportunity_report/      ← Skill 5 (Fase C — THE DELIVERABLE)
├─ 06_proposal/                ← Pasos 7-8 (Fase D)
├─ 07_contract_onboarding/     ← Paso 9 (Fase E)
├─ 08_solution_design/         ← Paso 10
├─ 09_implementation/          ← Paso 11
├─ 10_followup/                ← Paso 12 (30/60/90)
├─ 11_retainer/                ← Paso 13
├─ transcripts/                ← all meetings, audio in vault/Drive
├─ communications/             ← email/WhatsApp/Telegram captures
└─ archive/                    ← superseded
```

**Folders never move.** Phase tracked in `state.json`.

## `state.json` schema

Fields: `client`, `name`, `country`, `sector`, `started`, `owner`, `phase`, `phase_history[]`, `pilot`, `pricing`, `next_action`, `kpis`, `blockers[]`, `tags[]`, `recording_preference` (`jitsi-whisper` / `none` / `<FOSS-tool-TBD-plan-02>` — pre-ADR-038 wording was `Notion/Jitsi/none per ADR-024`; ADR-024 superseded by ADR-038; Plan 02 brainstorm decides if a third option lands).

**Phases:** prospect → intake → exploring → diagnostico_pendiente → diagnostico_delivered → propuesta_pendiente → propuesta_sent → propuesta_{accepted,rejected,revising} → cliente_firmado → diseño → implementación → seguimiento_30/60/90 → retainer_active. Plus `churned`, `nurture`, `retainer_paused`.

Transitions via Telegram (`/advance`, `/regress`, `/set-phase`, `/block`, `/unblock`) or Python orchestrator. Each transition appends to `phase_history` + emits `events.jsonl` entry. Required artifacts per gate (e.g., `kickoff_notes.md` to enter `diseño`) enforced by hook.

## Deliverable conventions — markdown → pandoc → Aurora

```
final_report.md  (canonical, git source of truth)
  ↓ pandoc + templates/pandoc-aurora.yaml + templates/aurora.docx
report.docx  (Aurora-branded, editable, regeneratable)
  ↓ libreoffice --headless --convert-to pdf
report.pdf  (Aurora-branded, CANONICAL client deliverable)
```

PDF is what we send. `delivered/` folder keeps the exact bytes sent (forensic). No hand-editing DOCX or PDF; edit MD and re-render.

## Aurora template (ADR-033)

Built via `python-docx`. Cover page with logo + Aurora gradient strip. Body pages: client-name header (Manrope 10pt, Steel Blue), footer "Nexostrat · Reporte confidencial · Página X de Y". H1 Space Grotesk 24pt Midnight w/ Amber Gold underline; H2 Space Grotesk 18pt Ocean Deep; body Manrope 11pt 1.5 line; code JetBrains Mono. Callout boxes: Quick Win (Emerald), Conclusión (Amber), Calificación (Sky Blue), Alerta (red).

**Same template for ALL outputs** — Diagnóstico, proposal, scope doc, kickoff agenda, impact report, user manual, even printable `-explicado.md` PDFs.

## `_template/` + `new-client.sh`

`pipeline/clients/_template/` is the canonical empty client folder. `infra/scripts/new-client.sh <slug> "<name>" <country> "<sector>"` copies template + substitutes placeholders + initializes state.json + emits `client.created` event + notifies Telegram. Telegram shortcut: `/new-client bodai "Bodai SAS" CO "food retail"`.

## Pilot vs paid paths

Same chain, different gates. Pilot: first 3 clients per Plan Maestro, free Diagnóstico, quality bar 7/10 to advance to paid. Paid: invoice in `operations/accounting/invoices/`, Stripe (Stage 2), bar 8/10. Qualified-prospect filter per ADR-015: client revenue ≥ USD 50K/yr + sector fit + decision-maker engagement.

---

# Section 8 — Meeting Capture Pipeline

## Meeting types

**Amended 2026-05-15 per ADR-038:** Notion-canonical posture withdrawn. Jitsi + Whisper.cpp promoted to canonical for both internal and client meetings pending Plan 02 brainstorm. If Plan 02 picks a different FOSS stack (e.g., self-hosted Meet + AppFlowy), a follow-on ADR will supersede this interim canonical.

| Type | Canonical capture | Shadow capture | Sensitivity |
|---|---|---|---|
| Internal R+JP | Jitsi + Whisper.cpp (FOSS-canonical, interim per ADR-038) | — | Medium-high |
| Client (default) | Jitsi + Whisper.cpp (FOSS-canonical, interim per ADR-038) | — | Client-confidential |
| Client (custom request) | TBD per Plan 02 brainstorm output | — | Per client agreement |
| Client (no recording) | Manual notes | — | Variable |
| Phone / async | Manual via `/note` + audio upload | — | Variable |

## Pre-meeting brief — two sends + confirmation (Section 8.2.1)

**Morning send (07:00 each user's TZ, per ADR-030):** full brief to group + each DM. Brief includes open actions from prior meetings in series, decisions awaiting followup, agenda items submitted via `/agenda`. Reply with `/confirm <meeting-id>`, `/decline <meeting-id> [reason]`, or `/reschedule <meeting-id>`. If silent by T-2h, bot pings individually. If anyone declines, reschedule flow offers cal.com slots.

**T-15 min send:** short reminder ("starting in 15 min").

## Client meetings — WhatsApp confirmation (future, via WAHA — Section 8.3.1)

When `comm_preference: whatsapp` is set in client `state.json`, a Python agent sends the WhatsApp message via `waha-nexostrat` (Nexostrat's own WAHA instance). Client confirms via WhatsApp. Stage 2 trigger: "first client engaged via WhatsApp" → enables waha-nexostrat docker service + integration.

## Client recording — options (post-ADR-038)

**Amended 2026-05-15:** Notion-canonical removed (ADR-038). Pending Plan 02 brainstorm, the active client-recording options are:

- **A. Nuestro sistema self-hosted (Jitsi + Whisper.cpp)** — default; FOSS-canonical interim per ADR-038
- **B. Sin grabación** — manual notes only

Choice stored in `state.json.recording_preference` (`jitsi-whisper` | `none`). Option B disables parity diff + runs extraction on manual notes. Plan 02 may add a third option once the FOSS docs stack is decided. Parity-diff infrastructure (Jitsi-vs-shadow) only runs when ≥2 capture paths are active; with single-canonical it's degenerate and skipped.

## Internal meeting flow (end-to-end)

T-15 reminder fires → `/meeting start partnership-weekly-mon` opens Jitsi recording → live annotation via `/meeting note|decision|action <user> <text> [by <date>]` → `/meeting end` → Whisper.cpp transcribes (CPU on HP at ~1.5× real-time; Spanish model) → Ollama-powered summary review ≤15 min (mandatory per JP's rule; Plan 02 picks the summarization tool) → `/confirm partnership-weekly-mon` → export to `00_PARTNERSHIP/meetings/weekly/<week>_<topic>.md` + frontmatter → AI extraction (summary/actions/dates/decisions) → calendar events created → tasks.json updated → decisions logged to `00_PARTNERSHIP/decisions/<date>_<slug>.md` → Telegram digest. *Pre-ADR-038 flow used Notion AI as canonical with Jitsi/Whisper as shadow + parity-diff job; that dual-tools layer is now degenerate (single canonical) — parity-diff infrastructure remains in the spec as a Stage-2 readiness mechanism if Plan 02 picks a tool with a polished alternative summary path.*

## Parity diff job

Python agent at `infra/agents/meeting/parity_diff.py`. Reads canonical + shadow transcripts → Ollama (Qwen 2.5 14B on desktop) scores 0-1 per minute → writes `parity_report.md` → appends to `infra/shadow/whisper/parity_score.md` rolling log. **Stage 2 trigger:** parity ≥ 0.9 for 4 consecutive internal meetings → propose Whisper-as-a-service to clients.

## AI extraction — 5 structured artifacts

| Artifact | Lands in | Format |
|---|---|---|
| Summary (5-bullet) | Meeting .md frontmatter + Telegram digest | YAML + markdown |
| Action items | `tasks.json` + client `06_proposal/client_followups.md` if client-facing | JSON entries |
| Decisions | `00_PARTNERSHIP/decisions/` or `pipeline/clients/<slug>/communications/decisions/` | One .md per decision |
| Dates mentioned | Google Calendar (via API) | Event with link back |
| Open questions | `<scope>/00_META/inbox/` as type=question | Inbox file |

Per-decision file is first-class — gets ID, follow-up owner, due date, audit at next quarterly review.

## Meeting protocol (ADR-035 + Section 8.5.1) — canonical at `00_GOVERNANCE/meeting-protocol.md`

States: `scheduled → confirmed → active → paused → active → ended → processed`.

**Commands:**
- `/meeting start <series-or-slug>` — opens recording
- `/meeting pause [reason]` — pauses recording; auto-pause if no `/meeting end` within 4h
- `/meeting resume` — resumes; gap <30 min = same meeting_id, >30 min = ask
- `/meeting end` — closes, triggers pipeline
- `/meeting recover <meeting-id>` — tries Whisper transcript → manual fallback (post-ADR-038: Notion arm removed; pre-amendment was `Notion → Whisper → manual`)
- `/meeting start --override <series> --reason <text>` — bypass confirmation (logged loudly)

## Meeting recall — pre-meeting brief brings prior context

Brief job pulls last 3 meetings in series → collects open action items + decisions w/ followup + overdue actions + `/agenda` submissions in last 24h → renders → posts to Telegram + saves brief as audit-trail file. Client meetings: brief pulls from `pipeline/clients/<slug>/communications/` + last transcript + outstanding `client_followups.md`.

## Audio archival

Internal: default delete the Jitsi recording after summary reviewed (post-ADR-038: previously "delete from Notion"); retain only with explicit reason → `vault/partnership/meetings/<date>/audio.m4a.age` ciphertext on Drive. Client: default retain (evidence) → `vault/clients/<slug>/meetings/<date>/audio.m4a.age`. Retention policy per `00_GOVERNANCE/meeting-protocol.md`: internal 0-90 days; client = contract duration + 12 months.

## Ambient chat capture (ADR-034 + Section 8.10)

The bot saves and understands all Telegram messages, not just slash commands. R+JP frequently throw tasks/dates/links in the group; nothing gets lost.

**Storage (F17):** during the day, every message → plaintext JSONL append at `/dev/shm/chat_log/{group,dm-ricardo,dm-jp}/YYYY-MM-DD.jsonl` (RAM tmpfs; atomic append works on a single-process bot). Daily at 23:59 a cron runs `infra/agents/infrastructure/chat_log_encrypt.py`, which reads `/dev/shm/chat_log/**/YYYY-MM-DD.jsonl`, encrypts each to `infra/telegram/chat_log/<scope>/YYYY-MM-DD.jsonl.age` (recipients = all `infra/age-recipients.txt` entries), then shreds the plaintext. Trade-off documented: plaintext on RAM tmpfs for up to 24h is the cost of single-process append-safety; the bot is the only writer so no append-race exists, but encryption-per-message would serialize the bot's hot path.

**Extraction agent:** `infra/agents/chat_extractor/` runs every 4h during office hours via systemd timer. Uses Ollama Qwen 2.5 14B (strong Spanish). Sensitive-content filter skips messages with potential secrets/PII/medical info. Extracts: tasks, dates, decisions, file/link mentions, client mentions, questions, reading recs. Each finding has confidence score.

**Fallback chain:** Ollama on desktop → API (Claude Haiku, cheap) when desktop asleep → queue for next desktop wake when both unreachable.

**Confirmation loop:** for findings with confidence ≥0.6, bot posts threaded reply: "I noticed [X]. Confirm? `/confirm-extract <id>` / `/reject-extract <id>` / `/edit-extract <id> <new>`. Auto-creating in 24h if no reply." On confirm: artifact lands in appropriate location (task → tasks.json, etc.) using SAME schemas as meeting extraction. Reaction 📌 marks parsed messages; 🚫 marks rejected.

**`/chat` inspection family:** `/chat search <keyword>`, `/chat from <user> since <date>`, `/chat extractions pending`, `/chat last <N>`, `/chat tasks-from-chat`.

---

# Section 9 — Trigger Chain (Python Agents + systemd Timers)

## ADR-029 — Orchestration substrate: Python agents + systemd timers

Nexostrat's orchestration substrate is **Python agents driven by systemd timers and a long-running event-router daemon**. Reasons:

- **Maintainability:** code in Python, version-controlled, diffable, refactorable.
- **Claude-authorship:** Claude writes Python fluently; that is the day-to-day editing surface.
- **Testing:** pytest covers every agent end-to-end; mocks for Anthropic/Gemini/Grok/Telegram + whatever FOSS workspace Plan 02 picks (pre-ADR-038 list included Notion).
- **Debugging:** stack traces, structured logs, the same tools as any Python service.
- **Composability:** agents call each other through `events.jsonl` and through normal Python imports of `infra/agents/_lib/`.
- **No vendor lock-in:** every external dependency is a thin SDK wrapper we own.
- **No UI/state drift:** there's no separate workflow definition that can drift from code.

Visual-workflow tools were considered and rejected on this stack: JP does not edit workflows; integrations are ~30 lines of SDK code each; the readability gain doesn't justify a second source of truth. **F22 closes this decision: no visual-workflow runtime is part of Nexostrat at any layer.**

## The spine — `events.jsonl`

Single append-only log at `/srv/Nexostrat/infra/events/events.jsonl`. Every meaningful action emits one line. Schema-enforced via `infra/events/schemas/<type>.json`. Required fields: `ts`, `id`, `actor`, `type`, `scope`. Optional: `data`, `correlation_id`, `causation_id`. Monthly rotation to `events-YYYY-MM.jsonl.zst` (zstd compressed); never pruned.

## Event taxonomy

10 domains, ~80 event types. Full catalog auto-generated at `docs/reference/event_taxonomy.md` from JSON schemas:
- **meta/governance:** session.*, checkpoint.*, adr.*, decision.*, docs.drift_detected
- **intake & pipeline:** client.created, client.qualified, intake.*, pipeline.{advanced,blocked,unblocked,regressed}
- **skills:** skill.{requested,started,raw_output_completed,synthesis_started,completed,awaiting_review,go,stopped,note_added,ask_received,benchmark_regression}
- **meetings:** meeting.{confirmed,declined,scheduled,brief_sent,started,paused,resumed,ended,transcribed,parity_computed,extracted,summary_published}
- **chat:** chat.{message_received,extraction_run,finding_extracted,finding_confirmed,finding_rejected,finding_auto_filed}
- **tasks:** task.{created,completed,overdue,reassigned,due_changed}
- **vault & secrets:** vault.{read,write}, key.{rotated_routine,rotated_emergency}, secret.rotated, recipient.{added,removed}
- **infrastructure:** service.*, backup.*, warm_standby.*, desktop.{awake,asleep,wake_requested}, ollama.*, failover.executed
- **external:** calendar.*, whatsapp.* (future); plus whatever FOSS workspace Plan 02 picks (pre-ADR-038 list included `notion.*` — removed per ADR-038)
- **errors & safety:** hook.blocked, agent.{failed,timeout}, pipeline.timeout, secret.leak_detected, deal_breaker.triggered

## Python agents — `infra/agents/`

```
infra/agents/
├─ _lib/                       shared utilities
│   ├─ events.py               atomic append + read events.jsonl
│   ├─ secrets.py              decrypt secrets.env.age
│   ├─ telegram.py             bot client
│   ├─ calendar.py  models.py  state.py  docs_gen.py  tz.py  (pre-ADR-038 included notion.py — removed; Plan 02 picks the FOSS workspace client module)
├─ skill_<N>_<name>/           Skills 1-5 agents (run_manual.py + run_api.py)
├─ judge/                       Claude-as-judge synthesizer
├─ pipeline_orchestrator/       chains skills end-to-end with gates
│   ├─ orchestrator.py
│   ├─ state_machine.py        explicit phase transitions, guard predicates
│   └─ tests/
├─ meeting/                     brief_morning, brief_t15, transcription_watcher, extractor, parity_diff
├─ chat_extractor/              extract_loop
├─ event_router.py              long-running daemon: tails events.jsonl, dispatches per routing.yaml
├─ delivery_flush.py            per-user TZ-aware Telegram queue flusher (ADR-030)
├─ infrastructure/              warm_standby_rsync, backup_verification, daily_brief, desktop_wake, post_receive_mirror
└─ dispatch.py                  CLI entrypoint: `nexostrat run skill1 --client bodai --mode=api`
```

## Scheduling — `infra/systemd/*.timer`

Declarative timer units, committed to git. `infra/scripts/install-systemd-units.sh` symlinks into `/etc/systemd/system/` and enables. Cleaner than crontab — version-controlled, auditable, dependency-aware.

Examples: `nexostrat-meeting-brief.timer` (07:00 daily per user TZ), `nexostrat-chat-extractor.timer` (every 4h office hours), `nexostrat-warm-rsync.timer` (nightly 03:00), `nexostrat-backup-verify.timer` (weekly Sun 02:00), `nexostrat-delivery-flush.timer` (every 5 min).

## State machines — explicit Python classes

Phase transitions via `transitions` library or hand-rolled. State persisted in `state.json` per client + cumulative in events.jsonl. Every legal + illegal transition tested with pytest. Refactor with confidence.

## Telegram bot — architecture

`infra/telegram/bot/`: `main.py`, `core/{allowlist,plugin_loader,event_bus,chat_logger,template_renderer,rate_limiter,ai_escalator}.py`, `middleware/{auth,sensitive_filter,metrics}.py`, `tests/`.

Single Docker service on HP. Plugin auto-reload on add/edit.

## Plugin framework — one folder per command

`infra/telegram/plugins/<command>/{manifest.yaml, handler.py, tests/}`. `manifest.yaml` is canonical machine-readable spec (command, aliases, description ES/EN, usage, example, allowed channels, fires_event, related_docs, ai_escalation). `docs/reference/telegram_commands.md` + `/help` reply both auto-generated from manifests.

## Routing — `infra/telegram/routing.yaml`

Maps events to recipients per tier (not per channel — tiers are resolved per user by the delivery scheduler).

```yaml
- match: { type: skill.completed }
  recipients: [group]
  tier: 2
  template: skill_completed.j2

- match: { type: skill.awaiting_review }
  recipients: [group]
  tier: 2
  template: skill_awaiting_review.j2
  gates: [go, stop, note, ask]

- match: { type: deal_breaker.triggered }
  recipients: [group, ricardo, jp]
  tier: 1
  template: deal_breaker.j2
```

Editing routing.yaml is an ADR-level action.

## Per-user TZ-aware delivery (ADR-030, F6)

`infra/telegram/users/<userid>.yaml` per user. Fields: `timezone` (IANA), `working_hours` per weekday, `delivery_rules` per tier (`quiet_hours`, `channels`, `deferred_to: next_07:00 | morning_brief`), `morning_brief.{time,enabled,include_tiers}`, `meeting_brief.{send_at, fallback_min_lead_time}`.

`delivery_flush.py` daemon walks each user's queue every 5 min; delivers items whose `target_time <= now`. Morning-brief deferred items bundled into 07:00 local brief per user.

**Per-user systemd timer pattern (F6).** "07:00 each user's TZ" is implemented as **one timer unit per user** with an IANA-zoned `OnCalendar=` line (systemd 248+):

```ini
# /etc/systemd/system/nexostrat-brief-ricardo.timer
[Timer]
OnCalendar=America/Tijuana 07:00:00
Unit=nexostrat-brief-ricardo.service

# /etc/systemd/system/nexostrat-brief-jp.timer
[Timer]
OnCalendar=America/Bogota 07:00:00
Unit=nexostrat-brief-jp.service
```

Adding a third user adds a third pair of units. Group-brief delivery (rare events that should land in *both* mailboxes at *both* local 07:00s) is a Plan 08 design choice — the three candidate behaviors (earlier-of-two, send-twice with dedup token, nominal firm-TZ) are not yet ranked. ADR-036 records this as a v0/v1 trade-off: until 3+ users exist, "single firm TZ" is acceptable v0 fidelity for group briefs.

**Tier 1 is hard-coded (no user override):** hp.down, vault.unreadable, secret.leak_detected, deal_breaker.triggered, server_compromised, mirror_failed, api_budget_exceeded. `/emergency <text>` lets either founder escalate anything to tier 1 deliberately.

**User commands:** `/prefs`, `/prefs set tz <ianatz>`, `/prefs set tier_<N> quiet <hh:mm-hh:mm>`, `/quiet <duration>`, `/dnd [off]`, `/wakeup`, `/whats-queued`.

## AI escalation rules

```
DEFAULT — canned responses (no AI, instant)
ESCALATE TO OLLAMA — /ask, /manual, long natural-language messages, chat-extraction confirms
ESCALATE TO CLAUDE API — Ollama unreachable, low confidence, /ask --fast, critical events
DECLINE — sensitive-content filter trips, not allowlisted, rate-limit reached
```

Every AI escalation logs `ai.ollama_called` or `ai.api_called` with cost.

## Wake-on-LAN

Triggered by chat extractor queue >5 items OR direct command. Magic packet via etherwake. 60s window for `desktop.awake` event. Fallback to API if timeout. Desktop posts `desktop.awake` on systemd boot via a small unit.

## Sample chains (end-to-end)

**Chain 1 — Intake to Diagnóstico delivered.** `/intake bodai` → `intake.completed` → orchestrator advances to exploring → Skills 1-3 parallel via `run_api.py` → judge → Skill 4 → pause → `/go bodai-skills-1-4` → Skill 5 → pause → human review → `/go bodai-diagnostico` → `pipeline.advanced` to delivered → `task.created` for followup +7 days. **~30-45 min wall clock + human review pace.**

**Chain 2 — Meeting to followup.** 07:00 brief job → Telegram with confirmation → `/confirm` ×2 → T-15 reminder → `/meeting start` → Jitsi recording → `/meeting end` → Whisper transcribes → `meeting.transcribed` → Ollama summarization → extraction agent → events for actions/decisions/dates → Telegram digest. *Pre-ADR-038 flow used Notion poll + Whisper in parallel with parity diff; that dual-path is single-canonical now per ADR-038.*

**Chain 3 — Ambient chat to task.** Group message → encrypted log → 12:00 cron → extractor agent → `chat.finding_extracted` → threaded confirmation → `/confirm-extract` → `chat.finding_confirmed` → `task.created` → 📌 reaction.

## Failure modes — observability

```
events.jsonl locked      → retry 3× backoff → write events.jsonl.pending → drain next cycle
Workflow timeout         → pipeline.timeout event → DM Ricardo
Bot crashes              → systemd watchdog restart → DM Ricardo with stack trace
Ollama unreachable       → ollama.unreachable event → API fallback
Whisper crashes          → retry once → mark "no-transcript" → /meeting recover prompt
                           (pre-ADR-038: 2 rows handled Notion summary missing + Whisper-as-shadow fallback)
Pre-receive blocks       → secret.leak_detected → DM Ricardo with file path
Backup fails             → DM Ricardo CRITICAL → investigate before next push
```

---

# Section 10 — Testing, Observability & Failure Modes

## 5-layer testing

```
Layer 1  Unit tests        per-agent pytest with mocks; 80% coverage target
Layer 2  Integration       end-to-end pipeline tests with mock APIs; ~5-10 min CI
Layer 3  Benchmark         Bodai regression on every skill prompt edit
Layer 4  Hook tests        pre-commit + pre-receive scripts have their own tests
Layer 5  Smoke tests       post-deploy "is it alive" via infra/scripts/smoke-test.sh
```

**Critical integration test:** `test_intake_two_file_isolation.py` proves `our_hypotheses.md` NEVER reaches the research stage. Cannot regress this.

## 3-layer observability

```
1. events.jsonl       canonical audit trail, jq-queryable, narrative reconstructable
2. Structured logs    /var/log/nexostrat/<service>/YYYY-MM-DD.jsonl, 90 days retention
3. Metrics            Prometheus /metrics on HP; Grafana dashboards (Stage 2)
4. Telegram surfaces  /status, /pipeline, /infra, /events recent, /errors today, /metrics
```

## Failure modes catalog

Five categories, ~30 specific failure modes, each with detection mechanism + RTO + runbook reference:

- **Infrastructure:** HP down (15-30 min), HP+standby down (4-8h), disk full, network partition, power outage
- **Security:** laptop stolen (1h block + 24h rotate), key compromise, secret leak (immediate), server compromise (24-48h)
- **Data integrity:** events.jsonl corrupted, tasks.json corrupted, state.json corrupted, mirror divergence, vault unreadable
- **Pipeline:** Anthropic/Gemini/Grok API down, Ollama unreachable (auto-fallback), skill regression, orchestrator hung, bot down, Whisper crash, pandoc fail, libreoffice fail, meeting recording lost, chat extractor backlog (pre-ADR-038 also listed `Notion API down` — removed)
- **Human/governance:** wrong client edited (pre-commit confirms), phase advanced by mistake (state.json history preserved), accidental delete (git restore), deal-breaker triggered (24h conflict protocol)

Each runbook at `docs/runbooks/<name>.md` + script at `infra/recovery/<name>.{sh,py}`. Runbook explains; script does. **All written before Stage 1 ships.**

## 4-tier alerting (per-user TZ-aware via ADR-030)

```
Tier 1 — CRITICAL   immediate to DMs + group, overrides quiet hours
Tier 2 — HIGH       to DM, deferred outside working hours
Tier 3 — MEDIUM     bundled into morning brief
Tier 4 — INFO       events.jsonl only; surface via /events or /status
```

Per-user `delivery_rules` in `infra/telegram/users/<userid>.yaml` defines quiet windows, channels, deferral behavior.

## Quality gates

```
Every commit         pre-commit passes; -explicado pair updated; CHECKPOINT.md valid
Every push to main   pre-receive passes; unit + integration tests pass; doc generators clean
Every skill edit    + benchmark passes; ADR if score changed >5%
Every deploy        + tested on standby 24h+; smoke tests green; rollback verified
Architectural change + ADR drafted; risk-auditor for ≥5-scope changes; JP review for medium+
```

## Stage 1 go-live checklist

Every box must be green before "Stage 1 live, ready for first pilot":

- **Foundation:** repo scaffolded, Gitea + GitHub + Codeberg, age keypairs, secrets.env.age, vault structure, warm-standby provisioned, Drive rclone
- **Services HP:** docker-compose smoke test, bot live, Jitsi/Nextcloud/Whisper running, event-router daemon
- **Services Desktop:** Tailscale up, Ollama with 3 models, suspend timer + WoL working
- **Governance:** ADR-001..035 in `00_GOVERNANCE/adr/`; partnership docs filled + signed
- **Skills:** Skill 1 in place; Bodai benchmark baseline; Skills 2-5 scaffolds
- **Pipeline:** `_template/`, `bodai/` scaffolded + intake filled, Skill 1 Mode A + Mode B both run end-to-end on Bodai, Aurora pandoc renders correctly
- **Docs:** `docs/README.md` + 4 folders populated; ≥10 how-tos covering core workflows; all paired
- **Observability:** `/status` returns truthful health; daily_brief.py runs at 07:00; routing.yaml live
- **Partnership:** founding meeting done; first pilot (Alfa Bitcoin) selected; cost-share signed

When every box green: `/release v1.0` → `deploy.released` event → first pilot starts.

---

## Open Items — what needs to happen before scaffolding

**All items closed as of 2026-05-16.** Historical record preserved (with completion dates) so the document narrative remains intact.

1. ~~**JP brand top-5 vote** (t-006, due 2026-05-14).~~ **DONE 2026-05-12** — JP voted; Nexostrat won; partnership signed same day.
2. ~~**Domain + handles secured** (t-007, due 2026-05-16).~~ **DONE 2026-05-12** — `nexostrat.com` registered (Hostinger). Email `contacto@nexostrat.com` provisioned. Trademark clearance pending Stage 2 when entity is constituted.
3. ~~**JP walkthrough** (t-010, due 2026-05-15).~~ **DONE 2026-05-13** — architecture review approved.
4. ~~**Founding Meeting (Plan Maestro Paso 1)** before scaffold. Sign partnership agreement.~~ **DONE 2026-05-12** — verbal+operational agreement; markdown PARTNERSHIP_AGREEMENT.md is the canonical artifact (per 2026-05-16 ceremony-reduction decision; formality returns at external need).
5. ~~**JP interface choice** (Heavy/Light — Hosted dropped per ADR-021bis).~~ **DONE 2026-05-15** — JP picked Light; JP-Light variant excludes Gitea web (per ADR-038 companion decision).

Going-forward backlog (was implicit, now explicit post-Plan-01a-execution): Plan 01b execute (mirrors + warm-standby; due 2026-06-05), Plan 01c execute (personas + hooks + smoke test; due 2026-06-12), Plan 02 brainstorm + write + execute (FOSS docs stack picks; load-bearing per ADR-038). Live state tracked in [`tasks.json`](../../tasks.json) and [`STATUS.md`](../../STATUS.md).

## Glossary

- **Aurora** — the brand palette (Midnight / Ocean Deep / Sky Blue / Emerald / Amber / Arctic White).
- **age** — modern encryption tool; per-user keys for vault + secrets.
- **CHECKPOINT.md** — per-persona session-handoff file; the baton between sessions.
- **Diagnóstico** — the firm's first deliverable (Skill 5 output); free for first 3 pilots, paid after.
- **events.jsonl** — append-only spine; every meaningful action emits one line.
- **judge prompt** — Claude-as-Judge synthesizer template at `skills/shared/judge_prompt.md`.
- **Mode A / Mode B** — dual pipeline: manual (CLI session, $0) and API (Python agents, ~$1.25/Diagnóstico).
- **parity diff** — transcript-vs-transcript comparison job; rolling readiness score. Originally (pre-ADR-038) ran Notion AI vs Whisper.cpp; post-ADR-038 the infrastructure remains as a Stage-2 readiness mechanism if Plan 02 picks a FOSS tool with a polished alternative summary path.
- **research_input.md** — slices 1+2 of intake (facts + private context); fed to research models.
- **our_hypotheses.md** — slice 3 of intake (judgment); SEALED during research, read at synthesis.
- **runs/** — per-skill folder holding multiple Mode A or Mode B runs; canonical.md symlinks the chosen one.
- **shadow** — the dual-tools FOSS mirror of paid tools (Jitsi, Nextcloud, Ollama, Whisper, Anytype).
- **warm-standby** — second laptop with idle docker-compose; manual failover RTO 15-30 min.
- **WAHA** — WhatsApp HTTP API; future client-side communication channel via `waha-nexostrat`.

## Change Log

| Date | Agent | Description |
|------|-------|-------------|
| 2026-05-13 | Claude (Opus 4.7 1M, with Ricardo at root) | Founding spec v1 written, consolidating 10 design sections + 4 cross-cutting additions ratified during the 2026-05-13 brainstorming session. Supersedes 2026-05-11 partial spec; introduces ADRs 021-035. Pending Ricardo's review of this written artifact before invoking the writing-plans skill for the implementation plan. |
| 2026-05-14 | Claude (Opus 4.7 1M, Batch 1 amendments) | Single-pass amendment per [`2026-05-14_amendments.md`](2026-05-14_amendments.md). Applied: F6 (per-user systemd timer pattern in §9 + ADR-030 amend), F9 (manifest.json schema in §6), F10 (persona table reallocation in §4 — Founder/Client-Owner/Skills-Master vault namespaces split), F11 (re-status of ADRs 005/013/018 to Amended with notes), F12 (root file map `events.json` → `calendar.json`; rename executed in terrain prep), F13 (Linux Mint recommended baseline for JP Heavy in §5), F17 (chat capture `/dev/shm` daytime + 23:59 encrypt cron in §8.10), F19 ("12-station chain + 3 cross-cutting" standardized — persona table fix in §4), F22 REVISED (all peripheral n8n references deleted; ADR-029 rewritten to positive framing "Python agents + systemd timers"), R3 (ADR-036 row added — Stage 1 v0/v1 fidelity), R4 (CHECKPOINT concurrent-session protection note in §4.10), R5 (ADR-037 row added — Notion canonical role Stage 2 review trigger), ADR-021bis row added (drop Hosted from JP options; §10 Open Items updated). Brain-references stripped per the no-Brain directive: lines that previously cited `/srv/brand/`, "personal Brain", or AttenBot/n8n peripherals in §§1/2/3/4/5/8/9 all rephrased Nexostrat-natively. Gitea host port `:3001` made explicit in §1 Network and §5 docker stack listing. F14 REVISED (Notion cost stays $0 to firm via JP's personal subscription) is a no-op on the spec — original §5 cost table already reflects this; Stage 1 envelope stays at $36-91/mo. Three new ADR bodies (021bis, 036, 037) drafted as separate Batch 1b commit. |
| 2026-05-16 | Claude (Opus 4.7 1M, ADR-038 sweep + hard-system-audit patches) | **`t-spec-notion-removal-amendment` sweep pulled forward** per 2026-05-16 hard system audit recommendation. Header status `PROPOSED` → `ACTIVE`. ADR-024 + ADR-037 flipped to `Superseded by ADR-038`. ADR-038 row added to ADR map with link to full body. ADR-001 substrate description amended ("markdown-in-git + Telegram + FOSS workspace TBD" — removed Notion). §2 file map: `inbox/` annotated `(PLAN 04)`, `shared/` annotated `(PLAN 01c)`, cost-sharing parenthetical de-Notioned. §5 cost table restructured: firm-paid is $0 Stage 1; pre-revenue founder personal-spend reflects Claude MAX subscription reality + Notion line removed (JP total drops to ~$207/mo from ~$237-257). §6 state.json recording_preference enum updated. §8 meeting-capture table + client recording options + internal meeting flow + /meeting recover + audio archival all amended to single-canonical (Jitsi + Whisper.cpp interim per ADR-038; Plan 02 may revise). §9 testing/event-taxonomy/`_lib` references purged of `notion.*` / `notion.py`. §9 Sample Chain 2 amended. §9 + §10 failure modes: 2 rows handling Notion failures collapsed to single Whisper-crash row. §10 Open Items 1-5 marked DONE with dates + going-forward backlog added. F14 REVISE-REVERSED (per ADR-038). M5 (REVENUE_DISTRIBUTION.md:38) fixed in companion partnership-file sweep same date. Glossary parity-diff entry amended. |
