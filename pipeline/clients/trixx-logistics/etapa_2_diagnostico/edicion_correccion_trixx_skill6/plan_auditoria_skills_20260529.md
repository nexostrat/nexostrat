# Plan de Auditoría — Skills de soporte de marca + Skill 6

> **Sesión:** 2026-05-29 | **Autor:** Claude (Founder) con Ricardo | **Para:** Ricardo + JP
> **Disparador:** el deck + cheat sheet de Andrea (hechos a mano hoy) son el *gold standard*. Queremos que Skill 6 + los skills de soporte alcancen ese nivel de forma reproducible.
> **Principio rector:** entender el *porqué* antes de ejecutar. Primero auditamos (entender), después implementamos (sesión aparte). No se toca código de skills hasta cerrar las auditorías.

---

## 0. Objetivo y alcance

Auditar los skills que producen o gobiernan la identidad visual de los entregables, y dejar claro **cómo Skill 6 debe usarlos** para que cada documento salga on-brand (logos, colores, fuentes correctos) sin trabajo manual.

**Orden de trabajo (este plan):**
1. Auditar los dos motores técnicos: `docx`, `pptx`.
2. Auditar las dos capas de marca: `nexostrat_editorial_designer`, `pptx_expert`.
3. Resolver la pregunta de integración (§4) — cómo Skill 6 "usa" estos skills.
4. Auditar Skill 6 a la luz de todo lo anterior.
5. (Sesión posterior) Implementar los cambios.

**Entregable de cada auditoría:** un `.md` con el formato ya probado — *lo que funciona / lo que no funciona / acción sugerida* — etiquetado [SKILL]/[LINUX]/[MARCA]/[INTEGRACIÓN].

---

## 1. Mapa de arquitectura (qué es cada skill y para qué sirve)

| Skill | Tipo | Rol | Motor | Ubicación | Dependencias |
|---|---|---|---|---|---|
| `docx` | Técnico (Anthropic) | Crear / editar / leer .docx | docx-js (Node), pandoc, LibreOffice | `~/.grok/skills/docx` (fuera del repo) | node/npm, pandoc, soffice, poppler |
| `pptx` | Técnico (Anthropic) | Crear / editar / leer .pptx | PptxGenJS (Node), markitdown, LibreOffice | `~/.grok/skills/pptx` (fuera del repo) | node/npm, markitdown, soffice |
| `nexostrat_editorial_designer` | Marca (Nexostrat) | "Emplatar" contenido como documento on-brand | Usa el skill `docx` | `skills/nexostrat_editorial_designer/` | docx skill, brand-identity.md, assets/logos |
| `pptx_expert` | Marca + estrategia (Nexostrat) | Diseño/narrativa de decks on-brand | Usa el skill `pptx` | `skills/pptx_expert/` | pptx skill, plantilla .pptx, brand-identity.md, assets/logos |
| `06_client_deliverables` (Skill 6) | Orquestador | Genera los 6 entregables del Ciclo 1 | Sus propios generadores `generate_*.js/.py` | `skills/06_client_deliverables/` | docx-js, brand.py (solo docx) |

**Flujo previsto (al que queremos llegar):**

```
                 ┌─ editorial_designer ──► docx  ──►  DOCX on-brand
   Skill 6 ──────┤
                 └─ pptx_expert ─────────► pptx  ──►  PPTX on-brand
                         ▲
              (todos leen UNA fuente de marca: logos + paleta + fuentes)
```

**Estado actual:** Skill 6 NO llama a editorial_designer ni a pptx_expert. Sus generadores reimplementan la marca por su cuenta (y a medias). De ahí los hallazgos de la auditoría del run Trixx (T1-T10).

---

## 2. Criterios transversales de auditoría (aplican a todos los skills)

Derivados de lo conversado en esta sesión:

