from src.domain.context import Context
from src.domain.tool_name import ToolName


def test_context_initialization_empty():
    ctx = Context()

    assert ctx.context == {}


def test_context_initialization_with_data():
    key = ToolName("VECTOR_SEARCH")

    ctx = Context({key: "result"})

    assert ctx.context[key] == "result"


def test_context_get_existing_key():
    key = ToolName("VECTOR_SEARCH")

    ctx = Context({key: "result"})

    assert ctx.get(key) == "result"


def test_context_get_missing_key_raises_error():
    ctx = Context()

    key = ToolName("MISSING")

    try:
        ctx.get(key)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == f"Cannot get {key} from context"


def test_context_update_adds_value():
    ctx = Context()

    key = ToolName("VECTOR_SEARCH")

    ctx.update(key, "new_value")

    assert ctx.context[key] == "new_value"


def test_context_update_overwrites_value():
    key = ToolName("VECTOR_SEARCH")

    ctx = Context({key: "old_value"})

    ctx.update(key, "new_value")

    assert ctx.context[key] == "new_value"


def test_context_str_empty():
    ctx = Context()

    assert str(ctx) == "Context(empty)"


def test_context_str_with_values():
    key1 = ToolName("A")
    key2 = ToolName("B")

    ctx = Context({
        key1: "1",
        key2: "2",
    })

    

    assert key1 in ctx.context
    assert key2 in ctx.context
    assert ctx.get(key1) == '1'
    assert ctx.get(key2) == '2'