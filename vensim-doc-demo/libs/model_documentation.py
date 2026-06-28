"""Automatische Dokumentationsbausteine aus Vensim-Variablen und Views."""

from __future__ import annotations

import pandas as pd

from models.vensim_structures import VensimModel
from .model_inspector import ModelInspector


class ModelDocumentationExtractor:
    """Erzeugt Markdown- und Tabellenbausteine fuer Quarto."""

    def __init__(self, model: VensimModel) -> None:
        self.model = model
        self.inspector = ModelInspector(model)

    def variable_markdown(self, variable_name: str) -> str:
        variable = self.model.variables[variable_name]
        upstream = variable.dependencies
        downstream = self.inspector.downstream_variables(variable_name)
        views = self.inspector.variable_to_views().get(variable_name, [])

        lines = [
            f"### {variable.name}",
            "",
            f"**Typ:** `{variable.kind}`  ",
            f"**Einheit:** `{variable.units}`  ",
            f"**Views:** {', '.join(views) if views else 'Keine View-Zuordnung gefunden.'}",
            "",
            "**Gleichung:**",
            "",
            "```text",
            variable.equation,
            "```",
            "",
            "**Kommentar aus Vensim:**",
            "",
            variable.documentation if variable.documentation else "_Keine Dokumentation vorhanden._",
            "",
            f"**Input-Dependencies:** {', '.join(upstream) if upstream else 'Keine direkten Inputs erkannt.'}",
            "",
            f"**Output-Dependencies:** {', '.join(downstream) if downstream else 'Keine direkten Outputs erkannt.'}",
        ]
        return "\n".join(lines)

    def view_markdown(self, view_name: str, max_variables: int = 20) -> str:
        view = self.model.views[view_name]
        comments = view.comments()
        variables = [name for name in view.variable_names() if name in self.model.variables]

        lines = [f"## {view.name}", ""]
        if comments:
            lines += ["### Kommentar aus der View", ""]
            for comment in comments:
                lines += [comment, ""]
        else:
            lines += ["_Keine View-Kommentare gefunden._", ""]

        lines += ["### Variablen in dieser View", ""]
        if variables:
            for name in variables[:max_variables]:
                variable = self.model.variables[name]
                lines.append(f"- **{name}** (`{variable.kind}`, `{variable.units}`): {variable.short_documentation(160)}")
            if len(variables) > max_variables:
                lines.append(f"- … {len(variables) - max_variables} weitere Variablen")
        else:
            lines.append("_Keine Modellvariablen in dieser View erkannt._")
        return "\n".join(lines)

    def chapter_markdown(self, title: str, view_names: list[str], max_variables_per_view: int = 12) -> str:
        lines = [f"# {title}", ""]
        for view_name in view_names:
            if view_name in self.model.views:
                lines += [self.view_markdown(view_name, max_variables=max_variables_per_view), ""]
        return "\n".join(lines)

    def view_comments_dataframe(self) -> pd.DataFrame:
        return self.inspector.view_comments_dataframe()

    def variable_documentation_dataframe(self) -> pd.DataFrame:
        df = self.inspector.variables_dataframe()
        return df[["name", "kind", "units", "views", "short_documentation", "equation"]]
