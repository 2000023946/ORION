from src.infrastructure.real.mcp_server.tools.core.tool_information import (
    VECTOR_SEARCH_TOOL,
    WEB_SEARCH_TOOL,
    DB_FILTER_TOOL,
    METADATA_FILTER_TOOL,
)
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


# -------------------------
# VECTOR SEARCH TOOL
# -------------------------
def test_vector_search_tool_structure():
    tool = VECTOR_SEARCH_TOOL

    assert tool.name.name == "VECTOR_SEARCH_TOOL"
    assert len(tool.inputs) == 1
    assert len(tool.outputs) == 1

    assert tool.inputs[0].name == ToolIOKeys.QUERY
    assert tool.outputs[0].name == ToolIOKeys.DOCS_IDS


# -------------------------
# WEB SEARCH TOOL
# -------------------------
def test_web_search_tool_structure():
    tool = WEB_SEARCH_TOOL

    assert tool.name.name == "WEB_SEARCH_TOOL"
    assert len(tool.inputs) == 1
    assert len(tool.outputs) == 1

    assert tool.inputs[0].name == ToolIOKeys.QUERY
    assert tool.outputs[0].name == ToolIOKeys.WEB_RESULTS


# -------------------------
# DB FILTER TOOL
# -------------------------
def test_db_filter_tool_structure():
    tool = DB_FILTER_TOOL

    assert tool.name.name == "DB_FILTER_TOOL"
    assert len(tool.inputs) == 2
    assert len(tool.outputs) == 1

    assert ToolIOKeys.DOCS_IDS in [i.name for i in tool.inputs]
    assert ToolIOKeys.QUERY in [i.name for i in tool.inputs]

    assert tool.outputs[0].name == ToolIOKeys.DOCUMENTS


# -------------------------
# METADATA FILTER TOOL
# -------------------------
def test_metadata_filter_tool_structure():
    tool = METADATA_FILTER_TOOL

    assert tool.name.name == "METADATA_FILTER_TOOL"
    assert len(tool.inputs) == 2
    assert len(tool.outputs) == 1

    assert ToolIOKeys.DOCS_IDS in [i.name for i in tool.inputs]
    assert ToolIOKeys.QUERY in [i.name for i in tool.inputs]

    assert tool.outputs[0].name == ToolIOKeys.DOCUMENTS


# -------------------------
# BASIC CONSISTENCY CHECK
# -------------------------
def test_all_tools_exist():
    assert VECTOR_SEARCH_TOOL is not None
    assert WEB_SEARCH_TOOL is not None
    assert DB_FILTER_TOOL is not None
    assert METADATA_FILTER_TOOL is not None