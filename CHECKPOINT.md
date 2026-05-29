# CHECKPOINT — root (Founder)

**Updated:** 2026-05-29T15:45:00-07:00
**By:** ricardo (via Claude Code session 30)
**Persona:** Founder/Skills-Master (operator-driven; trabajo sustantivo en skills/)
**Session topic:** Plan Maestro de skills — **Fase 2 (construir el trío de formato `00_nexostrat_{pptx,docx,html}`)**. Completa y validada con render real end-to-end.

## What just happened (last session — read once, don't re-litigate)

**Sesión 30 (2026-05-29).** Fase 2 del Plan Maestro: el trío de expertos de formato.

1. **Tres skills nuevos**, cada uno self-contained, leyendo UNA sola fuente de marca (`operations/marketing/brand/brand-identity.md`) y resolviendo logos desde `operations/marketing/brand/logos` (nunca bundleados):
   - **`skills/00_nexostrat_pptx`** (name `nexostrat-pptx`): base oficial `pptx_technical` + capa estratégica de `pptx_expert` (12 slides, grid con correcciones JP, plantilla `assets/Nexostrat_Template.pptx`, `references/nexostrat-template-reference.md`). SKILL.md fusionado con voz calibrada + Don Carlos; descartada la brand-identity.md vieja.
   - **`skills/00_nexostrat_docx`** (name `nexostrat-docx`): base oficial `docx_technical` (SKILL técnico → `references/docx-technical.md`) + editorial `design-specs.md`/`cover-designs.md`. Century Gothic→Inter. docx-js = entregable primario; reportlab referencia con salvedad (Inter en Linux es solo OTF/CFF; reportlab solo embebe TrueType → fallback Helvetica).
   - **`skills/00_nexostrat_html`** (name `nexostrat-html`): derivada de `frontend_design` (Apache 2.0, `PROVENANCE.md` §4(b)). Motor `assets/build_nexostrat_html.py` (generaliza `build_andrea.py`: tokens Aurora, motor de slides vanilla-JS, responsive, logos base64, QR F2) + exemplars `deck_example.html`/`cheatsheet_example.html` + `references/gold-standard-patterns.md`. Override consciente de la prohibición de Inter del base.
2. **Validación real end-to-end** (no solo "existe el script"): pptx → soffice PDF → imágenes; docx → soffice PDF → imágenes; html → Chrome headless real. Todo on-brand (Inter, Aurora, logos correctos, voz calibrada). QR del cierre HTML agrandado a 150px a pedido de Ricardo.

## Decisiones lockeadas (NO re-litigar)

- **D1-D7** del Plan Maestro firmes.
- **Sesión 30 (arquitectura, confirmadas por Ricardo):** motor HTML = **generador + guía rica**; toolchain OOXML **self-contained por skill** (docx y pptx copian `office/` + 39 schemas c/u); validación = **muestra representativa + QA visual** contra `brand-identity.md` (no hay gold standard hecho a mano para pptx/docx; el de Andrea es HTML-only).

## Stack state (live & verifiable next session)

- **El trío:** `skills/00_nexostrat_{pptx,docx,html}/` (commiteado esta sesión). Cero copias de `brand-identity.md` y cero logos bundleados dentro (verificado).
- **Los 5 skills viejos siguen INTACTOS:** `skills/pptx_expert`, `skills/nexostrat_editorial_designer`, `skills/docx_technical`, `skills/pptx_technical`, `skills/frontend_design`. Cero borrados — eso es Fase 3.
- **Fuente única de marca:** `operations/marketing/brand/brand-identity.md` (v2.0) + `operations/marketing/brand/logos/` (18 PNG). `skills/shared/brand.py` apunta ahí.
- **Fonts:** Inter + JetBrains Mono instaladas en la laptop (verificado fc-match). Inter solo como OTF/CFF.
- **Skill 6 base (Fase 4):** zip de JP `skills/drive-download-20260529T184628Z-3-001.zip` (untracked a propósito).
- **Gold standard:** `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reunion_andrea/`.
- **Deps de render** (pptxgenjs, docx, markitdown, qrcode) en `/tmp/nexo_render_2a` (venv) — efímeras, NO en el repo.

## Open items (carried forward)

| ID | Subject | Priority | Due |
|---|---|---|---|
| `t-skills-trio-fase3` | **Fase 3 next:** instalar/activar el trío en Claude Code + dedup de los 4 viejos (requiere OK explícito) + test_skills.sh | high | 2026-06-15 |
| `t-skills-trio-rebuild` | Paraguas del Plan Maestro (Fase 2 done; Fase 3+4 pendientes) | high | 2026-06-15 |
| `t-skill6-apply-audit-findings` | Fase 4 — aplicar T1-T10 sobre Skill 6 de JP + variante 6.A | medium | 2026-06-15 |
| `t-brandpy-slatelight` | Portar `Slate Light #A5B4C1` + regla dark-bg a `brand.py` | low | 2026-06-15 |
| `t-fix-logo-kit-html-fonts` | Alinear Logo_Kit.html a Inter | low | 2026-07-15 |

**Heredadas relevantes:** `t-plan-04-description-update` (OVERDUE, high), `t-012` Odoo CE stand-up (high, 2026-06-15), `t-pre-push-hook-block-mirrors` (high), `t-plan-01b-execute-warm-standby`, `t-skill5-reprofile-body`, `t-trixx-reporte-iteracion-notas-ricardo` (high, 2026-05-31).

**Cerradas esta sesión:** `t-install-brand-fonts-laptop` (done — fonts confirmadas en la laptop).

**Untracked a propósito (NO commitear sin pedir):**
- `skills/drive-download-20260529T184628Z-3-001.zip` — zip de JP (base de Skill 6, Fase 4).
- `pipeline/clients/trixx-logistics/transcripts/.../video.mkv` — lo maneja Ricardo.

**Cross-scope:** Sin Gemini handoff. Sin memos. Sin cambios en `vault/`. CLAUDE/GEMINI/README NO editados (sin entry de CHANGELOG).

## What next session opens onto

**Most likely: Fase 3.** (1) Instalar/activar `skills/00_nexostrat_{pptx,docx,html}` en Claude Code (symlinks en `.claude/skills/` como las skills 01-06) y verificar que cargan. (2) Con OK explícito de Ricardo, **borrar** los 4 skills viejos (`nexostrat_editorial_designer`, `pptx_expert`, `docx_technical`, `pptx_technical`) — git conserva historial. (3) Actualizar `infra/scripts/test_skills.sh` (registry + smoke) e índices `skills/README.md`. (4) Limpiar `__pycache__`/`node_modules`. Luego **Fase 4** (Skill 6 + 6.A con la auditoría T1-T10).

> **Recomendación al próximo Claude:** leer este CHECKPOINT + STATUS + journal `2026-05-29_session30-fase2-trio-skills.md` + el plan maestro. Fase 2 hecha y validada: NO re-construir el trío. NO borrar skills viejos sin OK explícito de Ricardo. Antes de borrar, instalar/activar el trío y confirmar que activa correctamente.
</content>
