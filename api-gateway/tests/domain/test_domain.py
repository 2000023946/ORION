import pytest

from src.domain.query import Query
from src.domain.retrieval_step import RetrievalStep
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.result_item import ResultItem
from src.domain.retrieval_result import RetrievalResult
from src.domain.search_answer import SearchAnswer
from src.domain.tool_description import ToolDescription


# -------------------------
# 1. Query test
# -------------------------
def test_query_creation():
    q = Query(text="what is AI?")
    assert q.text == "what is AI?"


# -------------------------
# 2. RetrievalStep basic
# -------------------------
def test_retrieval_step_basic():
    step = RetrievalStep(
        step_id="s1",
        type="semantic_search",
        input="AI agents",
        params={"top_k": 5},
        depends_on=[]
    )

    assert step.step_id == "s1"
    assert step.type == "semantic_search"
    assert step.input == "AI agents"
    assert step.params["top_k"] == 5
    assert step.depends_on == []


# -------------------------
# 3. RetrievalStep dependencies
# -------------------------
def test_retrieval_step_with_dependencies():
    step = RetrievalStep(
        step_id="s2",
        type="filter",
        input="s1",
        params={"max_results": 10},
        depends_on=["s1"]
    )

    assert step.depends_on == ["s1"]
    assert step.input == "s1"


# -------------------------
# 4. RetrievalPlan DAG structure
# -------------------------
def test_retrieval_plan_graph_structure():
    step1 = RetrievalStep("s1", "semantic_search", "AI", {})
    step2 = RetrievalStep("s2", "web_search", "AI news", {"recency": 7})
    step3 = RetrievalStep("s3", "filter", "s1+s2", {})

    steps = {
        "s1": step1,
        "s2": step2,
        "s3": step3
    }

    edges = [
        ("s1", "s3"),
        ("s2", "s3")
    ]

    plan = RetrievalPlan(query="AI query", steps=steps, edges=edges)

    assert plan.query == "AI query"
    assert len(plan.steps) == 3
    assert ("s1", "s3") in plan.edges
    assert ("s2", "s3") in plan.edges


# -------------------------
# 5. ResultItem test
# -------------------------
def test_result_item():
    item = ResultItem(content="AI is a field of CS", score=0.95)

    assert item.content == "AI is a field of CS"
    assert item.score == 0.95


# -------------------------
# 6. RetrievalResult test
# -------------------------
def test_retrieval_result():
    item1 = ResultItem("doc1", 0.9)
    item2 = ResultItem("doc2", 0.8)

    result = RetrievalResult(step_id="s1", items=[item1, item2])

    assert result.step_id == "s1"
    assert len(result.items) == 2
    assert result.items[0].score == 0.9


# -------------------------
# 7. SearchAnswer test
# -------------------------
def test_search_answer():
    answer = SearchAnswer(
        answer="AI is machine intelligence",
        sources=["doc1", "doc2"]
    )

    assert "AI" in answer.answer
    assert len(answer.sources) == 2


# -------------------------
# 8. Defaults test
# -------------------------
def test_defaults():
    step = RetrievalStep(
        step_id="s1",
        type="web_search",
        input="AI news"
    )

    assert step.params == {}
    assert step.depends_on == []
    


def test_tool_description_creation():
    desc = ToolDescription(
        name="Vector Search",
        description="Searches vector DB",
        inputs=["query: str", "top_k: int"],
        outputs=["List[ResultItem]"]
    )

    assert desc.name == "Vector Search"
    assert desc.description == "Searches vector DB"
    assert desc.inputs == ["query: str", "top_k: int"]
    assert desc.outputs == ["List[ResultItem]"]


def test_tool_description_equality():
    desc1 = ToolDescription(
        name="Tool A",
        description="desc",
        inputs=["a"],
        outputs=["b"]
    )

    desc2 = ToolDescription(
        name="Tool A",
        description="desc",
        inputs=["a"],
        outputs=["b"]
    )

    assert desc1 == desc2