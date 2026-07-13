from src.infrastructure.real.mcp_client.planning.answer_instruction import ANSWER_INSTRUCTION


def test_answer_instruction_exists():
    assert ANSWER_INSTRUCTION is not None
    assert isinstance(ANSWER_INSTRUCTION, str)
    assert len(ANSWER_INSTRUCTION) > 0

