# Especificaciones de Diseño — Nexostrat

Referencia detallada para tipografía, espaciado y elementos por tipo de documento. Leer cuando se necesiten valores exactos para implementación.

## Tabla de Contenidos

1. Escala Tipográfica por Tipo de Documento
2. Sistema de Márgenes
3. Ritmo Vertical
4. Reglas de Aplicación de Color
5. Especificaciones por Tipo de Documento
6. Elementos Especiales
7. Patrones de Diseño Nexostrat

---

## 1. Escala Tipográfica por Tipo de Documento

### Propuesta / Diagnóstico / Hoja de Ruta

| Elemento | Tamaño (pt) | Peso | Color | Spacing After (pt) | Notas |
|----------|-------------|------|-------|-------------------|-------|
| Título portada | 36–48 | Bold | Arctic White | — | Portada sobre fondo Midnight |
| Subtítulo portada | 18–22 | Regular | Sky Blue | — | Portada — acento de color |
| Título de sección (H1) | 28–32 | Bold | Midnight Blue | 20 | Comienza en nueva sección |
| Subsección (H2) | 18–22 | Bold | Midnight Blue | 14 | |
| Bloque / Categoría (H3) | 13–15 | Bold | Ocean Deep | 10 | |
| Cuerpo de texto | 11–12 | Regular | Dark Text | 8–10 | Interlineado 1.4–1.5 |
| Dato de impacto | 36–52 | Bold | Amber Gold | — | Uso excepcional — máx 2-3 por doc |
| Caption / Nota al pie | 9–10 | Regular | Gray 500 | 6 | |
| Número de página | 9 | Regular | Gray 500 | — | Footer |

### One-pager / Sell Sheet

| Elemento | Tamaño (pt) | Peso | Spacing After (pt) |
|----------|-------------|------|-------------------|
| Headline | 24–28 | Bold | 12 |
| Sub-headline | 16–18 | SemiBold | 10 |
| Cuerpo | 10–11 | Regular | 6 |
| Bullet points | 10–11 | Regular | 4 |
| CTA Text | 12–14 | Bold | — |

### Reporte / Whitepaper

| Elemento | Tamaño (pt) | Peso | Spacing After (pt) |
|----------|-------------|------|-------------------|
| Título del documento | 28–32 | Bold | 18 |
| Sección (H1) | 22–24 | Bold | 16 |
| Subsección (H2) | 16–18 | Bold | 12 |
| Sub-subsección (H3) | 13–14 | Bold | 10 |
| Cuerpo | 11 | Regular | 8 |
| Encabezado de tabla | 10–11 | Bold | — |
| Cuerpo de tabla | 10 | Regular | — |

---

## 2. Sistema de Márgenes

### Márgenes en pulgadas / DXA

| Tipo de Documento | Top | Bottom | Left | Right | DXA (top/bot/izq/der) |
|-------------------|-----|--------|------|-------|----------------------|
| Propuesta / Diagnóstico | 1.0" | 1.0" | 1.25" | 1.0" | 1440/1440/1800/1440 |
| Hoja de Ruta | 1.0" | 1.0" | 1.0" | 1.0" | 1440/1440/1440/1440 |
| One-pager | 0.75" | 0.75" | 0.75" | 0.75" | 1080/1080/1080/1080 |
| Reporte / Whitepaper | 1.0" | 1.0" | 1.0" | 1.0" | 1440/1440/1440/1440 |
| Carta / Comunicación | 1.0" | 1.0" | 1.0" | 1.0" | 1440/1440/1440/1440 |

### Portada (todas las variantes)
- Márgenes: 0 en todos los lados para la capa de fondo (tabla de fondo completo)
- Padding interior del texto: top 3600 DXA (2.5"), left/right 1440 DXA (1")

---

## 3. Ritmo Vertical

Usar una unidad base de 6pt u 8pt y multiplicar:

- Después de párrafo de cuerpo: 1× base (6–8pt)
- Después de encabezado: 2–3× base (12–24pt)
- Antes de encabezado: 3–4× base (18–32pt) — más espacio antes que después crea agrupación visual
- Salto de sección: 5–6× base (30–48pt) o salto de página
- Entre elementos especiales (callout, tabla) y cuerpo: 2–3× base arriba y abajo

