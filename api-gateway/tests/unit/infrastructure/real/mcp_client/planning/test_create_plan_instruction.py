from src.infrastructure.real.mcp_client.planning.create_plan_instruction import (
    CREATE_PLAN_INSTRUCTION,
)


# -------------------------
# BASIC VALIDATION
# -------------------------
def test_create_plan_instruction_exists():
    assert CREATE_PLAN_INSTRUCTION is not None
    assert isinstance(CREATE_PLAN_INSTRUCTION, str)
    assert len(CREATE_PLAN_INSTRUCTION) > 0



