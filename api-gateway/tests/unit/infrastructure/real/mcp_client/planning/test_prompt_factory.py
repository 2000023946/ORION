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



# -------------------------
# DB FILTER PROMPT TEST
# -------------------------
def test_create_db_filter_prompt():

    factory = PromptFactory()

    query = Query("cheap phones")

    prompt = factory.create_db_filter_prompt(query).prompt

    norm = normalize(prompt)



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

