from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName
from src.constants.constants import START_TOOL, END_TOOL


def test_generate_graph_basic_structure():
    a = ToolName("A")
    b = ToolName("B")

    edges = [ToolEdge(START_TOOL, a), ToolEdge(a, b), ToolEdge(b, END_TOOL)]

    plan = RetrievalPlan(edges)

    graph = plan.graph
    reverse = plan.reverse_graph

    # nodes exist
    assert START_TOOL in graph
    assert END_TOOL in graph
    assert a in graph
    assert b in graph

    # edges correct
    assert graph[START_TOOL] == [a]
    assert graph[a] == [b]
    assert graph[b] == [END_TOOL]

    # reverse edges correct
    assert reverse[a] == [START_TOOL]
    assert reverse[b] == [a]
    assert reverse[END_TOOL] == [b]


def test_get_children():
    a = ToolName("A")
    b = ToolName("B")

    edges = [ToolEdge(START_TOOL, a), ToolEdge(a, b)]

    plan = RetrievalPlan(edges)

    assert plan.get_children(START_TOOL) == [a]
    assert plan.get_children(a) == [b]
    assert plan.get_children(b) == []


def test_get_parents():
    a = ToolName("A")
    b = ToolName("B")

    edges = [ToolEdge(START_TOOL, a), ToolEdge(a, b)]

    plan = RetrievalPlan(edges)

    assert plan.get_parents(a) == [START_TOOL]
    assert plan.get_parents(b) == [a]
    assert plan.get_parents(START_TOOL) == []


def test_bfs_linear_chain():
    a = ToolName("A")
    b = ToolName("B")
    c = ToolName("C")

    edges = [
        ToolEdge(START_TOOL, a),
        ToolEdge(a, b),
        ToolEdge(b, c),
        ToolEdge(c, END_TOOL),
    ]

    plan = RetrievalPlan(edges)

    result = plan.bfs()

    assert result == [START_TOOL, a, b, c, END_TOOL]


def test_bfs_with_branching():
    a = ToolName("A")
    b = ToolName("B")
    c = ToolName("C")

    edges = [
        ToolEdge(START_TOOL, a),
        ToolEdge(a, b),
        ToolEdge(a, c),
    ]

    plan = RetrievalPlan(edges)

    result = plan.bfs()

    # BFS order should start correct
    assert result[0] == START_TOOL
    assert a in result
    assert b in result
    assert c in result


def test_empty_edges():
    plan = RetrievalPlan([])

    # only START/END should exist
    assert plan.get_children(START_TOOL) == []
    assert plan.get_children(END_TOOL) == []

    assert plan.bfs() == [START_TOOL]