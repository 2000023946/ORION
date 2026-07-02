import pytest  # type: ignore
from typing import Any, Dict
from unittest.mock import AsyncMock

from src.infrastructure.real.mcp_client.llm.llm import LLM
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter


# -------------------------
# FAKE HTTP RESPONSE
# -------------------------
class FakeHttpResponse:
    def __init__(self, body: Dict[str, Any]):
        self.status_code = 200
        self.headers = {}
        self.body = body


# -------------------------
# FAKE JSON PARSER
# -------------------------
class FakeJson(JsonAdapter):
    def __init__(self, return_value: Dict[str, Any]):
        self.return_value = return_value

    def to_json(self, data: str) -> Dict[str, Any]:
        return self.return_value


# -------------------------
# SUCCESS CASE
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_llm_generate_success(monkeypatch: Any) -> None:

    fake_http = AsyncMock()
    fake_http.post.return_value = FakeHttpResponse({
        "choices": [
            {"message": {"content": "Hello AI"}}
        ]
    })

    import src.infrastructure.real.mcp_client.llm.llm as llm_module

    class FakeSettings:
        llm_model = "gpt-test"
        llm_max_tokens = 100
        llm_api_key = "test-key"
        llm_base_url = "http://fake-llm"
        http_timeout = 10

    monkeypatch.setattr(llm_module, "settings", FakeSettings)

    client = LLM(fake_http, FakeJson({
        "choices": [
            {"message": {"content": "Hello AI"}}
        ]
    }))

    result = await client.generate(Prompt(prompt="say hello"))

    assert isinstance(result, LLMResponse)
    assert result.raw == "Hello AI"
    assert result.error is None


# -------------------------
# HTTP FAILURE
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_llm_generate_http_error(monkeypatch: Any) -> None:

    fake_http = AsyncMock()
    fake_http.post.side_effect = Exception("network failure")

    import src.infrastructure.real.mcp_client.llm.llm as llm_module

    class FakeSettings:
        llm_model = "gpt-test"
        llm_max_tokens = 100
        llm_api_key = "test-key"
        llm_base_url = "http://fake-llm"
        http_timeout = 10

    monkeypatch.setattr(llm_module, "settings", FakeSettings)

    client = LLM(fake_http, FakeJson({}))

    result = await client.generate(Prompt(prompt="say hello"))

    assert result.raw == ""
    assert result.error is not None


# -------------------------
# INVALID RESPONSE
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_llm_generate_invalid_response(monkeypatch: Any) -> None:

    fake_http = AsyncMock()
    fake_http.post.return_value = FakeHttpResponse({
        "bad": "response"
    })

    import src.infrastructure.real.mcp_client.llm.llm as llm_module

    class FakeSettings:
        llm_model = "gpt-test"
        llm_max_tokens = 100
        llm_api_key = "test-key"
        llm_base_url = "http://fake-llm"
        http_timeout = 10

    monkeypatch.setattr(llm_module, "settings", FakeSettings)

    client = LLM(fake_http, FakeJson({
        "bad": "response"
    }))

    result = await client.generate(Prompt(prompt="say hello"))

    assert result.error is not None