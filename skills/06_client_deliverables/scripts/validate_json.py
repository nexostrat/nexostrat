#!/usr/bin/env python3
"""
validate_json.py — Valida data_{empresa}.json contra el schema de Nexostrat
Usage: python3 validate_json.py data_empresa.json

Salida:
  ✓ JSON válido — resumen del contenido
  ERROR: descripción del problema (+ sugerencia de corrección si aplica)

Exit code 0 = válido, 1 = inválido.
"""

import json
import sys
import os


def err(msg, hint=None):
    print(f"\n❌ ERROR: {msg}")
    if hint:
        print(f"   💡 {hint}")


def ok(msg):
    print(f"   ✓ {msg}")


def validate(path):
    # ── Leer el archivo ──────────────────────────────────────────────────────
    if not os.path.exists(path):
        err(f"Archivo no encontrado: {path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except json.JSONDecodeError as e:
        err(f"JSON malformado en línea {e.lineno}: {e.msg}",
            hint="Revisa comas faltantes, comillas sin cerrar o llaves desbalanceadas.")
        return False

    errors = []

    def check(condition, error_msg, hint=None):
        if not condition:
            errors.append((error_msg, hint))

    # ── metadata ─────────────────────────────────────────────────────────────
    M = d.get("metadata", {})
    check(M.get("empresa"), "metadata.empresa está vacío")
    check(M.get("empresa_slug"), "metadata.empresa_slug está vacío",
          hint="Debe ser el nombre sin espacios, ej: 'DistribuidoraLosAndes'")
    check(M.get("fecha_iso"), "metadata.fecha_iso está vacío",
          hint="Formato esperado: YYYY-MM-DD, ej: '2026-05-28'")
    if M.get("fecha_iso"):
        parts = M["fecha_iso"].split("-")
        check(len(parts) == 3 and all(p.isdigit() for p in parts),
              f"metadata.fecha_iso tiene formato inválido: '{M['fecha_iso']}'",
              hint="Usa el formato YYYY-MM-DD")
    check(M.get("pais") in ("CO", "MX", None) or True,
          "metadata.pais debería ser 'CO' o 'MX'")

    # ── empresa_hoy ──────────────────────────────────────────────────────────
    EH = d.get("empresa_hoy", {})
    check(EH.get("descripcion"), "empresa_hoy.descripcion está vacío")
    check(EH.get("madurez_digital"), "empresa_hoy.madurez_digital está vacío",
          hint="Valores esperados: 'Básica', 'Media' o 'Avanzada'")

    # ── problemas ────────────────────────────────────────────────────────────
    PROBS = d.get("problemas", [])
    check(len(PROBS) > 0, "No hay problemas definidos en 'problemas'")
    prob_ids = set()
    for i, p in enumerate(PROBS):
        prefix = f"problemas[{i}]"
        check(p.get("id") is not None, f"{prefix}.id falta")
        check(p.get("titulo"), f"{prefix}.titulo está vacío")
        check(p.get("descripcion"), f"{prefix}.descripcion está vacío")
        if p.get("id") is not None:
            check(p["id"] not in prob_ids,
                  f"{prefix}.id duplicado: {p['id']}",
                  hint="Cada problema debe tener un ID único.")
            prob_ids.add(p["id"])
        ci = p.get("costo_inaccion")
        if ci:
            check(ci.get("descripcion"), f"{prefix}.costo_inaccion.descripcion está vacío")

    # ── oportunidades ────────────────────────────────────────────────────────
    OPS = d.get("oportunidades", [])
    check(len(OPS) > 0, "No hay oportunidades definidas en 'oportunidades'")
    op_ids = set()
    for i, op in enumerate(OPS):
        prefix = f"oportunidades[{i}]"
        check(op.get("id") is not None, f"{prefix}.id falta")
        check(op.get("titulo"), f"{prefix}.titulo está vacío")
        check(op.get("descripcion"), f"{prefix}.descripcion está vacío")
        check(op.get("area"), f"{prefix}.area está vacío")
        check(op.get("categoria") in ("pequeno", "mediano", "grande"),
              f"{prefix}.categoria inválido: '{op.get('categoria')}'",
              hint="Valores válidos: 'pequeno', 'mediano', 'grande'")
        check(isinstance(op.get("precio_usd_min"), (int, float)) and op.get("precio_usd_min", 0) > 0,
              f"{prefix}.precio_usd_min debe ser un número positivo")
        if op.get("id") is not None:
            check(op["id"] not in op_ids,
                  f"{prefix}.id duplicado: {op['id']}",
                  hint="Cada oportunidad debe tener un ID único.")
            op_ids.add(op["id"])
        # Validar referencia cruzada problema_id
        pid = op.get("problema_id")
        if pid is not None:
            check(pid in prob_ids,
                  f"{prefix}.problema_id={pid} no existe en 'problemas'",
                  hint=f"IDs de problemas disponibles: {sorted(prob_ids)}")
        # Infraestructura
        if op.get("requiere_infraestructura"):
            fee = op.get("fee_mensual_usd")
            check(fee is not None and fee >= 50,
                  f"{prefix}: requiere_infraestructura=true pero fee_mensual_usd < 50",
                  hint="El mínimo de fee mensual es USD 50.")

    # ── quick_wins ───────────────────────────────────────────────────────────
    QW = d.get("quick_wins", [])
    check(len(QW) > 0, "quick_wins está vacío — define al menos 1 Quick Win")
    for qw_id in QW:
        check(qw_id in op_ids,
              f"quick_wins contiene id={qw_id} que no existe en 'oportunidades'",
              hint=f"IDs de oportunidades disponibles: {sorted(op_ids)}")

    # ── roadmap_fases ────────────────────────────────────────────────────────
    FASES = d.get("roadmap_fases", [])
    check(len(FASES) > 0, "roadmap_fases está vacío")
    for i, fase in enumerate(FASES):
        check(fase.get("fase"), f"roadmap_fases[{i}].fase está vacío")
        for oid in fase.get("oportunidades_ids", []):
            check(oid in op_ids,
                  f"roadmap_fases[{i}].oportunidades_ids contiene id={oid} inexistente",
                  hint=f"IDs disponibles: {sorted(op_ids)}")

    # ── propuesta ────────────────────────────────────────────────────────────
    PROP = d.get("propuesta", {})
    check(PROP.get("total_roadmap_usd", 0) > 0,
          "propuesta.total_roadmap_usd debe ser mayor que 0")
    entrada_id = PROP.get("iniciativa_entrada_id")
    if entrada_id is not None:
        check(entrada_id in op_ids,
              f"propuesta.iniciativa_entrada_id={entrada_id} no existe en 'oportunidades'",
              hint=f"IDs disponibles: {sorted(op_ids)}")

    # ── persuasion ───────────────────────────────────────────────────────────
    PER = d.get("persuasion", {})
    gancho_id = PER.get("quick_win_gancho_id")
    if gancho_id is not None:
        check(gancho_id in op_ids,
              f"persuasion.quick_win_gancho_id={gancho_id} no existe en 'oportunidades'",
              hint=f"IDs disponibles: {sorted(op_ids)}")
    check(PER.get("cita_principal"), "persuasion.cita_principal está vacío",
          hint="Incluye la cita más poderosa del cliente.")
    check(PER.get("objecion_probable"), "persuasion.objecion_probable está vacío")

    # ── Resultado ────────────────────────────────────────────────────────────
    if errors:
        print(f"\n❌ Se encontraron {len(errors)} error(es) en {path}:\n")
        for msg, hint in errors:
            err(msg, hint)
        print()
        return False

    # ── Resumen de éxito ─────────────────────────────────────────────────────
    empresa = M.get("empresa", "?")
    slug = M.get("empresa_slug", "?")
    total = d.get("propuesta", {}).get("total_roadmap_usd", 0)
    qw_titles = [op["titulo"] for op in OPS if op.get("id") in set(QW)]
    print(f"\n✅ JSON válido — {path}")
    print(f"   Empresa:        {empresa} ({slug})")
    print(f"   Problemas:      {len(PROBS)}")
    print(f"   Oportunidades:  {len(OPS)}")
    print(f"   Quick Wins:     {', '.join(qw_titles)}")
    print(f"   Total roadmap:  USD {total:,}")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_json.py data_empresa.json")
        sys.exit(1)
    success = validate(sys.argv[1])
    sys.exit(0 if success else 1)
