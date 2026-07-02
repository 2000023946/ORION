import pytest

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.query_request_factory import QueryRequestFactory
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest


def test_query_request_factory_success():
    query = Query(text="hello world")

    registry = ToolOutputRegistry(query=query)

    factory = QueryRequestFactory()

    tool_name = ToolName("VECTOR_SEARCH_TOOL")

    request = factory.create(tool_name, registry)

    assert isinstance(request, ToolRequest)
    assert request.tool_name == tool_name
    assert request.params[ToolIOKeys.QUERY] == query


def test_query_request_factory_missing_query_raises():
    registry = ToolOutputRegistry(query=Query(text="init"))

    # manually remove query to simulate missing state
    registry.registry.pop(ToolIOKeys.QUERY)

    factory = QueryRequestFactory()

    with pytest.raises(ValueError):
        factory.create(ToolName("VECTOR_SEARCH_TOOL"), registry)