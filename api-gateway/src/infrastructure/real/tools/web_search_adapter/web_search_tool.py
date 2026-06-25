from src.config import Config
from src.domain.result_item import ResultItem
from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.real.tools.requests.query_search_request import (
    QuerySearchRequest,
)
from src.ports.http_port import HttpPort
from src.ports.tool_execution_port import ToolExecutionPort


class WebSearchTool(ToolExecutionPort):

    def __init__(self, http_port: HttpPort, config: Config):
        self.http_port = http_port
        self.config = config

    def execute(self, step: RetrievalStep) -> ResultItem:

        request = QuerySearchRequest.from_retrieval_step(step)

        response = self.http_port.post(
            url=self.config.WEB_API,
            body=request.to_dict()
        )

        return ResultItem(
            content=response.get("content", ""),
            score=response.get("score", 0.0)
        )