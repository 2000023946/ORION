from dataclasses import dataclass


@dataclass
class Tool:
    name: ToolName
    description: str
    inputs: list[Input]
    outputs: list[Output]