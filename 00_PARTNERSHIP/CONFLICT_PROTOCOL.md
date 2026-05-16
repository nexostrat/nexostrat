# Conflict protocol — 15-min raised-hand

**Effective:** 2026-05-12 (signed at Founding Meeting)
**Co-owners:** Ricardo Mejía Caicedo, Juan Pablo

## Principle

When the co-founders disagree on a non-trivial decision and conversation
has not resolved it within ~15 minutes of focused discussion, either co-founder
may invoke the **raised hand**. The disagreement pauses; the position is
captured in `raised_hand_log.md`; both parties sleep on it; the next
business-day session opens with the raised hand on the agenda.

## When to raise the hand

- Architectural decisions with ≥1 month of unwind cost
- Spend decisions ≥ USD 500 single-cost or ≥ USD 100/mo recurring
- Client-facing policy changes
- Public-facing brand changes
- Anything one co-founder feels would set a precedent they can't live with

Trivial day-to-day calls do not need the raised hand.

## Mechanism

1. **Either co-founder says: "I'm raising the hand on this."**
2. The active conversation pauses — no further argumentation in that thread.
3. The raiser writes a single entry in `raised_hand_log.md`:
   ```
   ## YYYY-MM-DD · <one-line summary>
   **Raised by:** <name>
   **Their position:** <2-4 sentences>
   **Other party's position:** <2-4 sentences as understood>
   **What's at stake:** <1-2 sentences>
   **Sleep-on-it deadline:** <next business day>
   **Resolution:** <added when resolved>
   ```
4. Both parties sleep on it (minimum overnight).
5. Next business day opens with the raised hand. If alignment is reached,
   the resolution is recorded. If not, escalate per § Escalation.

## Escalation

If sleep-on-it does not resolve:
1. **Cooling-off (1 week).** Both parties write a one-page position; exchange.
2. **External brain.** Trusted advisor (TBD — name in `ROLES.md` when picked)
   reads both positions and offers a recommendation. Recommendation is
   advisory, not binding.
3. **Fall-back rule per category:**
   - Code/architecture: Ricardo decides (operator-of-record).
   - Sales/client policy: JP decides (relationship-of-record).
   - Anything else: deadlock → defer the action; status quo holds.

## What this protocol is NOT

- Not a vote-counter (50/50 means deadlock = no action by default).
- Not a delay tactic — raised hands resolve in days, not weeks.
- Not a substitute for direct conversation. It exists for the cases where
  conversation has visibly stopped helping.

---

*Source: Plan Maestro Q-set, founding meeting 2026-05-12. JP's "15-min
raised hand" framing is verbatim from his questionnaire response (Q on
conflict mechanics).*
