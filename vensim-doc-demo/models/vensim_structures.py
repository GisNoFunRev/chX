"""Datenstrukturen fuer automatisch generierte Vensim-Dokumentation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


VariableKind = Literal["stock", "flow", "auxiliary", "constant", "lookup", "control"]


@dataclass(slots=True)
class VensimVariable:
    """Eine Variable/Gleichung aus einer Vensim .mdl-Datei."""

    name: str
    equation: str
    units: str = "Dmnl"
    documentation: str = ""
    dependencies: list[str] = field(default_factory=list)
    kind: VariableKind = "auxiliary"
    raw_block: str = ""

    def has_documentation(self) -> bool:
        return bool(self.documentation.strip())

    def has_units(self) -> bool:
        return bool(self.units.strip())

    def short_documentation(self, max_chars: int = 220) -> str:
        doc = " ".join(self.documentation.split())
        if len(doc) <= max_chars:
            return doc
        return doc[: max_chars - 1].rstrip() + "…"


@dataclass(slots=True)
class VensimDependency:
    """Gerichtete rechnerische Abhaengigkeit: source wird in target verwendet."""

    source: str
    target: str
    relation: str = "equation"


@dataclass(slots=True)
class VensimViewElement:
    """Ein sichtbares Objekt in einer Vensim-View."""

    element_id: str
    name: str
    x: float
    y: float
    kind: str = "node"
    width: float | None = None
    height: float | None = None
    text: str = ""
    raw_line: str = ""


@dataclass(slots=True)
class VensimViewEdge:
    """Ein Pfeil/Connector in einer Vensim-View."""

    edge_id: str
    source_id: str
    target_id: str
    source_name: str | None = None
    target_name: str | None = None
    raw_line: str = ""


@dataclass(slots=True)
class VensimView:
    """Eine Sketch-View aus Vensim."""

    name: str
    elements: list[VensimViewElement] = field(default_factory=list)
    edges: list[VensimViewEdge] = field(default_factory=list)

    def element_by_id(self) -> dict[str, VensimViewElement]:
        return {element.element_id: element for element in self.elements}

    def variable_names(self) -> list[str]:
        return sorted({element.name for element in self.elements if element.kind == "variable"})

    def comments(self) -> list[str]:
        return [element.text for element in self.elements if element.text.strip()]


@dataclass(slots=True)
class VensimModel:
    """Das geparste Gesamtmodell."""

    path: Path
    variables: dict[str, VensimVariable] = field(default_factory=dict)
    dependencies: list[VensimDependency] = field(default_factory=list)
    views: dict[str, VensimView] = field(default_factory=dict)

    def get_variable(self, name: str) -> VensimVariable:
        return self.variables[name]

    def variable_names(self) -> list[str]:
        return sorted(self.variables.keys())

    def view_names(self) -> list[str]:
        return list(self.views.keys())

    def summary(self) -> dict[str, int]:
        return {
            "variables": len(self.variables),
            "dependencies": len(self.dependencies),
            "views": len(self.views),
        }
