from src.config import Config

from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.config import config
from src.infrastructure.real.tools.registry.tool_registry import ToolRegistry

from src.infrastructure.real.tools.vector_service.vector_search_tool import VectorSearchTool
from src.infrastructure.real.tools.filter_service.filter_tool import FilterTool
from src.infrastructure.real.tools.metadata_service.metadata_tool import MetadataTool
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool

from src.ports.tool_execution_port import ToolExecutionPort


def test_get_tools_returns_all_registered_tools():
    http = DummyHttpAdapter()

    registry = ToolRegistry(http, config)

    tools = registry.get_tools()

    assert len(tools) == 4

    assert isinstance(tools[0], VectorSearchTool)
    assert isinstance(tools[1], FilterTool)
    assert isinstance(tools[2], MetadataTool)
    assert isinstance(tools[3], WebSearchTool)

    for tool in tools:
        assert isinstance(tool, ToolExecutionPort)