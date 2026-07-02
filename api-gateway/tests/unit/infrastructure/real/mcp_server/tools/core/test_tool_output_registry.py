import pytest

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.ports.tool_response import ToolResponse


def test_registry_stores_initial_query():
    query = Query(text="hello world")

    registry = ToolOutputRegistry(query=query)

    assert registry.get(ToolIOKeys.QUERY) == query


def test_save_response_adds_values():
    query = Query(text="test")
    registry = ToolOutputRegistry(query=query)

    response = ToolResponse(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        output={
            ToolIOKeys.WEB_RESULTS: ["result1", "result2"]
        },
        success=True
    )

    registry.save_response(response)

    assert registry.get(ToolIOKeys.WEB_RESULTS) == ["result1", "result2"]


def test_save_response_overwrites_existing_key():
    query = Query(text="test")
    registry = ToolOutputRegistry(query=query)

    registry.save_response(
        ToolResponse(
            tool_name=ToolName("T1"),
            output={ToolIOKeys.WEB_RESULTS: ["a"]}
        )
    )

    registry.save_response(
        ToolResponse(
            tool_name=ToolName("T2"),
            output={ToolIOKeys.WEB_RESULTS: ["b"]}
        )
    )

    assert registry.get(ToolIOKeys.WEB_RESULTS) == ["b"]


def test_get_missing_key_raises():
    query = Query(text="test")
    registry = ToolOutputRegistry(query=query)

    with pytest.raises(ValueError) as e:
        registry.get(ToolIOKeys.WEB_RESULTS)

    assert "not in ToolOutputRegistry" in str(e.value)