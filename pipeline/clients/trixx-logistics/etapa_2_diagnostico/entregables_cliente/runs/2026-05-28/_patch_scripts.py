#!/usr/bin/env python3
"""Copia los scripts del skill 06 a un dir temporal y neutraliza emojis/estrellas
para producir la VERSION LIMPIA (estándar Ricardo: cero emojis/iconos Unicode).
No toca el skill canónico."""
import os, re, shutil, sys

SRC = "/srv/Nexostrat/skills/06_client_deliverables/scripts"
DST = "/tmp/trixx_clean_scripts"

if os.path.exists(DST):
    shutil.rmtree(DST)
os.makedirs(DST)

# Copiar solo los generadores (node_modules se referencia vía NODE_PATH)
for f in os.listdir(SRC):
    if f.endswith(".js") or f.endswith(".py"):
        shutil.copy(os.path.join(SRC, f), os.path.join(DST, f))

# --- Reemplazos dirigidos por archivo (antes del strip genérico) ---
TARGETED = {
    "generate_client_docx.js": [
        # estrellas de score -> "N/5"
        ("'★'.repeat(op.impacto_score || 3) + '☆'.repeat(5 - (op.impacto_score || 3))",
         "((op.impacto_score || 3) + '/5')"),
        # frases que referencian el símbolo de rayo
        ("Las marcadas con ⚡ son Quick Wins: iniciativas de alta relación impacto/esfuerzo recomendadas como punto de entrada al Ciclo 2.",
         "Los Quick Wins son las iniciativas de mayor relación impacto/esfuerzo, recomendadas como punto de entrada al Ciclo 2."),
        ("La siguiente tabla muestra todas las iniciativas ordenadas por impacto y esfuerzo. Las marcadas con ⚡ son los Quick Wins recomendados como punto de entrada.",
         "La siguiente tabla muestra todas las iniciativas ordenadas por impacto y esfuerzo. Los Quick Wins son los recomendados como punto de entrada."),
        ("⚡ Quick Win  ·  Impacto: ★ = bajo → ★★★★★ = alto  ·  Complejidad: pequeño / mediano / grande",
         "Quick Win  ·  Impacto y esfuerzo en escala de 1 a 5  ·  Complejidad: pequeño / mediano / grande"),
        (" ⚠️ estimado", " (estimado)"),
        ("⚠️ estimado", "(estimado)"),
    ],
    "generate_pptx.js": [
        # iconos de próximos pasos -> números de paso
        ("icon: '📄'", "icon: '1'"),
        ("icon: '✅'", "icon: '2'"),
        ("icon: '💳'", "icon: '3'"),
        ("icon: '🚀'", "icon: '4'"),
    ],
    "generate_html_document.py": [
        (" ⚠️ estimado", " (estimado)"),
        ("⚠️ estimado", "(estimado)"),
    ],
}

# Rango de emojis/iconos a eliminar. Se EXCLUYEN flechas (→ U+2192) y el punto medio (·).
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF"   # símbolos y pictogramas
    "\U00002600-\U000027BF"     # misc symbols + dingbats (incluye ★☆✅✓⚠⚡❌➡)
    "\U00002B00-\U00002BFF"     # flechas/estrellas suplementarias (⭐)
    "\U0000FE0F"                 # variation selector
    "]"
)

for f in os.listdir(DST):
    p = os.path.join(DST, f)
    with open(p, encoding="utf-8") as fh:
        txt = fh.read()
    for a, b in TARGETED.get(f, []):
        txt = txt.replace(a, b)
    # quitar emoji + un espacio que le siga (limpia prefijos tipo "✅ Texto")
    txt = re.sub(EMOJI.pattern + r" ?", "", txt)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(txt)

# Verificación: ¿quedó algún emoji?
leftover = {}
for f in os.listdir(DST):
    with open(os.path.join(DST, f), encoding="utf-8") as fh:
        em = set(EMOJI.findall(fh.read()))
    if em:
        leftover[f] = sorted(em)
print("DST:", DST)
print("Emojis restantes en scripts:", leftover if leftover else "ninguno")
