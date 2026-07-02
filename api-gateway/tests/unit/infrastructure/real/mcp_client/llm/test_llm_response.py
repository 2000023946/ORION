import pytest  # type: ignore
from typing import Any, Dict

from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter
from src.infrastructure.real.http.http_response import HttpResponse


# -------------------------
# FAKE JSON ADAPTER
# -------------------------
class FakeJsonAdapter(JsonAdapter):
    def __init__(self, data: Dict[str, Any] | None = None, should_fail: bool = False):
        self.data = data or {}
        self.should_fail = should_fail

    def to_json(self, data: str) -> Dict[str, Any]:
        if self.should_fail:
            raise Exception("json parse error")
        return self.data


# -------------------------
# SUCCESS CASE
# -------------------------
def test_llm_response_success():

    http = HttpResponse(
        status_code=200,
        headers={},
        body={
            "choices": [
                {"message": {"content": "Hello world"}}
            ]
        },
    )

    parser = FakeJsonAdapter(http.body)

    result = LLMResponse.create(http, parser)

    assert result.error is None
    assert result.raw == "Hello world"
    assert result.is_error() is False


# -------------------------
# API ERROR FIELD
# -------------------------
def test_llm_response_api_error():

    http = HttpResponse(
        status_code=400,
        headers={},
        body={
            "error": {
                "message": "Invalid API key"
            }
        },
    )

    parser = FakeJsonAdapter(http.body)

    result = LLMResponse.create(http, parser)

    assert result.is_error() is True
    assert "Invalid API key" in result.error  # type: ignore


# -------------------------
# NO CHOICES
# -------------------------
def test_llm_response_missing_choices():

    http = HttpResponse(
        status_code=200,
        headers={},
        body={}
    )

    parser = FakeJsonAdapter(http.body)

    result = LLMResponse.create(http, parser)

    assert result.is_error() is True
    assert "No choices" in result.error  # type: ignore


# -------------------------
# NO CONTENT
# -------------------------
def test_llm_response_missing_content():

    http = HttpResponse(
        status_code=200,
        headers={},
        body={
            "choices": [
                {"message": {}}
            ]
        },
    )

    parser = FakeJsonAdapter(http.body)

    result = LLMResponse.create(http, parser)

    assert result.is_error() is True
    assert "No content" in result.error  # type: ignore


# -------------------------
# JSON PARSE FAILURE
# -------------------------
def test_llm_response_json_failure():

    http = HttpResponse(
        status_code=200,
        headers={},
        body='{"bad": json}',  # invalid structure for adapter
    )

    parser = FakeJsonAdapter(should_fail=True)

    result = LLMResponse.create(http, parser)

    assert result.is_error() is True
    assert result.raw == ""


# -------------------------
# get_response SUCCESS
# -------------------------
def test_get_response_success():

    obj = LLMResponse(raw="hello", error=None)

    assert obj.get_response() == "hello"


# -------------------------
# get_response ERROR RAISES
# -------------------------
def test_get_response_error_raises():

    obj = LLMResponse(raw="", error="failed")

    with pytest.raises(ValueError) as exc_info:  # type: ignore
        obj.get_response()

    assert "Failed" in str(exc_info.value) # type: ignore