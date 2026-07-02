import pytest  # type: ignore

from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.domain.tool_name import ToolName
from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_request import DBFilterRequest


# -------------------------
# success creation
# -------------------------
def test_db_filter_request_create_success():

    tool_request = ToolRequest(
        tool_name=ToolName("DB_FILTER_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("laptops under 1000")
        }
    )

    req = DBFilterRequest.create(tool_request)

    assert req is not None
    assert isinstance(req, DBFilterRequest)
    assert req.query.text == Query("laptops under 1000").text
    assert ToolIOKeys.QUERY in req.params


# -------------------------
# missing query should fail
# -------------------------
def test_db_filter_request_missing_query():

    tool_request = ToolRequest(
        tool_name=ToolName("DB_FILTER_TOOL"),
        params={}
    )

    with pytest.raises(ValueError) as e:
        DBFilterRequest.create(tool_request)

    assert "query" in str(e.value).lower()


# -------------------------
# basic structural safety
# -------------------------
def test_db_filter_request_params_preserved():

    tool_request = ToolRequest(
        tool_name=ToolName("DB_FILTER_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("phones"),
            ToolIOKeys.METADATA: {"debug": True}
        }
    )

    req = DBFilterRequest.create(tool_request)

    assert len(req.params) >= 1
    assert ToolIOKeys.QUERY in req.params