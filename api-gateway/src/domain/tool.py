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

    def __str__(self) -> str:
        inputs = ", ".join([str(i.name) for i in self.inputs]) if self.inputs else "none"
        outputs = ", ".join([str(o.name) for o in self.outputs]) if self.outputs else "none"

        return (
            f"Tool(name={self.name}, "
            f"inputs=[{inputs}], "
            f"outputs=[{outputs}])"
        )