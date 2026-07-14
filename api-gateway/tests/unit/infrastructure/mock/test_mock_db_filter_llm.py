import pytest
import json

from src.infrastructure.mock.mock_db_filter_llm import MockDbFilterLLM
from src.infrastructure.real.mcp_client.planning.prompt import Prompt


@pytest.mark.asyncio
async def test_db_filter_llm_extracts_phone_price():

    llm = MockDbFilterLLM()

    prompt = Prompt(
        prompt="phones with good battery life under 600"
    )

    response = await llm.generate(prompt)

    data = json.loads(response.get_response())

    assert data == {
        "max_price": 600
    }



@pytest.mark.asyncio
async def test_db_filter_llm_extracts_brand():

    llm = MockDbFilterLLM()

    prompt = Prompt(
        prompt="iphone under 600"
    )

    response = await llm.generate(prompt)

    data = json.loads(response.get_response())

    assert data["name"] == "iphone"
    assert data["max_price"] == 600



@pytest.mark.asyncio
async def test_db_filter_llm_does_not_guess_name():

    llm = MockDbFilterLLM()

    prompt = Prompt(
        prompt="good camera under 400"
    )

    response = await llm.generate(prompt)

    data = json.loads(response.get_response())

    assert "name" not in data
    assert data["max_price"] == 400