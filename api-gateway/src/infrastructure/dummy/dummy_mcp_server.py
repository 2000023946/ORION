from src.ports.mcp_server_port import MCPServerPort
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.ports.tool_response import ToolResponse


from src.ports.mcp_server_port import MCPServerPort
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.ports.tool_response import ToolResponse


class DummyMCPServer(MCPServerPort):

    async def get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="search_user",
                description="Find a user by query",
                inputs=[],
                outputs=[]
            ),
            Tool(
                name="get_orders",
                description="Get user orders",
                inputs=[],
                outputs=[]
            ),
            Tool(
                name="get_profile",
                description="Get user profile info",
                inputs=[],
                outputs=[]
            ),
            Tool(
                name="generate_recommendation",
                description="Generate recommendation for user",
                inputs=[],
                outputs=[]
            ),
        ]

    async def call_tool(self, tool_name: ToolName) -> ToolResponse:

        fake_outputs = {
            "search_user": {
                "userId": 123,
                "name": "John"
            },
            "get_orders": {
                "orders": [1, 2, 3]
            },
            "get_profile": {
                "age": 22,
                "location": "Atlanta"
            },
            "generate_recommendation": {
                "recommendation": "Buy more tech stocks"
            }
        }

        if tool_name in fake_outputs:
            return ToolResponse(
                tool_name=tool_name,
                output=fake_outputs[tool_name],
                success=True
            )

        return ToolResponse(
            tool_name=tool_name,
            output={},
            success=False,
            error="Unknown tool"
        )