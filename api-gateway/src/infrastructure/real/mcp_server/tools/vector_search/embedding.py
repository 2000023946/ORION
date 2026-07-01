from dataclasses import dataclass


@dataclass(frozen=True)
class Embedding:
    values: list[float]

    def dimension(self) -> int:
        return len(self.values)