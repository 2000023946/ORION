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




# -------------------------
# STRUCTURE RULES
# -------------------------
def test_create_plan_instruction_structure():
    assert "INPUT" in CREATE_PLAN_INSTRUCTION
    assert "EDGE RULE" in CREATE_PLAN_INSTRUCTION
    assert "START NODE RULE" in CREATE_PLAN_INSTRUCTION
    assert "END NODE RULE" in CREATE_PLAN_INSTRUCTION
    assert "OUTPUT FORMAT" in CREATE_PLAN_INSTRUCTION


# -------------------------
# TOOL SEMANTICS MUST EXIST
# -------------------------
def test_create_plan_instruction_tools_defined():
    assert "VECTOR_SEARCH_TOOL" in CREATE_PLAN_INSTRUCTION
    assert "WEB_SEARCH_TOOL" in CREATE_PLAN_INSTRUCTION
    assert "DB_FILTER_TOOL" in CREATE_PLAN_INSTRUCTION
    assert "METADATA_FILTER_TOOL" in CREATE_PLAN_INSTRUCTION


# -------------------------
# CRITICAL CONTRADICTIONS / GUARANTEES
# (these prevent your planner from drifting)
# -------------------------
def test_create_plan_instruction_constraints():
    assert "DO NOT invent tool dependencies" in CREATE_PLAN_INSTRUCTION
    assert "DO NOT chain tools unless IO types match" in CREATE_PLAN_INSTRUCTION
    assert "ALL tools are independent unless IO explicitly connects them" in CREATE_PLAN_INSTRUCTION


# -------------------------
# SAFETY: METADATA RULE MUST EXIST
# -------------------------
def test_metadata_filter_rule_exists():
    assert "METADATA_FILTER_TOOL does NOT depend on VECTOR_SEARCH_TOOL" in CREATE_PLAN_INSTRUCTION


# -------------------------
# OUTPUT FORMAT ENFORCEMENT
# -------------------------
def test_output_format_strict_json():
    assert "Return ONLY valid JSON" in CREATE_PLAN_INSTRUCTION
    assert '"edges"' in CREATE_PLAN_INSTRUCTION
    assert "NO markdown" in CREATE_PLAN_INSTRUCTION
    assert "NO explanation" in CREATE_PLAN_INSTRUCTION