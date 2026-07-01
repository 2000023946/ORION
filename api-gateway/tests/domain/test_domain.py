import pytest

from src.domain.query import Query
from src.domain.result_item import ResultItem
from src.domain.tool_type import ToolType
from src.domain.retrieval_step import RetrievalStep
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.retrieval_result import RetrievalResult
from src.domain.search_answer import SearchAnswer
from src.domain.tool_description import ToolDescription


# -------------------------
# Query
# -------------------------
def test_query():

    q = Query(text="hello")

    assert q.text == "hello"


# -------------------------
# ResultItem
# -------------------------
def test_result_item():

    r = ResultItem(content="data")

    assert r.content == "data"


# -------------------------
# ToolType
# -------------------------
def test_tool_type():

    assert ToolType.WEB_SEARCH.value == "web_search"
    assert ToolType.VECTOR_SEARCH.value == "vector_search"
    assert ToolType.METADATA.value == "metadata"
    assert ToolType.FILTER.value == "filter"


# -------------------------
# RetrievalStep
# -------------------------
def test_retrieval_step():

    step = RetrievalStep(
        tool_type=ToolType.WEB_SEARCH,
        params={"q": "test"}
    )

    assert step.tool_type == ToolType.WEB_SEARCH
    assert step.params["q"] == "test"


# -------------------------
# RetrievalResult
# -------------------------
def test_retrieval_result():

    item = ResultItem(content="x")

    rr = RetrievalResult(
        tool_type=ToolType.FILTER,
        items=[item]
    )

    assert rr.tool_type == ToolType.FILTER
    assert len(rr.items) == 1
    assert rr.items[0].content == "x"


# -------------------------
# SearchAnswer
# -------------------------
def test_search_answer():

    a = SearchAnswer(answer="final")

    assert a.answer == "final"
    assert isinstance(a.sources, list)


# -------------------------
# ToolDescription
# -------------------------
def test_tool_description():

    d = ToolDescription(
        name="web",
        description="search",
        inputs=["q"],
        outputs=["results"]
    )

    assert d.name == "web"
    assert "q" in d.inputs


# -------------------------
# RetrievalPlan
# -------------------------
def test_retrieval_plan():

    plan = RetrievalPlan(
        edges=[("A", "B")]
    )

    assert plan.edges == [("A", "B")]