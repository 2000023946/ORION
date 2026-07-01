from dataclasses import dataclass
from src.domain.variable import Variable

@dataclass
class Input(Variable):
    """Variables that are used for inputs"""

    def __post_init__(self):
        # Avoid double-appending if already present
        suffix = " (this field is input)"
        if suffix not in self.description:
            self.description += suffix