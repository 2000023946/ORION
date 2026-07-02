

from src.domain.tool_name import ToolName


def test_tool_name_initialization():
    tool = ToolName("VECTOR_SEARCH")

    assert tool.name == "VECTOR_SEARCH"


def test_tool_name_equal_when_names_match():
    tool1 = ToolName("VECTOR_SEARCH")
    tool2 = ToolName("VECTOR_SEARCH")

    assert tool1 == tool2


def test_tool_name_not_equal_when_names_differ():
    tool1 = ToolName("VECTOR_SEARCH")
    tool2 = ToolName("WEB_SEARCH")

    assert tool1 != tool2


def test_tool_name_not_equal_to_non_tool_name():
    tool = ToolName("VECTOR_SEARCH")

    assert tool != "VECTOR_SEARCH"
    assert tool != 123
    assert tool != None


def test_tool_name_hash_matches_name_hash():
    tool = ToolName("VECTOR_SEARCH")

    assert hash(tool) == hash("VECTOR_SEARCH")


def test_equal_tool_names_have_same_hash():
    tool1 = ToolName("VECTOR_SEARCH")
    tool2 = ToolName("VECTOR_SEARCH")

    assert hash(tool1) == hash(tool2)


def test_tool_name_can_be_used_in_set():
    tool1 = ToolName("VECTOR_SEARCH")
    tool2 = ToolName("VECTOR_SEARCH")

    tool_set = {tool1, tool2}

    assert len(tool_set) == 1


def test_tool_name_can_be_used_as_dictionary_key():
    tool = ToolName("VECTOR_SEARCH")

    data = {tool: "works"}

    assert data[ToolName("VECTOR_SEARCH")] == "works"