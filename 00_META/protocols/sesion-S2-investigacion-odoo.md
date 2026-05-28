# Protocolo S2 — Instalación Odoo CE (CRM/funnel) · [decisión CRM YA tomada]

## DECISIÓN LOCKED — 2026-05-28 (sesión 27)

La pregunta "Odoo vs Notion" quedó **resuelta por Ricardo: Odoo Community Edition.** La investigación comparativa de abajo es ahora histórica/de respaldo; este protocolo gobierna la **sesión de instalación** (en el HP server, donde se instala Odoo). Decisiones cerradas en sesión 27 vía brainstorming (diseño aprobado en principio):

- **Edición:** Odoo **Community Edition** (LGPLv3, free forever, sin subscripción). Enterprise NO.
- **Reemplaza Baserow por completo** (Odoo = CRM/funnel humano **y** state-store). Baserow estaba dormido (nunca usado a mano; deploy chunk-c abierto) → low-regret.
- **Alcance (broad suite):** CRM + Contacts + Sales + Project + Invoicing + Calendar.
- **Host:** HP server `100.64.121.80` (always-on, Tailscale, WAN-firewalled), donde ya viven Gitea + FOSS stack.
- **Despliegue:** extender `infra/docker/foss-stack/docker-compose.yml` (servicios `odoo` image `odoo:18` + `odoo-db` `postgres:16`), nuevo vhost Caddy `odoo.nexostrat.local` → `:8069` (+ websocket `:8072`), mismo binding 127.0.0.1 + Tailscale, secrets en `secrets.env.age`. Fuente offline/local; sin red externa requerida por Odoo.
- **Pipeline stages = funnel Nexostrat** (`contacto → agendada → skill-chain → call → diagnóstico → entregado/seguimiento`); usuarios Ricardo + JP.
- **Migración en 4 fases (Baserow NO se remueve hasta que Odoo pruebe su trabajo):** (1) parar Odoo + apps + funnel stages [= "start con Odoo y aprender"]; (2) modelar clients/meetings/deliverables/financials en Odoo; (3) repuntar los 5 skill renderers + reconcile de Baserow API → Odoo API (XML-RPC/JSON-RPC); (4) retirar Baserow del compose + plegar Odoo pg_dump + filestore al backup posture (chunk-c) + runbooks.

**Por qué Docker y no apt:** menos chore (Odoo + Postgres con un comando; upgrade = bump de imagen); la energía de aprendizaje va al uso de Odoo, no al install hell (wkhtmltopdf/deps). Decisión Ricardo: free o pago único → CE es $0, mejor que un pago único.

**Tracker:** `t-012` (reframed a "stand up Odoo CE", high, due 2026-06-15). Spec/plan completos vía `writing-plans` se escriben **en** la sesión de instalación, no antes.

**Pendiente al abrir la sesión de instalación:** confirmar versión Odoo (18 propuesto), Postgres 16, MagicDNS/hosts para `odoo.nexostrat.local`, y verificar HP encendido (atado a `t-weekend-desktop-on-decision`).

---

# Protocolo S2 (histórico) — Investigación Odoo vs Notion (decisión CRM)

**Fase del roadmap:** F6 del spec v2 (`00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md`)
**Task tracker:** `t-012` (tasks.json, auto-extraída del meeting 2026-05-28 07:05) + bloquea decisión pregunta (1) del doc `2026-05-27_preguntas-jp-pipeline-v2.md`
**Estado:** DRAFT
**Prerequisitos:** ninguno (Ricardo solo, no requiere JP en vivo — sí requiere su opinión al final)
**Tiempo estimado:** 1-2 h sesión

---

## Objetivo

Decidir formal y documentadamente **qué CRM adoptamos en Nexostrat**: Odoo (self-hosted, opción que Ricardo levantó en reunión 2026-05-28) o Notion (opción que JP propuso por flexibilidad visual + APIs IA). El output es un documento de decisión + actualización del spec v2 cerrando pregunta (1).

