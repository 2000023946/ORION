from dataclasses import dataclass

@dataclass
class WebSearchResult:
    title: str
    url: str
    snippet: str
    score: float | None = None