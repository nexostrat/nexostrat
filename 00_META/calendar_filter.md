# Nexostrat calendar filter v1

This is the **canonical source of truth** for which Google Calendar events qualify as Nexostrat-relevant. The Claude session populating `calendar_cache.json` MUST honor this rule. Events failing the rule MUST NOT enter the cache (no exceptions).

## Filter rule v1

An event qualifies if **any** of:

1. `summary` contains "nexo" (case-insensitive).
2. The event sits on a sub-calendar literally named `Nexostrat`.
3. The attendee list contains JP's email (configured per-deploy; today: `jp@example.com` placeholder until JP's actual email is wired in).

Events failing all three: **filtered out. Period.**

Defensive default: events with missing `summary` / `attendees` / `source_calendar` fields do NOT match. Better to drop a real Nexostrat event than leak a personal one into the Nexostrat-scoped cache.

## Cache schema

`calendar_cache.json` includes a top-level `filter_applied: "nexostrat-v1"` field naming the filter version. A future audit detects drift by comparing this field to the heading of this file. The constant lives at `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py::FILTER_VERSION`.

## Implementation

The reference implementation is `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py::nexostrat_filter(event, jp_email) -> bool`. The Claude session imports this filter directly rather than re-implementing the rule. Tests at `/srv/brain-hub/tests/test_nexostrat_calendar_filter.py`.

## Migration trigger

Provision firm-owned Google account (`ops@nexostrat.com` or similar) **before Stage 1 launch**. Cut over the calendar to that account. Drop the filter (whole account = Nexostrat scope by construction). At cutover, bump `filter_applied:` to `nexostrat-noop-firm-account-v1` and replace the body of `nexostrat_filter()` with `return True` (or remove the call site entirely).

## Audit

This file ratifies audit B7. Any change to the filter rule requires:

1. Bumping `FILTER_VERSION` in `calendar_filter_nexostrat.py`.
2. Updating this file's heading + Filter rule section.
3. A new ADR if the change is non-trivial (e.g., scope expansion to include new attendees).
4. Brain Architect sign-off — calendar privacy is load-bearing for Nexostrat's separation from Personal.
