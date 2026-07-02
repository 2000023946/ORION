from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


def test_tool_io_keys_values():
    assert ToolIOKeys.QUERY.value == "query"
    assert ToolIOKeys.WEB_RESULTS.value == "results"
    assert ToolIOKeys.DOCUMENTS.value == "documents"
    assert ToolIOKeys.METADATA.value == "metadata"
    assert ToolIOKeys.DOCS_IDS.value == "docs_ids"


def test_tool_io_keys_lookup_by_value():
    assert ToolIOKeys("query") is ToolIOKeys.QUERY
    assert ToolIOKeys("results") is ToolIOKeys.WEB_RESULTS
    assert ToolIOKeys("documents") is ToolIOKeys.DOCUMENTS
    assert ToolIOKeys("metadata") is ToolIOKeys.METADATA
    assert ToolIOKeys("docs_ids") is ToolIOKeys.DOCS_IDS


def test_tool_io_keys_contains_expected_number_of_members():
    assert len(ToolIOKeys) == 5