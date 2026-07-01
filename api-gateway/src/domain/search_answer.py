class SearchAnswer:
    def __init__(self, answer: str):
        self.answer = answer

    def __repr__(self):
        return f"SearchAnswer(answer={self.answer})"
    
    def to_dict(self):
        return {"answer": self.answer}