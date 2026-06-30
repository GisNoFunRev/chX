"""Erzeugt die statischen Daten fuer die HTML-Variablensuche.

Ausfuehrung aus dem Projektroot:

    python scripts/build_search_assets.py

Die Ausgabe landet in:

    assets/model_search_data.js

Diese Datei wird von der Quarto-HTML-Seite im Browser gelesen.

Zusatzdokumentation:
    Wenn docs/variable_documentation.csv vorhanden ist, werden die fachlichen
    Felder purpose, logic, assumption, source, calibration, interpretation und
    status pro Variable in die Suchdaten integriert.

Performance-Hinweis:
    Standardmaessig werden bestehende SVG-Grafiken aus assets/model_search_data.js
    wiederverwendet. Dadurch ist das Aktualisieren der CSV-Dokumentation schnell.
    Falls du nach Modellstruktur-Aenderungen alle Graphen neu bauen willst:

        python scripts/build_search_assets.py --regenerate-graphs
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from libs import ModelInspector, VensimModelParser
from libs.model_graph import GraphvizModelVisualizer, ModelGraphBuilder

MODEL_PATH = PROJECT_ROOT / "data" / "DiamondDuckTheClean.mdl"
DOC_PATH = PROJECT_ROOT / "docs" / "variable_documentation.csv"
OUTPUT_PATH = PROJECT_ROOT / "assets" / "model_search_data.js"

DOC_FIELDS = [
    "purpose",
    "logic",
    "assumption",
    "source",
    "calibration",
    "interpretation",
    "status",
]

JS_PREFIX = "window.VENSIM_SEARCH_DATA = "


def detect_delimiter(csv_path: Path) -> str:
    """Erkennt Komma, Semikolon oder Tab als CSV-Trennzeichen."""
    first_lines = csv_path.read_text(encoding="utf-8-sig", errors="ignore")[:4096]
    try:
        dialect = csv.Sniffer().sniff(first_lines, delimiters=",;\t")
        return dialect.delimiter
    except csv.Error:
        header = first_lines.splitlines()[0] if first_lines.splitlines() else ""
        if "\t" in header:
            return "\t"
        if ";" in header:
            return ";"
        return ","


def load_variable_documentation(csv_path: Path) -> dict[str, dict[str, str]]:
    """Liest optionale fachliche Dokumentation aus docs/variable_documentation.csv."""
    if not csv_path.exists():
        print(f"Keine zusätzliche Dokumentationsdatei gefunden: {csv_path}")
        return {}

    delimiter = detect_delimiter(csv_path)
    documentation: dict[str, dict[str, str]] = {}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=delimiter)

        if not reader.fieldnames or "name" not in reader.fieldnames:
            raise ValueError("Die Dokumentations-CSV braucht eine Spalte 'name'.")

        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue

            documentation[name] = {
                field: (row.get(field) or "").strip()
                for field in DOC_FIELDS
            }

    print(f"Loaded documentation for {len(documentation)} variables from {csv_path.name}")
    return documentation


def load_existing_graphs(output_path: Path) -> dict[str, str]:
    """Laedt bestehende SVG-Graphen aus assets/model_search_data.js, falls vorhanden."""
    if not output_path.exists():
        return {}

    text = output_path.read_text(encoding="utf-8", errors="ignore").strip()
    if not text.startswith(JS_PREFIX):
        return {}

    json_text = text[len(JS_PREFIX):].strip()
    if json_text.endswith(";"):
        json_text = json_text[:-1]

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError:
        return {}

    graphs = {
        variable.get("name", ""): variable.get("graphSvg", "")
        for variable in payload.get("variables", [])
        if variable.get("name") and variable.get("graphSvg")
    }

    print(f"Reusing {len(graphs)} existing SVG graphs")
    return graphs


def build_payload(regenerate_graphs: bool = False) -> dict:
    model = VensimModelParser(MODEL_PATH).parse()
    inspector = ModelInspector(model)
    view_map = inspector.variable_to_views()
    documentation_by_name = load_variable_documentation(DOC_PATH)
    existing_graphs = {} if regenerate_graphs else load_existing_graphs(OUTPUT_PATH)

    graphs: GraphvizModelVisualizer | None = None
    if regenerate_graphs or len(existing_graphs) < len(model.variables):
        graph_builder = ModelGraphBuilder(model)
        graphs = GraphvizModelVisualizer(graph_builder)

    variables = []
    variable_names = model.variable_names()

    for index, name in enumerate(variable_names, start=1):
        variable = model.variables[name]
        downstream = inspector.downstream_variables(name)
        views = view_map.get(name, [])
        extra_doc = documentation_by_name.get(variable.name, {})

        graph_svg = existing_graphs.get(name, "")
        if not graph_svg and graphs is not None:
            try:
                graph_svg = graphs.draw_neighborhood_svg(
                    target=name,
                    upstream_depth=2,
                    downstream_depth=2,
                    show_units=True,
                    show_kind=True,
                )
            except Exception as exc:  # noqa: BLE001 - generation should not fail the whole export
                graph_svg = f"<p>Grafik konnte nicht erzeugt werden: {exc}</p>"

        variables.append(
            {
                "name": variable.name,
                "kind": variable.kind,
                "units": variable.units,
                "equation": variable.equation,
                "documentation": variable.documentation,
                "shortDocumentation": variable.short_documentation(),
                "purpose": extra_doc.get("purpose", ""),
                "logic": extra_doc.get("logic", ""),
                "assumption": extra_doc.get("assumption", ""),
                "source": extra_doc.get("source", ""),
                "calibration": extra_doc.get("calibration", ""),
                "interpretation": extra_doc.get("interpretation", ""),
                "documentationStatus": extra_doc.get("status", ""),
                "upstream": variable.dependencies,
                "downstream": downstream,
                "views": views,
                "graphSvg": graph_svg,
            }
        )

        if index % 25 == 0:
            print(f"Exported {index}/{len(variable_names)} variables")

    return {
        "modelPath": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
        "documentationPath": str(DOC_PATH.relative_to(PROJECT_ROOT)) if DOC_PATH.exists() else "",
        "nVariables": len(variables),
        "nDependencies": len(model.dependencies),
        "nViews": len(model.views),
        "variables": variables,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--regenerate-graphs",
        action="store_true",
        help="Alle Graphviz-SVGs neu erzeugen. Dauert deutlich laenger.",
    )
    args = parser.parse_args()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload(regenerate_graphs=args.regenerate_graphs)
    js = JS_PREFIX + json.dumps(payload, ensure_ascii=False) + ";\n"
    OUTPUT_PATH.write_text(js, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Variables: {payload['nVariables']}")
    print(f"Documentation CSV: {payload['documentationPath'] or 'not used'}")


if __name__ == "__main__":
    main()
