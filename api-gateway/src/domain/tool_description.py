from dataclasses import dataclass


@dataclass
class ToolDescription:
    name: str
    description: str
    inputs: list[str]
    outputs: list[str]