Esta decisión gobierna:
- Funnel CRM etapas (pregunta 9 del doc) — desbloquea esa pregunta a su vez
- Schema de la tabla `clients` en Baserow (Plan 02a) — puede haber que migrar
- Integración técnica con la propuesta de marketing-content-pipeline (un canal CRM nutre el otro)

## Contexto necesario al inicio

Leer:
1. `CHECKPOINT.md` (estándar)
2. `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` §3 pregunta (1) y §2.2 contexto
3. Resumen reunión 2026-05-28: `/srv/meetings/nexostrat/2026-05-28/2026-05-28_07-05_buyer-persona-trixx-logistic-pipeline/summary.md` § Discusión Técnica > Selección de CRM (3 líneas)
4. `00_META/proposals/2026-05-19_foss-stack-design.md` — el spec de Baserow ya decidido (state-store + CRM metadata) — ¿Odoo / Notion CRM lo reemplaza, complementa, o es input para una capa de presentación encima?
5. `00_META/plans/2026-05-19_plan-02a-foss-stack.md` § Baserow schema — qué tablas ya están planeadas, ver si colisionan

## Procedimientos paso por paso

### Paso 1 — Definir criterios de decisión

Antes de investigar, listar los criterios que pesan. Sugerencia inicial:

| Criterio | Peso | Por qué importa |
|---|---|---|
| Self-hosting (no SaaS de terceros) | alto | alineado con Plan 02a (Baserow, BookStack) — soberanía de datos |
| Costo recurrente | medio | Stage 1 budget cero firmware-side |
| Curva de aprendizaje (Ricardo + JP usabilidad) | alto | JP Light mode + Ricardo operador |
| Integración con LLMs / IA | alto | spec v2 §2 marketing-content-pipeline depende de esto |
| Funnel sales nativo | alto | propósito principal del CRM |
| Multi-canal entrada (WhatsApp / email / form) | medio | Pipeline v2 paso 1 captación |
| Coexistencia con Baserow | medio | NO duplicar state-store; CRM puede vivir encima de Baserow o reemplazar parcialmente |
| Mantenimiento operativo (upgrades, backups) | medio | Ricardo es DevOps solo |
| Extensibilidad (plugins comunidad) | bajo | Odoo gana acá, pero ¿lo necesitamos? |

Pesos confirmar al inicio de sesión con Ricardo (no asumir).

### Paso 2 — Investigación Odoo

Web research (vía WebFetch + WebSearch):

- **Versión community vs enterprise** — qué viene en community gratis (CRM + Sales + Mail + ?)
- **Self-hosting setup** — Docker compose? requisitos? upgrades?
- **APIs nativas** — REST? XML-RPC? Cómo conectar LLMs (DeepSeek, Claude)?
- **Funnel sales** — kanban etapas, automatizaciones disponibles, reportes
- **Integraciones canal entrada** — WhatsApp Business? email forwarding? formulario web?
- **Costos reales** — hosting (~$10-50 USD/mes según Cloudron/VPS?), backups, monitoreo
- **Casos reales PyME comparables** — buscar reviews honestos de Odoo en PyMEs <50 empleados

### Paso 3 — Investigación Notion

- **Free tier limits** — # bloques, # databases, multi-usuario gratis?
- **Notion API + Notion AI** — APIs para automatizaciones, costo Notion AI
- **CRM patterns nativos** — templates comunidad para CRM
- **Self-hosting** — NO existe oficial; ¿alternativas open-source compatibles (AppFlowy)?
- **Privacy / sovereignty** — su data en servidores Notion (vs Plan 02a soberanía)
- **Integración con Baserow** — ¿coexisten o redundantes?

### Paso 4 — Tabla comparativa

| Criterio | Peso | Odoo | Notion | Ganador |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Llenar honestamente. Sin sesgos hacia Odoo por ser self-hosted ni hacia Notion por ser conocido.

