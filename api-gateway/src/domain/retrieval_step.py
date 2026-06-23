class RetrievalStep:
    def __init__(
        self, step_id: 
        str, type: str, 
        input: str, 
        params: dict = None, 
        depends_on: list[str] = None
    ):
        self.step_id = step_id
        self.type = type
        self.input = input
        self.params = params or {}
        self.depends_on = depends_on or []