class Context:
    def __init__(self, context: dict[str, any]):
        self.context = context

    def get(self, key: str) -> any:
        return self.context[key]