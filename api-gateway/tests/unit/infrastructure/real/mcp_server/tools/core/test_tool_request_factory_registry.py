import pytest  # type: ignore
from unittest.mock import MagicMock

from src.infrastructure.real.mcp_server.tools.core.tool_request_factory_registry import ToolRequestFactoryRegistry
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory import ToolRequestFactory
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry


# -------------------------
# SUCCESS: factory registered + create request
# -------------------------
def test_registry_creates_request_success():

    tool_name = ToolName("TEST_TOOL")

    mock_request = ToolRequest(
        tool_name=tool_name,
        params={}
    )

    mock_factory = MagicMock(spec=ToolRequestFactory)
    mock_factory.create.return_value = mock_request

    registry = ToolRequestFactoryRegistry()
    registry.register_factory(tool_name, mock_factory)

    output_registry = MagicMock(spec=ToolOutputRegistry)

    result = registry.create_request(tool_name, output_registry)

    assert isinstance(result, ToolRequest)
    assert result.tool_name == tool_name

    mock_factory.create.assert_called_once_with(tool_name, output_registry)


# -------------------------
# ERROR: unregistered tool
# -------------------------
def test_registry_unregistered_tool_raises():

    registry = ToolRequestFactoryRegistry()

    tool_name = ToolName("UNKNOWN_TOOL")
    output_registry = MagicMock(spec=ToolOutputRegistry)

    with pytest.raises(ValueError) as e:
        registry.create_request(tool_name, output_registry)

    assert "not registered" in str(e.value)


# -------------------------
# MULTIPLE FACTORIES: correct routing
# -------------------------
def test_registry_multiple_factories():

    tool1 = ToolName("TOOL_1")
    tool2 = ToolName("TOOL_2")

    factory1 = MagicMock(spec=ToolRequestFactory)
    factory2 = MagicMock(spec=ToolRequestFactory)

    factory1.create.return_value = ToolRequest(tool_name=tool1, params={})
    factory2.create.return_value = ToolRequest(tool_name=tool2, params={})

    registry = ToolRequestFactoryRegistry()
    registry.register_factory(tool1, factory1)
    registry.register_factory(tool2, factory2)

    output_registry = MagicMock(spec=ToolOutputRegistry)

    r1 = registry.create_request(tool1, output_registry)
    r2 = registry.create_request(tool2, output_registry)

    assert r1.tool_name == tool1
    assert r2.tool_name == tool2

    factory1.create.assert_called_once()
    factory2.create.assert_called_once()