from src.config import Config
from src.domain.result_item import ResultItem
from src.domain.retrieval_step import RetrievalStep
from src.domain.tool_description import ToolDescription
from src.infrastructure.real.tools.requests.meta_data_search_request import MetadataRequest
from src.ports.http_port import HttpPort
from src.ports.tool_execution_port import ToolExecutionPort


class MetadataTool(ToolExecutionPort):

    def __init__(self, http_port: HttpPort, config: Config):
        self.http_port = http_port
        self.config = config

    def execute(self, step: RetrievalStep) -> ResultItem:

        # 1. Convert retrieval step → metadata request
        request = MetadataRequest.from_retrieval_step(step)

        # 2. Call external metadata service (DB/API)
        response = self.http_port.post(
            url=self.config.METADATA_API,
            body=request.to_dict()
        )

        # 3. Return unified result format
        return ResultItem(
            content=response.get("content", ""),
            score=response.get("score", 0.0)
        )

    def describe(self) -> ToolDescription:
        return ToolDescription(
            name="Metadata Tool",
            description=(
                "Retrieves structured metadata about documents, entities, or stored records. "
                "Useful when the system needs factual or structured attributes rather than semantic search."
            ),
            inputs=[
                "query: str (text or identifier used to fetch metadata)",
                "filters: dict (optional constraints for narrowing metadata results)"
            ],
            outputs=[
                "ResultItem containing structured metadata content and relevance score"
            ]
        )