import pytest

from src.infrastructure.mock.mock_llm_answer import MockAnswerLLM
from src.infrastructure.real.mcp_client.planning.prompt import Prompt


@pytest.mark.asyncio
async def test_mock_answer_llm_returns_answer():

    llm = MockAnswerLLM()

    prompt = Prompt(
        prompt="""
        User Query:
        find iphone under 600

        Tool Results:
        [
            {
                "title": "iPhone 15",
                "price": 599
            }
        ]
        """
    )

    response = await llm.generate(prompt)

    assert response.get_response() != ""
    assert "iphone" in response.get_response().lower()


@pytest.mark.asyncio
async def test_mock_answer_llm_unknown_context():

    llm = MockAnswerLLM()

    prompt = Prompt(
        prompt="""
        User Query:
        something unknown

        Tool Results:
        []
        """
    )

    response = await llm.generate(prompt)

    assert (
        "could not find enough information"
        in response.get_response()
    )