- **C1 — Logos correctos y de una sola fuente.** Cada skill debe usar el logo real correcto por fondo (claro/oscuro/mono). Hoy hay **tres copias** de los logos (editorial_designer/assets, pptx_expert/assets, y la canónica `operations/assets/brand/Logos/`). Riesgo de drift. Decidir: ¿una sola fuente referenciada, o copias sincronizadas con check?
- **C2 — Paleta Aurora exacta.** Hex correctos, regla Amber Gold (solo stats/CTA), combinaciones prohibidas respetadas. Verificar que todas las fuentes de marca coincidan al hex.
- **C3 — Fuentes correctas por canal y disponibles en Linux.** Docs = Century Gothic; web = Inter; pptx = Inter. **Century Gothic probablemente NO está instalada en Linux** → LibreOffice sustituye y rompe la marca. Verificar instalación o definir alternativa libre equivalente (p. ej. una geométrica libre) y fijarla.
- **C4 — Linux-readiness end-to-end.** El skill corre completo en esta máquina (binarios + módulos Python como markitdown + `npm install` de docx/pptxgenjs + thumbnails vía LibreOffice). Probar un render real, no solo "existe el script".
- **C5 — Una sola fuente de verdad de marca.** Hoy la marca vive en: `skills/shared/brand.py`, `editorial_designer/references/brand-identity.md`, `pptx_expert/references/brand-identity.md`, `operations/assets/brand/Nexostrat_Brand_Guide.docx`, `Nexostrat_Logo_Kit.html`. Eso es drift garantizado. Definir la canónica y que el resto derive de ella.

---

## 3. Auditoría por skill (qué revisar específicamente)

### 3.1 `docx` (motor técnico)
- **Qué es:** motor para crear/editar/leer .docx (docx-js + unpack/pack XML + pandoc/LibreOffice).
- **Revisar:** corre en Linux (scripts/office: unpack, pack, validate, soffice; convertir a PDF/imagen); que `npm install -g docx` o local funcione; defaults genéricos (Arial/negro) — confirmar que nunca se use crudo para entregables (la marca va encima).
- **Pregunta de integración:** es un *prompt-skill* (instrucciones para Claude), no una librería llamable. ¿Cómo lo consume Skill 6? (ver §4).

### 3.2 `pptx` (motor técnico)
- **Qué es:** motor para crear/editar/leer .pptx (PptxGenJS + unpack/pack + markitdown + thumbnails).
- **Revisar:** `markitdown` instalado; thumbnails vía LibreOffice; PptxGenJS instalable; paletas genéricas que trae NO deben filtrarse a entregables Nexostrat.

### 3.3 `nexostrat_editorial_designer` (capa de marca — documentos)
- **Revisar:**
  - `references/brand-identity.md` coincide al hex/fuente con la canónica (C2/C5).
  - `assets/logos/` ¿copia o canónica? (C1).
  - Fuente: usa Century Gothic — ¿disponible en Linux? (C3).
  - **Gap probable:** parece orientado a .docx. El gold standard de Andrea es **HTML**. ¿El skill produce/contempla HTML premium? Si no, es una brecha a cubrir (el HTML es ahora un canal de primera clase).
  - Workflow asume leer el skill `docx` — validar que esa dependencia esté declarada y funcione.

### 3.4 `pptx_expert` (capa de marca + estrategia — decks)
- **Revisar:**
  - Plantilla `assets/Nexostrat_Template.pptx` on-brand y vigente; `references/nexostrat-template-reference.md` coincide con la realidad.
  - `references/brand-identity.md` coincide con la canónica (C2/C5).
  - `assets/logos/` copia/canónica (C1); usa Inter (C3).
  - Depende de leer el skill `pptx` — validar dependencia.
  - **Nota:** JP está editando este flujo de presentaciones. Coordinar para no chocar (ver auditoría Skill 6, sección H).

---

## 4. La pregunta clave de integración (Skill 6 ↔ skills de marca)

Hay una tensión arquitectónica que la auditoría debe resolver, **no prejuzgar**:

