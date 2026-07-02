from src.infrastructure.real.mcp_client.planning.prompt import Prompt


def test_prompt_creation():
    p = Prompt(prompt="hello world")

    assert p.prompt == "hello world"