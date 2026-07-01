from dataclasses import dataclass
from src.domain.variable import Variable
@dataclass
class Input(Variable):
    "Variables that are used for inputs"