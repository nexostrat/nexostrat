# Entregables Ciclo 1 — Grupo Trixx — 2026-05-28

Dos versiones, por decisión de Ricardo (sesión 28):

## `skill_raw/` — Salida cruda del Skill 6 (nexostrat-client-deliverables)
Tal cual la generó el skill, **sin tocar**. Sirve de evidencia para que **JP corrija el skill**:
- Contiene emojis e iconos Unicode (`✅ ⚡ 🚀 💰 🎯`, estrellas `★☆`, `⚠`) — el skill los inyecta por diseño.
- Pricing con el framework del skill (USD 250/h): iniciativas USD 4,000–15,000, roadmap USD 52–73k.
- DOCX cliente: 18 páginas (sobre el máximo de 15 del propio spec del skill).
- Fuente de datos: `../data_Trixx.json` (copia en `skill_raw/data_Trixx_skill.json`).

Cosas que JP debería arreglar en el skill: (1) quitar emojis/iconos y reemplazar estrellas por "N/5"; (2) revisar el framework de pricing vs. el floor real de USD 3,000; (3) controlar la longitud del DOCX (saltos de página por sección lo inflan a ~17-18).

## `version_limpia/` — Versión filtrada a estándar Ricardo (lista para revisar/entregar)
Misma estructura, corregida a mano:
- **Cero emojis / cero iconos Unicode** en los 6 archivos. Scores como `N/5`.
- **Pricing al floor de USD 3,000** + números de las reuniones con JP: iniciativas USD 3,000–8,000, paquete de 3 quick wins USD 6,500, roadmap USD 18–23k, fee mensual USD 50–100.
- **DOCX cliente: 14 páginas** (dentro de 10–15). PPTX: 9 slides.
- Contenido enfocado: 2 pilares (camiones + contenedores), 5 iniciativas líderes, lenguaje sin "bot/robot", marco "menores disrupciones / liberar al equipo".
- Fuente de datos: `version_limpia/data_Trixx_limpio.json`.

### Cómo se produjo la versión limpia (reproducible)
Se copiaron los scripts del skill a un dir temporal y se parchearon **sin tocar el skill canónico**:
- `_patch_scripts.py` (en esta carpeta) — neutraliza emojis/iconos y reemplaza estrellas por `N/5`.
- Ajuste adicional ad-hoc: se removieron 4 saltos de página forzados en el generador de DOCX para bajar de 18 a 14 páginas.
- JSON repreciado y recortado (4→3 problemas, situación por área 4→3, sin la conciliación del broker en el cuerpo — queda en Fase 3 narrativa).

## Pendientes antes de enviar al cliente
- Contacto: `contacto@nexostrat.com` / `+57 333 286 3963` (confirmado, ya en la versión limpia).
- Copia desechable para revisión rápida en `~/Desktop/Trixx_Entregables_20260528/` (Ricardo la borrará; la canónica vive aquí en el pipeline).
- Revisar pricing final (Ricardo + JP).
- El briefing interno sale a 2 páginas (spec pide 1) — cosmético.
- Insumo de origen (Etapa 5): `../../diagnostico_refinado/runs/2026-05-28/Trixx_Diagnostico_Refinado_20260528.md`.
