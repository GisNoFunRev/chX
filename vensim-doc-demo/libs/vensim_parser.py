"""Robuster, pragmatischer Parser fuer Vensim-PLE .mdl-Dateien.

Der Parser extrahiert:
- Variablen, Gleichungen, Units und Kommentare
- rechnerische Dependencies aus Gleichungen
- Vensim Views, View-Nodes, View-Pfeile und Textkommentare
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from models.vensim_structures import (
    VensimDependency,
    VensimModel,
    VensimVariable,
    VensimView,
    VensimViewEdge,
    VensimViewElement,
)


class VensimModelParser:
    """Liest eine Vensim .mdl-Datei in ein VensimModel ein."""

    SKETCH_HEADER = "Sketch information - do not modify anything except names"
    SKETCH_END_PREFIX = "///---"

    def __init__(self, model_path: str | Path, encoding: str = "utf-8") -> None:
        self.model_path = Path(model_path)
        self.encoding = encoding

    def parse(self) -> VensimModel:
        text = self._read_text()
        equation_text, sketch_text = self._split_equations_and_sketch(text)

        variables = self._parse_variables(equation_text)
        self._post_classify_flows(variables)
        self._attach_dependencies(variables)

        dependencies = [
            VensimDependency(source=dep, target=var.name)
            for var in variables.values()
            for dep in var.dependencies
        ]
        views = self._parse_views(sketch_text)

        return VensimModel(
            path=self.model_path,
            variables=variables,
            dependencies=dependencies,
            views=views,
        )

    def _read_text(self) -> str:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        text = self.model_path.read_text(encoding=self.encoding, errors="ignore")
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _split_equations_and_sketch(self, text: str) -> tuple[str, str]:
        header_index = text.find(self.SKETCH_HEADER)
        if header_index == -1:
            return text, ""

        marker_index = text.rfind("\\\\\\---///", 0, header_index)
        if marker_index == -1:
            marker_index = text.rfind("\\\\---///", 0, header_index)
        if marker_index == -1:
            marker_index = text.rfind("\n", 0, header_index)
        if marker_index == -1:
            marker_index = header_index

        return text[:marker_index], text[marker_index:]

    def _parse_variables(self, equation_text: str) -> dict[str, VensimVariable]:
        equation_text = re.sub(r"^\{UTF-8\}\s*", "", equation_text.strip())

        # Wichtig: Vensim speichert das Block-Ende manchmal als Tab + Pipe.
        # Diese Variante findet mehr Variablen als ein Split, der nur eine eigene Pipe-Zeile erwartet.
        raw_blocks = re.split(r"[\t ]*\|[\t ]*(?:\n|$)", equation_text)

        variables: dict[str, VensimVariable] = {}
        for raw_block in raw_blocks:
            block = raw_block.strip()
            if not block or block.startswith("********************************************************"):
                continue
            parsed = self._parse_variable_block(block)
            if parsed is not None:
                variables[parsed.name] = parsed
        return variables

    def _parse_variable_block(self, block: str) -> VensimVariable | None:
        parts = block.split("~", maxsplit=2)
        if len(parts) < 2:
            return None

        equation_part = self._clean_continuation(parts[0]).strip()
        units = self._clean_text(parts[1]) if len(parts) >= 2 else "Dmnl"
        documentation = self._clean_text(parts[2]) if len(parts) >= 3 else ""

        if "=" not in equation_part:
            return None

        name, equation = equation_part.split("=", maxsplit=1)
        name = self._normalize_name(name)
        equation = self._clean_continuation(equation).strip()

        if not name:
            return None

        kind = self._classify_variable(name=name, equation=equation, units=units)
        return VensimVariable(
            name=name,
            equation=equation,
            units=units or "Dmnl",
            documentation=documentation,
            kind=kind,
            raw_block=block,
        )

    def _post_classify_flows(self, variables: dict[str, VensimVariable]) -> None:
        """Markiert Variablen als Flow, wenn sie als erster INTEG-Input verwendet werden."""
        flow_candidates: set[str] = set()
        for variable in variables.values():
            if variable.kind != "stock":
                continue
            integ_args = self._extract_integ_arguments(variable.equation)
            if not integ_args:
                continue
            first_arg = integ_args[0].strip()
            first_arg = re.sub(r"^[-+]\s*", "", first_arg).strip()
            if first_arg in variables:
                flow_candidates.add(first_arg)

        for name in flow_candidates:
            if variables[name].kind == "auxiliary":
                variables[name].kind = "flow"

    def _attach_dependencies(self, variables: dict[str, VensimVariable]) -> None:
        variable_names = sorted(variables.keys(), key=len, reverse=True)
        for var in variables.values():
            expression = var.equation
            deps: list[str] = []
            for candidate in variable_names:
                if candidate == var.name:
                    continue
                if self._contains_variable_reference(expression, candidate):
                    deps.append(candidate)
            var.dependencies = sorted(set(deps))

    def _parse_views(self, sketch_text: str) -> dict[str, VensimView]:
        if not sketch_text:
            return {}

        end_index = sketch_text.find(self.SKETCH_END_PREFIX)
        if end_index != -1:
            sketch_text = sketch_text[:end_index]

        views: dict[str, VensimView] = {}
        current_view: VensimView | None = None
        id_to_name: dict[str, str] = {}

        lines = sketch_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if line.startswith("*"):
                view_name = line[1:].strip()
                current_view = VensimView(name=view_name)
                views[view_name] = current_view
                id_to_name = {}
                i += 1
                continue

            if current_view is None or line.startswith("$") or line.startswith("V300"):
                i += 1
                continue

            row = self._parse_csv_line(line)
            if not row:
                i += 1
                continue

            object_type = row[0]

            if object_type == "10":
                element = self._parse_view_node(row, line)
                if element:
                    current_view.elements.append(element)
                    id_to_name[element.element_id] = element.name
                i += 1
                continue

            if object_type == "1":
                edge = self._parse_view_edge(row, id_to_name, line)
                if edge:
                    current_view.edges.append(edge)
                i += 1
                continue

            if object_type in {"11", "12"}:
                text = ""
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not self._is_sketch_object_line(next_line):
                        text = self._clean_view_text(next_line)
                        i += 1

                element = self._parse_view_annotation(row, line, text=text)
                if element:
                    current_view.elements.append(element)
                    id_to_name[element.element_id] = element.name
                i += 1
                continue

            i += 1

        return views

    def _parse_view_node(self, row: list[str], raw_line: str) -> VensimViewElement | None:
        try:
            return VensimViewElement(
                element_id=row[1],
                name=self._normalize_name(row[2]),
                x=float(row[3]),
                y=float(row[4]),
                width=float(row[5]) if len(row) > 5 and row[5] else None,
                height=float(row[6]) if len(row) > 6 and row[6] else None,
                kind="variable",
                raw_line=raw_line,
            )
        except (IndexError, ValueError):
            return None

    def _parse_view_annotation(
        self,
        row: list[str],
        raw_line: str,
        text: str = "",
    ) -> VensimViewElement | None:
        try:
            element_id = row[1]
            name = text[:60] if text else f"annotation_{element_id}"
            return VensimViewElement(
                element_id=element_id,
                name=name,
                x=float(row[3]),
                y=float(row[4]),
                width=float(row[5]) if len(row) > 5 and row[5] else None,
                height=float(row[6]) if len(row) > 6 and row[6] else None,
                kind="annotation",
                text=text,
                raw_line=raw_line,
            )
        except (IndexError, ValueError):
            return None

    def _parse_view_edge(
        self, row: list[str], id_to_name: dict[str, str], raw_line: str
    ) -> VensimViewEdge | None:
        try:
            source_id = row[2]
            target_id = row[3]
            return VensimViewEdge(
                edge_id=row[1],
                source_id=source_id,
                target_id=target_id,
                source_name=id_to_name.get(source_id),
                target_name=id_to_name.get(target_id),
                raw_line=raw_line,
            )
        except IndexError:
            return None

    @staticmethod
    def _parse_csv_line(line: str) -> list[str]:
        try:
            return next(csv.reader(io.StringIO(line)))
        except Exception:
            return []

    @staticmethod
    def _clean_continuation(text: str) -> str:
        text = re.sub(r"\\\s*\n\s*", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _clean_text(text: str) -> str:
        text = re.sub(r"\\\s*\n\s*", " ", text)
        text = text.replace("\t", " ")
        text = text.replace("|<<NnN>>|", "\n")
        text = text.replace("<<NnN>>", "\n")
        text = text.replace("\u2028", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text.strip()

    @staticmethod
    def _normalize_name(name: str) -> str:
        return name.strip().strip('"').strip()

    @staticmethod
    def _contains_variable_reference(expression: str, variable_name: str) -> bool:
        pattern = r"(?<![A-Za-z0-9_])" + re.escape(variable_name) + r"(?![A-Za-z0-9_])"
        return re.search(pattern, expression) is not None

    @staticmethod
    def _classify_variable(name: str, equation: str, units: str) -> str:
        eq_upper = equation.upper()
        name_upper = name.upper()
        units_upper = units.upper()

        if name_upper in {"INITIAL TIME", "FINAL TIME", "TIME STEP", "SAVEPER"}:
            return "control"
        if re.search(r"\bINTEG\s*\(", eq_upper):
            return "stock"
        if "WITH LOOKUP" in eq_upper:
            return "lookup"
        if re.fullmatch(r"[-+*/(). 0-9eE]+", equation.strip()):
            return "constant"
        if "/YEAR" in units_upper or name_upper.endswith(" RATE") or name_upper.endswith(" CHANGE"):
            return "flow"
        return "auxiliary"

    @staticmethod
    def _extract_integ_arguments(equation: str) -> list[str]:
        match = re.search(r"\bINTEG\s*\((.*)\)\s*$", equation, flags=re.IGNORECASE | re.DOTALL)
        if not match:
            return []
        body = match.group(1)
        args: list[str] = []
        depth = 0
        current: list[str] = []
        for char in body:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            if char == "," and depth == 0:
                args.append("".join(current).strip())
                current = []
            else:
                current.append(char)
        if current:
            args.append("".join(current).strip())
        return args

    @staticmethod
    def _is_sketch_object_line(line: str) -> bool:
        return bool(re.match(r"^\d+,", line)) or line.startswith("*") or line.startswith("$") or line.startswith("V300")

    @staticmethod
    def _clean_view_text(text: str) -> str:
        text = text.replace("|<<NnN>>|", "\n")
        text = text.replace("<<NnN>>", "\n")
        text = text.replace("\u2028", "\n")
        text = text.replace("|", "")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text.strip()
