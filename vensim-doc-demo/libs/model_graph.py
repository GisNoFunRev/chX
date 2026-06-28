"""Graphen fuer Vensim-Modelldokumentation."""

from __future__ import annotations

from collections import deque

import networkx as nx
from graphviz import Digraph

from models.vensim_structures import VensimModel


class ModelGraphBuilder:
    """Erstellt NetworkX-Graphen aus Modelllogik und Vensim-Views."""

    def __init__(self, model: VensimModel) -> None:
        self.model = model

    def dependency_graph(self) -> nx.DiGraph:
        graph = nx.DiGraph()
        for variable in self.model.variables.values():
            graph.add_node(variable.name, kind=variable.kind, units=variable.units)
        for dependency in self.model.dependencies:
            graph.add_edge(dependency.source, dependency.target, relation=dependency.relation)
        return graph

    def view_graph(self, view_name: str, only_model_variables: bool = True) -> nx.DiGraph:
        view = self.model.views[view_name]
        graph = nx.DiGraph()

        for element in view.elements:
            if element.kind != "variable":
                continue
            if only_model_variables and element.name not in self.model.variables:
                continue
            variable = self.model.variables.get(element.name)
            graph.add_node(
                element.name,
                kind=variable.kind if variable else "auxiliary",
                units=variable.units if variable else "",
            )

        for edge in view.edges:
            if edge.source_name and edge.target_name:
                if edge.source_name in graph and edge.target_name in graph:
                    graph.add_edge(edge.source_name, edge.target_name, relation="view")

        return graph

    def view_dependency_graph(self, view_name: str) -> nx.DiGraph:
        """Dependency-Graph, reduziert auf Variablen, die in einer View vorkommen."""
        view = self.model.views[view_name]
        names = {name for name in view.variable_names() if name in self.model.variables}
        full = self.dependency_graph()
        return full.subgraph(names).copy()

    def neighborhood_graph(
        self,
        target: str,
        upstream_depth: int = 1,
        downstream_depth: int = 1,
    ) -> nx.DiGraph:
        graph = self.dependency_graph()
        if target not in graph:
            raise KeyError(f"Variable not found: {target}")

        nodes = {target}
        nodes |= self._walk(graph.reverse(copy=False), target, upstream_depth)
        nodes |= self._walk(graph, target, downstream_depth)
        return graph.subgraph(nodes).copy()

    @staticmethod
    def _walk(graph: nx.DiGraph, start: str, depth: int) -> set[str]:
        visited: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(start, 0)])
        while queue:
            node, level = queue.popleft()
            if level >= depth:
                continue
            for successor in graph.successors(node):
                if successor not in visited:
                    visited.add(successor)
                    queue.append((successor, level + 1))
        return visited


