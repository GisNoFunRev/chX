"""Statischer Model Explorer fuer Quarto.

Die Klasse ist bewusst nicht als interaktive App gebaut. Man stellt in einer
Quarto-Code-Zelle Suchbegriff, Fokusvariable und Anzeigeoptionen ein. Danach
werden stabile HTML-Bloecke ausgegeben: Grafik, Einheit, Dokumentation,
Gleichung, Dependencies und View-Zuordnung.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from models.vensim_structures import VensimModel
from .model_documentation import ModelDocumentationExtractor
from .model_graph import GraphvizModelVisualizer, ModelGraphBuilder
from .model_inspector import ModelInspector


@dataclass(slots=True)
class SearchResult:
    title: str
    markdown: str
    table: pd.DataFrame | None = None
    svg: str | None = None


class StaticModelExplorer:
    """Statische Such- und Anzeige-Funktionen fuer die Modell-Doku."""

    def __init__(self, model: VensimModel) -> None:
        self.model = model
        self.inspector = ModelInspector(model)
        self.docs = ModelDocumentationExtractor(model)
        self.builder = ModelGraphBuilder(model)
        self.graphs = GraphvizModelVisualizer(self.builder)

    def explain_perspectives_markdown(self) -> str:
        return """
## Wie diese Dokumentation gelesen werden kann

Diese Dokumentation zeigt das Modell aus mehreren Perspektiven. Die Perspektiven sind nicht interaktiv, sondern bewusst statisch aufgebaut, damit die Dokumentation einfach lesbar bleibt.

**Nach View / Submodul:** Diese Perspektive erklärt das Modell in thematischen Blöcken. Eine View entspricht einem fachlichen Teil des Modells, zum Beispiel Population, Transport, Mieten, Wohnraumnachfrage oder Landumwandlung. Diese Perspektive ist am besten für das Gesamtverständnis.

**Nach Variable:** Diese Perspektive erklärt einzelne Modellbestandteile. Für jede Variable werden Typ, Einheit, Gleichung, Kommentar, Input-Dependencies, Output-Dependencies und View-Zugehörigkeit angezeigt. Diese Perspektive ist gut zum Nachschlagen und Debuggen.

**Nach Dependencies:** Eine Dependency von A nach B bedeutet: Variable A wird in der Gleichung von Variable B verwendet. Dependencies zeigen also die rechnerische Einflussstruktur des Modells. Sie zeigen nicht automatisch, ob der Effekt positiv oder negativ ist; dafür muss die Gleichung betrachtet werden.

