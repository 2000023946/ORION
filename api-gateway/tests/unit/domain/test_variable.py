from src.domain.variable import Variable
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


def test_variable_initialization():
    variable = Variable(
        name=ToolIOKeys.QUERY,
        type="str",
        description="The user's query",
        required=False,
    )

    assert variable.name == ToolIOKeys.QUERY
    assert variable.type == "str"
    assert variable.description == "The user's query"
    assert variable.required is False


def test_variable_required_defaults_to_true():
    variable = Variable(
        name=ToolIOKeys.QUERY,
        type="str",
        description="The user's query",
    )

    assert variable.required is True