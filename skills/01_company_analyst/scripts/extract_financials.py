#!/usr/bin/env python3
"""
extract_financials.py — Supersociedades Financial Data Extractor
Usage: python3 extract_financials.py "<company_name_or_NIT>"

Searches the Supersociedades Colombia Excel files bundled with this skill
and returns formatted financial data for the requested company.

Values are in thousands of COP (COP miles).
"""

import sys
import os
import re
import pandas as pd
from pathlib import Path

# ── Locate asset files ────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR.parent / "assets"

BALANCE_FILE = ASSETS_DIR / "supersociedades_balance_general.xlsx"
INCOME_FILE  = ASSETS_DIR / "supersociedades_estado_resultados.xlsx"

# ── Key column mappings ───────────────────────────────────────────────────────
COL_NIT     = "NIT"
COL_NAME    = "Razón social de la sociedad"
COL_CIIU    = "Clasificación Industrial Internacional Uniforme Versión 4 A.C (CIIU)"
COL_TYPE    = "Tipo societario"
COL_CITY    = "Ciudad de la dirección del domicilio"
COL_DEPT    = "Departamento de la dirección del domicilio"
COL_PERIOD  = "Periodo"
COL_CUTOFF  = "Fecha de Corte"

# Balance General
COL_ASSETS      = "Total de activos (Assets)"
COL_LIABILITIES = "Total pasivos (Liabilities)"
COL_EQUITY      = "Patrimonio total (Equity)"
COL_CURR_ASSETS = "Activos corrientes totales (CurrentAssets)"
COL_CASH        = "Efectivo y equivalentes al efectivo (CashAndCashEquivalents)"

# Income Statement
COL_REVENUE     = "Ingresos de actividades ordinarias (Revenue)"
COL_COGS        = "Costo de ventas (CostOfSales)"
COL_GROSS       = "Ganancia bruta (GrossProfit)"
COL_OPER_PROFIT = "Ganancia (pérdida) por actividades de operación (ProfitLossFromOperatingActivities)"
COL_NET_INCOME  = "Ganancia (pérdida) (ProfitLoss)"
COL_TAX_EXP     = "Ingreso (gasto) por impuestos (IncomeTaxExpenseContinuingOperations)"
COL_ADMIN_EXP   = "Gastos de administración (AdministrativeExpense)"
COL_SELL_EXP    = "Gastos de ventas (DistributionCosts)"

TRM_USD = 4200  # Approximate COP/USD exchange rate


def fmt(value, decimals=0):
    """Format a number or return 'N/D' if null."""
    if pd.isna(value) or value is None:
        return "N/D"
    try:
        v = float(value)
        if decimals == 0:
            return f"{v:,.0f}"
        return f"{v:,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/D"


def pct_change(curr, prev):
    """Calculate percentage change between two periods."""
    try:
        c, p = float(curr), float(prev)
        if pd.isna(c) or pd.isna(p) or p == 0:
            return "N/D"
        return f"{((c - p) / abs(p)) * 100:+.1f}%"
    except (ValueError, TypeError):
        return "N/D"


def pct(numerator, denominator, label=""):
    """Calculate percentage ratio."""
    try:
        n, d = float(numerator), float(denominator)
        if pd.isna(n) or pd.isna(d) or d == 0:
            return "N/D"
        return f"{(n / d) * 100:.1f}%"
    except (ValueError, TypeError):
        return "N/D"


def normalize_nit(raw):
    """Strip non-digits from a NIT string for comparison."""
    return re.sub(r'\D', '', str(raw)) if raw else ""


