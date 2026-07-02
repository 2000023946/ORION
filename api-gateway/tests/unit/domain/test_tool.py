from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.domain.input import Input
from src.domain.output import Output
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


def test_tool_initialization():
    inputs = [
        Input(
            name=ToolIOKeys.QUERY,
            type="str",
            description="The search query",
        )
    ]

    outputs = [
        Output(
            name=ToolIOKeys.DOCUMENTS,
            type="list",
            description="Matching documents",
        )
    ]

    tool = Tool(
        name=ToolName("VECTOR_SEARCH"),
        description="Searches the vector database.",
        inputs=inputs,
        outputs=outputs,
    )

    assert tool.name == ToolName("VECTOR_SEARCH")
    assert tool.description == "Searches the vector database."
    assert tool.inputs == inputs
    assert tool.outputs == outputs


def test_tool_with_empty_inputs_and_outputs():
    tool = Tool(
        name=ToolName("EMPTY_TOOL"),
        description="No inputs or outputs.",
        inputs=[],
        outputs=[],
    )

    assert tool.inputs == []
    assert tool.outputs == []
    assert tool.name == ToolName("EMPTY_TOOL")
    assert tool.description == "No inputs or outputs."