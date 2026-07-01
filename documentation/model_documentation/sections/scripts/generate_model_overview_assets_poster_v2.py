#!/usr/bin/env vensim
"""
Generate graphical overview assets for a Vensim .mdl model.

Outputs:
- model_variables.csv
- model_edges.csv
- model_views.csv
- model_view_edges.csv
- model_overview_by_view.svg / .png
- model_view_dependency_map.svg / .png

The script is intentionally standalone so it works even if the existing
Vensim/Quarto helper classes are not available in the project yet.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


SKETCH_MARKER_RE = re.compile(r"\\{3}---/// Sketch information[^\n]*", re.MULTILINE)
MODEL_FUNCTIONS = {
    "ABS", "ARCCOS", "ARCSIN", "ARCTAN", "COS", "EXP", "IF", "THEN", "ELSE",
    "INTEGER", "LN", "LOG", "MAX", "MIN", "MODULO", "PULSE", "RAMP", "SIN",
    "SQRT", "STEP", "TAN", "WITH", "LOOKUP", "ZIDZ", "XIDZ", "SMOOTH",
    "DELAY", "FIXED", "TREND", "SAMPLE", "RANDOM", "NORMAL", "INITIAL", "INTEG",
}
CONTROL_VARIABLES = {"INITIAL TIME", "FINAL TIME", "SAVEPER", "TIME STEP"}

# Semantic groups used only for the overview graphics.
# They do not change the model equations; they only make the generated SVGs easier to read.
MACRO_VIEW = "Macro_Ebene"
AMM_DYNAMIC_VIEWS = {
    "01_Population_Household",
    "02_Transport_and_Commuting",
    "03_Income_and_Productivity",
    "04_Urban_Rent_and_Land_Tightness",
}
AMM_LOGIC_VIEWS = {
    "05_AMM_Budget_and_Housing_Demand",
    "08_Agriculture_and_Scarcity",
    "09_Urban_Land_Conversion_Logic",
    "10_Soil_Protection_and_Agricultural_Pressure",
}
WEST_COURT = {
    "11_Innovation_and_City_Size"
}
COBB_DOUG = {
    "07_Cobb_Douglas_Utility",
}
# A small additional variable-level heuristic. This catches central AMM variables even
# when they are shown from another view or occur in the macro layer.
AMM_RELEVANT_KEYWORDS = (
    "amm", "budget", "housing", "rent", "land demand", "urban land",
    "agricultural", "conversion", "cobb", "utility", "scarcity",
)


@dataclass
class VensimVariable:
    name: str
    equation: str
    units: str = ""
    documentation: str = ""
    var_type: str = "Auxiliary"
    primary_view: str = "Unassigned"
    views: list[str] = field(default_factory=list)
    in_degree: int = 0
    out_degree: int = 0


@dataclass
class ViewOccurrence:
    view: str
    name: str
    node_id: str
    x: float
    y: float


def clean_text(value: str) -> str:
    value = value.replace("\\\n", " ")
    value = value.replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", value).strip()


def parse_variable_chunk(chunk: str) -> VensimVariable | None:
    chunk = chunk.strip()
    if not chunk:
        return None
    chunk = chunk.replace("{UTF-8}", "").strip()
    if "=" not in chunk or "~" not in chunk:
        return None

    parts = chunk.split("~")
    left = parts[0].strip()
    if "=" not in left:
        return None

    name, equation = left.split("=", 1)
    name = clean_text(name)
    equation = clean_text(equation)
    if not name:
        return None

    units = clean_text(parts[1]) if len(parts) > 1 else ""
    documentation = clean_text(" ".join(parts[2:])) if len(parts) > 2 else ""
    return VensimVariable(name=name, equation=equation, units=units, documentation=documentation)


def parse_equations(text: str) -> dict[str, VensimVariable]:
    equation_part = SKETCH_MARKER_RE.split(text, maxsplit=1)[0]
    variables: dict[str, VensimVariable] = {}
    for chunk in equation_part.split("|"):
        variable = parse_variable_chunk(chunk)
        if variable:
            variables[variable.name] = variable
    return variables


def parse_views(text: str, model_variable_names: set[str]) -> tuple[list[str], list[ViewOccurrence], dict[str, set[str]]]:
    view_names: list[str] = []
    occurrences: list[ViewOccurrence] = []
    view_to_vars: dict[str, set[str]] = defaultdict(set)

    sections = SKETCH_MARKER_RE.split(text)
    # Section 0 is the equation part. Every later section should contain one sketch view.
    for section in sections[1:]:
        section = section.split("///---\\\\\\", 1)[0]
        lines = [line.rstrip("\n") for line in section.splitlines() if line.strip()]
        view_name = None
        for line in lines:
            if line.startswith("*") and not line.startswith("********************************************************"):
                view_name = line[1:].strip()
                break
        if not view_name:
            continue
        view_names.append(view_name)

        for line in lines:
            if not line.startswith("10,"):
                continue
            try:
                row = next(csv.reader([line]))
            except Exception:
                continue
            if len(row) < 5:
                continue
            node_id = row[1].strip()
            name = row[2].strip()
            if name not in model_variable_names:
                continue
            try:
                x = float(row[3])
                y = float(row[4])
            except ValueError:
                x = 0.0
                y = 0.0
            occurrences.append(ViewOccurrence(view=view_name, name=name, node_id=node_id, x=x, y=y))
            view_to_vars[view_name].add(name)

    return view_names, occurrences, view_to_vars


def build_dependency_edges(variables: dict[str, VensimVariable]) -> list[tuple[str, str]]:
    names = sorted(variables.keys(), key=len, reverse=True)
    escaped = [re.escape(name) for name in names]
    # Match variable names as complete model identifiers, not as substrings of longer names.
    pattern = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(escaped) + r")(?![A-Za-z0-9_])")

    edges: set[tuple[str, str]] = set()
    for target, variable in variables.items():
        rhs = variable.equation.replace('"', "")
        for match in pattern.finditer(rhs):
            source = match.group(1)
            if source != target:
                edges.add((source, target))
    return sorted(edges)


def split_top_level_args(function_call: str) -> list[str]:
    start = function_call.find("(")
    end = function_call.rfind(")")
    if start == -1 or end == -1 or end <= start:
        return []
    inner = function_call[start + 1 : end]
    args: list[str] = []
    level = 0
    current = []
    for ch in inner:
        if ch == "(":
            level += 1
        elif ch == ")":
            level -= 1
        if ch == "," and level == 0:
            args.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        args.append("".join(current).strip())
    return args


def classify_variables(variables: dict[str, VensimVariable], edges: list[tuple[str, str]]) -> None:
    graph = nx.DiGraph()
    graph.add_nodes_from(variables)
    graph.add_edges_from(edges)

    # Variables used in the first INTEG argument are treated as flows/rates.
    variable_names = sorted(variables.keys(), key=len, reverse=True)
    flow_names: set[str] = set()
    for variable in variables.values():
        if variable.equation.strip().upper().startswith("INTEG"):
            args = split_top_level_args(variable.equation)
            if args:
                first_arg = args[0]
                for name in variable_names:
                    if name == variable.name:
                        continue
                    if re.search(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", first_arg):
                        # Initial values in INTEG are not flows; skip obvious initial/reference values.
                        if not name.lower().startswith(("initial ", "reference initial")):
                            flow_names.add(name)

    for name, variable in variables.items():
        eq_upper = variable.equation.strip().upper()
        dependency_count = sum(1 for source, target in edges if target == name)
        numeric_constant = re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?", variable.equation.strip()) is not None

        if name.upper() in CONTROL_VARIABLES:
            variable.var_type = "Control"
        elif eq_upper.startswith("INTEG"):
            variable.var_type = "Stock"
        elif "WITH LOOKUP" in eq_upper:
            variable.var_type = "Lookup"
        elif name in flow_names:
            variable.var_type = "Flow"
        elif numeric_constant or dependency_count == 0:
            variable.var_type = "Parameter"
        elif any(token in eq_upper for token in ("MAX(", "MIN(", "ZIDZ(", "XIDZ(", "IF THEN ELSE")):
            variable.var_type = "Decision / Guard"
        elif any(word in name.lower() for word in ("index", "gap", "error", "total", "potential")):
            variable.var_type = "KPI / Output"
        else:
            variable.var_type = "Auxiliary"

        variable.in_degree = int(graph.in_degree(name)) if name in graph else 0
        variable.out_degree = int(graph.out_degree(name)) if name in graph else 0


def assign_views(
    variables: dict[str, VensimVariable],
    view_names: list[str],
    view_to_vars: dict[str, set[str]],
) -> None:
    preferred_views = [v for v in view_names if v not in {"00_Legend", "Macro_Ebene"}]
    fallback_views = view_names

    for variable in variables.values():
        variable.views = [view for view in view_names if variable.name in view_to_vars.get(view, set())]
        primary = None
        for view in preferred_views:
            if variable.name in view_to_vars.get(view, set()):
                primary = view
                break
        if primary is None:
            for view in fallback_views:
                if variable.name in view_to_vars.get(view, set()):
                    primary = view
                    break
        variable.primary_view = primary or "Unassigned"


def build_view_edges(variables: dict[str, VensimVariable], edges: list[tuple[str, str]]) -> list[tuple[str, str, int]]:
    counts: Counter[tuple[str, str]] = Counter()
    for source, target in edges:
        source_view = variables[source].primary_view
        target_view = variables[target].primary_view
        if source_view == target_view or source_view == "Unassigned" or target_view == "Unassigned":
            continue
        counts[(source_view, target_view)] += 1
    return [(source, target, weight) for (source, target), weight in sorted(counts.items())]


def write_tables(
    variables: dict[str, VensimVariable],
    edges: list[tuple[str, str]],
    view_names: list[str],
    view_to_vars: dict[str, set[str]],
    view_edges: list[tuple[str, str, int]],
    out_dir: Path,
) -> None:
    variable_rows = []
    for variable in sorted(variables.values(), key=lambda item: (item.primary_view, item.var_type, item.name)):
        variable_rows.append(
            {
                "name": variable.name,
                "type": variable.var_type,
                "units": variable.units,
                "primary_view": variable.primary_view,
                "views": "; ".join(variable.views),
                "view_count": len(variable.views),
                "inputs": variable.in_degree,
                "outputs": variable.out_degree,
                "degree": variable.in_degree + variable.out_degree,
                "equation": variable.equation,
                "documentation": variable.documentation,
            }
        )
    pd.DataFrame(variable_rows).to_csv(out_dir / "model_variables.csv", index=False)
    pd.DataFrame([{"source": s, "target": t} for s, t in edges]).to_csv(out_dir / "model_edges.csv", index=False)
    pd.DataFrame([{"source_view": s, "target_view": t, "weight": w} for s, t, w in view_edges]).to_csv(
        out_dir / "model_view_edges.csv", index=False
    )

    graph = nx.DiGraph()
    graph.add_nodes_from(variables)
    graph.add_edges_from(edges)

    view_rows = []
    for view in view_names + (["Unassigned"] if any(v.primary_view == "Unassigned" for v in variables.values()) else []):
        names = [name for name, variable in variables.items() if variable.primary_view == view]
        type_counts = Counter(variables[name].var_type for name in names)
        incoming = sum(1 for s, t in edges if variables[t].primary_view == view and variables[s].primary_view != view)
        outgoing = sum(1 for s, t in edges if variables[s].primary_view == view and variables[t].primary_view != view)
        view_rows.append(
            {
                "view": view,
                "variables": len(names),
                "stocks": type_counts.get("Stock", 0),
                "flows": type_counts.get("Flow", 0),
                "parameters": type_counts.get("Parameter", 0),
                "lookups": type_counts.get("Lookup", 0),
                "auxiliaries": type_counts.get("Auxiliary", 0),
                "guards": type_counts.get("Decision / Guard", 0),
                "kpis": type_counts.get("KPI / Output", 0),
                "incoming_cross_view_edges": incoming,
                "outgoing_cross_view_edges": outgoing,
            }
        )
    pd.DataFrame(view_rows).to_csv(out_dir / "model_views.csv", index=False)


def _shorten_label(text: str, max_len: int = 28) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def view_category(view_name: str) -> str:
    """Return the semantic role of a Vensim view for visual styling."""
    if view_name == MACRO_VIEW:
        return "macro"
    if view_name in AMM_DYNAMIC_VIEWS:
        return "amm_dynamic"
    if view_name in AMM_LOGIC_VIEWS:
        return "amm_logic"
    if view_name in WEST_COURT:
        return "westcourt"
    if view_name in COBB_DOUG:
        return "cobb_doug"
    if view_name in {"Unassigned", "00_Legend"}:
        return "technical"
    return "other"


def is_amm_relevant_variable(variable: VensimVariable) -> bool:
    """Heuristic used only for highlighting central AMM variables in the graph."""
    if variable.primary_view in AMM_LOGIC_VIEWS:
        return True
    text = f"{variable.name} {variable.equation} {variable.documentation}".lower()
    return any(keyword in text for keyword in AMM_RELEVANT_KEYWORDS)


def draw_overview_by_view(
    variables: dict[str, VensimVariable],
    edges: list[tuple[str, str]],
    occurrences: list[ViewOccurrence],
    view_names: list[str],
    out_dir: Path,
) -> None:
    """Draw a poster-oriented semantic full-model overview grouped by Vensim views.

    Poster-specific changes compared with the earlier overview:
    - A0-like portrait layout.
    - Macro_Ebene is deliberately flatter because it contains few nodes.
    - The grey Unassigned panel is not drawn.
    - Text and legend are enlarged for presentation use.
    - The legend is an explanatory box placed in the free area to the right of
      11_Innovation_and_City_Size.
    - Urban Land and Agricultural Land are highlighted as red, larger stock nodes.
    - High-degree nodes are gently pulled toward the centre of their own view box,
      while low-degree nodes stay closer to their original Vensim sketch position.
      This is not a full re-layout; the Vensim sketch remains the basis.
    """
    from matplotlib.lines import Line2D
    import matplotlib.patheffects as pe

    # -------------------------------------------------------------------------
    # Poster controls: change these if the poster still feels too dense.
    # -------------------------------------------------------------------------
    POSTER_FIGSIZE = (23.4, 33.1)  # A0 ratio in inches, portrait orientation.
    FONT_SCALE = 2.0
    MACRO_HEIGHT = 0.42
    CELL_W = 1.0
    CELL_H = 0.82
    COLS = 3
    INNER_MARGIN_X = 0.09
    INNER_MARGIN_TOP = 0.18
    INNER_MARGIN_BOTTOM = 0.12
    HUB_PULL_MAX = 0.30  # 0=no pull; 1=all high-degree nodes to panel centre.
    IMPORTANT_STOCKS = {"Urban Land", "Agricultural Land"}

    semantic_styles = {
        "macro": {
            "label": "Macro-Ebene / zentrale Übersicht",
            "face": "#FFF3BF",
            "edge": "#B7791F",
            "node": "#F6AD55",
            "marker": "s",
            "panel_lw": 2.8,
        },
        "amm_dynamic": {
            "label": "AMM-Dynamisierung, Views 01-04",
            "face": "#E3F2FD",
            "edge": "#1565C0",
            "node": "#4299E1",
            "marker": "o",
            "panel_lw": 1.8,
        },
        "amm_logic": {
            "label": "AMM-relevante Kernlogik",
            "face": "#FFF3E0",
            "edge": "#EF6C00",
            "node": "#ED8936",
            "marker": "D",
            "panel_lw": 1.8,
        },
        "other": {
            "label": "Weitere Modellteile",
            "face": "#FAFAFA",
            "edge": "#9E9E9E",
            "node": "#718096",
            "marker": "o",
            "panel_lw": 1.2,
        },
        "westcourt": {
            "label": "West-Bettencourt / Innovation und Stadtgrösse",
            "face": "#F1BEE3",
            "edge": "#9E9E9E",
            "node": "#718096",
            "marker": "o",
            "panel_lw": 1.2,
        },
        "cobb_doug": {
            "label": "Cobb-Douglas Nutzenlogik",
            "face": "#E6FFFA",
            "edge": "#2C7A7B",
            "node": "#38B2AC",
            "marker": "h",
            "panel_lw": 1.6,
        },
        "technical": {
            "label": "Technisch / nicht zugewiesen",
            "face": "#F5F5F5",
            "edge": "#BDBDBD",
            "node": "#A0AEC0",
            "marker": "X",
            "panel_lw": 1.0,
        },
    }

    detail_views = [v for v in view_names if v not in {"00_Legend", "Unassigned"}]
    if not detail_views:
        detail_views = sorted({variable.primary_view for variable in variables.values() if variable.primary_view != "Unassigned"})

    def view_sort_key(view: str) -> tuple[int, str]:
        if view == MACRO_VIEW:
            return (-1, view)
        prefix = view.split("_", 1)[0]
        if prefix.isdigit():
            return (int(prefix), view)
        return (999, view)

    detail_views = sorted(detail_views, key=view_sort_key)
    macro_present = MACRO_VIEW in detail_views
    non_macro_views = [v for v in detail_views if v != MACRO_VIEW]
    grid_rows = math.ceil(len(non_macro_views) / COLS) if non_macro_views else 0

    fig, ax = plt.subplots(figsize=POSTER_FIGSIZE)
    ax.set_axis_off()

    occs_by_view: dict[str, list[ViewOccurrence]] = defaultdict(list)
    for occ in occurrences:
        occs_by_view[occ.view].append(occ)

    node_pos: dict[str, tuple[float, float]] = {}
    view_box: dict[str, tuple[float, float, float, float]] = {}

    max_degree = max((v.in_degree + v.out_degree for v in variables.values()), default=1)
    ranked = sorted(variables.values(), key=lambda v: v.in_degree + v.out_degree, reverse=True)
    hub_names = {v.name for v in ranked[:30]}
    important_types = {"Stock", "Flow", "Lookup", "KPI / Output"}

    def variable_category(variable: VensimVariable) -> str:
        if variable.primary_view == MACRO_VIEW:
            return "macro"
        if variable.primary_view in AMM_DYNAMIC_VIEWS:
            return "amm_dynamic"
        if variable.primary_view in AMM_LOGIC_VIEWS or is_amm_relevant_variable(variable):
            return "amm_logic"
        if variable.primary_view in {"Unassigned", "00_Legend"}:
            return "technical"
        if variable.primary_view in WEST_COURT:
            return "westcourt"
        if variable.primary_view in COBB_DOUG:
            return "cobb_doug"
        return "other"

    def should_label(variable: VensimVariable) -> bool:
        return (
            variable.name in IMPORTANT_STOCKS
            or variable.primary_view == MACRO_VIEW
            or variable.var_type in important_types
            or variable.name in hub_names
            or variable.primary_view in {"05_AMM_Budget_and_Housing_Demand", "09_Urban_Land_Conversion_Logic"}
        )

    def node_size_for_name(name: str) -> float:
        variable = variables[name]
        degree = variable.in_degree + variable.out_degree
        if name in IMPORTANT_STOCKS:
            return 650
        category = variable_category(variable)
        base = 80 if category != "macro" else 180
        scale = 230 if category != "macro" else 330
        return base + scale * math.sqrt(degree + 1) / math.sqrt(max_degree + 1)

    def add_view_panel(view: str, x0: float, y0: float, w: float, h: float) -> None:
        category = view_category(view)
        style = semantic_styles[category]
        view_box[view] = (x0, y0, w, h)

        rect = plt.Rectangle(
            (x0 + 0.02, y0 - h + 0.035),
            w - 0.04,
            h - 0.07,
            facecolor=style["face"],
            edgecolor=style["edge"],
            linewidth=style["panel_lw"] * 1.25,
            alpha=0.88,
            zorder=0,
        )
        ax.add_patch(rect)

        title_size = (9.0 if view == MACRO_VIEW else 6.6) * FONT_SCALE
        ax.text(
            x0 + 0.04,
            y0 - 0.030,
            view,
            fontsize=title_size,
            fontweight="bold",
            color=style["edge"],
            va="top",
            zorder=5,
        )
        if view == MACRO_VIEW:
            ax.text(
                x0 + w - 0.05,
                y0 - 0.032,
                "zentrale Modellübersicht",
                fontsize=5.6 * FONT_SCALE,
                color=style["edge"],
                va="top",
                ha="right",
                zorder=5,
            )

        view_occs = [o for o in occs_by_view.get(view, []) if variables[o.name].primary_view == view]
        if not view_occs:
            return

        min_x, max_x = min(o.x for o in view_occs), max(o.x for o in view_occs)
        min_y, max_y = min(o.y for o in view_occs), max(o.y for o in view_occs)
        span_x = max(max_x - min_x, 1.0)
        span_y = max(max_y - min_y, 1.0)
        centre_x = x0 + 0.50 * w
        centre_y = y0 - 0.52 * h

        for occ in view_occs:
            # Original Vensim sketch position, mapped into the panel.
            px = x0 + INNER_MARGIN_X * w + (1 - 2 * INNER_MARGIN_X) * w * ((occ.x - min_x) / span_x)
            py = y0 - INNER_MARGIN_TOP * h - (1 - INNER_MARGIN_TOP - INNER_MARGIN_BOTTOM) * h * ((occ.y - min_y) / span_y)

            # Degree-based inward pull. High-degree nodes move gently toward the panel centre.
            degree = variables[occ.name].in_degree + variables[occ.name].out_degree
            degree_ratio = math.sqrt(degree + 1) / math.sqrt(max_degree + 1)
            pull = HUB_PULL_MAX * degree_ratio
            px = px * (1 - pull) + centre_x * pull
            py = py * (1 - pull) + centre_y * pull

            # Safety clamp: no node should touch the box border.
            px = min(max(px, x0 + 0.08 * w), x0 + 0.92 * w)
            py = min(max(py, y0 - 0.88 * h), y0 - 0.16 * h)
            node_pos[occ.name] = (px, py)

    y_cursor = 0.0
    if macro_present:
        add_view_panel(MACRO_VIEW, 0.0, y_cursor, COLS * CELL_W, MACRO_HEIGHT)
        y_cursor -= MACRO_HEIGHT

    for idx, view in enumerate(non_macro_views):
        row = idx // COLS
        col = idx % COLS
        x0 = col * CELL_W
        y0 = y_cursor - row * CELL_H
        add_view_panel(view, x0, y0, CELL_W, CELL_H)

    # Deliberately do not draw the old grey Unassigned panel.
    # Variables without a Vensim sketch position are omitted from this poster view.

    def clamp_to_panel(view: str, x: float, y: float) -> tuple[float, float]:
        """Keep a node clearly inside its view panel."""
        x0, y0, w, h = view_box[view]
        x = min(max(x, x0 + 0.085 * w), x0 + 0.915 * w)
        y = min(max(y, y0 - 0.865 * h), y0 - 0.175 * h)
        return x, y

    def separate_close_nodes() -> None:
        """
        Reduce local node and label collisions without replacing the Vensim layout.

        Rule used for the poster: if two nodes are close in the same panel, they
        should not sit on the same horizontal line. The algorithm therefore applies
        a small vertical separation, stronger for high-degree nodes but always
        clamped inside the panel.
        """
        names_by_view: dict[str, list[str]] = defaultdict(list)
        for name in node_pos:
            view = variables[name].primary_view
            if view in view_box:
                names_by_view[view].append(name)

        for view, names in names_by_view.items():
            if len(names) < 2:
                continue
            x0, y0, w, h = view_box[view]
            min_dx = 0.105 * w
            min_dy = 0.070 * h
            for _ in range(7):
                for i, name_i in enumerate(names):
                    xi, yi = node_pos[name_i]
                    for j in range(i + 1, len(names)):
                        name_j = names[j]
                        xj, yj = node_pos[name_j]
                        close_x = abs(xj - xi) < min_dx
                        close_y = abs(yj - yi) < min_dy
                        if not (close_x and close_y):
                            continue

                        # If both nodes are nearly on the same horizontal height,
                        # move them in opposite vertical directions.
                        if abs(yj - yi) < 1e-6:
                            direction = 1 if (i + j) % 2 == 0 else -1
                        else:
                            direction = 1 if yj > yi else -1
                        shift = 0.5 * (min_dy - abs(yj - yi)) + 0.004 * h

                        # Keep the stronger hub a little closer to its current
                        # position and move the weaker node slightly more.
                        deg_i = variables[name_i].in_degree + variables[name_i].out_degree + 1
                        deg_j = variables[name_j].in_degree + variables[name_j].out_degree + 1
                        total = deg_i + deg_j
                        shift_i = shift * deg_j / total
                        shift_j = shift * deg_i / total

                        yi -= direction * shift_i
                        yj += direction * shift_j
                        node_pos[name_i] = clamp_to_panel(view, xi, yi)
                        node_pos[name_j] = clamp_to_panel(view, xj, yj)
                        xi, yi = node_pos[name_i]

    separate_close_nodes()

    node_sizes_by_name = {name: node_size_for_name(name) for name in node_pos}

    def arrow_margin_points(name: str, factor: float, minimum: float) -> float:
        variable = variables[name]
        category = variable_category(variable)
        marker_bonus = 8.0 if name in IMPORTANT_STOCKS else (5.0 if category in {"macro", "amm_logic", "technical"} else 2.5)
        return max(minimum, math.sqrt(node_sizes_by_name[name]) * factor + marker_bonus)

    # Draw dependency edges first. Direction is source/input -> target/equation variable.
    for source, target in edges:
        if source not in node_pos or target not in node_pos:
            continue
        x1, y1 = node_pos[source]
        x2, y2 = node_pos[target]
        same_view = variables[source].primary_view == variables[target].primary_view
        alpha = 0.17 if same_view else 0.31
        lw = 0.65 if same_view else 1.05
        color = "#4A5568" if same_view else "#2D3748"
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                lw=lw,
                alpha=alpha,
                color=color,
                shrinkA=arrow_margin_points(source, factor=0.50, minimum=9),
                shrinkB=arrow_margin_points(target, factor=0.90, minimum=15),
                mutation_scale=10 if same_view else 12,
                connectionstyle="arc3,rad=0.06" if not same_view else "arc3,rad=0.02",
            ),
            zorder=1,
        )

    nodes_by_category: dict[str, list[str]] = defaultdict(list)
    special_stock_nodes = []
    for name in node_pos:
        if name in IMPORTANT_STOCKS:
            special_stock_nodes.append(name)
        else:
            nodes_by_category[variable_category(variables[name])].append(name)

    for category, names in nodes_by_category.items():
        style = semantic_styles[category]
        xs = [node_pos[name][0] for name in names]
        ys = [node_pos[name][1] for name in names]
        sizes = [node_sizes_by_name[name] for name in names]
        ax.scatter(
            xs,
            ys,
            s=sizes,
            c=style["node"],
            marker=style["marker"],
            edgecolors="white" if style["marker"] != "x" else style["edge"],
            linewidths=1.25,
            zorder=3,
            alpha=0.94,
        )

    # Central stock variables get a strong red highlight.
    if special_stock_nodes:
        xs = [node_pos[name][0] for name in special_stock_nodes]
        ys = [node_pos[name][1] for name in special_stock_nodes]
        sizes = [node_sizes_by_name[name] for name in special_stock_nodes]
        ax.scatter(
            xs,
            ys,
            s=sizes,
            c="#D7191C",
            marker="o",
            edgecolors="black",
            linewidths=1.8,
            zorder=4,
            alpha=0.98,
        )

    # Labels: enlarged and with a white outline for readability on dense edges.
    # Labels are placed after a small collision pass. Close labels in the same
    # view are staggered vertically, so neighbouring nodes are not labelled on
    # exactly the same horizontal height.
    label_candidates = []
    for name, (x, y) in node_pos.items():
        variable = variables[name]
        if not should_label(variable):
            continue
        if name in IMPORTANT_STOCKS:
            label_size = 6.9 * FONT_SCALE
            weight = "bold"
            text = _shorten_label(name, max_len=30)
        elif variable.primary_view == MACRO_VIEW:
            label_size = 5.3 * FONT_SCALE
            weight = "normal"
            text = _shorten_label(name, max_len=30)
        else:
            label_size = 4.5 * FONT_SCALE
            weight = "normal"
            text = _shorten_label(name, max_len=28)

        view = variable.primary_view
        if view in view_box:
            x0, y0, w, h = view_box[view]
            centre_x = x0 + 0.5 * w
            # Labels on the right half are placed to the left of the node. This
            # keeps text inside the panel and reduces overlap with neighbouring panels.
            if name in IMPORTANT_STOCKS:
                lx = x
                ly = y + 0.048 * h
                ha = "center"
            elif x > centre_x:
                lx = x - 0.020 * w
                ly = y + 0.020 * h
                ha = "right"
            else:
                lx = x + 0.020 * w
                ly = y + 0.020 * h
                ha = "left"
            label_candidates.append(
                {
                    "name": name,
                    "view": view,
                    "x": lx,
                    "y": ly,
                    "ha": ha,
                    "fontsize": label_size,
                    "weight": weight,
                    "text": text,
                }
            )

    # Collision pass per view. This is intentionally simple and deterministic:
    # sort from top to bottom, then push later labels downward if they are too
    # close to labels already placed in the same horizontal neighbourhood.
    labels_by_view: dict[str, list[dict]] = defaultdict(list)
    for item in label_candidates:
        labels_by_view[item["view"]].append(item)

    for view, items in labels_by_view.items():
        if view not in view_box:
            continue
        x0, y0, w, h = view_box[view]
        min_gap = 0.064 * h
        horizontal_neighbourhood = 0.40 * w
        placed: list[dict] = []
        for item in sorted(items, key=lambda d: (-d["y"], d["x"])):
            y = item["y"]
            for prev in placed:
                same_x_area = abs(item["x"] - prev["x"]) < horizontal_neighbourhood
                too_close_y = abs(y - prev["y"]) < min_gap
                if same_x_area and too_close_y:
                    y = prev["y"] - min_gap
            # Keep labels inside the panel and away from titles and lower border.
            y = min(max(y, y0 - 0.850 * h), y0 - 0.145 * h)
            item["y"] = y
            placed.append(item)

        # If clamping at the bottom created new collisions, do a light upward pass.
        placed = sorted(placed, key=lambda d: (d["y"], d["x"]))
        for idx in range(1, len(placed)):
            prev = placed[idx - 1]
            item = placed[idx]
            same_x_area = abs(item["x"] - prev["x"]) < horizontal_neighbourhood
            if same_x_area and abs(item["y"] - prev["y"]) < min_gap:
                item["y"] = min(prev["y"] + min_gap, y0 - 0.145 * h)

        for item in placed:
            ax.text(
                item["x"],
                item["y"],
                item["text"],
                fontsize=item["fontsize"],
                fontweight=item["weight"],
                ha=item["ha"],
                va="center",
                zorder=5,
                path_effects=[pe.withStroke(linewidth=3.4, foreground="white", alpha=0.90)],
            )

    # -------------------------------------------------------------------------
    # Explanatory legend box in the free space right of 11_Innovation_and_City_Size.
    # This is intentionally textual because the poster needs to explain why only
    # selected nodes are labelled.
    # -------------------------------------------------------------------------
    legend_x = 1.04
    legend_y = y_cursor - 3 * CELL_H - 0.07
    legend_w = 1.92
    legend_h = 0.54
    legend_box = plt.Rectangle(
        (legend_x, legend_y - legend_h),
        legend_w,
        legend_h,
        facecolor="white",
        edgecolor="#4A5568",
        linewidth=1.5,
        alpha=0.93,
        zorder=6,
    )
    ax.add_patch(legend_box)

    title_fs = 6.2 * FONT_SCALE
    text_fs = 4.3 * FONT_SCALE
    line_gap = 0.064
    tx = legend_x + 0.045
    ty = legend_y - 0.045
    ax.text(tx, ty, "Legende und Leseregel", fontsize=title_fs, fontweight="bold", zorder=7, va="top")
    ty -= 0.083

    legend_lines = [
        "Pfeile: Input-Variable → berechnete Zielvariable.",
        "Farben der Boxen: Macro, AMM-Dynamisierung, AMM-Kernlogik, Cobb-Douglas, Innovation.",
        "Beschriftet sind nicht alle Nodes, sondern leserelevante Variablen:",
        "Stocks und Flows, wichtige Outputs, zentrale Hubs mit vielen Kanten sowie AMM-Kernvariablen.",
        "Urban Land und Agricultural Land sind rot markiert, weil sie die zentralen Bestandsgrössen sind.",
        "Unbeschriftete Nodes sind Hilfs-, Parameter- oder Zwischenvariablen und bleiben zur Orientierung sichtbar.",
    ]
    for line in legend_lines:
        ax.text(tx, ty, line, fontsize=text_fs, zorder=7, va="top")
        ty -= line_gap

    # Small visual examples inside the legend.
    sym_y = legend_y - legend_h + 0.075
    ax.scatter([legend_x + 0.055], [sym_y], s=190, c="#D7191C", edgecolors="black", linewidths=1.2, zorder=7)
    ax.text(legend_x + 0.085, sym_y, "zentrale Stocks", fontsize=text_fs, va="center", zorder=7)
    ax.scatter([legend_x + 0.43], [sym_y], s=150, c="#ED8936", marker="D", edgecolors="white", linewidths=1.0, zorder=7)
    ax.text(legend_x + 0.46, sym_y, "AMM-Kernlogik", fontsize=text_fs, va="center", zorder=7)
    ax.scatter([legend_x + 0.86], [sym_y], s=150, c="#4299E1", marker="o", edgecolors="white", linewidths=1.0, zorder=7)
    ax.text(legend_x + 0.89, sym_y, "AMM-Dynamisierung", fontsize=text_fs, va="center", zorder=7)

    ax.set_title(
        "Gesamtübersicht des Vensim-Modells nach Views",
        fontsize=10.5 * FONT_SCALE,
        fontweight="bold",
        pad=18,
    )

    total_h = MACRO_HEIGHT + grid_rows * CELL_H
    ax.set_xlim(-0.02, COLS * CELL_W + 0.02)
    ax.set_ylim(-total_h - 0.10, 0.12)
    plt.tight_layout()
    fig.savefig(out_dir / "model_overview_by_view.svg", bbox_inches="tight")
    fig.savefig(out_dir / "model_overview_by_view.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

def _wrap_view_label(view_name: str) -> str:
    # Keep the numeric prefix readable and wrap the semantic part.
    parts = view_name.split("_")
    if parts and parts[0].isdigit():
        prefix = parts[0]
        words = parts[1:]
    else:
        prefix = ""
        words = parts
    lines = []
    current = prefix if prefix else ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > 18 and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines[:4])


def draw_view_dependency_map(
    variables: dict[str, VensimVariable],
    view_edges: list[tuple[str, str, int]],
    out_dir: Path,
) -> None:
    """Draw directed dependencies between Vensim views with semantic styling."""
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    graph = nx.DiGraph()
    all_views = sorted({v.primary_view for v in variables.values()}, key=lambda v: (view_sort_number(v), v))
    for view in all_views:
        if view not in {"Unassigned", "00_Legend"}:
            graph.add_node(view)
    for source, target, weight in view_edges:
        if source not in {"00_Legend", "Unassigned"} and target not in {"00_Legend", "Unassigned"}:
            graph.add_edge(source, target, weight=weight)

    if len(graph) == 0:
        return

    view_styles = {
        "macro": {"node": "#F6AD55", "edge": "#B7791F", "marker": "s", "label": "Macro-Ebene"},
        "amm_dynamic": {"node": "#4299E1", "edge": "#1565C0", "marker": "o", "label": "AMM-Dynamisierung, Views 01-04"},
        "amm_logic": {"node": "#ED8936", "edge": "#EF6C00", "marker": "D", "label": "AMM-relevante Kernlogik"},
        "westcourt": {"node": "#C6A6D0", "edge": "#718096", "marker": "o", "label": "West-Bettencourt"},
        "cobb_doug": {"node": "#A6D0AE", "edge": "#718096", "marker": "o", "label": "Cobb-Douglas"},
        "other": {"node": "#CBD5E0", "edge": "#718096", "marker": "o", "label": "Weitere Views"},
        "technical": {"node": "#E2E8F0", "edge": "#A0AEC0", "marker": "X", "label": "Technisch"},
    }

    fig, ax = plt.subplots(figsize=(15, 13))
    ax.set_axis_off()

    view_order = sorted(graph.nodes, key=lambda v: (view_sort_number(v), v))
    macro_exists = MACRO_VIEW in graph.nodes
    outer_nodes = [node for node in view_order if node != MACRO_VIEW]

    pos: dict[str, tuple[float, float]] = {}
    if macro_exists:
        pos[MACRO_VIEW] = (0.0, 0.0)
        radius = 1.24
        n = len(outer_nodes)
        for i, node in enumerate(outer_nodes):
            angle = math.pi / 2 - 2 * math.pi * i / max(n, 1)
            pos[node] = (radius * math.cos(angle), radius * math.sin(angle))
    else:
        radius = 1.0
        n = len(view_order)
        for i, node in enumerate(view_order):
            angle = math.pi / 2 - 2 * math.pi * i / max(n, 1)
            pos[node] = (radius * math.cos(angle), radius * math.sin(angle))

    type_counts_by_view: dict[str, Counter[str]] = defaultdict(Counter)
    for variable in variables.values():
        type_counts_by_view[variable.primary_view][variable.var_type] += 1

    labels = {}
    node_sizes: dict[str, float] = {}
    for node in graph.nodes:
        count = sum(type_counts_by_view[node].values())
        if node == MACRO_VIEW:
            node_sizes[node] = 5200 + count * 260
        elif node in AMM_DYNAMIC_VIEWS:
            node_sizes[node] = 2100 + count * 120
        elif node in AMM_LOGIC_VIEWS:
            node_sizes[node] = 2300 + count * 125
        else:
            node_sizes[node] = 1600 + count * 95
        labels[node] = f"{_wrap_view_label(node)}\n({count} Variablen)"

    edge_widths = [0.75 + graph[u][v].get("weight", 1) * 0.28 for u, v in graph.edges]
    for (source, target), width in zip(graph.edges, edge_widths):
        # Draw view edges manually instead of relying on NetworkX defaults.
        # This gives us per-node margins, which prevents arrowheads from being
        # placed inside large symbols such as Macro_Ebene.
        source_margin = max(26, math.sqrt(node_sizes[source]) * 0.68)
        target_margin = max(36, math.sqrt(node_sizes[target]) * 0.98)
        arrow = plt.matplotlib.patches.FancyArrowPatch(
            posA=pos[source],
            posB=pos[target],
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=width,
            color="#2D3748",
            alpha=0.42,
            shrinkA=source_margin,
            shrinkB=target_margin,
            connectionstyle="arc3,rad=0.14",
            zorder=1,
        )
        ax.add_patch(arrow)

    for category, style in view_styles.items():
        nodes = [node for node in graph.nodes if view_category(node) == category]
        if not nodes:
            continue
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=nodes,
            node_size=[node_sizes[node] for node in nodes],
            node_color=style["node"],
            edgecolors=style["edge"],
            linewidths=3.2 if category == "macro" else 1.8,
            node_shape=style["marker"],
            alpha=0.95,
            ax=ax,
        )

    # Draw labels manually so Macro_Ebene can be larger.
    for node, (x, y) in pos.items():
        size = 10.5 if node == MACRO_VIEW else 8.2
        weight = "bold" if node == MACRO_VIEW else "normal"
        ax.text(x, y, labels[node], ha="center", va="center", fontsize=size, fontweight=weight, zorder=5)

    edge_labels = {
        (u, v): graph[u][v].get("weight", 1)
        for u, v in graph.edges
        if graph[u][v].get("weight", 1) >= 3
    }
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels,
        ax=ax,
        font_size=7.5,
        rotate=False,
        bbox=dict(alpha=0.55, edgecolor="none", facecolor="white"),
    )

    legend_handles = [
        Line2D([0], [0], marker=view_styles["macro"]["marker"], color="w",
               label=view_styles["macro"]["label"], markerfacecolor=view_styles["macro"]["node"],
               markeredgecolor=view_styles["macro"]["edge"], markersize=15),
        Line2D([0], [0], marker=view_styles["amm_dynamic"]["marker"], color="w",
               label=view_styles["amm_dynamic"]["label"], markerfacecolor=view_styles["amm_dynamic"]["node"],
               markeredgecolor=view_styles["amm_dynamic"]["edge"], markersize=10),
        Line2D([0], [0], marker=view_styles["amm_logic"]["marker"], color="w",
               label=view_styles["amm_logic"]["label"], markerfacecolor=view_styles["amm_logic"]["node"],
               markeredgecolor=view_styles["amm_logic"]["edge"], markersize=10),
        Line2D([0], [0], marker=view_styles["westcourt"]["marker"], color="w",
            label=view_styles["westcourt"]["label"], markerfacecolor=view_styles["westcourt"]["node"],
            markeredgecolor=view_styles["westcourt"]["edge"], markersize=10),
        Line2D([0], [0], marker=view_styles["cobb_doug"]["marker"], color="w",
            label=view_styles["cobb_doug"]["label"], markerfacecolor=view_styles["cobb_doug"]["node"],
            markeredgecolor=view_styles["westcourt"]["edge"], markersize=10),
        Line2D([0], [0], marker=view_styles["other"]["marker"], color="w",
               label=view_styles["other"]["label"], markerfacecolor=view_styles["other"]["node"],
               markeredgecolor=view_styles["other"]["edge"], markersize=9),
        Patch(facecolor="#FFFFFF", edgecolor="#2D3748", label="Pfeile: Quell-View → Ziel-View; Zahl = Anzahl Abhängigkeiten"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=2,
        frameon=False,
        fontsize=9,
    )

    ax.set_title("Gerichtete Abhängigkeiten zwischen Vensim-Views", fontsize=17, fontweight="bold", pad=18)
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.47, 1.50)
    plt.tight_layout()
    fig.savefig(out_dir / "model_view_dependency_map.svg", bbox_inches="tight")
    fig.savefig(out_dir / "model_view_dependency_map.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def view_sort_number(view: str) -> int:
    if view == MACRO_VIEW:
        return -1
    prefix = view.split("_", 1)[0]
    if prefix.isdigit():
        return int(prefix)
    return 999


def render(mdl_path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    text = mdl_path.read_text(encoding="utf-8", errors="replace")

    variables = parse_equations(text)
    edges = build_dependency_edges(variables)
    classify_variables(variables, edges)
    view_names, occurrences, view_to_vars = parse_views(text, set(variables.keys()))
    assign_views(variables, view_names, view_to_vars)
    view_edges = build_view_edges(variables, edges)

    write_tables(variables, edges, view_names, view_to_vars, view_edges, out_dir)
    draw_overview_by_view(variables, edges, occurrences, view_names, out_dir)
    draw_view_dependency_map(variables, view_edges, out_dir)

    summary = {
        "model_file": str(mdl_path),
        "variables": len(variables),
        "edges": len(edges),
        "views": len(view_names),
        "stocks": sum(1 for v in variables.values() if v.var_type == "Stock"),
        "flows": sum(1 for v in variables.values() if v.var_type == "Flow"),
        "lookups": sum(1 for v in variables.values() if v.var_type == "Lookup"),
        "parameters": sum(1 for v in variables.values() if v.var_type == "Parameter"),
    }
    pd.DataFrame([summary]).to_csv(out_dir / "model_summary.csv", index=False)
    print("Generated model overview assets in", out_dir)
    print(summary)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate overview graphics and tables for a Vensim .mdl file.")
    parser.add_argument("mdl_path", type=Path, help="Path to the Vensim .mdl file")
    parser.add_argument("--out-dir", type=Path, default=Path("assets/model_overview"), help="Output directory")
    args = parser.parse_args()

    if not args.mdl_path.exists():
        raise FileNotFoundError(f"Model file not found: {args.mdl_path}")
    render(args.mdl_path, args.out_dir)


if __name__ == "__main__":
    main()
