from dataclasses import dataclass
from src.domain.tool_name import ToolName
from src.domain.input import Input
from src.domain.output import Output

@dataclass
class Tool:
    name: ToolName
    description: str
    inputs: list[Input]
    outputs: list[Output]