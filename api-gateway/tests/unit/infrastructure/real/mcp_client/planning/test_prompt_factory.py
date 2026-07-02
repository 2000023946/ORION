import pytest  # type: ignore

from src.infrastructure.real.mcp_client.planning.prompt_factory import PromptFactory
from src.infrastructure.real.mcp_client.planning.prompt import Prompt


from src.domain.query import Query
from src.domain.context import Context
from src.domain.tool import Tool
from src.domain.tool_name import ToolName


# -------------------------
# helper (normalize whitespace)
# -------------------------
def normalize(text: str) -> str:
    return " ".join(text.split())


# -------------------------
# PLAN PROMPT TEST
# -------------------------
def test_create_plan_prompt():

    factory = PromptFactory()

    query = Query("find laptops")
    tools = [
        Tool(ToolName("toolA"), "desc A", [], []),
        Tool(ToolName("toolB"), "desc B", [], []),
    ]

    prompt = factory.create_plan_prompt(query, tools).prompt

    assert isinstance(prompt, str)

    norm = normalize(prompt)

    assert "STRICT IO-based retrieval DAG planner" in norm
    assert "find laptops" in norm
    assert "AVAILABLE TOOLS" in norm
    assert "toolA" in norm
    assert "toolB" in norm
    assert "Return ONLY JSON" in norm


# -------------------------
# ANSWER PROMPT TEST
# -------------------------
def test_create_answer_prompt():

    factory = PromptFactory()

    query = Query("what is AI")
    context = Context()

    prompt = factory.create_answer_prompt(query, context).prompt

    norm = normalize(prompt)

    # IMPORTANT: test substrings, NOT full block equality
    assert "You are a QA assistant" in norm
    assert "what is AI" in norm
    assert "USER QUERY" in norm
    assert "TOOL RESULTS" in norm
    assert "FINAL ANSWER" in norm


# -------------------------
# DB FILTER PROMPT TEST
# -------------------------
def test_create_db_filter_prompt():

    factory = PromptFactory()

    query = Query("cheap phones")

    prompt = factory.create_db_filter_prompt(query).prompt

    norm = normalize(prompt)

    assert "database query generator" in norm.lower()
    assert "cheap phones" in norm
    assert "USER QUERY" in norm
    assert "FINAL OUTPUT" in norm


# -------------------------
# PROMPT WRAPPER TEST
# -------------------------
def test_prompt_factory_returns_prompt_objects():

    factory = PromptFactory()

    assert isinstance(factory.create_plan_prompt(Query("x"), []), Prompt)
    assert isinstance(factory.create_answer_prompt(Query("x"), Context()), Prompt)
    assert isinstance(factory.create_db_filter_prompt(Query("x")), Prompt)


# -------------------------
# SAFETY TEST (INSTRUCTION PRESENCE ONLY)
# -------------------------
def test_core_instructions_present():

    factory = PromptFactory()

    plan = factory.create_plan_prompt(Query("x"), []).prompt
    answer = factory.create_answer_prompt(Query("x"), Context()).prompt
    db = factory.create_db_filter_prompt(Query("x")).prompt

    plan_n = normalize(plan)
    answer_n = normalize(answer)
    db_n = normalize(db)

    assert "STRICT IO-based retrieval DAG planner" in plan_n
    assert "You are a QA assistant" in answer_n
    assert "database query generator" in db_n.lower()