class GraphvizModelVisualizer:
    """Saubere Graphviz-SVGs fuer statische Quarto-HTML-Dokumentation."""

    def __init__(self, builder: ModelGraphBuilder) -> None:
        self.builder = builder
        self.model = builder.model

    def draw_neighborhood_svg(
        self,
        target: str,
        upstream_depth: int = 2,
        downstream_depth: int = 1,
        direction: str = "LR",
        show_units: bool = True,
        show_kind: bool = True,
    ) -> str:
        graph = self.builder.neighborhood_graph(
            target=target,
            upstream_depth=upstream_depth,
            downstream_depth=downstream_depth,
        )
        dot = self._base_dot(f"neighborhood_{self._safe_id(target)}", direction=direction)
        dot.attr(label=f"Dependency-Umfeld: {target}", labelloc="t", fontsize="18")

        for node in graph.nodes:
            variable = self.model.variables.get(node)
            kind = variable.kind if variable else "auxiliary"
            units = variable.units if variable else ""
            style = self._style_for_kind(kind)
            if node == target:
                style = {**style, "penwidth": "3.0", "color": "#dc2626", "fillcolor": "#fee2e2"}
            dot.node(
                self._safe_id(node),
                label=self._node_label(node, kind, units, show_units, show_kind),
                **style,
            )

        for source, target_node in graph.edges:
            dot.edge(self._safe_id(source), self._safe_id(target_node))

        return dot.pipe(format="svg").decode("utf-8")

    def draw_view_svg(
        self,
        view_name: str,
        direction: str = "LR",
        show_units: bool = False,
        show_kind: bool = True,
        dependency_edges: bool = False,
    ) -> str:
        graph = (
            self.builder.view_dependency_graph(view_name)
            if dependency_edges
            else self.builder.view_graph(view_name)
        )
        dot = self._base_dot(f"view_{self._safe_id(view_name)}", direction=direction)
        edge_label = "Dependencies" if dependency_edges else "Vensim-View-Pfeile"
        dot.attr(label=f"{view_name} ({edge_label})", labelloc="t", fontsize="18")

        for node in graph.nodes:
            variable = self.model.variables.get(node)
            kind = variable.kind if variable else "auxiliary"
            units = variable.units if variable else ""
            dot.node(
                self._safe_id(node),
                label=self._node_label(node, kind, units, show_units, show_kind),
                **self._style_for_kind(kind),
            )

        for source, target in graph.edges:
            dot.edge(self._safe_id(source), self._safe_id(target))

        return dot.pipe(format="svg").decode("utf-8")

    def draw_full_dependency_svg(
        self,
        max_nodes: int = 60,
        direction: str = "LR",
        show_units: bool = False,
        show_kind: bool = True,
    ) -> str:
        graph = self.builder.dependency_graph()
        if graph.number_of_nodes() > max_nodes:
            degrees = dict(graph.degree())
            selected_nodes = sorted(degrees, key=degrees.get, reverse=True)[:max_nodes]
            graph = graph.subgraph(selected_nodes).copy()

        dot = self._base_dot("full_dependency_graph", direction=direction)
        dot.attr(label=f"Reduzierter Gesamtgraph: Top {graph.number_of_nodes()} vernetzte Variablen", labelloc="t", fontsize="18")

        for node in graph.nodes:
            variable = self.model.variables.get(node)
            kind = variable.kind if variable else "auxiliary"
            units = variable.units if variable else ""
            dot.node(
                self._safe_id(node),
                label=self._node_label(node, kind, units, show_units, show_kind),
                **self._style_for_kind(kind),
            )

        for source, target in graph.edges:
            dot.edge(self._safe_id(source), self._safe_id(target))

        return dot.pipe(format="svg").decode("utf-8")

    def _base_dot(self, name: str, direction: str = "LR") -> Digraph:
        dot = Digraph(name=name, format="svg")
        dot.attr(
            rankdir=direction,
            bgcolor="white",
            splines="ortho",
            nodesep="0.55",
            ranksep="0.85",
            concentrate="false",
            fontname="Helvetica",
        )
        dot.attr(
            "node",
            shape="box",
            style="rounded,filled",
            fontname="Helvetica",
            fontsize="10",
            margin="0.12,0.08",
            color="#4b5563",
            fillcolor="#f9fafb",
        )
        dot.attr(
            "edge",
            color="#6b7280",
            arrowsize="0.7",
            penwidth="1.2",
            fontname="Helvetica",
            fontsize="9",
        )
        return dot

    def _style_for_kind(self, kind: str) -> dict[str, str]:
        styles = {
            "stock": {"shape": "box", "fillcolor": "#dbeafe", "color": "#1d4ed8", "penwidth": "2.0"},
            "flow": {"shape": "box", "fillcolor": "#ede9fe", "color": "#7c3aed", "penwidth": "1.8"},
            "auxiliary": {"shape": "box", "fillcolor": "#f9fafb", "color": "#6b7280"},
            "constant": {"shape": "ellipse", "fillcolor": "#ecfdf5", "color": "#047857"},
            "lookup": {"shape": "component", "fillcolor": "#fef3c7", "color": "#b45309"},
            "control": {"shape": "folder", "fillcolor": "#f3f4f6", "color": "#374151"},
        }
        return styles.get(kind.lower(), styles["auxiliary"])

    @staticmethod
    def _node_label(name: str, kind: str, units: str, show_units: bool, show_kind: bool) -> str:
        meta: list[str] = []
        if show_kind:
            meta.append(kind)
        if show_units and units:
            meta.append(units)
        return name if not meta else f"{name}\n({ ' | '.join(meta) })"

    @staticmethod
    def _safe_id(value: str) -> str:
        return "n_" + "".join(char if char.isalnum() else "_" for char in value)


class MermaidExporter:
    """Erzeugt Mermaid-Code als Fallback oder fuer Markdown-Beispiele."""

    def __init__(self, builder: ModelGraphBuilder) -> None:
        self.builder = builder

    def neighborhood_mermaid(
        self,
        target: str,
        upstream_depth: int = 1,
        downstream_depth: int = 1,
        direction: str = "LR",
    ) -> str:
        graph = self.builder.neighborhood_graph(target, upstream_depth, downstream_depth)
        return self._to_mermaid(graph, direction=direction)

    @staticmethod
    def _to_mermaid(graph: nx.DiGraph, direction: str = "LR") -> str:
        lines = [f"graph {direction}"]
        node_ids = {node: f"n{i}" for i, node in enumerate(graph.nodes(), start=1)}
        for node, node_id in node_ids.items():
            safe_label = str(node).replace('"', "'")
            lines.append(f'    {node_id}["{safe_label}"]')
        for source, target in graph.edges():
            lines.append(f"    {node_ids[source]} --> {node_ids[target]}")
        return "\n".join(lines)
