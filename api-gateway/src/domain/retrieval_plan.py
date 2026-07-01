from collections import defaultdict
from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName


class RetrievalPlan:
    def __init__(self, edges: list[ToolEdge]):
        self.edges = edges
        self.graph: dict[ToolName, list[ToolName]] = {}
        self.sources: list[ToolName] = []

        self.generate_graph()

    def generate_graph(self) -> dict[ToolName, list[ToolName]]:
        if self.graph:
            return self.graph

        adj_list: dict[ToolName, list[ToolName]] = defaultdict(list)
        in_degree: dict[ToolName, int] = defaultdict(int)

        # Build graph + in-degree map
        for edge in self.edges:
            src = edge.source
            dst = edge.to

            adj_list[src].append(dst)

            # ensure nodes exist in in_degree
            if dst not in in_degree:
                in_degree[dst] = 0
            if src not in in_degree:
                in_degree[src] = 0

            in_degree[dst] += 1

        self.graph = dict(adj_list)

        # Find source nodes (in-degree = 0)
        self.sources = [node for node, deg in in_degree.items() if deg == 0]

        return self.graph