from src.domain.retrieval_step import RetrievalStep

class RetrievalPlan:
    def __init__(
        self,
        query: str,
        steps: dict[str, RetrievalStep],
        edges: list[tuple[str, str]]
    ):
        self.query = query
        self.steps = steps
        self.edges = edges