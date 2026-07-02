from src.domain.output import Output
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


def test_output_appends_suffix_to_description():
    output_var = Output(
        name=ToolIOKeys.QUERY,
        type="str",
        description="The tool result",
    )

    assert output_var.description == "The tool result (this field is output)"


def test_output_does_not_append_suffix_twice():
    description = "The tool result (this field is output)"

    output_var = Output(
        name=ToolIOKeys.QUERY,
        type="str",
        description=description,
    )

    assert output_var.description == description