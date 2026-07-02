import pytest  # type: ignore
from typing import Any, Dict

from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.http.http_response import HttpResponse


# -------------------------
# MOCK RESPONSE OBJECT
# -------------------------
class FakeResponse:
    def __init__(self) -> None:
        self.status_code: int = 200
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}
        self.text: str = '{"ok": true}'


# -------------------------
# GET TEST
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_get_request(monkeypatch: Any) -> None:

    client = RealHttpClient()

    def fake_request(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(client._session, "request", fake_request) # type: ignore

    response = await client.get("http://test.com")

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.body == '{"ok": true}'


# -------------------------
# POST TEST
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_post_request(monkeypatch: Any) -> None:

    client = RealHttpClient()

    def fake_request(*args: Any, **kwargs: Any) -> FakeResponse:
        assert kwargs["json"] == {"a": 1}
        return FakeResponse()

    monkeypatch.setattr(client._session, "request", fake_request) # type: ignore

    response = await client.post("http://test.com", json={"a": 1})

    assert response.status_code == 200
    assert response.body == '{"ok": true}'


# -------------------------
# PUT TEST
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_put_request(monkeypatch: Any) -> None:

    client = RealHttpClient()

    def fake_request(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(client._session, "request", fake_request) # type: ignore

    response = await client.put("http://test.com", data="x")

    assert response.status_code == 200


# -------------------------
# DELETE TEST
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_delete_request(monkeypatch: Any) -> None:

    client = RealHttpClient()

    def fake_request(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(client._session, "request", fake_request) # type: ignore

    response = await client.delete("http://test.com")

    assert response.status_code == 200
    assert response.body == '{"ok": true}'


# -------------------------
# VERIFY INTERNAL REQUEST CALLED
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_internal_request_called(monkeypatch: Any) -> None:

    client = RealHttpClient()

    called: Dict[str, str] = {}

    def fake_request(method: str, url: str, **kwargs: Any) -> FakeResponse:
        called["method"] = method
        called["url"] = url
        return FakeResponse()

    monkeypatch.setattr(client._session, "request", fake_request) # type: ignore

    await client.get("http://example.com")

    assert called["method"] == "GET"
    assert called["url"] == "http://example.com"