def find_company(df, query):
    """
    Find company rows by NIT (exact) or name (case-insensitive contains).
    Returns DataFrame with matched rows.
    """
    query = str(query).strip()
    q_nit = normalize_nit(query)

    # 1. Try exact NIT match
    if q_nit.isdigit() and len(q_nit) >= 6:
        mask = df[COL_NIT].astype(str).apply(normalize_nit) == q_nit
        result = df[mask]
        if not result.empty:
            return result, "NIT exacto"

    # 2. Try name contains (case-insensitive)
    q_upper = query.upper()
    mask = df[COL_NAME].str.upper().str.contains(q_upper, na=False, regex=False)
    result = df[mask]
    if not result.empty:
        return result, "nombre (búsqueda parcial)"

    # 3. Try each word individually (most flexible)
    words = [w for w in q_upper.split() if len(w) >= 4]
    for word in words:
        mask = df[COL_NAME].str.upper().str.contains(word, na=False, regex=False)
        result = df[mask]
        if not result.empty:
            return result, f"palabra clave '{word}'"

    return pd.DataFrame(), "no encontrado"


def budget_signal(revenue_cop_miles, net_margin_pct, debt_ratio_pct):
    """
    Classify the company's investment capacity for AI consulting.
    Revenue in COP miles. Returns (classification, explanation).
    """
    try:
        rev = float(revenue_cop_miles) if not pd.isna(revenue_cop_miles) else 0
        margin = float(net_margin_pct) if not pd.isna(net_margin_pct) else 0
        debt = float(debt_ratio_pct) if not pd.isna(debt_ratio_pct) else 0
    except (ValueError, TypeError):
        return "Indeterminada", "Datos insuficientes para evaluar capacidad de inversión."

    # Revenue in COP millions (divide miles by 1000)
    rev_m = rev / 1000

    if rev_m < 500:
        classification = "Baja"
        explanation = f"Ingresos menores a COP $500M ({rev_m:,.0f}M). Ticket de entrada puede ser restrictivo."
    elif rev_m < 5000:
        if margin < 0:
            classification = "Media-Baja"
            explanation = f"Ingresos de COP ${rev_m:,.0f}M pero margen negativo ({margin:.1f}%). Priorizar Quick Wins de alta ROI."
        elif debt > 70:
            classification = "Media-Baja"
            explanation = f"Ingresos de COP ${rev_m:,.0f}M pero endeudamiento alto ({debt:.0f}%). Evaluar con cuidado."
        else:
            classification = "Media"
            explanation = f"Ingresos de COP ${rev_m:,.0f}M con margen {margin:.1f}%. Capacidad para diagnóstico + Quick Win."
    elif rev_m < 50000:
        if margin < 2:
            classification = "Media"
            explanation = f"Ingresos de COP ${rev_m:,.0f}M pero margen ajustado ({margin:.1f}%). Buen prospecto si el ROI es claro."
        else:
            classification = "Alta"
            explanation = f"Ingresos de COP ${rev_m:,.0f}M con margen {margin:.1f}%. Buen prospecto para consultoría completa."
    else:
        classification = "Alta"
        explanation = f"Empresa grande (COP ${rev_m:,.0f}M en ingresos). Alta capacidad de inversión pero evaluar fit con servicios PYME."

    return classification, explanation


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 extract_financials.py '<nombre_empresa_o_NIT>'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # ── Load data ────────────────────────────────────────────────────────────
    if not BALANCE_FILE.exists():
        print(f"ERROR: No se encontró {BALANCE_FILE}")
        print("Asegúrate de ejecutar el script desde el directorio correcto del skill.")
        sys.exit(1)

    print(f"Cargando archivos de Supersociedades... (puede tomar unos segundos)")
    bg = pd.read_excel(BALANCE_FILE)
    er = pd.read_excel(INCOME_FILE)

    # ── Find company ─────────────────────────────────────────────────────────
    bg_match, bg_method = find_company(bg, query)
    er_match, er_method = find_company(er, query)

    if bg_match.empty and er_match.empty:
        print("=" * 60)
        print("RESULTADO: NO ENCONTRADO EN SUPERSOCIEDADES")
        print("=" * 60)
        print(f"Búsqueda: '{query}'")
        print(f"Archivos consultados: {BALANCE_FILE.name}, {INCOME_FILE.name}")
        print()
        print("La empresa no está en los archivos de Supersociedades.")
        print("Posibles razones:")
        print("  - No es vigilada por Supersociedades (empresa muy pequeña o sector no regulado)")
        print("  - No reportó estados financieros en el período disponible (2024)")
        print("  - Nombre/NIT diferente al buscado")
        print()
        print("INSTRUCCIÓN PARA EL REPORTE: Escribir en la sección 4:")
        print('  "No se encontró en Supersociedades. Empresa no vigilada o datos no disponibles."')
        print("  NUNCA inventar cifras financieras.")
        sys.exit(0)

    # Use balance sheet data for company identity
    source_df = bg_match if not bg_match.empty else er_match
    method = bg_method if not bg_match.empty else er_method

    # If multiple companies found, show list and pick largest
    unique_nits = source_df[COL_NIT].unique()
    if len(unique_nits) > 1:
        print(f"Se encontraron {len(unique_nits)} empresas con '{query}':")
        for _, row in source_df[source_df[COL_PERIOD] == 'Periodo Actual'].drop_duplicates(COL_NIT).iterrows():
            print(f"  NIT {row[COL_NIT]}: {row[COL_NAME]} ({row[COL_CITY]})")
        print()
        # Use the first match (could be refined by user providing NIT)
        chosen_nit = unique_nits[0]
        print(f"→ Usando el primero: {chosen_nit}. Si no es la empresa correcta, proporciona el NIT exacto.\n")
        source_df = source_df[source_df[COL_NIT] == chosen_nit]
        bg_match = bg_match[bg_match[COL_NIT] == chosen_nit] if not bg_match.empty else bg_match
        er_match = er_match[er_match[COL_NIT] == chosen_nit] if not er_match.empty else er_match

    # Extract current and prior periods
    bg_curr = bg_match[bg_match[COL_PERIOD] == 'Periodo Actual'].iloc[0] if not bg_match.empty else None
    bg_prev = bg_match[bg_match[COL_PERIOD] == 'Periodo Anterior'].iloc[0] if len(bg_match) > 1 else None
    er_curr = er_match[er_match[COL_PERIOD] == 'Periodo Actual'].iloc[0] if not er_match.empty else None
    er_prev = er_match[er_match[COL_PERIOD] == 'Periodo Anterior'].iloc[0] if len(er_match) > 1 else None

    ref = bg_curr if bg_curr is not None else er_curr

    # ── Calculate KPIs ───────────────────────────────────────────────────────
    def g(row, col):
        """Safely get value from row."""
        if row is None:
            return None
        return row.get(col) if hasattr(row, 'get') else (row[col] if col in row.index else None)

    revenue_curr = g(er_curr, COL_REVENUE)
    revenue_prev = g(er_prev, COL_REVENUE)
    net_income_curr = g(er_curr, COL_NET_INCOME)
    net_income_prev = g(er_prev, COL_NET_INCOME)
    assets_curr = g(bg_curr, COL_ASSETS)
    assets_prev = g(bg_prev, COL_ASSETS)
    liab_curr = g(bg_curr, COL_LIABILITIES)
    equity_curr = g(bg_curr, COL_EQUITY)
    gross_curr = g(er_curr, COL_GROSS)
    gross_prev = g(er_prev, COL_GROSS)
    oper_curr = g(er_curr, COL_OPER_PROFIT)
    oper_prev = g(er_prev, COL_OPER_PROFIT)
    cash_curr = g(bg_curr, COL_CASH)

    # Margin calculations (as raw floats for budget signal)
    try:
        net_margin_f = (float(net_income_curr) / float(revenue_curr)) * 100 if revenue_curr and not pd.isna(revenue_curr) and float(revenue_curr) != 0 else 0
    except (ValueError, TypeError):
        net_margin_f = 0

    try:
        debt_ratio_f = (float(liab_curr) / float(assets_curr)) * 100 if assets_curr and not pd.isna(assets_curr) and float(assets_curr) != 0 else 0
    except (ValueError, TypeError):
        debt_ratio_f = 0

    budget_class, budget_explanation = budget_signal(revenue_curr, net_margin_f, debt_ratio_f)

    # Revenue in USD for display
    try:
        rev_usd = f"~USD ${float(revenue_curr) * 1000 / TRM_USD:,.0f}" if revenue_curr and not pd.isna(revenue_curr) else "N/D"
    except (ValueError, TypeError):
        rev_usd = "N/D"

    # ── Print formatted output ───────────────────────────────────────────────
    print("=" * 70)
    print("SUPERSOCIEDADES — DATOS FINANCIEROS")
    print("=" * 70)
    print(f"Búsqueda: '{query}'  |  Método: {method}")
    print()
    print("── IDENTIFICACIÓN ──────────────────────────────────────────────────")
    print(f"NIT:              {g(ref, COL_NIT)}")
    print(f"Razón social:     {g(ref, COL_NAME)}")
    print(f"CIIU:             {g(ref, COL_CIIU)}")
    print(f"Tipo societario:  {g(ref, COL_TYPE)}")
    print(f"Ciudad:           {g(ref, COL_CITY)}")
    print(f"Departamento:     {g(ref, COL_DEPT)}")
    print(f"Fecha de corte:   {g(ref, COL_CUTOFF)}")
    print()
    print("── ESTADO DE RESULTADOS (COP miles) ───────────────────────────────")
    print(f"{'Concepto':<35} {'Periodo Actual':>18} {'Periodo Anterior':>18} {'Variación':>10}")
    print("-" * 85)
    items_er = [
        ("Ingresos operacionales",        revenue_curr,    revenue_prev),
        ("Costo de ventas",               g(er_curr, COL_COGS), g(er_prev, COL_COGS)),
        ("Ganancia bruta",                gross_curr,      gross_prev),
        ("Gastos de administración",      g(er_curr, COL_ADMIN_EXP), g(er_prev, COL_ADMIN_EXP)),
        ("Gastos de ventas",              g(er_curr, COL_SELL_EXP), g(er_prev, COL_SELL_EXP)),
        ("Utilidad operacional",          oper_curr,       oper_prev),
        ("Utilidad neta",                 net_income_curr, net_income_prev),
    ]
    for label, curr, prev in items_er:
        print(f"{label:<35} {fmt(curr):>18} {fmt(prev):>18} {pct_change(curr, prev):>10}")
    print()
    print("── BALANCE GENERAL (COP miles) ─────────────────────────────────────")
    print(f"{'Concepto':<35} {'Periodo Actual':>18} {'Periodo Anterior':>18} {'Variación':>10}")
    print("-" * 85)
    items_bg = [
        ("Activos corrientes",            g(bg_curr, COL_CURR_ASSETS), g(bg_prev, COL_CURR_ASSETS)),
        ("Efectivo y equivalentes",       cash_curr,       g(bg_prev, COL_CASH)),
        ("Total activos",                 assets_curr,     assets_prev),
        ("Total pasivos",                 liab_curr,       g(bg_prev, COL_LIABILITIES)),
        ("Patrimonio total",              equity_curr,     g(bg_prev, COL_EQUITY)),
    ]
    for label, curr, prev in items_bg:
        print(f"{label:<35} {fmt(curr):>18} {fmt(prev):>18} {pct_change(curr, prev):>10}")
    print()
    print("── INDICADORES CALCULADOS ──────────────────────────────────────────")
    print(f"Margen bruto:             {pct(gross_curr, revenue_curr)}")
    print(f"Margen operacional:       {pct(oper_curr, revenue_curr)}")
    print(f"Margen neto:              {pct(net_income_curr, revenue_curr)}")
    print(f"Razón de endeudamiento:   {pct(liab_curr, assets_curr)}")
    print(f"Ingresos en USD (aprox.): {rev_usd}  (TRM ~$4,200 COP/USD)")
    print()
    print("── SEÑAL DE PRESUPUESTO ────────────────────────────────────────────")
    print(f"Clasificación:  {budget_class}")
    print(f"Explicación:    {budget_explanation}")
    print()
    print("── NOTAS ───────────────────────────────────────────────────────────")
    print("• Valores en miles de pesos colombianos (COP miles)")
    print("• Fuente: Supersociedades Colombia — archivos 210030 y 310030")
    print("• Período Anterior puede ser anual o trimestral según la fecha de corte")
    print("• Para más contexto, verificar el sitio de Supersociedades directamente")
    print("=" * 70)


if __name__ == "__main__":
    main()
