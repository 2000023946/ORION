import json
import pytest

from src.infrastructure.mock.mock_llm_plan import MockPlanLLM
from src.infrastructure.real.mcp_client.planning.prompt import Prompt


@pytest.mark.asyncio
async def test_mock_plan_llm_returns_response():

    llm = MockPlanLLM()

    prompt = Prompt(
        prompt="Create execution plan"
    )

    response = await llm.generate(prompt)

    assert response.error is None
    assert response.raw is not None


@pytest.mark.asyncio
async def test_mock_plan_llm_returns_valid_json():

    llm = MockPlanLLM()

    prompt = Prompt(
        prompt="Create execution plan"
    )

    response = await llm.generate(prompt)

    plan = json.loads(response.raw)

    assert "edges" in plan
    assert isinstance(plan["edges"], list)


@pytest.mark.asyncio
async def test_mock_plan_llm_edges_are_valid():

    llm = MockPlanLLM()

    prompt = Prompt(
        prompt="Create execution plan"
    )

    response = await llm.generate(prompt)

    plan = json.loads(response.raw)

    for edge in plan["edges"]:
        assert isinstance(edge, list)
        assert len(edge) == 2

        assert isinstance(edge[0], str)
        assert isinstance(edge[1], str)


@pytest.mark.asyncio
async def test_mock_plan_llm_returns_allowed_plan():

    llm = MockPlanLLM()

    prompt = Prompt(
        prompt="Create execution plan"
    )

    response = await llm.generate(prompt)

    plan = json.loads(response.raw)

    valid_plans = [
        {
            "edges": [
                ["START", "VECTOR_SEARCH_TOOL"],
                ["VECTOR_SEARCH_TOOL", "METADATA_FILTER_TOOL"],
                ["METADATA_FILTER_TOOL", "END"],
            ]
        },
        {
            "edges": [
                ["START", "DB_FILTER_TOOL"],
                ["DB_FILTER_TOOL", "END"],
            ]
        },
        {
            "edges": [
                ["START", "WEB_SEARCH_TOOL"],
                ["WEB_SEARCH_TOOL", "END"],
            ]
        },
    ]

    assert plan in valid_plans