---

## 4. Reglas de Aplicación de Color

### Dónde Usar los Colores de Marca

| Elemento | Tratamiento de Color |
|----------|---------------------|
| Cuerpo de texto | Dark Text (`#1F2937`) — nunca negro puro |
| Encabezados H1 | Midnight Blue (`#0C1A2E`) |
| Encabezados H2 | Midnight Blue (`#0C1A2E`) |
| Encabezados H3 | Ocean Deep (`#0D4A6B`) |
| Reglas horizontales | Sky Blue (`#0EA5E9`) o Gray Mid (`#D1D5DB`) — delgadas |
| Borde izquierdo de callout | Sky Blue (`#0EA5E9`), 4pt |
| Fondo de callout | Arctic White (`#F0FBFF`) |
| Encabezado de tabla | Midnight Blue fondo / blanco texto |
| Filas alternas de tabla | Blanco / Gray Light (`#F5F5F5`) |
| Borde de tabla | Gray Mid (`#D1D5DB`), 1pt |
| Números de página | Gray 500 (`#6B7280`) |
| Título en portada | Arctic White (`#F0FBFF`) sobre fondo Midnight |
| Acento en portada | Sky Blue (`#0EA5E9`) — línea o subtítulo |
| Dato de impacto | Amber Gold (`#F59E0B`) — SOLO números estadísticos |

### Color Don'ts

- Nunca Amber Gold en cuerpo de texto
- Nunca más de 3 colores de la paleta en una sola página
- Nunca fondos de color en páginas de texto (blanco o Arctic White solamente)
- Nunca Sky Blue como fondo para texto extenso
- Nunca gradientes entre colores de la paleta

---

## 5. Especificaciones por Tipo de Documento

### Propuesta Comercial

**Estructura:**
1. Portada (fondo Midnight Blue, título Arctic White, logo de texto, fecha, nombre del prospecto)
2. Resumen ejecutivo / problema que resuelve
3. Nuestra propuesta de valor
4. Proceso / metodología (pasos numerados)
5. Entregables y tiempos
6. Inversión
7. Próximos pasos / CTA

**Reglas especiales:**
- El nombre del prospecto en la portada es un diferenciador — siempre incluirlo si se conoce
- La sección de inversión puede usar un dato en Amber Gold para el número clave (precio)
- CTA final con fondo Midnight Blue o recuadro prominente
- Máximo 1 dato de impacto por sección

### Diagnóstico Inicial

**Estructura:**
1. Portada
2. Snapshot de situación actual
3. Oportunidades de IA identificadas (3 mínimo)
4. Nivel de madurez digital
5. Quick Wins recomendados
6. Próximos pasos

**Reglas especiales:**
- Usar callout boxes para resaltar las oportunidades identificadas
- Tablas para comparar estado actual vs. estado deseado
- Datos de impacto (porcentajes, horas recuperadas) en Amber Gold

### Hoja de Ruta de IA

**Estructura:**
1. Portada
2. Resumen de hallazgos del diagnóstico
3. Fases de implementación (timeline visual)
4. Detalle por fase (objetivos, herramientas, entregables)
5. ROI proyectado
6. Recursos requeridos
7. Condiciones de éxito

**Reglas especiales:**
- Timelines y fases pueden usar Sky Blue como color de hilo conductor
- Cada fase debe tener numeración clara (01, 02, 03)
- El ROI proyectado es candidato a dato en Amber Gold

### One-pager / Sell Sheet

**Reglas especiales:**
- Todo en una página (máximo dos)
- El lector debe captar el mensaje clave en 5 segundos — jerarquía visual agresiva
- Bullet points son aceptables y recomendados
- Un solo CTA fuerte al final
- El uso de color puede ser más audaz que en documentos largos (la portada ya no existe)
- Dato de impacto prominente (Amber Gold) en la mitad superior de la página

### Carta / Comunicación Formal

**Reglas especiales:**
- Letterhead: logo de texto + línea Sky Blue inferior
- Cuerpo limpio: márgenes generosos, cuerpo en Inter Regular 12pt
- Mínima decoración interior
- Footer con nexostrat.com y datos de contacto

