import pytest

from src.domain.query import Query
from src.domain.tool_name import ToolName

from src.infrastructure.real.mcp_server.tools.core.docs_ids_request_factory import DocsIdsRequestFactory
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import (
    ToolOutputRegistry,
)
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId
from src.ports.tool_response import ToolResponse


class TestDocsIdsRequestFactory:

    def test_create_builds_tool_request_with_doc_ids(self):
        # Arrange
        factory = DocsIdsRequestFactory()
        tool_name = ToolName("TEST_TOOL")

        registry = ToolOutputRegistry(Query("test query"))

        registry.save_response(
            ToolResponse(
                tool_name=tool_name,
                output={
                    ToolIOKeys.DOCS_IDS: [
                        {"id": "doc1"},
                        {"id": "doc2"},
                        {"id": "doc3"},
                    ]
                }
            )
        )

        # Act
        request = factory.create(tool_name, registry)

        # Assert
        assert request.tool_name == tool_name

        doc_ids = request.params[ToolIOKeys.DOCS_IDS]

        assert len(doc_ids) == 3
        assert all(isinstance(doc, DocId) for doc in doc_ids)
        assert [doc.doc_id for doc in doc_ids] == ["doc1", "doc2", "doc3"]