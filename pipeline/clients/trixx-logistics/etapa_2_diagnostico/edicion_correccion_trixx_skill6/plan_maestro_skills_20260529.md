# Plan Maestro — Reconstrucción de skills de marca (docx / pptx / html) + Skill 6

> **Sesión:** 2026-05-29 | **Autor:** Claude (Founder) con Ricardo | **Para:** Ricardo + JP
> **Supersede:** `plan_auditoria_skills_20260529.md` (v1, solo auditoría).
> **Gold standard de referencia:** el deck + cheat sheet de Andrea (`reunion_andrea/`, HTML hecho a mano). A ese nivel apuntamos, pero **reproducible** vía skills.
> **Filosofía:** entender antes de ejecutar; una sola fuente de marca; validar cada skill contra el gold standard antes de avanzar.

---

## 0. Idea central

Dejar de "parchar" y **reconstruir tres expertos especializados** — uno por formato — cada uno montado sobre la base oficial de Anthropic + la inteligencia de marca de Nexostrat:

```
  00_nexostrat_docx   = docx oficial (Anthropic)        + lo relevante de editorial_designer
  00_nexostrat_pptx   = pptx oficial (Anthropic)        + lo relevante de pptx_expert
  00_nexostrat_html   = frontend-design (Anthropic)     + patrones gold-standard (Andrea)   ← el más completo
```

Luego Skill 6 (y una variante 6.A) consumen el trío. Todos leen **una sola** fuente de marca (logos, paleta, fuente, voz, persona).

---

## 1. Decisiones tomadas (2026-05-29)

| # | Decisión | Detalle |
|---|---|---|
| D1 | **Web expert dedicado** | Se crea `00_nexostrat_html`, dueño de TODO el HTML premium (documento-HTML + presentación-HTML). |
| D2 | **Fuente de marca única, primero** | Consolidar antes de construir nada (Fase 0). |
| D3 | **Tipografía: Inter en todo** | docs, pptx y web en Inter. Reemplaza Century Gothic (no está en Linux; rompía la marca). *Sujeto a visto bueno de JP por ser decisión de marca.* |
| D4 | **Base HTML = frontend-design** | Plugin oficial de Anthropic (no existe un skill "html" estilo docx/pptx). |
| D5 | **Autoría de skills: ambos + síntesis** | Correr `skill-creator` (oficial) y `writing-skills` (superpowers) y fusionar lo mejor. |
| D6 | **Dedup: borrar los viejos** | Tras absorberse, eliminar `editorial_designer`, `pptx_expert`, `docx_technical`, `pptx_technical` (git conserva historial). |
| D7 | **Skill 6: base JP + 6.A** | 6 = versión de JP (pricing/roadmap ya resueltos) + nuestros cambios, con su enfoque de presentación. 6.A = variante gold-standard. Dos puntos de comparación. |

**Pendientes de decidir (no bloquean el arranque):**
- Integración Skill 6 ↔ trío: scripts deterministas vs flujo Claude-driven vs híbrido (parcialmente resuelto por el par 6 / 6.A). Confirmar con JP.
- Home de marca único: `operations/assets/brand/` vs `operations/marketing/brand/` (hoy partido). Propuesta: consolidar en `operations/marketing/brand/`.
- Mecanismo exacto de "instalar" un skill en Claude Code (verificar que cargan/activan).

---

## 2. Estado de partida (hallazgos verificados)

- **Oficiales docx + pptx YA vendorizados:** `skills/docx_technical/`, `skills/pptx_technical/` (SKILL.md + LICENSE + scripts). El paso "descargar" solo aplica a HTML.
- **No hay skill HTML oficial** estilo docx/pptx → base = `frontend-design`.
- **Logos: 4 copias** (operations/marketing/brand/logos, operations/assets/brand/Logos, + copia interna en cada skill). Consolidar en `operations/marketing/brand/logos`.
- **buyer_persona Don Carlos** disponible en `operations/marketing/buyer_personas/` (.md + 2 .docx; ignorar el .mp4 de 34 MB).
- **Brand guide:** `operations/assets/brand/Nexostrat_Brand_Guide.docx`.
- **Skill 6 de JP** ya resolvió T3 (pricing 3K/8K/15K + "depende del alcance") y B1 (sin total de roadmap). Nuestra auditoría de Skill 6 se reduce a: T1, T2, T4, T5, emojis, logos/marca, cheat sheet, T10 (nombre), calidad HTML.
- **pptx del zip = regresión** (Century Gothic vs Inter del repo). No adoptar; el repo manda. Con D3 (Inter) el punto queda zanjado.

---

## 3. Assets canónicos que los skills referencian (sin copiar)

