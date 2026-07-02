import asyncio

from src.components.mcp_server_infrastructure import MCPServerInfrastructure
from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_information import (
    VECTOR_SEARCH_TOOL,
    WEB_SEARCH_TOOL,
    DB_FILTER_TOOL,
    METADATA_FILTER_TOOL,
)
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


async def main() -> None:
    mcp_server = MCPServerInfrastructure().mcp_server

    tool_list = await mcp_server.get_tools()
    print("Tools:", tool_list)

    # ----------------------------
    # 1. Build query
    # ----------------------------
    query = Query("phones with good battery life that are under 600")
    ids = [DocId("p3"), DocId("p5")]

    # ----------------------------
    # 2. Build ToolRequests
    # ----------------------------

    vector_request = ToolRequest(
        tool_name=VECTOR_SEARCH_TOOL.name,
        params={
            ToolIOKeys.QUERY: query
        }
    )

    web_request = ToolRequest(
        tool_name=WEB_SEARCH_TOOL.name,
        params={
            ToolIOKeys.QUERY: query
        }
    )

    db_request = ToolRequest(
        tool_name=DB_FILTER_TOOL.name,
        params={
            ToolIOKeys.QUERY: query
        }
    )

    metadata_request = ToolRequest(
        tool_name=METADATA_FILTER_TOOL.name,
        params={
            ToolIOKeys.DOCS_IDS: ids
        }
    )

    # ----------------------------
    # 3. Execute ALL tools in parallel
    # ----------------------------

    results = await asyncio.gather(
        mcp_server.call_tool(VECTOR_SEARCH_TOOL.name, vector_request),
        mcp_server.call_tool(WEB_SEARCH_TOOL.name, web_request),
        mcp_server.call_tool(DB_FILTER_TOOL.name, db_request),
        mcp_server.call_tool(METADATA_FILTER_TOOL.name, metadata_request),
    )

    # ----------------------------
    # 4. Print results
    # ----------------------------

    print("\n=== VECTOR RESULT ===")
    print(results[0])

    print("\n=== WEB RESULT ===")
    print(results[1])

    print("\n=== DB FILTER RESULT ===")
    print(results[2])

    print("\n=== METADATA FILTER RESULT ===")
    print(results[3])


if __name__ == "__main__":
    asyncio.run(main())