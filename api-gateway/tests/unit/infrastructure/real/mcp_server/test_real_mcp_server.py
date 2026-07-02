import pytest
from unittest.mock import AsyncMock, MagicMock

from src.domain.tool import Tool
from src.domain.tool_name import ToolName

from src.infrastructure.real.mcp_server.real_mcp_server import RealMCPServer
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.tool_response import ToolResponse


@pytest.mark.asyncio
async def test_get_tools_delegates_to_information_registry():
    mock_registry = MagicMock()
    mock_tool_registry = MagicMock()

    fake_tools = [
        Tool(
            name=ToolName("A"),
            description="tool A",
            inputs=[],
            outputs=[]
        )
    ]

    mock_registry.get_all_information.return_value = fake_tools

    server = RealMCPServer(
        tool_registry_port=mock_tool_registry,
        tool_information_registry=mock_registry
    )

    result = await server.get_tools()

    assert result == fake_tools
    mock_registry.get_all_information.assert_called_once()


@pytest.mark.asyncio
async def test_call_tool_delegates_to_tool_registry():
    mock_registry = AsyncMock()
    mock_info_registry = MagicMock()

    tool_name = ToolName("VECTOR_SEARCH_TOOL")
    tool_request = ToolRequest(tool_name=tool_name, params={})

    expected_response = ToolResponse(
        tool_name=tool_name,
        output={"result": "ok"},
        success=True
    )

    mock_registry.call_tool.return_value = expected_response

    server = RealMCPServer(
        tool_registry_port=mock_registry,
        tool_information_registry=mock_info_registry
    )

    response = await server.call_tool(tool_name, tool_request)

    assert response == expected_response
    mock_registry.call_tool.assert_called_once_with(tool_name, tool_request)