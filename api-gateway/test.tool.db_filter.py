import asyncio

from src.domain.query import Query
from src.infrastructure.config.seed import MongoSeeder
from src.infrastructure.config.seed_data import SEED_DATA
from src.infrastructure.config.settings import settings
from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.mcp_client.llm.llm import LLM
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter
from src.infrastructure.real.mcp_client.planning.prompt_factory import PromptFactory
from src.infrastructure.real.mcp_server.tools.core.tool_information import DB_FILTER_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_tool import DBFilterTool
from src.infrastructure.real.mcp_server.tools.metadata_filter.mongo_http_client import MongoHttpClient


"""
DB Filter Tool Test

This script runs an end-to-end test of the DBFilterTool.

Flow:
User Query → LLM Planning → JSON Parsing → Mongo Query → Filtered Results
"""


async def main() -> None:
    # ----------------------------
    # 0. Seed MongoDB
    # ----------------------------
    seeder = MongoSeeder()
    seeder.reset_and_seed(SEED_DATA)
    print("Successfully seeded DB!")
    
    # ----------------------------
    # 1. Mongo HTTP client (DB layer)
    # ----------------------------
    mongo_http_client = MongoHttpClient(
        uri=settings.metadata_db_url,
        db_name=settings.metadata_db_name,
    )

    # ----------------------------
    # 2. LLM + supporting components
    # ----------------------------
    real_http_client = RealHttpClient()
    json_parser = JsonAdapter()
    llm = LLM(http_client=real_http_client, json_parser=json_parser)


    prompt_factory = PromptFactory()

    # ----------------------------
    # 3. DB Filter Tool
    # ----------------------------
    db_filter_tool = DBFilterTool(
        http_client=mongo_http_client,
        llm_port=llm,
        prompt_factory=prompt_factory,
        json_parser=json_parser,
    )

    # ----------------------------
    # 4. User query
    # ----------------------------
    query = "Products below $500"

    tool_request = ToolRequest(
        tool_name=DB_FILTER_TOOL.name,
        params={
            ToolIOKeys.QUERY: Query(query)
        }
    )

    # ----------------------------
    # 5. Execute pipeline
    # ----------------------------
    response = await db_filter_tool.execute(tool_request)

    # ----------------------------
    # 6. Print results
    # ----------------------------
    print("\n=== DB FILTER RESPONSE ===")
    print(response)


# ----------------------------
# Run script
# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())