### Paso 5 — Test práctico mínimo (opcional pero recomendado)

Si el tiempo lo permite:
- Spin up Odoo Community en Docker local (1 contenedor, ~20 min)
- O abrir Notion gratis con template CRM (5 min)
- Crear 5 prospects ficticios (incluyendo Trixx como fila real) y simular el funnel:
  - Entrar al CRM
  - Mover a "Llamada agendada"
  - Mover a "Diagnóstico en producción"
  - Cerrar como "Ciclo 2 firmado" o "Perdido"
- Evaluar UX honesta

### Paso 6 — Decisión + documentación

Output canónico:
- `00_META/proposals/<YYYY-MM-DD>_crm-decision-odoo-vs-notion.md` con:
  - Criterios + pesos confirmados
  - Tabla comparativa completa
  - Test práctico resumen (si se hizo)
  - **DECISIÓN** explícita: Odoo / Notion / híbrido / status quo (carpetas+archivo)
  - Plan de migración si aplica
  - Costos esperados Stage 1 / Stage 2

### Paso 7 — Validación con JP (asíncrono)

Antes de cerrar la decisión "locked", mandar el doc a JP por Telegram + esperar OK o veto. Si no contesta en <48h, decisión Ricardo unilateral con nota.

### Paso 8 — Actualizar spec v2 + tasks

- `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` §2.2 pregunta (1): mover de PARCIAL → CERRADA con respuesta
- `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` §3: cerrar pregunta (1), eventualmente cerrar (9) funnel CRM etapas también
- Cerrar `t-012` en tasks.json
- Desbloquear F7 (Captación + seguimiento) en el roadmap si CRM era prerequisito

## Outputs esperados al cierre

1. `00_META/proposals/<YYYY-MM-DD>_crm-decision-odoo-vs-notion.md` — decisión documentada
2. `tasks.json` — `t-012` cerrado
3. `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` §2.2 + §3 actualizados
4. Si decisión = Odoo: opcional snapshot del docker-compose en `infra/odoo/docker-compose.yml` (placeholder, real install separado)
5. Journal entry estándar

## Criterios de éxito

- Decisión explícita (sin "depende")
- Honestidad sobre los costos reales de mantenimiento (incluyendo tiempo de Ricardo)
- Coherencia con Plan 02a Baserow (no duplicar state-store)
- JP firmó o se notó "decisión unilateral por no respuesta"

## Manejo de bloqueos

- **Investigación web devuelve info incoherente:** levantar handoff a Gemini para fresh search (Gemini bueno para info de instalaciones recientes que mi knowledge cutoff puede no cubrir).
- **Self-hosting Odoo resulta más caro que esperado:** evaluar opción híbrida (Notion para discovery + handoff manual a Baserow para post-pago).
- **JP propone una tercera opción:** evaluarla rápidamente contra los criterios; si pesa más, integrar a la tabla comparativa antes de cerrar.

## Memorias relevantes

- `project_no_notion` — Notion dropped a nivel firma 2026-05-15 (ADR-038). ESTE protocolo lo reabre porque JP lo propone para CRM (no para docs, que es lo que ADR-038 cerró). Documentar tensión + resolución explícitamente.
- `feedback_drop_n8n_entirely` — workflows Python+systemd; cualquier "automatización" en Odoo/Notion debe respetarlo (no traer n8n por la puerta de atrás).
- `feedback_do_it_right_do_it_once` — la decisión CRM se cierra una vez; cambiarla después tiene costo de migración.

---

**Al cerrar la sesión, actualizar este protocolo agregando un bloque al inicio:**

```
## EJECUTADO — YYYY-MM-DD
- Journal: 00_META/journal/YYYY-MM-DD_<topic>.md
- Decisión: Odoo / Notion / híbrido
- Output: 00_META/proposals/...
- Next: ...
```
