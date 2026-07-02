from src.domain.input import Input
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


def test_input_appends_suffix_to_description():
    input_var = Input(
        name=ToolIOKeys.QUERY,
        type="str",
        description="The user's query",
    )

    assert input_var.description == "The user's query (this field is input)"


def test_input_does_not_append_suffix_twice():
    description = "The user's query (this field is input)"

    input_var = Input(
        name=ToolIOKeys.QUERY,
        type="str",
        description=description,
    )

    assert input_var.description == description