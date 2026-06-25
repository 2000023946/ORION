from dataclasses import dataclass, field
from src.domain.retrieval_step import RetrievalStep
from src.domain.query import Query

@dataclass
class QuerySearchRequest:
    query: Query
    params: dict = field(default_factory=dict)

    @classmethod
    def from_retrieval_step(cls, step: RetrievalStep):
        if step.type != "query":
            raise ValueError(
                f"Expected step type 'query', got '{step.type}'"
            )

        return cls(
            query=Query(step.input),
            params=step.params
        )

    def to_dict(self):
        return {
            "query": self.query.text,
            "params": self.params
        }