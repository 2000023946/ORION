from src.infrastructure.real.mcp_server.tools.web_search.web_search_result import WebSearchResult


# -------------------------
# BASIC FIELD ASSIGNMENT
# -------------------------
def test_web_search_result_fields():

    result = WebSearchResult(
        title="AI Overview",
        url="https://example.com/ai",
        snippet="Artificial intelligence is...",
        score=0.95
    )

    assert result.title == "AI Overview"
    assert result.url == "https://example.com/ai"
    assert result.snippet == "Artificial intelligence is..."
    assert result.score == 0.95


# -------------------------
# DEFAULT SCORE IS NONE
# -------------------------
def test_web_search_result_default_score():

    result = WebSearchResult(
        title="AI Overview",
        url="https://example.com/ai",
        snippet="Artificial intelligence is..."
    )

    assert result.score is None


# -------------------------
# TYPE STABILITY CHECK
# -------------------------
def test_web_search_result_is_dataclass():

    result = WebSearchResult(
        title="t",
        url="u",
        snippet="s"
    )

    assert isinstance(result, WebSearchResult)
    assert hasattr(result, "title")
    assert hasattr(result, "url")
    assert hasattr(result, "snippet")
    assert hasattr(result, "score")