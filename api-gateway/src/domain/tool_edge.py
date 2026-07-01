from src.domain.tool_name import ToolName
class ToolEdge:
    def __init__(self, source: ToolName, to: ToolName):
        self.source = source
        self.to = to
