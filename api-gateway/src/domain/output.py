from dataclasses import dataclass
from src.domain.variable import Variable


@dataclass
class Output(Variable):
    """Variables that are used for outputs"""

    def __post_init__(self):
        suffix = " (this field is output)"
        if suffix not in self.description:
            self.description += suffix