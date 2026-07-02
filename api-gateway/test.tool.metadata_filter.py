"""
Metadata Filter Tool - Integration Test

This file seeds MongoDB, initializes the MetadataFilterTool,
and executes a real filter request.

Expected behavior:
- MongoDB is seeded with test data
- Tool connects through RealHttpClient
- Tool queries MongoDB via backend service
- Returns filtered documents
"""
import asyncio
from src.infrastructure.config.settings import settings
from src.infrastructure.config.mongo_seeder import MongoSeeder
from src.infrastructure.config.seed_data import SEED_DATA
from src.infrastructure.real.mcp_server.tools.core.tool_information import METADATA_FILTER_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.metadata_filter.mongo_http_client import MongoHttpClient
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId
from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_filter_tool import MetadataFilterTool


async def main() -> None:
    """
    End-to-end integration test for MetadataFilterTool.
    """

    # ----------------------------
    # 1. Seed MongoDB
    # ----------------------------
    seeder = MongoSeeder()
    seeder.reset_and_seed(SEED_DATA)
    print("Successfully seeded DB!")

    # ----------------------------
    # 2. Create HTTP client
    # ----------------------------
    http_client = MongoHttpClient(
        uri=settings.metadata_db_url, 
        db_name=settings.metadata_db_name
    )

    # ----------------------------
    # 3. Build test request
    # ----------------------------
    ids = [DocId("p1"), DocId("p6")]

    tool_request = ToolRequest(
        tool_name=METADATA_FILTER_TOOL.name,
        params={
            ToolIOKeys.DOCS_IDS: ids
        }
    )

    # ----------------------------
    # 4. Execute tool
    # ----------------------------
    tool = MetadataFilterTool(http_client=http_client)

    response = await tool.execute(tool_request)

    # ----------------------------
    # 5. Print results
    # ----------------------------
    print("\n=== METADATA FILTER RESPONSE ===")
    print(response)

    print("\nTool initialized:", tool)


if __name__ == "__main__":
    asyncio.run(main())