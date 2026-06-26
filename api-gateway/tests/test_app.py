import pytest

from src.components.app import Application
from src.application.mcp_orchestrator import MCPOrchestrator

from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.infrastructure.real.tools.vector_service.vector_search_tool import VectorSearchTool
from src.infrastructure.real.tools.filter_service.filter_tool import FilterTool
from src.infrastructure.real.tools.metadata_service.metadata_tool import MetadataTool
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool


def test_application_initializes_all_components():
    app = Application()

    assert isinstance(app.http, DummyHttpAdapter)

    assert isinstance(app.vector_tool, VectorSearchTool)
    assert isinstance(app.filter_tool, FilterTool)
    assert isinstance(app.metadata_tool, MetadataTool)
    assert isinstance(app.web_tool, WebSearchTool)

    assert isinstance(app.orchestrator, MCPOrchestrator)