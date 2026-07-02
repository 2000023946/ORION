from typing import Any

from src.domain.query import Query
from src.infrastructure.config.settings import settings
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter
from src.infrastructure.real.mcp_client.planning.prompt_factory import PromptFactory
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter import DBFilter
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_request import DBFilterRequest
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_response import DBFilterResponse
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.ports.tool_response import ToolResponse


class DBFilterTool(ToolPort):

    def __init__(
        self,
        http_client: HttpClientPort,
        llm_port: LLMPort,
        prompt_factory: PromptFactory,
        json_parser: JsonAdapter
    ):
        self.http_client = http_client
        self.llm_port = llm_port
        self.prompt_factory = prompt_factory
        self.json_parser = json_parser

    async def execute(self, tool_request: ToolRequest) -> ToolResponse:

        # ----------------------------
        # 1. Parse request
        # ----------------------------
        request = DBFilterRequest.create(tool_request)
        query: Query = request.query

        # ----------------------------
        # 2. Create prompt
        # ----------------------------
        prompt = self.prompt_factory.create_db_filter_prompt(query)

        # ----------------------------
        # 3. Call LLM
        # ----------------------------
        llm_response: LLMResponse = await self.llm_port.generate(prompt)
        # ----------------------------
        # 4. Parse JSON
        # ----------------------------
        parsed_json: dict[str, Any] = self.json_parser.to_json(llm_response.raw)
        # ----------------------------
        # 5. Convert to DBFilter
        # ----------------------------
        db_filter: DBFilter = DBFilter.create(parsed_json)
        db_query: dict[str, Any] = db_filter.get_db_query()
        # ----------------------------
        # 7. Call database
        # ----------------------------
        response = await self.http_client.post(
            url=f"{settings.metadata_db_url}/query",
            json={
                "index": settings.metadata_db_index,
                "filter": db_query
            },
            timeout=settings.http_timeout
        )

        raw_docs = response.require("documents")

        # ----------------------------
        # 8. Convert to typed response
        # ----------------------------
        db_response = DBFilterResponse.from_raw(raw_docs)

        # ----------------------------
        # 9. Return ToolResponse
        # ----------------------------
        return ToolResponse(
            tool_name=tool_request.tool_name,
            output={
                ToolIOKeys.DOCUMENTS: db_response.documents
            },
            success=True
        )