# Procedencia — frontend_design (vendorizado)

- **Qué es:** copia verbatim del skill oficial **frontend-design** de Anthropic, usado como **base** del experto HTML `00_nexostrat_html` (Plan Maestro, Fase 1).
- **Origen:** `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/` (plugin oficial, autor Anthropic, `support@anthropic.com`).
- **Versión:** `plugin.json` no declara campo `version` (cache lo reporta como `unknown`).
- **Capturado:** 2026-05-29.
- **Licencia:** Apache License 2.0 (`LICENSE.txt`, verbatim del origen).
- **Modificaciones:** **ninguna** — `SKILL.md` y `LICENSE.txt` son copias byte-idénticas al origen (verificado con `diff -q`). Este directorio es el material upstream sin tocar.

## Cómo se usa (Fase 2)

El experto de marca `00_nexostrat_html` (a construir en Fase 2) es una **obra derivada** de este base + la marca Nexostrat (`operations/marketing/brand/brand-identity.md`). Las modificaciones de marca van en `00_nexostrat_html`, no aquí — este directorio se mantiene como referencia upstream limpia (paralelo a `skills/docx_technical/` y `skills/pptx_technical/`).

### Tensión a resolver en Fase 2 (importante)

El `SKILL.md` oficial instruye explícitamente: *"Avoid generic fonts like Arial and **Inter**"* y *"NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial...)"*.

Esto **choca con la marca Nexostrat** (decisión D3: **Inter en todos los canales**). En `00_nexostrat_html` la marca manda: Inter es una elección tipográfica deliberada de marca, no un default genérico. El experto HTML debe **override** explícitamente esta guía del base, conservando del oficial el rigor de diseño (composición, motion, atmósfera, anti-"AI slop") pero anclando tipografía + paleta a la identidad Aurora.

Per Apache 2.0 §4(b): cualquier archivo modificado respecto al upstream debe llevar nota visible del cambio — esas notas vivirán en `00_nexostrat_html`, no en este base sin tocar.
