from src.ports.tool_execution_port import ToolExecutionPort
from src.domain.retrieval_step import RetrievalStep

class FilterTool(ToolExecutionPort):
    def execute(self, step: RetrievalStep):
        pass