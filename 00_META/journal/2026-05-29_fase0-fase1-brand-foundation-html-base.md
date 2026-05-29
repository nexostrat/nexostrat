# Sesión 29 — Plan Maestro de skills: Fase 0 (marca única) + Fase 1 (base HTML)

**Fecha:** 2026-05-29 (tarde) · **Persona:** Founder/Skills-Master (operator-driven, Ricardo) · **Tema:** ejecución de las Fases 0 y 1 del Plan Maestro de reconstrucción de skills.

## Contexto

Sesión de ejecución del Plan Maestro committeado en la sesión 28 (`pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/plan_maestro_skills_20260529.md`). Arranqué leyendo el plan, la auditoría del Skill 6 y el gold standard de Andrea. Verifiqué el gate de Fase 0 (OK de JP a "Inter en todo"): no estaba registrado en ningún artefacto; lo confirmó Ricardo en sesión. Decisiones de la sesión tomadas vía AskUserQuestion.

## Fase 0 — fundación de marca única

**Home elegido:** `operations/marketing/brand/` (decisión de Ricardo; el plan lo proponía).

1. **Logos.** Verifiqué con `diff -rq` que las 4 copias son byte-idénticas (18 PNG c/u). Mapeé todas las referencias de código: solo 2 apuntaban a la copia a borrar — `skills/shared/brand.py:54` y `reunion_andrea/build_andrea.py:16`. Repunté ambas a `operations/marketing/brand/logos` y verifiqué que los logos resuelven. Borré `operations/assets/brand/Logos` (los 18 PNG seguían en HEAD; quité solo del working tree con `rm`, luego `git rm --cached` para finalizar el dedup en índice → recuperables). Las copias internas de `pptx_expert` y `nexostrat_editorial_designer` NO las toqué: esos skills mueren en Fase 3 (D6) y referencian su copia local vía `{skill_dir}/assets/logos`; borrarlas ahora los rompería.

2. **`brand-identity.md` canónico v2.0** (`operations/marketing/brand/brand-identity.md`). Fusioné las 2 copias previas (la de `editorial_designer` v1.0 = base con cobertura completa; la de `pptx_expert` v1.1 aportó Inter-unificado + `Slate Light #A5B4C1` + regla de contraste dark-bg). Apliqué lo locked y los hallazgos de auditoría:
   - **Inter** en docs/pptx/web (un solo sistema tipográfico); Century Gothic eliminado.
   - **Geografía LatAm México→Colombia** (la persona Don Carlos es México-primario Tijuana cross-border / Colombia secundario; el brand viejo decía "Colombia, nunca mencionar México" — al revés). Cierra el espíritu de `t-editorial-designer-fix-description`.
   - **Pricing fuera del brand** (lo posee Skill 6, modelo 3K/8K/15K) — evita dos fuentes de precio.
   - **Don Carlos** como audiencia objetivo: referencia al archivo + tabla de 12 dimensiones + nota de riesgo de track record (Nota 2 del formulario).
   - **Voz** calibrada con T1 (calibrar a lo que sabemos), T2 (IA fuera de títulos), T4 (no reemplazamos, liberamos), T5 (sin "robot"), T7 (emojis con propósito; nota de que el chat sigue sin emojis).

3. **Backup fix (side-finding).** Al verificar git status descubrí que `operations/marketing/brand/` estaba 100% gitignored (`operations/marketing/.gitignore` con `*` + excepciones solo para `website-intro/`, `buyer_personas/`, README). Es decir: los logos canónicos + el brand-identity.md nuevo NO llegaban a Gitea/GitHub/Codeberg, y yo acababa de borrar la única copia rastreada (`assets/brand/Logos`). Lo presenté a Ricardo; eligió la opción de agregar excepción al `.gitignore` (mismo patrón y rationale que buyer_personas/tv-loop: "artefactos canónicos de marca, en git para sobrevivir pérdida de disco + alinearse entre mirrors"). `git add --dry-run` confirma 19 archivos ahora rastreables (brand-identity.md + 18 logos, 432 KB).

## Fase 1 — base HTML

Vendoricé el plugin oficial de Anthropic `frontend-design` a `skills/frontend_design/`:
- `SKILL.md` + `LICENSE.txt` (Apache 2.0) copiados **verbatim** (verificado byte-idéntico con `diff -q`).
- `PROVENANCE.md` con origen, versión (plugin.json no declara `version`), fecha, "sin modificaciones", y la **tensión a resolver en Fase 2**: el SKILL.md oficial instruye explícitamente *"Avoid generic fonts like Arial and Inter"* / *"NEVER use ... Inter"* — choca con la marca (D3). El experto `00_nexostrat_html` debe override esa guía (Inter es elección deliberada de marca, no default genérico), conservando del oficial el rigor de diseño.

## Decisiones (AskUserQuestion)

- Gate Inter: JP dio OK → procedo.
- Home de marca: `operations/marketing/brand/`.
- Geografía: LatAm México→Colombia.
- Pricing: fuera del brand (lo posee Skill 6).
- Emojis (P7): con propósito (no cero).
- Backup: excepción .gitignore en marketing/brand.
- `t-editorial-designer-fix-description`: cerrar como superseded.

## Estado al cierre

Fases 0 y 1 completas y backup-correctas. **Commit de milestone 0+1** al cierre (no antes). Siguiente: Fase 2 (construir el trío `00_nexostrat_{docx,pptx,html}` con skill-creator + writing-skills, validando contra el gold standard de Andrea). Prompt de arranque actualizado en `edicion_correccion_trixx_skill6/PROMPT_proxima_sesion.md`.

**Flags para Fase 2+:** (1) `00_nexostrat_html` override de la prohibición de Inter; (2) en la instalación de skills (cross-cutting) ojo con colisión de nombres (`frontend_design` tiene `name: frontend-design`, igual que el plugin instalado — análogo a docx_technical/pptx_technical que conservan `name: docx`/`pptx`); (3) `Slate Light` aún no está en `brand.py` (`t-brandpy-slatelight`, low).

**Untracked a propósito:** `skills/drive-download-...zip` (zip JP, input transitorio), `pipeline/clients/trixx-logistics/transcripts/` (transcript Andrea, lo maneja Ricardo).
