# Cost-sharing agreement (pre-revenue)

**Effective:** 2026-05-12. **Amended 2026-05-16** per ADR-038 (Notion drop) — Notion line removed; JP total recalculated. Reviewed at first revenue + every quarter.

## Principle

Pre-revenue, the firm-as-entity carries no costs. Each co-founder absorbs
their domain's tooling on personal subscriptions; the firm reimburses at
first-revenue per the schedule below.

## Stage 1 — pre-revenue (current)

| Cost line | Who pays | Personal account holder | Monthly | Reimbursable? |
|---|---|---|---|---|
| **Claude MAX (Ricardo)** | Ricardo | Ricardo personal Anthropic | ~USD 200 | Yes (capped at engagement count) |
| **Claude MAX (JP)** | JP | JP personal Anthropic | ~USD 200 | Yes (same cap) |
| **Gemini API** | (free tier) | n/a | $0 until ~Oct 2026 | n/a |
| **Grok API** | Ricardo | Ricardo personal X | ~USD 5-15 | Yes |
| ~~Notion + AI add-on~~ | ~~JP~~ | ~~JP personal Notion~~ | ~~USD 30-50~~ | **REMOVED 2026-05-16 per ADR-038** (Notion exits firm-level; FOSS replacement TBD in Plan 02) |
| **Domain (nexostrat.com)** | JP | JP personal registrar | ~USD 12/yr amortized | Yes |
| **Email (contacto@nexostrat.com)** | JP | JP personal hosting | ~USD 6/mo | Yes |
| **Hosting (Gitea + bot, currently HP-laptop)** | $0 | n/a | $0 | n/a |
| **Drive 2TB** | Ricardo | Ricardo personal Google | ~USD 10/mo | Yes |
| **Bitwarden Premium** | Each personal | each | ~USD 1/mo each | No (personal hygiene) |
| **Hardware (HP-laptop, JP-laptop, peripherals)** | Each | each | n/a | No (personal asset) |
| **Tailscale** | (free tier — personal accounts) | n/a | $0 | n/a |
| **Signal** | n/a | n/a | $0 | n/a |
| **Telegram** | n/a | n/a | $0 | n/a |
| **Total firm pays in Stage 1** | | | **USD $0/mo** | |
| **Total Ricardo personal pays (reimbursable)** | | | **~USD 215-225/mo** (Claude MAX 200 + Grok 5-15 + Drive 10) | Yes |
| **Total JP personal pays (reimbursable)** | | | **~USD 207/mo** (Claude MAX 200 + Domain ~1 + Email 6) | Yes |

> **2026-05-16 amendment note:** Per ADR-038, Notion exits the Nexostrat architecture at the firm level. JP's personal Notion subscription, if he keeps it, is outside firm scope and not reimbursable. The Plan 02 brainstorm picks FOSS replacements (Whisper.cpp + Ollama + EspoCRM/AppFlowy/etc.) for the four roles Notion was filling. JP's recalculated total drops from ~$237-257/mo to **~$207/mo**.

## Reimbursement schedule (triggered at first revenue)

When firm cumulative revenue ≥ USD 1,000:
1. Ricardo and JP each submit a 12-month rolling reimbursement claim from
   `cost-sharing-agreement.md` line items (no receipts needed for the
   subscriptions listed above; dollar figures are honor-system at the
   subscription cost).
2. Reimbursements paid in order: hosting/domain/email first (hard
   infrastructure), then Drive, then Claude MAX (capped at the
   number of engagements Claude was used on × per-engagement budget).
3. Capped at 50% of accumulated Company-bucket reserve to keep operating
   reserves intact.

## Stage 2 trigger (firm absorbs costs directly)

When ANY of:
- Cumulative revenue ≥ USD 5,000
- Reserve target met (USD 5K)
- First payroll drawn

…the firm switches to direct billing for the FOSS self-hosting infrastructure picked in Plan 02 (Whisper.cpp/Ollama/CRM hosting if any), plus Drive + email + domain
(Bitwarden org sub at this point too, per Stage 2 ADR-019). Claude MAX
remains personal until single-month firm spend on AI exceeds USD 500.

## Reconciliation cadence

Quarterly (`00_PARTNERSHIP/reviews/<YYYY>-Q<N>.md`): both co-founders confirm
their personal-spend lines are unchanged or update them. Unchanged is the
default — no one needs to email a receipt.

---

*Source: 2026-05-14 Aurora HTML presentation Card 28 cost reality (Card 28
post-amendment) + Founding Meeting verbal agreement on personal-spend
reimbursability. **Amended 2026-05-16** per ADR-038 sweep (`t-spec-notion-removal-amendment` pulled forward post-hard-system-audit). Spec §5 cost table updated in the same sweep to align with this document.*
