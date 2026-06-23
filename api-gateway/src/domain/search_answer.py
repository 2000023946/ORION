class SearchAnswer:
    def __init__(self, answer: str, sources: list[str] = None):
        self.answer = answer
        self.sources = sources or []