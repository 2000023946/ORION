class Context:
    def __init__(self, context: dict[str, any] | None = None):
        self.context = context or {}

    def get(self, key: str) -> any:
        return self.context.get(key, {})