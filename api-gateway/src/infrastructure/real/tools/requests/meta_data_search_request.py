from dataclasses import dataclass, field
from src.domain.retrieval_step import RetrievalStep


@dataclass
class MetadataRequest:
    ids: list[str]
    params: dict = field(default_factory=dict)

    @classmethod
    def from_retrieval_step(cls, step: RetrievalStep):
        if step.type != "metadata":
            raise ValueError(
                f"Expected step type 'metadata', got '{step.type}'"
            )

        # Expect IDs to come from params or input
        # (you can standardize later in MCP planner)
        ids = step.params.get("ids")

        if not ids:
            raise ValueError("MetadataRequest requires 'ids' in step.params")

        return cls(
            ids=ids,
            params=step.params
        )

    def to_dict(self):
        return {
            "ids": self.ids,
            "params": self.params
        }