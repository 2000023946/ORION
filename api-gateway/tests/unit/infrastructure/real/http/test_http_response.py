import pytest  # type: ignore

from src.infrastructure.real.http.http_response import HttpResponse


# -------------------------
# GET METHOD
# -------------------------
def test_get_returns_value() -> None:

    resp = HttpResponse(
        status_code=200,
        headers={},
        body={"name": "Mo", "age": 25},
    )

    assert resp.get("name") == "Mo"
    assert resp.get("age") == 25


def test_get_returns_default_when_missing() -> None:

    resp = HttpResponse(
        status_code=200,
        headers={},
        body={"name": "Mo"},
    )

    assert resp.get("missing", "default") == "default"


# -------------------------
# REQUIRE METHOD
# -------------------------
def test_require_returns_value() -> None:

    resp = HttpResponse(
        status_code=200,
        headers={},
        body={"key": "value"},
    )

    assert resp.require("key") == "value"


def test_require_raises_when_missing() -> None:

    resp = HttpResponse(
        status_code=200,
        headers={},
        body={"key": "value"},
    )

    with pytest.raises(KeyError) as exc_info: # type: ignore
        resp.require("missing")

    assert "Missing required key" in str(exc_info.value) # type: ignore


# -------------------------
# TO_DICT METHOD
# -------------------------
def test_to_dict_returns_full_structure() -> None:

    resp = HttpResponse(
        status_code=201,
        headers={"Content-Type": "application/json"},
        body={"a": 1, "b": 2},
    )

    result = resp.to_dict()

    assert result["status_code"] == 201
    assert result["headers"]["Content-Type"] == "application/json"
    assert result["body"] == {"a": 1, "b": 2}


# -------------------------
# EDGE CASE: EMPTY BODY
# -------------------------
def test_empty_body_behavior() -> None:

    resp = HttpResponse(
        status_code=204,
        headers={},
        body={},
    )

    assert resp.get("x") is None

    with pytest.raises(KeyError): # type: ignore
        resp.require("x")