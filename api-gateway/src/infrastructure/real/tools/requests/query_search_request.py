from dataclasses import dataclass, field
from src.domain.retrieval_step import RetrievalStep
from src.domain.query import Query

@dataclass
class QuerySearchRequest:
    query: Query

    @classmethod
    def from_retrieval_step(cls, step: RetrievalStep):
        if 'query' not in step.params:
            raise ValueError("expected query in params, did not receive!")
        return cls(
            query = Query(step.params['query'])
        )

    def to_dict(self):
        return {
            "query": self.query.text,
        }