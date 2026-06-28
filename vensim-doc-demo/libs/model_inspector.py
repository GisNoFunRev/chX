"""Tabellarische Auswertungen fuer die Quarto-Dokumentation."""

from __future__ import annotations

import pandas as pd

from models.vensim_structures import VensimModel


class ModelInspector:
    """Erzeugt DataFrames fuer Modelluebersicht, Views, Variablen und Qualitaetschecks."""

    def __init__(self, model: VensimModel) -> None:
        self.model = model

    def summary_dataframe(self) -> pd.DataFrame:
        summary = self.model.summary()
        summary["view_comments"] = len(self.view_comments_dataframe())
        return pd.DataFrame([summary])

    def variables_dataframe(self) -> pd.DataFrame:
        view_map = self.variable_to_views()
        rows = []
        for variable in self.model.variables.values():
            rows.append(
                {
                    "name": variable.name,
                    "kind": variable.kind,
                    "units": variable.units,
                    "dependencies": ", ".join(variable.dependencies),
                    "n_dependencies": len(variable.dependencies),
                    "n_outputs": len(self.downstream_variables(variable.name)),
                    "views": ", ".join(view_map.get(variable.name, [])),
                    "has_documentation": variable.has_documentation(),
                    "documentation": variable.documentation,
                    "short_documentation": variable.short_documentation(),
                    "equation": variable.equation,
                }
            )
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows).sort_values(["kind", "name"]).reset_index(drop=True)

    def dependencies_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"source": dep.source, "target": dep.target, "relation": dep.relation}
                for dep in self.model.dependencies
            ]
        )

    def views_dataframe(self) -> pd.DataFrame:
        rows = []
        for view in self.model.views.values():
            variables = [v for v in view.variable_names() if v in self.model.variables]
            comments = view.comments()
            rows.append(
                {
                    "view": view.name,
                    "n_variables": len(variables),
                    "n_edges": len(view.edges),
                    "n_comments": len(comments),
                    "first_comment": comments[0] if comments else "",
                }
            )
        return pd.DataFrame(rows)

    def view_elements_dataframe(self, view_name: str) -> pd.DataFrame:
        view = self.model.views[view_name]
        return pd.DataFrame(
            [
                {
                    "view": view.name,
                    "element_id": element.element_id,
                    "name": element.name,
                    "kind": element.kind,
                    "x": element.x,
                    "y": element.y,
                    "text": element.text,
                }
                for element in view.elements
            ]
        )

    def view_variables_dataframe(self, view_name: str) -> pd.DataFrame:
        view = self.model.views[view_name]
        variable_names = [name for name in view.variable_names() if name in self.model.variables]
        df = self.variables_dataframe()
        return df[df["name"].isin(variable_names)].reset_index(drop=True)

    def view_comments_dataframe(self) -> pd.DataFrame:
        rows = []
        for view in self.model.views.values():
            for element in view.elements:
                if element.text.strip():
                    rows.append(
                        {
                            "view": view.name,
                            "element_id": element.element_id,
                            "text": element.text,
                            "x": element.x,
                            "y": element.y,
                        }
                    )
        return pd.DataFrame(rows)

    def variable_to_views(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for view in self.model.views.values():
            for variable_name in view.variable_names():
                if variable_name in self.model.variables:
                    result.setdefault(variable_name, []).append(view.name)
        return {key: sorted(set(value)) for key, value in result.items()}

    def upstream_variables(self, variable_name: str) -> list[str]:
        return self.model.variables[variable_name].dependencies

    def downstream_variables(self, variable_name: str) -> list[str]:
        return sorted(
            dep.target for dep in self.model.dependencies if dep.source == variable_name
        )

    def variables_by_kind(self) -> pd.DataFrame:
        df = self.variables_dataframe()
        if df.empty:
            return pd.DataFrame(columns=["kind", "n_variables"])
        return (
            df.groupby("kind", as_index=False)
            .agg(n_variables=("name", "count"))
            .sort_values("n_variables", ascending=False)
        )

    def stocks_dataframe(self) -> pd.DataFrame:
        df = self.variables_dataframe()
        return df[df["kind"] == "stock"][["name", "units", "equation", "short_documentation", "views"]]

    def parameters_dataframe(self) -> pd.DataFrame:
        df = self.variables_dataframe()
        return df[df["kind"].isin(["constant", "control"])] [
            ["name", "kind", "units", "equation", "short_documentation", "views"]
        ].reset_index(drop=True)

    def undocumented_variables(self) -> pd.DataFrame:
        df = self.variables_dataframe()
        return df.loc[~df["has_documentation"], ["name", "kind", "units", "equation", "views"]]

    def short_documentation_variables(self, max_chars: int = 40) -> pd.DataFrame:
        df = self.variables_dataframe()
        mask = df["documentation"].str.len().lt(max_chars)
        return df.loc[mask, ["name", "kind", "units", "documentation", "equation", "views"]]

    def variables_containing(self, text: str) -> pd.DataFrame:
        text_lower = text.lower()
        df = self.variables_dataframe()
        mask = (
            df["name"].str.lower().str.contains(text_lower, regex=False)
            | df["equation"].str.lower().str.contains(text_lower, regex=False)
            | df["documentation"].str.lower().str.contains(text_lower, regex=False)
            | df["views"].str.lower().str.contains(text_lower, regex=False)
        )
        return df.loc[mask].reset_index(drop=True)
