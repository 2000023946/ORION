import pytest

from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.docs_ids_request_factory import DocsIdsRequestFactory
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


def test_docs_ids_request_factory_success():
    doc_ids = [DocId("1"), DocId("2")]

    registry = ToolOutputRegistry(query=None)  # query not needed for this factory
    registry.registry[ToolIOKeys.DOCS_IDS] = doc_ids

    factory = DocsIdsRequestFactory()

    tool_name = ToolName("METADATA_FILTER_TOOL")

    request = factory.create(tool_name, registry)

    assert isinstance(request, ToolRequest)
    assert request.tool_name == tool_name
    assert request.params[ToolIOKeys.DOCS_IDS] == doc_ids


def test_docs_ids_request_factory_missing_docs_raises():
    registry = ToolOutputRegistry(query=None)

    factory = DocsIdsRequestFactory()

    with pytest.raises(ValueError):
        factory.create(ToolName("METADATA_FILTER_TOOL"), registry)