from dataclasses import dataclass

from src.infrastructure.real.graph_executor.real_graph_executor import ToolInputs

@dataclass
class Variable:
    name: ToolInputs
    type: str
    description: str
    required: bool = True