`pptx_expert` y `editorial_designer` son **prompt-skills** (instrucciones que Claude lee y ejecuta con criterio). Skill 6, hoy, son **scripts deterministas** (`generate_*.js/.py`). "Que Skill 6 los use" tiene dos lecturas:

- **Opción A — Capa de marca compartida (determinista).** Skill 6 sigue siendo scripts, pero la marca (constantes de color, fuentes, rutas de logo, helpers de header/footer, plantillas) se extrae a **un módulo único compartido** — lo que hoy es `brand.py`, extendido a HTML y PPTX. Los prompt-skills y los scripts leen esa misma fuente. *Ventaja:* reproducible, testeable, sin drift. *Costo:* el "criterio de diseño" de los prompt-skills no se aplica automáticamente; hay que codificarlo.
- **Opción B — Flujo dirigido por Claude.** Skill 6 deja de ser puramente scripts y pasa a un flujo donde Claude lee `pptx_expert`/`editorial_designer` y genera con criterio (como se hizo a mano con el deck de Andrea). *Ventaja:* calidad gold-standard, flexibilidad. *Costo:* menos determinista/reproducible, más caro por corrida.
- **Opción C — Híbrido.** Scripts deterministas para la estructura + una pasada de Claude con los prompt-skills para el diseño fino. (El deck de Andrea sugiere que el híbrido es viable.)

**Esta decisión se toma con JP** y condiciona todo el rework de Skill 6. El plan la marca como el primer entregable de la auditoría de Skill 6.

---

## 5. Auditoría de Skill 6 (después de §3 y §4)

- Revisar los 6 generadores y qué marca hardcodean hoy.
- Mapear cada hallazgo ya documentado (T1-T10 + B/C/D/E/F/H del reporte `auditoria_skill6_trixx_20260529.md`) a archivo/generador concreto → entender el *porqué* de cada error.
- Decidir, por la Opción de §4, cómo se cablea cada generador a la capa de marca.
- **Salida:** lista de cambios accionable, ordenada, con el *porqué* de cada uno — lista para ejecutar en la sesión de implementación, e integrable con la entrega de JP (presentaciones).

---

## 6. Secuencia y dependencias

| Paso | Auditoría | Depende de | Output |
|---|---|---|---|
| 1 | `docx` + `pptx` (técnicos) | — | 1 .md (Linux + capacidades + cómo se consumen) |
| 2 | `editorial_designer` + `pptx_expert` (marca) | Paso 1 | 1 .md por skill (marca + dependencias + gaps) |
| 3 | Decisión de integración §4 | Pasos 1-2 + JP | Decisión registrada (A/B/C) |
| 4 | Skill 6 | Pasos 1-3 + reporte T1-T10 | Lista de cambios accionable |
| 5 | Implementación | Paso 4 + entrega de JP | (sesión aparte) |

**Regla:** no se implementa nada hasta cerrar el paso 4. El objetivo de auditar primero es entender el porqué y ejecutar los cambios de forma más acertada (y una sola vez).

---

## 7. Hallazgos preliminares ya visibles (a confirmar en la auditoría formal)

- **P1 [LINUX/MARCA]** Century Gothic probablemente ausente en Linux → docs off-brand vía LibreOffice. (C3)
- **P2 [MARCA]** Logos triplicados (2 skills + canónica). (C1)
- **P3 [MARCA]** Fuente de marca fragmentada en 5 lugares. (C5)
- **P4 [INTEGRACIÓN]** Skill 6 no invoca a editorial_designer ni pptx_expert; reimplementa marca a medias.
- **P5 [GAP]** editorial_designer parece docx-only; falta canal HTML premium (el del gold standard de Andrea).
- **P6 [UBICACIÓN]** Los motores `docx`/`pptx` viven en `~/.grok/skills/` (fuera del repo, machine-local) — dependencia no versionada con Nexostrat; evaluar si eso es un riesgo de portabilidad.
