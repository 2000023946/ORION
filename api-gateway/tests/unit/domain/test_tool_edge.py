from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName


def test_tool_edge_initialization():
    source = ToolName("VECTOR_SEARCH")
    target = ToolName("WEB_SEARCH")

    edge = ToolEdge(source=source, to=target)

    assert edge.source == source
    assert edge.to == target


def test_tool_edge_fields_are_independent():
    source = ToolName("A")
    target = ToolName("B")

    edge = ToolEdge(source, target)

    assert edge.source.name == "A"
    assert edge.to.name == "B"