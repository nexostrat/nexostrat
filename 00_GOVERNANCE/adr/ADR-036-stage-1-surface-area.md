# ADR-036 — Stage 1 surface area: v0 vs v1 fidelity (deliberate trade-offs)

**Status:** Accepted
**Date:** 2026-05-14
**Decided by:** Ricardo + Claude (Batch 1 amendments per [`2026-05-14_amendments.md`](../../00_META/proposals/2026-05-14_amendments.md) §R3)

## Context

The founding spec describes the full v1 architecture in detail. Several features are designed at v1 fidelity but only need **v0 fidelity** to ship Stage 1 successfully — that is, to onboard the first paying clients and prove the firm works end-to-end with two co-founders. Treating every feature as v1-or-bust delays Stage 1 unnecessarily; treating every feature as v0-forever creates a long tail of half-built systems.

This ADR enumerates the v0/v1 split explicitly, so future-Ricardo, future-Claude, and future-JP can tell which corners are intentionally cut vs which are oversights.

The 2026-05-14 audit (Recommendation 3) requested this artifact: without it, every "but the spec says X" question requires re-deriving whether X was a v0 or v1 commitment.

## Decision

The following features ship at **v0 fidelity** in Stage 1, with **v1 deferred** until a documented trigger. v1 work is real work; it's just not Stage 1 work.

### Per-user timezone delivery (ADR-030)

- **v0:** single firm TZ for group briefs (configurable to either America/Tijuana or America/Bogota, but the same for both founders). Per-user TZ infrastructure exists (`infra/telegram/users/<userid>.yaml`) and works for DM-only deliveries.
- **v1:** group-brief TZ resolution (earlier-of-two, send-twice-with-dedup, or nominal-firm-TZ) designed and implemented per Plan 08.
- **Trigger to v1:** a third user joins the bot's allowlist, OR Ricardo and JP report measurable friction from the v0 compromise.

### Ambient chat extraction (ADR-034)

- **v0:** manual `/note` capture is acceptable. The Telegram bot stores all messages encrypted (per ADR-034) but extraction-confirmation flow can be skipped — Ricardo/JP read chat logs directly during sessions when needed.
- **v1:** Ollama-based 4-hourly extraction loop with confirmation threads, sensitive-content filter, wake-on-LAN integration.
- **Trigger to v1:** chat volume exceeds ~50 messages/day for 2 consecutive weeks, OR a quarterly review identifies a meaningful action item that was lost in chat.

### Two-tier docs hook (ADR-025)

- **v0:** pre-commit refuses unpaired modifications in tier-1 folders, but the weekly drift audit (Sunday 06:00) is run manually by Ricardo when he remembers.
- **v1:** automated weekly drift audit cron + summary to Telegram.
- **Trigger to v1:** Plan 02 execution (docs system build-out).

### Meeting parity diff (ADR-024)

- **v0:** Notion AI is canonical for both internal and client meetings; Jitsi/Whisper shadow is optional and run by Ricardo when he wants to compare. Parity score tracked manually in `infra/shadow/whisper/parity_score.md`.
- **v1:** automated parity diff agent runs per meeting, rolling score, Stage 2 trigger evaluation per ADR-024.
- **Trigger to v1:** Plan 08 execution (meeting pipeline build-out).

### Backup verification (§3 backup ladder)

- **v0:** Ricardo manually runs `infra/scripts/verify-backups.sh` on Sundays.
- **v1:** systemd weekly timer runs verification, posts result to Telegram.
- **Trigger to v1:** Plan 01b execution (mirrors + standby) — the timer ships with that plan.

### Observability (§10.2)

- **v0:** structured logs + `events.jsonl` + Telegram `/status` `/pipeline` `/errors` plugins. Prometheus `/metrics` endpoint exists; Grafana dashboards do not.
- **v1:** Grafana dashboards on HP with alerting rules.
- **Trigger to v1:** Stage 2 (post first 3 paid clients) OR an operational incident reveals a missing dashboard.

### Multi-language (Spanish/English)

- **v0:** internal artifacts English; client-facing artifacts Spanish (Mexico/Colombia register). Templates parameterized by locale but only `es-MX` and `es-CO` are filled in; `en-US` skeletons exist for future client work in English.
- **v1:** full bilingual Jinja2 templates for `en-US` exercised on at least one English-speaking client engagement.
- **Trigger to v1:** first English-speaking client signed.

## Consequences

**Positive:**
- Stage 1 milestone (`v0.1-foundation` through `v1.0` per Plan 10) is reachable in 7-9 weeks instead of indefinite.
- Each "v0" entry is a deliberate, documented choice with a known trigger — there is no surprise-tech-debt list.
- v1 work becomes self-prioritizing: when a trigger fires, the next plan-write cycle picks it up.

**Negative:**
- The spec describes v1 in places where Stage 1 only ships v0. Readers may assume the v1 description is what's live. This ADR is the antidote — anyone confused about "is X actually built?" reads ADR-036 and finds out.
- A v0 feature that lives too long can ossify (manual processes accumulate undocumented exceptions). Quarterly review explicitly looks at this list and asks "should any trigger be considered fired?"

**Review cadence:** quarterly partnership review revisits this ADR. Triggers that fired but weren't acted on get scheduled; triggers that haven't fired remain dormant.
