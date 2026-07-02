import pytest  # type: ignore
from typing import Any, Optional, Dict

from src.infrastructure.real.mcp_client.parsing.retrieval_plan_parser import RetrievalPlanParser
from src.infrastructure.real.mcp_client.parsing.json_port import JsonPort

from src.domain.tool_edge import ToolEdge
from src.domain.tool_name import ToolName


# -------------------------
# FAKE JSON ADAPTER (TYPED)
# -------------------------
class FakeJson(JsonPort):
    def __init__(
        self,
        return_value: Optional[Dict[str, Any]] = None,
        should_fail: bool = False
    ) -> None:
        self.return_value = return_value
        self.should_fail = should_fail

    def to_json(self, data: str) -> Dict[str, Any]:
        if self.should_fail:
            raise Exception("bad json")

        if self.return_value is None:
            return {}

        return self.return_value


# -------------------------
# SUCCESS CASE
# -------------------------
def test_parse_valid_edges() -> None:

    json_adapter = FakeJson({
        "edges": [["A", "B"], ["A", "C"]]
    })

    parser = RetrievalPlanParser(json_adapter)

    result = parser.parse('{"edges": [["A","B"],["A","C"]]}')

    assert len(result) == 2

    assert isinstance(result[0], ToolEdge)
    assert result[0].source == ToolName("A")
    assert result[0].to == ToolName("B")

    assert result[1].source == ToolName("A")
    assert result[1].to == ToolName("C")


# -------------------------
# INVALID JSON FROM ADAPTER
# -------------------------
def test_parse_invalid_json_raises() -> None:

    json_adapter = FakeJson(should_fail=True)
    parser = RetrievalPlanParser(json_adapter)

    with pytest.raises(ValueError) as exc_info: # type: ignore
        parser.parse("bad json")

    error_msg: str = str(exc_info.value) # type: ignore
    assert "Invalid JSON from LLM" in error_msg


# -------------------------
# MISSING EDGES FIELD
# -------------------------
def test_missing_edges_field() -> None:

    json_adapter = FakeJson({
        "not_edges": []
    })

    parser = RetrievalPlanParser(json_adapter)

    with pytest.raises(ValueError) as exc_info: # type: ignore
        parser.parse("{}")

    error_msg: str = str(exc_info.value) # type: ignore
    assert "Missing 'edges'" in error_msg


# -------------------------
# INVALID EDGE FORMAT
# -------------------------
def test_invalid_edge_format() -> None:

    json_adapter = FakeJson({
        "edges": [["A", "B", "C"]]  # invalid length
    })

    parser = RetrievalPlanParser(json_adapter)

    with pytest.raises(ValueError) as exc_info: # type: ignore
        parser.parse('{"edges": [["A","B","C"]]}')

    error_msg: str = str(exc_info.value) # type: ignore
    assert "Invalid edge format" in error_msg


# -------------------------
# SINGLE EDGE
# -------------------------
def test_single_edge_parsing() -> None:

    json_adapter = FakeJson({
        "edges": [["START", "END"]]
    })

    parser = RetrievalPlanParser(json_adapter)

    result = parser.parse("{}")

    assert len(result) == 1
    assert result[0].source == ToolName("START")
    assert result[0].to == ToolName("END")