| Asset | Ruta canónica |
|---|---|
| Logos | `operations/marketing/brand/logos/` (única, tras dedup) |
| Brand guide | `operations/assets/brand/Nexostrat_Brand_Guide.docx` |
| Buyer persona | `operations/marketing/buyer_personas/Nexostrat_BuyerPersona_DonCarlos_*` |
| Reglas de marca (machine-readable) | UN `brand-identity.md` canónico (consolidar en Fase 0; propuesta: `operations/marketing/brand/`) |

---

## 4. Fases

### Fase 0 — Fundación de marca única (prerrequisito)
- Consolidar **logos** en `operations/marketing/brand/logos`; borrar las otras 3 copias; actualizar `skills/shared/brand.py` para apuntar ahí.
- Consolidar **un `brand-identity.md` canónico** (Inter en todo, paleta Aurora, reglas Amber, voz). Derivar del mejor existente + brand guide.
- Fijar referencias a **brand guide** + **persona Don Carlos**.

### Fase 1 — Obtener base HTML
- Descargar el oficial **frontend-design** (no instalar aún). Vendorizar como base del experto HTML (paralelo a docx_technical/pptx_technical).

### Fase 2 — Construir el trío (con `skill-creator` + `writing-skills`, sintetizando)
- **2a) PPTX → `00_nexostrat_pptx`.** Auditar oficial `pptx` (vendorizado) vs `pptx_expert`; portar del oficial lo aplicable. Conservar la capa **estratégica/narrativa** de pptx_expert y la **plantilla** + reference. Inter (no la regresión Century Gothic).
- **2b) DOCX → `00_nexostrat_docx`.** Comparar oficial `docx` vs `editorial_designer`; llevar lo relevante de editorial_designer al oficial → experto exclusivo de docx.
- **2c) HTML → `00_nexostrat_html`.** Igual con frontend-design. **El más completo:** hace diseños HTML propios + integra/implementa diseños de los otros dos skills. Encodea los patrones del gold standard de Andrea (motor de slides, scroll, tokens de marca, responsive, logos base64, link privado, QR).
- Cada skill: referencia assets canónicos (Fase 3), Inter, y **conoce a Don Carlos** (mensajes enfocados al persona).

### Fase 3 — Nombrado, wiring y dedup
- Nombrar con prefijo `00_`: `00_nexostrat_docx`, `00_nexostrat_pptx`, `00_nexostrat_html`.
- Referenciar logos/persona/brand guide canónicos (no copiar logos dentro de cada skill).
- **Borrar** (D6): `editorial_designer`, `pptx_expert`, `docx_technical`, `pptx_technical`.
- Verificar compatibilidad **Linux** (binarios + módulos Python + `npm`); eliminar archivos repetidos; limpiar `__pycache__`; optimizar espacio/memoria.

### Fase 4 — Skill 6 + 6.A
- **Skill 6:** base = versión de JP + nuestros cambios pendientes (T1, T2, T4, T5, emojis, logos/marca, cheat sheet, T10, calidad HTML). Mantiene el enfoque de presentación de JP. Cableado a `00_nexostrat_{docx,pptx,html}`.
- **Skill 6.A:** variante que produce al **estándar gold** (HTML-first, calidad Andrea, cheat sheet como entregable). Segundo punto de comparación.
- Ambos: acceso al trío.

### Cross-cutting (toda fase)
- **Instalar** todos los skills (activarlos en Claude Code) y verificar que cargan.
- **Linux:** probar render real end-to-end, no solo "existe el script".
- **Dedup / espacio:** sin logos ni reglas de marca duplicadas; node_modules y __pycache__ controlados.
- **Validación / muestra-patrón:** tras cada skill y tras 6 vs 6.A, correr sobre input conocido (datos de prueba de Skill 6, o Trixx) y comparar contra el gold standard.

---

## 5. Secuencia y dependencias

```
Fase 0 (marca única)
  └─► Fase 1 (base HTML)
        └─► Fase 2a/2b/2c (trío)  ──validación por skill──►
              └─► Fase 3 (nombrado + wiring + dedup + Linux)
                    └─► Fase 4 (Skill 6 + 6.A)  ──validación 6 vs 6.A vs gold──►
```

Regla: no se construye el trío sin la marca única (Fase 0); no se toca Skill 6 sin el trío validado (Fase 3).

---

## 6. Insumos relacionados
- Auditoría detallada de Skill 6 (hallazgos T1-T10 + B/C/D/E/F/H): `auditoria_skill6_trixx_20260529.md` → alimenta la Fase 4.
- Gold standard: `reunion_andrea/` (deck + cheat sheet + build_andrea.py).
- Versiones entrantes (zip de JP) extraídas en staging: `/tmp/skills_incoming_20260529/` (client-deliverables nueva = base de Skill 6; pptx-expert = regresión, descartada; editorial-designer = idéntica).
