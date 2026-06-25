from src.config import Config
from src.domain.result_item import ResultItem
from src.domain.retrieval_step import RetrievalStep
from src.domain.query import Query
from src.infrastructure.real.tools.requests.query_search_request import QuerySearchRequest
from src.infrastructure.real.llm.prompts.filter_prompt import FILTER_PROMPT
from src.ports.http_port import HttpPort
from src.ports.tool_execution_port import ToolExecutionPort


class FilterTool(ToolExecutionPort):

    def __init__(self, http_port: HttpPort, config: Config):
        self.http_port = http_port
        self.config = config

    def execute(self, step: RetrievalStep) -> ResultItem:

        # 1. Build structured request
        request = QuerySearchRequest.from_retrieval_step(step)

        # 2. First call: LLM → SQL JSON
        llm_response = self.http_port.post(
            url=self.config.DB_LLM,
            body={
                "system_prompt": FILTER_PROMPT,
                "query": request.query.text,
                "params": request.params
            }
        )

        sql_query = llm_response.get("content", "")

        # 3. Second call: execute SQL against DB service
        db_response = self.http_port.post(
            url=self.config.FILTER_API,  # or DB API endpoint
            body={
                "query": sql_query
            }
        )

        # 4. Return unified result
        return ResultItem(
            content=db_response.get("content", ""),
            score=db_response.get("score", 0.0)
        )