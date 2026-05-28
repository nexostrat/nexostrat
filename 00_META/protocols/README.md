# Protocolos de sesión

Protocolos pre-escritos para sesiones de Claude Code Founder con objetivo + alcance + procedimientos definidos antes de arrancar.

**Cuándo usarlos:** cuando una sesión tiene una meta clara, los insumos están preparados, y querés que Claude ejecute con disciplina sin re-derivar contexto.

**Cómo invocarlos:** al abrir sesión, escribir:

> Start session siguiendo el protocolo `00_META/protocols/<archivo>.md`

Claude leerá primero el protocolo (que ya tiene su propio Session Start mínimo) + después contexto adicional si el protocolo lo indica.

## Protocolos activos

| Archivo | Sesión | Objetivo | Prerequisitos | Cuándo activar |
|---|---|---|---|---|
| [sesion-S1-catalogo-capacidades.md](sesion-S1-catalogo-capacidades.md) | S1 — F4 | 1-pager Catálogo Capacidades Nexostrat | JP disponible (sincrónico o asíncrono) | cuando JP confirme bandwidth |
| [sesion-S2-investigacion-odoo.md](sesion-S2-investigacion-odoo.md) | S2 — F6 | Decisión Odoo vs Notion para CRM | ninguno | cuando Ricardo quiera resolver el CRM |
| [sesion-S3-reporte-oportunidad-trixx.md](sesion-S3-reporte-oportunidad-trixx.md) | S3 — Trixx | Refinar Reporte Oportunidades Trixx con notas Ricardo | ninguno (insumos listos) | cuando Ricardo quiera el reporte final-final |

## Lifecycle

- **DRAFT** — protocolo escrito, sesión no ejecutada todavía.
- **EJECUTADO** — al cierre de la sesión, agregar nota al inicio con journal entry + outputs path + status final.
- **ARCHIVADO** — mover a `00_META/protocols/archive/YYYY-MM-DD_<archivo>.md` después de que el output esté en producción.

## Convención de naming

`sesion-S<N>-<topic-slug>.md` — el `<N>` es solo orden estratégico (no fecha; las sesiones ocurren cuando Ricardo decide). Después del cierre, podés agregar fecha de ejecución en el journal pero el archivo del protocolo mantiene su número.
