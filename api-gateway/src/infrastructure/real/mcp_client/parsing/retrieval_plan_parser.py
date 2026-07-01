from infrastructure.real.mcp_client.parsing.json_port import JsonPort
from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName


class RetrievalPlanParser:

    def __init__(self, json: JsonPort):
        self.json = json

    def parse(self, edge_str: str) -> list[ToolEdge]:
        """
        Converts LLM JSON string into list of ToolEdge.
        Expected format:
        {
            "edges": [["A","B"], ["A","C"]]
        }
        """

        try:
            data = self.json.to_json(edge_str)
        except Exception as e:
            raise ValueError(f"Invalid JSON from LLM: {e}")

        if "edges" not in data:
            raise ValueError("Missing 'edges' field")

        edges: list[ToolEdge] = []

        for edge in data["edges"]:
            if len(edge) != 2:
                raise ValueError(f"Invalid edge format: {edge}")

            src, dst = edge

            edges.append(
                ToolEdge(
                    source=ToolName(src),
                    to=ToolName(dst)
                )
            )

        return edges