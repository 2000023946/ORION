import pytest  # type: ignore

from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest


# -------------------------
# HAPPY PATH
# -------------------------
def test_tool_request_get_success():

    req = ToolRequest(
        tool_name=ToolName("search_tool"),
        params={
            ToolIOKeys.QUERY: "hello world",
            ToolIOKeys.METADATA: {"source": "test"}
        }
    )

    assert req.get(ToolIOKeys.QUERY) == "hello world"
    assert req.get(ToolIOKeys.METADATA) == {"source": "test"}


# -------------------------
# MISSING KEY ERROR
# -------------------------
def test_tool_request_missing_key_raises():

    req = ToolRequest(
        tool_name=ToolName("search_tool"),
        params={}
    )

    with pytest.raises(ValueError) as e:  # type: ignore[misc]
        req.get(ToolIOKeys.QUERY)

    assert "Tool Input" in str(e.value) # type: ignore


# -------------------------
# ENUM KEY STORAGE VALIDATION
# -------------------------
def test_tool_request_params_use_enum_keys():

    req = ToolRequest(
        tool_name=ToolName("search_tool"),
        params={
            ToolIOKeys.DOCUMENTS: ["doc1", "doc2"]
        }
    )

    # ensure enum key works correctly
    assert ToolIOKeys.DOCUMENTS in req.params
    assert req.get(ToolIOKeys.DOCUMENTS) == ["doc1", "doc2"]


# -------------------------
# TOOL NAME PRESERVED
# -------------------------
def test_tool_request_tool_name():

    req = ToolRequest(
        tool_name=ToolName("my_tool"),
        params={}
    )

    assert req.tool_name == ToolName("my_tool")