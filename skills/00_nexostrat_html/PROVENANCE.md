# Procedencia — 00_nexostrat_html (obra derivada)

- **Qué es:** experto HTML/web premium de Nexostrat. **Obra derivada** del skill oficial **frontend-design** de Anthropic + la marca Nexostrat (`operations/marketing/brand/brand-identity.md`) + los patrones del gold standard `build_andrea.py` (deck + cheat sheet hechos a mano para la reunión con Andrea, Trixx, mayo 2026).
- **Base upstream:** `skills/frontend_design/` (vendorizado verbatim, Apache 2.0, capturado 2026-05-29). La guía base vive aquí sin tocar en `references/frontend-design-base.md`.
- **Licencia:** Apache License 2.0 (`LICENSE.txt`, verbatim del upstream).

## Modificaciones respecto al upstream (Apache 2.0 §4(b))

Este skill **modifica/extiende** la guía de `frontend-design`. Cambios visibles, requeridos por §4(b):

1. **Override de tipografía.** La guía base prohíbe Inter (*"avoid generic fonts like Arial and Inter"*, *"NEVER use ... Inter, Roboto, Arial..."*). Aquí se **anula conscientemente**: Inter es la tipografía deliberada de marca de Nexostrat en todos los canales (decisión D3). No es un default genérico; es identidad. Documentado en `SKILL.md` § "Override de marca".
2. **Paleta anclada.** La base promueve elecciones de color libres/inesperadas; aquí la paleta Aurora (Midnight/Ocean/Sky/Emerald/Amber/Arctic) es obligatoria, con la regla de escasez del Amber Gold.
3. **Motor y patrones añadidos.** Se añade `assets/build_nexostrat_html.py` (motor de slides vanilla-JS, tokens, logos base64, QR) y exemplars, encodeando el gold standard de Andrea — material propio de Nexostrat, no de Anthropic.

Lo que se **preserva** del upstream: el rigor de diseño intencional, composición, motion de alto impacto, atmósfera/profundidad y el rechazo al "AI slop". El override es tipográfico y de paleta, no de calidad.

## Relación con el trío

Paralelo a `skills/00_nexostrat_pptx/` y `skills/00_nexostrat_docx/`. Los tres leen UNA sola fuente de marca (`operations/marketing/brand/brand-identity.md`) y resuelven los logos desde `operations/marketing/brand/logos` (nunca los bundlean). Este experto es el dueño del canal web y puede producir la versión-HTML de documentos y presentaciones.
</content>
