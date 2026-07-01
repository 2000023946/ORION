from dataclasses import dataclass

@dataclass(frozen=True)
class ToolName:
    name: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, ToolName):
            return False
        return self.name == other.name