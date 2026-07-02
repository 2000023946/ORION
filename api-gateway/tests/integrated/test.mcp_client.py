import asyncio
from collections import defaultdict, deque
from typing import DefaultDict, Dict, List, Set

from src.components.mcp_client_infrastructure import MCPClientInfrastructure
from src.constants.constants import START_TOOL
from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_information import (
    DB_FILTER_TOOL,
    METADATA_FILTER_TOOL,
    VECTOR_SEARCH_TOOL,
    WEB_SEARCH_TOOL,
)




Graph = Dict[ToolName, List[ToolName]]


def draw_dag_levels(graph: Graph) -> None:
    """
    Prints DAG as BFS execution levels.
    Each level represents tools that can run in parallel.
    """

    print("\n=== DAG LEVELS (BFS) ===\n")

    levels: DefaultDict[int, List[ToolName]] = defaultdict(list)
    visited: Set[ToolName] = set()

    queue: deque[tuple[ToolName, int]] = deque([(START_TOOL, 0)])
    visited.add(START_TOOL)

    while queue:
        node, level = queue.popleft()

        levels[level].append(node)

        for child in graph.get(node, []):
            if child not in visited:
                visited.add(child)
                queue.append((child, level + 1))

    for level in sorted(levels.keys()):
        tools = ", ".join(str(tool) for tool in levels[level])
        print(f"Level {level}: {tools}")


async def main() -> None:
    mcp_client_infrastructure = MCPClientInfrastructure()
    mcp_client = mcp_client_infrastructure.mcp_client

    tools = [
        VECTOR_SEARCH_TOOL,
        WEB_SEARCH_TOOL,
        DB_FILTER_TOOL,
        METADATA_FILTER_TOOL,
    ]

    query = Query("phones with good battery life")

    plan = await mcp_client.create_plan(
        query=query,
        tools=tools,
    )

    print("\n=== EDGES ===")
    print(plan.edges)

    draw_dag_levels(plan.graph)


if __name__ == "__main__":
    asyncio.run(main())