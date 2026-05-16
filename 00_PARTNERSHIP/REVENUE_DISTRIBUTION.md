# Revenue distribution — 20/20/20/40

**Effective:** 2026-05-12 (signed at Founding Meeting)
**Co-owners:** Ricardo Mejía Caicedo, Juan Pablo

## Per-engagement split

For each invoiced engagement, gross revenue (after Stripe/payment-processor
fees but BEFORE direct delivery costs like API tokens) splits as:

| Bucket | % | Goes to |
|---|---|---|
| **Company** | 20% | Held in `operations/accounting/`; covers shared expenses + reserves + reinvestment |
| **Originator** | 20% | The co-founder who first sourced the prospect |
| **Closer** | 20% | The co-founder who landed the contract |
| **Executor** | 40% | The co-founder who delivered the engagement (split pro-rata if both contributed materially) |

## Originator vs Closer vs Executor — definitions

- **Originator:** First non-trivial introduction of the prospect into our pipeline.
  Trivial = "I saw their LinkedIn"; non-trivial = "I had a discovery
  conversation, qualified them, brought them to a Diagnóstico-eligible state."
- **Closer:** Signed the contract — name on the proposal-acceptance email,
  led the pricing conversation.
- **Executor:** Delivered the work — Skills runs, meetings led, artifacts
  written. Multi-person engagements split this bucket pro-rata by
  documented effort (logged via Telegram `/expense time` entries against
  the client; quarterly review reconciles).

A co-founder can hold all three roles for one engagement (= 80% of revenue
to that founder; 20% to company). This is fine and expected for
founder-sourced-and-delivered work.

## Cost handling

- **Direct API costs** (Anthropic, Gemini, Grok per engagement) are paid by
  Company before split. Tracked in `operations/accounting/api-spend.md`.
- **Shared infrastructure** (Notion, hosting, domain — see
  `cost-sharing-agreement.md`) does NOT come out of per-engagement revenue;
  it's pre-revenue founder personal-spend reimbursed at first-revenue per
  the cost-sharing agreement.

## Reserves

The Company 20% accumulates until reserve target is met:
- **Stage 1 target:** USD 5,000 reserve (covers ~3 months of API + tooling
  if revenue dries up).
- **Stage 2 target:** 6 months of fully-loaded operating cost.

Once reserves are full, excess Company-bucket distributes 50/50 between
co-founders (treated as additional dividends, not as bonus to a particular
role).

## Quarterly review

Every quarter end (Mar/Jun/Sep/Dec, last Friday): both co-founders review
the per-engagement split log, reconcile any disputed
originator/closer/executor calls, and acknowledge the company-bucket
balance. Output: a one-page `00_PARTNERSHIP/reviews/<YYYY>-Q<N>.md`.

---

*Source: Plan Maestro Q-set, founding meeting 2026-05-12. The 20/20/20/40
ratio is verbatim from JP's revenue-mechanics response.*
