# Partnership Agreement — Nexostrat

**Effective:** 2026-05-12 (Founding Meeting)
**Co-owners:** Ricardo Mejía Caicedo, Juan Pablo

---

> **This document IS the partnership agreement at Stage 1.** Ricardo and JP are brothers
> operating Nexostrat as an informal 50/50 partnership; no notarized or signed legal
> artifact exists. Formality (signed PDF, notarization, registered entity) returns at the
> point of external need — first paying client, first hire, regulator exposure, or
> dissolution. Until then, this markdown is the canonical reference for terms, and
> amendments happen by editing this file with both founders' consent (recorded via git
> commit history).

---

## Co-owners

| Co-founder | Role | Bandwidth |
|---|---|---|
| **Ricardo Mejía Caicedo** | Architect/Operator — infra, Skills, AI pipeline, bookkeeping | ~30+ h/wk (full-time Stage 1) |
| **Juan Pablo** | Sales/Relations — prospect sourcing, closing, client brand voice | ~10 h/wk (Stage 1; parallel obligations) |

Full role definitions and decision rights in [`ROLES.md`](ROLES.md).

## Equity

- **50/50 split** — equal ownership of Nexostrat.
- Fully vested at founding meeting (2026-05-12); no cliff, no vesting schedule.
- No buyout preference for either founder.
- Both names on any future entity formation.
- Equity dilution (new partners, investor, etc.) requires both founders' signatures.

## Revenue distribution

Per-engagement gross revenue (after payment-processor fees, before direct API costs)
splits on the **20/20/20/40** model:

| Bucket | % | Recipient |
|---|---|---|
| **Company** | 20% | Firm reserve + shared expenses |
| **Originator** | 20% | Founder who first sourced the prospect |
| **Closer** | 20% | Founder who landed the contract |
| **Executor** | 40% | Founder(s) who delivered the engagement |

A founder who fills all three roles receives 80%; 20% goes to Company. Full definitions and
reserve targets in [`REVENUE_DISTRIBUTION.md`](REVENUE_DISTRIBUTION.md).

## Decision-making

- **50/50 voting** on architecture, brand, hiring, and any spend ≥ USD 500.
- **Operational autonomy** within each founder's domain — no sign-off needed for
  day-to-day calls inside your lane (see [`ROLES.md`](ROLES.md)).
- **Conflict mechanism:** JP's 15-min raised-hand; details in
  [`CONFLICT_PROTOCOL.md`](CONFLICT_PROTOCOL.md).

## Cost-sharing (pre-revenue)

Pre-revenue, the firm carries USD $0/mo. Each founder absorbs domain tooling on personal
subscriptions (Ricardo ~USD 215-225/mo; JP ~USD 207/mo per ADR-038 amendment 2026-05-16 — Notion line removed; was ~$237-257). Reimbursement triggers when
firm cumulative revenue ≥ USD 1,000. Full schedule and line-item table in
[`cost-sharing-agreement.md`](cost-sharing-agreement.md).

## KPIs (Stage 1 — 12 months from launch)

| Metric | Target |
|---|---|
| Paying clients | ≥ 10 |
| Total revenue | ≥ USD 20,000 |
| Diagnóstico → paid conversion rate | ≥ 30% |
| Bodai benchmark score | ≥ 7/10 (pilot start), ≥ 8/10 (paid graduation) |

Full pipeline health and quality metrics in [`KPIs.md`](KPIs.md).

## Termination / dissolution

- Either founder may initiate dissolution with **6-month written notice** (Signal message
  is sufficient at Stage 1).
- During notice period: both founders preserve all firm assets; no unilateral asset
  disposal.
- Asset disposition and wind-down procedure per
  `00_GOVERNANCE/dissolution-protocol.md` (to be drafted at Stage 2 or when first
  external need arises).

## Amendment procedure

> Amendments happen by editing this file with both founders' consent. The commit history
> is the audit trail; the raised-hand mechanism in `CONFLICT_PROTOCOL.md` precedes any
> substantive change. If/when the firm graduates to a notarized legal artifact (driven by
> external need — e.g., first hire, registered entity formation, dissolution), the formal
> document supersedes this markdown and this file becomes the plain-language summary.

---

**Form of agreement:** plain markdown (no notarized PDF; brothers-as-partners — see top blockquote)
**Founding Meeting:** 2026-05-12 (verbal + operational agreement on these terms; both founders present)
**This document updated:** 2026-05-16 (Plan 01a Task 17 reframed per `feedback_prefer_architecture_over_ceremony.md`; cost-sharing JP total recalculated per ADR-038 sweep same date)
**Amendment procedure:** edit this file with both founders' consent; commit message documents the change; raised-hand (`CONFLICT_PROTOCOL.md`) precedes any substantive amendment.
