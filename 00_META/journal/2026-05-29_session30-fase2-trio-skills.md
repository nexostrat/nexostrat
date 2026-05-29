# Session 30 — Plan Maestro de skills, Fase 2: el trío de formato

**Fecha:** 2026-05-29 (tercera sesión del día; sigue a la 28 [auditoría + gold standard + plan maestro] y la 29 [Fase 0 marca única + Fase 1 base HTML]).
**Persona:** Skills-Master (trabajo en `skills/`), operator-driven (Ricardo).
**Topic:** Construir el trío de expertos de formato `00_nexostrat_{pptx,docx,html}` sobre las bases oficiales de Anthropic + la marca única, validando cada uno con render real contra el gold standard de Andrea.

## Qué se hizo

Ejecutada la **Fase 2 completa** del Plan Maestro (`plan_maestro_skills_20260529.md`). Tres expertos nuevos, cada uno self-contained, leyendo UNA sola fuente de marca (`operations/marketing/brand/brand-identity.md`) y resolviendo logos desde `operations/marketing/brand/logos` (nunca bundleados).

### Decisiones de arquitectura (confirmadas por Ricardo vía AskUserQuestion)
- **Motor HTML = ambos:** generador reutilizable + guía rica.
- **Toolchain OOXML = self-contained por skill:** docx y pptx copian cada uno `office/` + 39 schemas XSD (byte-idénticos entre ambos). Sobreviven el borrado de las bases en Fase 3.
- **Validación = muestra representativa + QA visual** contra `brand-identity.md` (no hay gold standard hecho a mano para pptx/docx; el de Andrea es HTML-only).

### 2a — `skills/00_nexostrat_pptx` (name: `nexostrat-pptx`)
- Base técnica oficial copiada de `pptx_technical` (scripts/office/schemas + `pptxgenjs.md` + `editing.md` + LICENSE + QA).
- Capa estratégica de `pptx_expert` absorbida: 12 tipos de slide, grid con correcciones de JP, briefing, 3 workflows, doble-revisión, helpers de logo, tagline → conservados en `references/nexostrat-template-reference.md` + `assets/Nexostrat_Template.pptx`.
- Descartada su copia obsoleta de `brand-identity.md` (Colombia-only, pricing dentro). El SKILL.md fusionado apunta al canónico, suma voz calibrada (T1/T4/T5) y Don Carlos.
- Logos: `findBrandLogos()` resuelve la ruta canónica desde la raíz del repo (patrón `build_andrea.py`).
- **Validado:** deck muestra PptxGenJS → soffice PDF → imágenes. Portada, contenido+bullets, KPIs (Amber sobre Midnight), cierre/CTA. Inter, Aurora, logos correctos, voz calibrada.

### 2b — `skills/00_nexostrat_docx` (name: `nexostrat-docx`)
- Base técnica oficial copiada de `docx_technical` (scripts/office/schemas + LICENSE; el SKILL técnico oficial preservado verbatim como `references/docx-technical.md`).
- Capa editorial de `nexostrat_editorial_designer` absorbida: filosofía, workflow, checklist, `design-specs.md`, `cover-designs.md`.
- **Regresión corregida:** Century Gothic → Inter en todas las referencias (D3).
- **Hallazgo no obvio:** Inter en este Linux es solo OTF/CFF y reportlab embebe solo TrueType. Resuelto: el `.docx` (docx-js, Inter por nombre vía LibreOffice) es el entregable primario; reportlab queda como referencia con `fc-match` + fallback a Helvetica y salvedad documentada; las portadas premium las cubre `00_nexostrat_html`.
- **Validado:** .docx docx-js → soffice PDF → imágenes. Portada full-bleed Midnight + logo + tagline; cuerpo **justificado** (T8); callout barra Sky; **bullets reales y completos — el bug de truncado D-2 no reaparece**; tabla Midnight/alternas; dato Amber único con fuente; header con logo + línea Sky; footer con paginación.

### 2c — `skills/00_nexostrat_html` (name: `nexostrat-html`)
- Obra derivada de `frontend_design` (Apache 2.0). `PROVENANCE.md` con la nota de cambio §4(b); guía base preservada verbatim en `references/frontend-design-base.md`.
- **Override consciente:** Inter + paleta Aurora son elección deliberada de marca; anula el "avoid Inter / distinctive colors" del base (documentado en SKILL.md y PROVENANCE).
- **Motor `assets/build_nexostrat_html.py`:** generaliza el gold standard `build_andrea.py` — tokens Aurora en `:root`, Inter, motor de slides vanilla-JS (translateX 100vw, cubic-bezier .55s, teclado+dots+botones+progreso), responsive `clamp()` + breakpoint 860px, logos base64, `qr_datauri()` (QR F2), constructores de slide + `build_deck` + `build_cheatsheet`. Exemplars `deck_example.html` + `cheatsheet_example.html` (vara de calidad).
- `references/gold-standard-patterns.md` documenta los patrones encodables con snippets.
- **Validado** en Chrome headless real (servido por http; `file://` bloqueado): portada, slide de oportunidades (g5 + strip Emerald), cierre con **2 QR**, y cheat sheet con advertencias (caja roja) **antes** del guion. Navegación por teclado funciona, Inter carga.

## Interacción con Ricardo
- Mid-sesión pidió **QR más grandes** → `.qr img` 118px → 150px, regenerado y verificado.

## Estado al cierre
- Los 5 skills viejos (`pptx_expert`, `nexostrat_editorial_designer`, `docx_technical`, `pptx_technical`, `frontend_design`) **siguen intactos**. Cero borrados (eso es Fase 3, requiere OK explícito de Ricardo — nueva tarea `t-skills-trio-fase3`).
- Verificado: cero copias de `brand-identity.md` y cero logos bundleados dentro del trío.
- Tasks: `t-install-brand-fonts-laptop` cerrada (Inter + JetBrains Mono confirmadas en la laptop); `t-skills-trio-rebuild` actualizada (Fase 2 done); `t-skills-trio-fase3` creada (high, 2026-06-15).
- Deps de render (pptxgenjs, docx, markitdown, qrcode) instaladas en `/tmp/nexo_render_2a` (venv) — NO tocan el repo.
- Sin Gemini handoff. Sin memos. Sin cambios en `vault/`. CLAUDE/GEMINI/README no editados (sin entry de CHANGELOG).
- Untracked a propósito (sin commitear): zip de JP (`skills/drive-download-...zip`, base de Fase 4) y `pipeline/clients/trixx-logistics/transcripts/.../video.mkv` (lo maneja Ricardo).

## Siguiente
Fase 3: instalar/activar el trío en Claude Code (symlinks en `.claude/skills/`) + dedup de los 4 viejos (con OK de Ricardo) + actualizar `test_skills.sh` e índices. Luego Fase 4 (aplicar auditoría T1-T10 sobre Skill 6 + variante 6.A).
</content>
