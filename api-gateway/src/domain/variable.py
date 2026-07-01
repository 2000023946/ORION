from dataclasses import dataclass

from src.infrastructure.real.graph_executor.real_graph_executor import ToolIOKeys

@dataclass
class Variable:
    name: ToolIOKeys
    type: str
    description: str
    required: bool = True