**Nach Qualität:** Diese Perspektive zeigt, wo die automatische Dokumentation noch schwach ist, zum Beispiel Variablen ohne Kommentar, sehr kurze Kommentare oder Parameter ohne Erklärung.
""".strip()

    # ------------------------------------------------------------------
    # Variable search / configurable blocks
    # ------------------------------------------------------------------

    def search_variables(
        self,
        query: str,
        kinds: list[str] | None = None,
        views: list[str] | None = None,
        max_results: int | None = None,
    ) -> pd.DataFrame:
        """
        Sucht Variablen nach Name, Gleichung, Dokumentation oder View-Zuordnung.

        Parameter
        ---------
        query:
            Suchbegriff. Beispiele: "Urban Land", "Rent", "Transport".
        kinds:
            Optionaler Filter auf Variablentypen, z. B. ["stock", "constant"].
        views:
            Optionaler Filter auf View-Namen.
        max_results:
            Optional: maximale Anzahl Zeilen in der Ausgabe.
        """
        df = self.inspector.variables_containing(query)

        if kinds:
            allowed = {kind.lower() for kind in kinds}
            df = df[df["kind"].str.lower().isin(allowed)]

        if views:
            wanted_views = [view.lower() for view in views]
            mask = df["views"].str.lower().apply(
                lambda value: any(view in value for view in wanted_views)
            )
            df = df[mask]

        columns = [
            "name",
            "kind",
            "units",
            "views",
            "short_documentation",
            "equation",
        ]
        df = df[columns].reset_index(drop=True)

        if max_results is not None:
            df = df.head(max_results)

        return df

    def select_variable(self, query: str, selected_variable: str | None = None) -> str:
        """
        Waehlt eine konkrete Variable fuer die Detailanzeige aus.

        Logik:
        1. Wenn selected_variable gesetzt ist, wird diese Variable verwendet.
        2. Wenn query exakt einem Variablennamen entspricht, wird query verwendet.
        3. Sonst wird der erste Suchtreffer verwendet.
        """
        if selected_variable:
            if selected_variable not in self.model.variables:
                raise KeyError(f"Variable nicht gefunden: {selected_variable}")
            return selected_variable

        if query in self.model.variables:
            return query

        matches = self.search_variables(query, max_results=1)
        if matches.empty:
            raise ValueError(f"Keine Variable fuer Suchbegriff gefunden: {query}")

        return str(matches.iloc[0]["name"])

    def variable_search_blocks(
        self,
        variable_name: str,
        *,
        show_graph: bool = True,
        show_units: bool = True,
        show_documentation: bool = True,
        show_equation: bool = True,
        show_dependencies: bool = True,
        show_views: bool = True,
        upstream_depth: int = 2,
        downstream_depth: int = 2,
    ) -> dict[str, Any]:
        """
        Erstellt konfigurierbare Ausgabebloecke fuer eine Variable.

        Die Rueckgabe ist ein Dictionary mit sprechenden Blocknamen. In Quarto
        koennen diese Bloecke mit display_variable_search_blocks() direkt
        angezeigt werden.
        """
        if variable_name not in self.model.variables:
            raise KeyError(f"Variable nicht gefunden: {variable_name}")

        variable = self.model.variables[variable_name]
        blocks: dict[str, Any] = {}

        blocks["Titel"] = f"## Suchergebnis: {variable.name}"

        if show_graph:
            blocks["Grafik"] = self.graphs.draw_neighborhood_svg(
                target=variable_name,
                upstream_depth=upstream_depth,
                downstream_depth=downstream_depth,
                show_units=True,
                show_kind=True,
            )

        if show_units:
            blocks["Einheiten"] = pd.DataFrame(
                [
                    {
                        "Variable": variable.name,
                        "Typ": variable.kind,
                        "Einheit": variable.units,
                    }
                ]
            )

        if show_documentation and variable.documentation.strip():
            blocks["Dokumentation"] = variable.documentation.strip()

        if show_equation:
            blocks["Gleichung"] = (
                "```text\n"
                f"{variable.equation}\n"
                "```"
            )

        if show_dependencies:
            blocks["Dependencies"] = self.variable_dependencies_dataframe(variable_name)

        if show_views:
            blocks["View-Zuordnung"] = self.variable_views_dataframe(variable_name)

        return blocks

    def display_variable_search_blocks(self, blocks: dict[str, Any]) -> None:
        """
        Zeigt die von variable_search_blocks() erzeugten Bloecke in Quarto/Jupyter an.
        """
        from IPython.display import Markdown, SVG, display

        for block_name, content in blocks.items():
            if block_name == "Titel":
                display(Markdown(str(content)))
                continue

            display(Markdown(f"### {block_name}"))

            if block_name == "Grafik":
                display(SVG(str(content)))
            elif isinstance(content, pd.DataFrame):
                display(content)
            else:
                display(Markdown(str(content)))

    def variable_dependencies_dataframe(self, variable_name: str) -> pd.DataFrame:
        variable = self.model.variables[variable_name]
        rows = []

        for source in variable.dependencies:
            rows.append(
                {
                    "Richtung": "Input / upstream",
                    "Von": source,
                    "Nach": variable_name,
                    "Bedeutung": f"{source} wird in der Gleichung von {variable_name} verwendet.",
                }
            )

        for target in self.inspector.downstream_variables(variable_name):
            rows.append(
                {
                    "Richtung": "Output / downstream",
                    "Von": variable_name,
                    "Nach": target,
                    "Bedeutung": f"{variable_name} wird in der Gleichung von {target} verwendet.",
                }
            )

        if not rows:
            return pd.DataFrame(
                [
                    {
                        "Richtung": "-",
                        "Von": variable_name,
                        "Nach": "-",
                        "Bedeutung": "Keine direkten Dependencies erkannt.",
                    }
                ]
            )

        return pd.DataFrame(rows)

    def variable_views_dataframe(self, variable_name: str) -> pd.DataFrame:
        views = self.inspector.variable_to_views().get(variable_name, [])
        if not views:
            return pd.DataFrame(
                [{"Variable": variable_name, "View": "Keine View-Zuordnung gefunden."}]
            )
        return pd.DataFrame(
            [{"Variable": variable_name, "View": view_name} for view_name in views]
        )

    def search_help_markdown(self) -> str:
        return """
## Statische Variablensuche

Die Suche ist bewusst einfach gehalten. Sie ist keine interaktive App, sondern eine konfigurierbare Quarto-Zelle. Dadurch bleibt die fertige HTML-Dokumentation ruhig und lesbar.

**So funktioniert die Suche:**

1. Setze `SEARCH_QUERY` auf einen Suchbegriff, zum Beispiel `"Urban Land"`, `"Rent"` oder `"Transport"`.
2. Optional kannst du mit `SELECTED_VARIABLE` eine konkrete Variable festlegen. Wenn `SELECTED_VARIABLE = None` ist, wird automatisch der erste Suchtreffer verwendet.
3. Mit den `SHOW_...`-Optionen stellst du ein, welche Bloecke angezeigt werden.

**Verfügbare Bloecke:**

- `SHOW_GRAPH`: zeigt den Dependency-Graph rund um die Variable.
- `SHOW_UNITS`: zeigt Typ und Einheit der Variable.
- `SHOW_DOCUMENTATION`: zeigt den Vensim-Kommentar, falls vorhanden.
- `SHOW_EQUATION`: zeigt die Gleichung.
- `SHOW_DEPENDENCIES`: zeigt direkte Inputs und Outputs.
- `SHOW_VIEWS`: zeigt, in welchen Vensim-Views die Variable vorkommt.

