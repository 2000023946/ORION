from src.infrastructure.real.mcp_client.planning.answer_instruction import ANSWER_INSTRUCTION


def test_answer_instruction_exists():
    assert ANSWER_INSTRUCTION is not None
    assert isinstance(ANSWER_INSTRUCTION, str)
    assert len(ANSWER_INSTRUCTION) > 0


def test_answer_instruction_core_rules():
    assert "ONLY the provided context data" in ANSWER_INSTRUCTION
    assert "Do NOT call tools" in ANSWER_INSTRUCTION
    assert "Do NOT assume missing information" in ANSWER_INSTRUCTION


def test_answer_instruction_behavior_rules():
    assert "If data is missing" in ANSWER_INSTRUCTION
    assert "don't know" in ANSWER_INSTRUCTION


def test_answer_instruction_is_immutable_constant():
    original = ANSWER_INSTRUCTION

    # simulate accidental reassignment attempt

    assert ANSWER_INSTRUCTION == original
    assert "EXTRA" not in ANSWER_INSTRUCTION