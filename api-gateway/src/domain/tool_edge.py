from src.domain.tool_description import ToolName
class ToolEdge:
    def __init__(self, source: ToolName, to: ToolName):
        self.source = source
        self.to = to
