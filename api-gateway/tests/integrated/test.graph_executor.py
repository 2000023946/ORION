import asyncio

from src.components.graph_executor_infrastructure import (
    GraphExecutorInfrastructure,
)
from src.components.mcp_server_infrastructure import (
    MCPServerInfrastructure,
)
from src.constants.constants import START_TOOL, END_TOOL
from src.domain.query import Query
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_edge import ToolEdge
from src.infrastructure.real.mcp_server.tools.core.tool_information import (
    VECTOR_SEARCH_TOOL,
    METADATA_FILTER_TOOL,
    WEB_SEARCH_TOOL,
)


async def main():
    # Build a simple retrieval plan
    plan = RetrievalPlan(
        [
            ToolEdge(START_TOOL, VECTOR_SEARCH_TOOL.name),
            ToolEdge(START_TOOL, WEB_SEARCH_TOOL.name),
            ToolEdge(WEB_SEARCH_TOOL.name, END_TOOL),
            ToolEdge(VECTOR_SEARCH_TOOL.name, METADATA_FILTER_TOOL.name),
            ToolEdge(METADATA_FILTER_TOOL.name, END_TOOL),
        ]
    )

    print("Retrieval Plan")
    print(plan)
    print()

    # Infrastructure
    mcp_server = MCPServerInfrastructure().mcp_server
    graph_executor = GraphExecutorInfrastructure().graph_executor

    # Query
    query = Query("find the newest iphones")

    # Execute
    context = await graph_executor.execute(
        query=query,
        plan=plan,
        mcp_server=mcp_server,
    )

    print("Execution Context")
    print(context.context)


if __name__ == "__main__":
    asyncio.run(main())