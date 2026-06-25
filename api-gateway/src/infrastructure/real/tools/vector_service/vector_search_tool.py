from src.config import config
from src.domain.result_item import ResultItem
from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.real.tools.requests.query_search_request import (
    QuerySearchRequest,
)
from src.ports.http_port import HttpPort
from src.ports.tool_execution_port import ToolExecutionPort


class VectorSearchTool(ToolExecutionPort):

    def __init__(self, http_port: HttpPort):
        self.http_port = http_port

    def execute(self, step: RetrievalStep) -> ResultItem:

        request = QuerySearchRequest.from_retrieval_step(step)

        response = self.http_port.post(
            url=config.VECTOR_DB_API,
            body=request.to_dict()
        )

        return ResultItem(
            content=response.get("content", ""),
            score=response.get("score", 0.0)
        )