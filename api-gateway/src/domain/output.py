from dataclasses import dataclass
from src.domain.variable import Variable
@dataclass
class Output(Variable):
    "Variables that are used for outputs"