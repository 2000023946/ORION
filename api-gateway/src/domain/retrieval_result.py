from src.domain.result_item import ResultItem

class RetrievalResult:
    def __init__(self, step_id: str, items: list[ResultItem]):
        self.step_id = step_id
        self.items = items