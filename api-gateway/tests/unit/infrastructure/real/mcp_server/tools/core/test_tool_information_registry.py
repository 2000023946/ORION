import pytest

from src.domain.tool_name import ToolName
from src.domain.tool import Tool
from src.domain.input import Input
from src.domain.output import Output
from src.infrastructure.real.mcp_server.tools.core.tool_information_registry import ToolInformationRegistry


def make_tool(name: str) -> Tool:
    return Tool(
        name=ToolName(name),
        description="test tool",
        inputs=[
            Input(name="query", type="str", description="test input")
        ],
        outputs=[
            Output(name="result", type="str", description="test output")
        ]
    )


def test_register_and_get_information():
    registry = ToolInformationRegistry()

    tool = make_tool("VECTOR_SEARCH_TOOL")

    registry.register(tool.name, tool)

    result = registry.get_information(tool.name)

    assert result == tool
    assert result.name == ToolName("VECTOR_SEARCH_TOOL")


def test_overwrite_tool_information():
    registry = ToolInformationRegistry()

    tool1 = make_tool("TOOL_A")
    tool2 = make_tool("TOOL_A")

    tool2.description = "updated description"  # works only if Tool not frozen

    registry.register(tool1.name, tool1)
    registry.register(tool2.name, tool2)

    result = registry.get_information(ToolName("TOOL_A"))

    assert result.description == tool2.description


def test_get_all_information():
    registry = ToolInformationRegistry()

    tool_a = make_tool("A")
    tool_b = make_tool("B")

    registry.register(tool_a.name, tool_a)
    registry.register(tool_b.name, tool_b)

    all_tools = registry.get_all_information()

    assert len(all_tools) == 2
    assert tool_a in all_tools
    assert tool_b in all_tools


def test_get_information_missing_key_raises():
    registry = ToolInformationRegistry()

    with pytest.raises(KeyError):
        registry.get_information(ToolName("MISSING"))