---

## 6. Elementos Especiales

### Callout Box

Elemento de una columna con borde izquierdo de acento. Ideal para hallazgos clave, advertencias, o información que debe destacar del flujo normal.

```
Implementación DOCX (docx-js):
Una tabla de 2 columnas: columna izquierda angosta (200 DXA) con fondo Sky Blue,
columna derecha con fondo Arctic White y el contenido.
Todos los bordes: NONE (el efecto visual viene del contraste de fondos).
Padding interior derecho: top/bottom 140, left/right 200 DXA.

Implementación PDF (reportlab):
Rectángulo de fondo Arctic White.
Rectángulo delgado (8pt ancho) Sky Blue pegado al borde izquierdo.
Texto renderizado con padding left adecuado.
```

Cuándo usar: hallazgos importantes, reglas críticas, advertencias, síntesis de punto clave. Máximo 2-3 por documento.

### Dato de Impacto

Un número estadístico grande en Amber Gold que comunica impacto en un vistazo.

```
Implementación: Párrafo aislado con:
- Fuente: Inter Bold
- Tamaño: 36–52pt según el espacio disponible
- Color: Amber Gold (#F59E0B)
- Alineación: centrado o izquierda según el layout
- Label debajo en 10pt Dark Text o Gray 500

Ejemplo visual:
    83%
    de empresas que adoptan IA reportan
    incremento en ingresos

Uso máximo: 2-3 datos de impacto por documento completo.
Si se abusa, el efecto desaparece.
```

### Tabla de Datos

```
Encabezado: fondo Midnight Blue (#0C1A2E), texto blanco, Inter Bold 10-11pt
Filas alternas: blanco / Gray Light (#F5F5F5)
Bordes: Gray Mid (#D1D5DB), 1pt, todos los lados
Padding de celda: top/bottom 80-100 DXA, left/right 140 DXA
Texto de cuerpo: Inter Regular 10-11pt, Dark Text
```

### Regla Horizontal

```
Línea delgada para separar secciones dentro de una página.
Color: Sky Blue (#0EA5E9) o Gray Mid (#D1D5DB)
Grosor: 1–2pt
Espaciado: 24-36pt arriba y abajo
Ancho: 60-80% del ancho de texto, centrado (opcional — puede ser full width)
```

### Etiqueta de Sección (Section Label)

Etiqueta pequeña en mayúsculas que precede a los H1, similar al estilo de Nexostrat en su brand guide.

```
Texto: "01 — FILOSOFÍA DE MARCA" (número + em dash + título en mayúsculas)
Fuente: Inter Bold, 9-10pt
Color: Sky Blue (#0EA5E9)
Tratamiento: Con borde inferior Sky Blue 2pt
Espaciado: before 360 DXA, after 60 DXA
```

---

## 7. Patrones de Diseño Nexostrat

### El Patrón "Whitespace Profesional"

Los documentos premium usan significativamente más whitespace que los documentos de negocios típicos. Esto es contraintuitivo — se siente como "desperdiciar espacio" — pero es el mayor indicador de calidad de diseño.

En Nexostrat:
- Las portadas deben ser al menos 50% espacio negativo
- Los márgenes deben ser más amplios que el default de Word
- El espaciado de párrafos usa space-after, no sangría de primera línea
- Después de cada H1, hay siempre un spacer antes del primer párrafo

### El Patrón "Un Solo Acento"

Elige una forma de usar el color de acento (Sky Blue) y úsalo consistentemente en todo el documento. No mezcles: si usas Sky Blue para bordes de callout, no lo uses también para H2 y para reglas horizontales.

Opciones de patrones de acento consistentes:
- Sky Blue como borde izquierdo de callout boxes (patrón más común Nexostrat)
- Sky Blue como línea de sección (etiqueta de sección + regla)
- Sky Blue como color de H3 + borde de tabla header complementario

### El Patrón "Amber es Raro"

El Amber Gold solo aparece en máximo 2-3 lugares por documento. Cuando aparece, debe sorprender. Si el Amber aparece en todas partes, se convierte en ruido. Trata cada instancia de Amber como si tuvieras un presupuesto de 3 usos por documento — úsalos bien.
