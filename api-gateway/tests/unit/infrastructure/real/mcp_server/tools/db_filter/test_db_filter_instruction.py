import pytest
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_instruction import DB_FILTER_INSTRUCTION  # type: ignore




# -------------------------
# basic sanity: exists
# -------------------------
def test_instruction_exists():
    assert DB_FILTER_INSTRUCTION is not None
    assert isinstance(DB_FILTER_INSTRUCTION, str)


# -------------------------
# size sanity (prevents accidental deletion/truncation)
# -------------------------
def test_instruction_is_reasonably_large():
    assert len(DB_FILTER_INSTRUCTION) > 500  # ensures full prompt is loaded


# -------------------------
# required sections exist
# -------------------------
def test_instruction_contains_required_sections():

    assert "NAME RULE" in DB_FILTER_INSTRUCTION
    assert "PRICE RULES" in DB_FILTER_INSTRUCTION
    assert "STRICT OUTPUT RULES" in DB_FILTER_INSTRUCTION
    assert "OUTPUT FORMAT" in DB_FILTER_INSTRUCTION


# -------------------------
# safety behavior rules exist
# -------------------------
def test_instruction_contains_guardrails():

    assert "DO NOT guess" in DB_FILTER_INSTRUCTION
    assert "ONLY return" in DB_FILTER_INSTRUCTION
    assert "NEVER hallucinate" in DB_FILTER_INSTRUCTION


# -------------------------
# ensures JSON-only constraint
# -------------------------
def test_instruction_requires_json_output():

    assert "Return ONLY valid JSON" in DB_FILTER_INSTRUCTION
    assert "No markdown" in DB_FILTER_INSTRUCTION
    assert "No explanation" in DB_FILTER_INSTRUCTION