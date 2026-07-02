import pytest  # type: ignore

from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter


# -------------------------
# SUCCESS CASE
# -------------------------
def test_to_json_valid_string():
    adapter = JsonAdapter()

    data = '{"name": "Mo", "age": 25}'
    result = adapter.to_json(data)

    assert isinstance(result, dict)
    assert result["name"] == "Mo"
    assert result["age"] == 25


# -------------------------
# NESTED JSON
# -------------------------
def test_to_json_nested_object():
    adapter = JsonAdapter()

    data = '{"user": {"id": 1, "meta": {"active": true}}}'
    result = adapter.to_json(data)

    assert result["user"]["id"] == 1
    assert result["user"]["meta"]["active"] is True


# -------------------------
# ARRAY JSON
# -------------------------
def test_to_json_array():
    adapter = JsonAdapter()

    data = '{"items": [1, 2, 3]}'
    result = adapter.to_json(data)

    assert result["items"] == [1, 2, 3]


# -------------------------
# FAILURE CASE (INVALID JSON)
# -------------------------
def test_to_json_invalid_json():
    adapter = JsonAdapter()

    data = "{bad json}"

    with pytest.raises(Exception):  # type: ignore
        adapter.to_json(data)


# -------------------------
# EDGE CASE: EMPTY OBJECT
# -------------------------
def test_to_json_empty_object():
    adapter = JsonAdapter()

    data = "{}"
    result = adapter.to_json(data)

    assert result == {}