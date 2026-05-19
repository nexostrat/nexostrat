# trixx-logistics — Trixx Logistics Corp. (Grupo Trixx)

**Country:** MX · **Sector:** logistica-cross-border · **Started:** 2026-05-18 · **Pilot:** true

Per-client work folder. Structure inherited from `pipeline/clients/_template/` —
see [`../_template/README.md`](../_template/README.md) for the 12-station + 3-cross-cutting
layout and the state-machine reference.

## Where things live (this client)

- **`00_intake/research_input.md`** — facts (ADR-027 slice 1+2). Read by Skills 01-03.
- **`00_intake/our_hypotheses.md`** — judgment (ADR-027 slice 3). SEALED during research; read by Skills 04-05.
- **`state.json`** — phase + history + pricing + KPIs. State-machine reference in `../_template/README.md`.
- **`checkpoint.md`** — session continuity baton (per ADR-031).
- **`<NN>_<stage>/`** — one folder per pipeline station (00 → 11).

## Next step

After editing `00_intake/research_input.md`, say in this Claude Code session:

> `Analiza trixx-logistics`

That triggers Skill 01 (company-analyst) with `research_input.md` as the operator-supplied context.
`our_hypotheses.md` remains sealed; it only opens when Skill 04 runs.
