from typing import Any

from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.mcp_server_port import MCPServerPort
from src.ports.tool_response import ToolResponse


class DummyMCPServer(MCPServerPort):
    
    async def get_tools(self) -> list[Tool]:
        return [
            Tool(
                name=ToolName("search_user"),
                description="Find a user by query",
                inputs=[],
                outputs=[]
            ),
            Tool(
                name=ToolName("get_orders"),
                description="Get user orders",
                inputs=[],
                outputs=[]
            ),
            Tool(
                name=ToolName("get_profile"),
                description="Get user profile info",
                inputs=[],
                outputs=[]
            ),
            Tool(
                name=ToolName("generate_recommendation"),
                description="Generate recommendation for user",
                inputs=[],
                outputs=[]
            ),
        ]

    async def call_tool(self, tool_name: ToolName, tool_request: ToolRequest) -> ToolResponse:

        from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys

        fake_outputs: dict[str, dict[ToolIOKeys, Any]] = {
            "search_user": {
                ToolIOKeys.METADATA: {
                    "userId": 123,
                    "name": "John"
                }
            },
            "get_orders": {
                ToolIOKeys.METADATA: {
                    "orders": [1, 2, 3]
                }
            },
            "get_profile": {
                ToolIOKeys.METADATA: {
                    "age": 22,
                    "location": "Atlanta"
                }
            },
            "generate_recommendation": {
                ToolIOKeys.METADATA: {
                    "recommendation": "Buy more tech stocks"
                }
            }
        }

        key = tool_name.name
    
        if key in fake_outputs:
            return ToolResponse(
                tool_name=tool_name,
                output=fake_outputs[key],
                success=True
            )

        return ToolResponse(
            tool_name=tool_name,
            output={},
            success=False,
            error="Unknown tool"
        )