Die Dependency-Grafik zeigt rechnerische Abhängigkeiten. Ein Pfeil von `A` nach `B` bedeutet: `A` wird in der Gleichung von `B` verwendet.
""".strip()

    # ------------------------------------------------------------------
    # Existing POC helpers
    # ------------------------------------------------------------------

    def variable_result(
        self,
        variable_name: str,
        upstream_depth: int = 2,
        downstream_depth: int = 1,
    ) -> SearchResult:
        markdown = self.docs.variable_markdown(variable_name)
        variable = self.model.variables[variable_name]
        rows = []
        for source in variable.dependencies:
            rows.append({"direction": "Input", "source": source, "target": variable_name})
        for target in self.inspector.downstream_variables(variable_name):
            rows.append({"direction": "Output", "source": variable_name, "target": target})
        table = pd.DataFrame(rows)
        svg = self.graphs.draw_neighborhood_svg(
            target=variable_name,
            upstream_depth=upstream_depth,
            downstream_depth=downstream_depth,
            show_units=True,
            show_kind=True,
        )
        return SearchResult(title=variable_name, markdown=markdown, table=table, svg=svg)

    def view_result(self, view_name: str, dependency_edges: bool = False) -> SearchResult:
        markdown = self.docs.view_markdown(view_name)
        table = self.inspector.view_variables_dataframe(view_name)[
            ["name", "kind", "units", "short_documentation", "equation"]
        ]
        svg = self.graphs.draw_view_svg(
            view_name=view_name,
            dependency_edges=dependency_edges,
            show_units=False,
            show_kind=True,
        )
        return SearchResult(title=view_name, markdown=markdown, table=table, svg=svg)

    def dependency_result(
        self,
        variable_name: str,
        upstream_depth: int = 2,
        downstream_depth: int = 2,
    ) -> SearchResult:
        upstream = self._recursive_upstream(variable_name, upstream_depth)
        downstream = self._recursive_downstream(variable_name, downstream_depth)
        markdown = f"""
### Dependency-Perspektive: {variable_name}

Diese Perspektive zeigt, welche Variablen `{variable_name}` beeinflussen und welche Variablen durch `{variable_name}` beeinflusst werden.

**Upstream** bedeutet: Diese Variablen fliessen rechnerisch in `{variable_name}` ein.

**Downstream** bedeutet: `{variable_name}` wird in den Gleichungen dieser Variablen verwendet.

Eine Dependency ist keine vollständige Wirkungsinterpretation. Sie zeigt zuerst nur die rechnerische Verbindung. Ob der Effekt positiv, negativ oder nichtlinear ist, muss aus der Gleichung gelesen werden.
""".strip()
        table = pd.DataFrame(
            [{"direction": "upstream", "variable": name} for name in sorted(upstream)]
            + [{"direction": "downstream", "variable": name} for name in sorted(downstream)]
        )
        svg = self.graphs.draw_neighborhood_svg(
            target=variable_name,
            upstream_depth=upstream_depth,
            downstream_depth=downstream_depth,
            show_units=True,
            show_kind=True,
        )
        return SearchResult(title=f"Dependencies: {variable_name}", markdown=markdown, table=table, svg=svg)

    def quality_tables(self) -> dict[str, pd.DataFrame]:
        return {
            "Variablen ohne Dokumentation": self.inspector.undocumented_variables(),
            "Variablen mit sehr kurzem Kommentar": self.inspector.short_documentation_variables(max_chars=45),
            "Parameter und Control-Variablen": self.inspector.parameters_dataframe(),
        }

    def chapter_overview_dataframe(self, chapters: dict[str, list[str]]) -> pd.DataFrame:
        rows = []
        views_df = self.inspector.views_dataframe().set_index("view")
        for chapter, view_names in chapters.items():
            rows.append(
                {
                    "chapter": chapter,
                    "views": ", ".join(view_names),
                    "n_views": len(view_names),
                    "n_variables": int(sum(views_df.loc[v, "n_variables"] for v in view_names if v in views_df.index)),
                    "n_comments": int(sum(views_df.loc[v, "n_comments"] for v in view_names if v in views_df.index)),
                }
            )
        return pd.DataFrame(rows)

    def _recursive_upstream(self, variable_name: str, depth: int) -> set[str]:
        selected: set[str] = set()
        frontier = {variable_name}
        for _ in range(depth):
            parents: set[str] = set()
            for name in frontier:
                if name in self.model.variables:
                    parents.update(self.model.variables[name].dependencies)
            selected.update(parents)
            frontier = parents
        selected.discard(variable_name)
        return selected

    def _recursive_downstream(self, variable_name: str, depth: int) -> set[str]:
        selected: set[str] = set()
        frontier = {variable_name}
        for _ in range(depth):
            children: set[str] = set()
            for name in frontier:
                children.update(self.inspector.downstream_variables(name))
            selected.update(children)
            frontier = children
        selected.discard(variable_name)
        return selected
