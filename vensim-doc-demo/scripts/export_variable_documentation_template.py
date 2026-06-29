"""Erzeugt eine ausfuellbare CSV fuer die fachliche Variablendokumentation.

Ausfuehrung aus dem Projektroot:

    python scripts/export_variable_documentation_template.py

Standardausgabe:

    docs/variable_documentation.csv

Was das Script macht:
- liest das Vensim-Modell aus data/DiamondDuckTheClean.mdl
- extrahiert technische Informationen je Variable
- erzeugt leere Spalten fuer fachliche Dokumentation
- setzt eine vorgeschlagene Prioritaet und Begruendung
- bewahrt bereits ausgefuellte Doku-Felder, wenn die CSV schon existiert

Optional:

    python scripts/export_variable_documentation_template.py --output docs/my_doc.csv
    python scripts/export_variable_documentation_template.py --include-controls
    python scripts/export_variable_documentation_template.py --model data/MeinModell.mdl
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from libs import ModelInspector, VensimModelParser  # noqa: E402

DEFAULT_MODEL_PATH = PROJECT_ROOT / "data" / "DiamondDuckTheClean.mdl"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "docs" / "variable_documentation.csv"

# Diese Felder kommen automatisch aus dem Vensim-Modell.
TECHNICAL_COLUMNS = [
    "name",
    "kind",
    "units",
    "equation",
    "vensim_comment",
    "views",
    "inputs",
    "outputs",
    "n_inputs",
    "n_outputs",
]

# Diese Felder fuellt ihr manuell aus.
DOCUMENTATION_COLUMNS = [
    "priority",
    "purpose",
    "logic",
    "assumption",
    "source",
    "calibration",
    "interpretation",
    "status",
]

# Diese Felder helfen beim Priorisieren.
HELPER_COLUMNS = [
    "suggested_priority",
    "suggested_reason",
    "needs_source",
    "needs_assumption",
]

OUTPUT_COLUMNS = TECHNICAL_COLUMNS + DOCUMENTATION_COLUMNS + HELPER_COLUMNS

HIGH_PRIORITY_VARIABLES = {
    "Urban Land",
    "Aggricultural Land",
    "Land Conversion Rate",
    "Land Conversion Pressure Factors",
    "AMM Consistent Economic Land Conversion Demand",
    "Max Feasible Conversion",
    "Desired Urban Land Total",
    "Urban Land Gap",
    "Land Demand per Household q",
    "Mean Urban Rent",
    "Desired Mean Urban Rent",
    "Agricultural Rent",
    "Desired Agricultural Rent",
    "Expected Population",
    "Number of Households",
    "Mean Household Size",
    "Income per Capita",
    "Transport Cost per km",
    "Innovation Index",
    "Total Urban Innovation Potential",
}

PARAMETER_KEYWORDS_REQUIRING_SOURCE = [
    "initial",
    "base",
    "minimum",
    "maximum",
    "elasticity",
    "sensitivity",
    "share",
    "factor",
    "exponent",
    "threshold",
    "treshold",  # aktueller Tippfehler im Modell
    "time",
    "cost",
    "kcal",
    "caloric",
    "protection",
    "planning",
    "planing",  # aktueller Tippfehler im Modell
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Erzeugt docs/variable_documentation.csv aus dem Vensim-Modell."
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Pfad zur .mdl-Datei. Standard: data/DiamondDuckTheClean.mdl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Pfad zur Ausgabe-CSV. Standard: docs/variable_documentation.csv",
    )
    parser.add_argument(
        "--include-controls",
        action="store_true",
        help="Auch INITIAL TIME, FINAL TIME, TIME STEP und SAVEPER exportieren.",
    )
    return parser.parse_args()


def resolve_project_path(path: Path) -> Path:
    """Erlaubt relative Pfade ab Projektroot oder absolute Pfade."""
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def load_existing_documentation(path: Path) -> dict[str, dict[str, str]]:
    """
    Lädt bestehende Dokumentationsdaten aus CSV/TSV/Semikolon-CSV.

    Die Funktion ist absichtlich tolerant, weil Excel CSV-Dateien je nach
    Spracheinstellung mit Komma, Semikolon oder Tab speichern kann.
    """
    if not path.exists():
        return {}

    read_attempts = [
        {"sep": ",", "engine": "python"},
        {"sep": ";", "engine": "python"},
        {"sep": "\t", "engine": "python"},
        {"sep": None, "engine": "python"},
    ]

    last_error = None

    for kwargs in read_attempts:
        try:
            existing_df = pd.read_csv(
                path,
                dtype=str,
                encoding="utf-8-sig",
                on_bad_lines="warn",
                **kwargs,
            ).fillna("")

            if "name" in existing_df.columns:
                existing = {}

                for _, row in existing_df.iterrows():
                    variable_name = str(row.get("name", "")).strip()

                    if not variable_name:
                        continue

                    existing[variable_name] = {
                        column: str(row.get(column, "")).strip()
                        for column in existing_df.columns
                    }

                print(f"Bestehende Dokumentation geladen: {len(existing)} Variablen")
                return existing

        except Exception as error:
            last_error = error

    raise ValueError(
        f"Die Datei {path} konnte nicht als CSV/TSV gelesen werden. "
        f"Letzter Fehler: {last_error}"
    )


def needs_source(variable_name: str, kind: str) -> bool:
    name_lower = variable_name.lower()
    if kind in {"stock", "flow", "lookup"}:
        return True
    if kind == "constant" and any(keyword in name_lower for keyword in PARAMETER_KEYWORDS_REQUIRING_SOURCE):
        return True
    return False


def needs_assumption(variable_name: str, kind: str) -> bool:
    name_lower = variable_name.lower()
    if kind in {"stock", "flow", "lookup"}:
        return True
    if kind == "constant" and any(
        keyword in name_lower
        for keyword in ["factor", "share", "elasticity", "sensitivity", "exponent", "threshold", "treshold"]
    ):
        return True
    return False


def suggest_priority(
    variable_name: str,
    kind: str,
    documentation: str,
    n_inputs: int,
    n_outputs: int,
) -> tuple[str, str]:
    reasons: list[str] = []

    if variable_name in HIGH_PRIORITY_VARIABLES:
        reasons.append("zentrale Variable aus empfohlener Startliste")

    if kind in {"stock", "flow", "lookup"}:
        reasons.append(f"{kind} sollte fachlich erklaert werden")

    if kind == "constant" and needs_source(variable_name, kind):
        reasons.append("Parameter/Konstante braucht Quelle oder Wertbegruendung")

    if not documentation.strip():
        reasons.append("kein Vensim-Kommentar vorhanden")
    elif len(documentation.strip()) < 60:
        reasons.append("Vensim-Kommentar ist sehr kurz")

    if n_inputs + n_outputs >= 6:
        reasons.append("stark vernetzt")

    if kind == "control":
        return "low", "technische Simulationssteuerung"

    if any(
        reason in reasons
        for reason in [
            "zentrale Variable aus empfohlener Startliste",
            f"{kind} sollte fachlich erklaert werden",
            "kein Vensim-Kommentar vorhanden",
        ]
    ):
        return "high", "; ".join(reasons)

    if reasons:
        return "medium", "; ".join(reasons)

    return "low", "technisch extrahiert; vermutlich nur bei Bedarf vertiefen"


def build_rows(model_path: Path, include_controls: bool, existing: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    model = VensimModelParser(model_path).parse()
    inspector = ModelInspector(model)
    view_map = inspector.variable_to_views()

    rows: list[dict[str, Any]] = []

    for name in model.variable_names():
        variable = model.variables[name]

        if variable.kind == "control" and not include_controls:
            continue

        inputs = variable.dependencies
        outputs = inspector.downstream_variables(name)
        views = view_map.get(name, [])
        suggested_priority, suggested_reason = suggest_priority(
            variable_name=name,
            kind=variable.kind,
            documentation=variable.documentation,
            n_inputs=len(inputs),
            n_outputs=len(outputs),
        )

        old = existing.get(name, {})

        row: dict[str, Any] = {
            "name": name,
            "kind": variable.kind,
            "units": variable.units,
            "equation": variable.equation,
            "vensim_comment": variable.documentation,
            "views": "; ".join(views),
            "inputs": "; ".join(inputs),
            "outputs": "; ".join(outputs),
            "n_inputs": len(inputs),
            "n_outputs": len(outputs),
            # Manuelle Felder: bestehende Inhalte behalten, sonst Vorschlag setzen.
            "priority": old.get("priority", suggested_priority) or suggested_priority,
            "purpose": old.get("purpose", ""),
            "logic": old.get("logic", ""),
            "assumption": old.get("assumption", ""),
            "source": old.get("source", ""),
            "calibration": old.get("calibration", ""),
            "interpretation": old.get("interpretation", ""),
            "status": old.get("status", "todo") or "todo",
            "suggested_priority": suggested_priority,
            "suggested_reason": suggested_reason,
            "needs_source": needs_source(name, variable.kind),
            "needs_assumption": needs_assumption(name, variable.kind),
        }
        rows.append(row)

    priority_order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(key=lambda r: (priority_order.get(str(r["priority"]), 9), str(r["kind"]), str(r["name"])))
    return rows


def main() -> None:
    args = parse_args()
    model_path = resolve_project_path(args.model)
    output_path = resolve_project_path(args.output)

    if not model_path.exists():
        raise FileNotFoundError(f"Modell nicht gefunden: {model_path}")

    existing = load_existing_documentation(output_path)
    rows = build_rows(model_path=model_path, include_controls=args.include_controls, existing=existing)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Geschrieben: {output_path.relative_to(PROJECT_ROOT)}")
    print(f"Variablen exportiert: {len(df)}")
    print("Prioritaeten:")
    print(df["priority"].value_counts().to_string())
    print("\nNaechster Schritt: CSV oeffnen und purpose / logic / assumption / source ergaenzen.")


if __name__ == "__main__":
    main()
