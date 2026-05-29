# CHECKPOINT — root (Founder)

**Updated:** 2026-05-29T14:00:00-07:00
**By:** ricardo (via Claude Code session 29)
**Persona:** Founder/Skills-Master (operator-driven; trabajo sustantivo en skills/ + operations/marketing/brand/)
**Session topic:** Ejecución del Plan Maestro de skills — **Fase 0 (fundación de marca única)** + **Fase 1 (base HTML vendorizada)**. Backup-correctas. Fase 2 (construir el trío) diferida a sesión dedicada.

## What just happened (last session — read once, don't re-litigate)

**Sesión 29 (2026-05-29).** Fases 0 y 1 del Plan Maestro.

1. **Gate despejado.** JP dio OK a "Inter en todo" (D3). `t-jp-inter-blessing` → done.
2. **Fase 0 — home de marca único = `operations/marketing/brand/`:**
   - Logos consolidados ahí (18 PNG). Borrada la copia byte-idéntica `operations/assets/brand/Logos` (`git rm --cached`). Las copias internas de `pptx_expert`/`nexostrat_editorial_designer` se dejan morir con su skill en Fase 3.
   - `brand-identity.md` canónico v2.0 (`operations/marketing/brand/brand-identity.md`): fusión de las 2 copias previas + Inter en todo + LatAm México→Colombia + Don Carlos + pricing fuera + voz calibrada (T1/T2/T4/T5/T7). **Es la fuente única que leerán el trío + Skill 6.**
   - `skills/shared/brand.py` + `reunion_andrea/build_andrea.py` repuntados a `operations/marketing/brand/logos`.
   - **Backup fix:** el home estaba gitignored; agregada excepción en `operations/marketing/.gitignore` → 19 archivos (brand-identity.md + 18 logos) ahora llegan a mirrors.
3. **Fase 1 — base HTML:** `skills/frontend_design/` = vendorizado verbatim de `frontend-design` (Apache 2.0) + `PROVENANCE.md`.

## Decisiones lockeadas (NO re-litigar)

- **D1-D7** del Plan Maestro siguen firmes (web expert HTML dedicado, marca única primero, Inter en todo, base HTML = frontend-design, autoría skill-creator + writing-skills, borrar editorial_designer/pptx_expert/docx_technical/pptx_technical en Fase 3, Skill 6 base JP + 6.A).
- **Sesión 29:** home = `operations/marketing/brand/`; geografía LatAm México→Colombia; pricing fuera del brand; emojis con propósito (P7); brand-identity v2.0 aprobado por Ricardo tal cual.

## Stack state (live & verifiable next session)

- **Fuente única de marca:** `operations/marketing/brand/brand-identity.md` (v2.0) + `operations/marketing/brand/logos/` (18 PNG, tracked). `skills/shared/brand.py` apunta ahí (`BRAND_FONT="Inter"`, `BRAND_FONT_MONO="JetBrains Mono"`; falta `SLATE_LIGHT` → `t-brandpy-slatelight`).
- **Brand guide visual:** `operations/assets/brand/Nexostrat_Brand_Guide.docx` (+ Logo_Kit.html) siguen ahí, tracked. (No se movieron al home; el canónico los referencia. Mover físico = polish opcional.)
- **Persona:** `operations/marketing/buyer_personas/Nexostrat_BuyerPersona_DonCarlos_Ricardo_2026-05-27.md` (México-primario).
- **Bases oficiales vendorizadas:** `skills/docx_technical/`, `skills/pptx_technical/`, **`skills/frontend_design/`** (nuevo).
- **Skills a absorber+borrar en Fase 3 (D6):** `skills/nexostrat_editorial_designer/`, `skills/pptx_expert/` (+ docx_technical/pptx_technical tras portar lo aplicable al trío).
- **Skill 6 base:** versión de JP en `skills/drive-download-20260529T184628Z-3-001.zip` (untracked; pricing + roadmap ya resueltos). pptx-expert del zip = regresión (descartar). editorial-designer del zip = idéntico.
- **Gold standard:** `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reunion_andrea/` (deck + cheat sheet + build_andrea.py).

## Open items (carried forward)

| ID | Subject | Priority | Due |
|---|---|---|---|
| `t-skills-trio-rebuild` | Plan Maestro — **Fase 2 next** (trío docx/pptx/html), luego Fase 3 (dedup) + Fase 4 (Skill 6/6.A) | high | 2026-06-15 |
| `t-skill6-apply-audit-findings` | Aplicar T1-T10 sobre Skill 6 de JP (Fase 4) | medium | 2026-06-15 |
| `t-brandpy-slatelight` | Portar `Slate Light #A5B4C1` + regla dark-bg a `brand.py` | low | 2026-06-15 |
| `t-install-brand-fonts-laptop` | Instalar fonts-inter + jetbrains-mono en ricardo-hp-laptop | high | 2026-05-30 |
| `t-fix-logo-kit-html-fonts` | Alinear Logo_Kit.html a Inter | low | 2026-07-15 |

**Heredadas relevantes (de CHECKPOINT 28/27):** `t-plan-04-description-update` (OVERDUE, high), `t-012` Odoo CE stand-up (high, 2026-06-15), `t-pre-push-hook-block-mirrors` (high), `t-plan-01b-execute-warm-standby`, `t-skill5-reprofile-body`, `t-trixx-reporte-iteracion-notas-ricardo` (high, 2026-05-31).

**Cerradas esta sesión:** `t-jp-inter-blessing` (done), `t-editorial-designer-fix-description` (cancelled — superseded por el canónico).

**Untracked a propósito al cierre (NO commitear sin pedir):**
- `skills/drive-download-20260529T184628Z-3-001.zip` — zip de JP (base de Skill 6, Fase 4).
- `pipeline/clients/trixx-logistics/transcripts/` — transcript Andrea (lo maneja Ricardo).

**Cross-scope:** Sin Gemini handoff. Sin memos. Sin cambios en `vault/`. CLAUDE/GEMINI/README NO editados (sin entry de CHANGELOG); sí editado `operations/marketing/.gitignore`.

## What next session opens onto

**Most likely:** Ricardo abre la sesión de **Fase 2** (construir el trío). Usar el prompt en `pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/PROMPT_proxima_sesion.md`. Orden sugerido: 2a (pptx) → 2b (docx) → 2c (html). Cada experto: leer SOLO `operations/marketing/brand/brand-identity.md` como fuente de marca, conocer a Don Carlos, validar render real contra el gold standard de Andrea.

> **Recomendación al próximo Claude:** leer este CHECKPOINT + STATUS + journal `2026-05-29_fase0-fase1-brand-foundation-html-base.md` + el plan maestro + el `brand-identity.md` canónico. Fases 0-1 hechas: NO re-litigar marca/logos/Inter. Estudiar el gold standard de Andrea antes de construir el HTML. El `00_nexostrat_html` debe override la prohibición de Inter del base frontend-design. NO ejecutar borrados de skills (D6/Fase 3) sin confirmación explícita de Ricardo.
