"""Erzeugt die statischen Daten fuer die HTML-Variablensuche.

Ausfuehrung aus dem Projektroot:

    python scripts/build_search_assets.py

Die Ausgabe landet in:

    assets/model_search_data.js

Diese Datei wird von der Quarto-HTML-Seite im Browser gelesen.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from libs import ModelInspector, VensimModelParser
from libs.model_graph import GraphvizModelVisualizer, ModelGraphBuilder

MODEL_PATH = PROJECT_ROOT / "data" / "DiamondDuckTheClean.mdl"
OUTPUT_PATH = PROJECT_ROOT / "assets" / "model_search_data.js"


def build_payload() -> dict:
    model = VensimModelParser(MODEL_PATH).parse()
    inspector = ModelInspector(model)
    graph_builder = ModelGraphBuilder(model)
    graphs = GraphvizModelVisualizer(graph_builder)
    view_map = inspector.variable_to_views()

    variables = []
    variable_names = model.variable_names()

    for index, name in enumerate(variable_names, start=1):
        variable = model.variables[name]
        downstream = inspector.downstream_variables(name)
        views = view_map.get(name, [])

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
        "nVariables": len(variables),
        "nDependencies": len(model.dependencies),
        "nViews": len(model.views),
        "variables": variables,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    js = "window.VENSIM_SEARCH_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n"
    OUTPUT_PATH.write_text(js, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Variables: {payload['nVariables']}")


if __name__ == "__main__":
    main()
