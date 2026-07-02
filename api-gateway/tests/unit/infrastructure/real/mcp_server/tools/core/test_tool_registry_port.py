import pytest  # type: ignore
from unittest.mock import AsyncMock, MagicMock

from src.infrastructure.real.mcp_server.tools.core.tool_registry_port import ToolRegistryPort
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest


# -------------------------
# SUCCESS: tool is registered and called
# -------------------------
@pytest.mark.asyncio
async def test_tool_registry_call_success():

    tool_name = ToolName("TEST_TOOL")

    mock_tool = AsyncMock()
    mock_tool.execute.return_value = MagicMock(
        tool_name=tool_name,
        output={"result": "ok"},
        success=True
    )

    registry = ToolRegistryPort()
    registry.register(tool_name, mock_tool)

    request = ToolRequest(
        tool_name=tool_name,
        params={}
    )

    result = await registry.call_tool(tool_name, request)

    assert result.success is True
    assert result.output["result"] == "ok"

    mock_tool.execute.assert_called_once_with(request)


# -------------------------
# ERROR: tool not registered
# -------------------------
@pytest.mark.asyncio
async def test_tool_registry_missing_tool():

    registry = ToolRegistryPort()

    request = ToolRequest(
        tool_name=ToolName("UNKNOWN_TOOL"),
        params={}
    )

    with pytest.raises(KeyError):
        await registry.call_tool(ToolName("UNKNOWN_TOOL"), request)


# -------------------------
# MULTIPLE TOOLS: correct routing
# -------------------------
@pytest.mark.asyncio
async def test_tool_registry_multiple_tools():

    tool1 = ToolName("TOOL_1")
    tool2 = ToolName("TOOL_2")

    mock_tool1 = AsyncMock()
    mock_tool2 = AsyncMock()

    mock_tool1.execute.return_value = MagicMock(success=True, output={"id": 1})
    mock_tool2.execute.return_value = MagicMock(success=True, output={"id": 2})

    registry = ToolRegistryPort()
    registry.register(tool1, mock_tool1)
    registry.register(tool2, mock_tool2)

    req1 = ToolRequest(tool_name=tool1, params={})
    req2 = ToolRequest(tool_name=tool2, params={})

    r1 = await registry.call_tool(tool1, req1)
    r2 = await registry.call_tool(tool2, req2)

    assert r1.output["id"] == 1
    assert r2.output["id"] == 2

    mock_tool1.execute.assert_called_once()
    mock_tool2.execute.assert_called_once()