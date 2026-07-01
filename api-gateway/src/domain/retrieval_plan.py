from collections import defaultdict

from src.constants.constants import START_TOOL, END_TOOL
from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName


class RetrievalPlan:
    def __init__(self, edges: list[ToolEdge]):
        self.edges = edges

        self.graph: dict[ToolName, list[ToolName]] = {}
        self.reverse_graph: dict[ToolName, list[ToolName]] = {}

        self.generate_graph()

    def generate_graph(self) -> dict[ToolName, list[ToolName]]:
        if self.graph:
            return self.graph

        graph: dict[ToolName, list[ToolName]] = defaultdict(list)
        reverse_graph: dict[ToolName, list[ToolName]] = defaultdict(list)

        # Ensure special nodes always exist
        graph.setdefault(START_TOOL, [])
        graph.setdefault(END_TOOL, [])

        reverse_graph.setdefault(START_TOOL, [])
        reverse_graph.setdefault(END_TOOL, [])

        for edge in self.edges:
            graph[edge.source].append(edge.to)
            reverse_graph[edge.to].append(edge.source)

            # Ensure every node exists in both graphs
            graph.setdefault(edge.to, [])
            reverse_graph.setdefault(edge.source, [])

        self.graph = dict(graph)
        self.reverse_graph = dict(reverse_graph)

        return self.graph

    def get_children(self, tool: ToolName) -> list[ToolName]:
        return self.graph.get(tool, [])

    def get_parents(self, tool: ToolName) -> list[ToolName]:
        return self.reverse_graph.get(tool, [])