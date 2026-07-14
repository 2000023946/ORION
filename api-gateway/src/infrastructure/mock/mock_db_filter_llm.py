import json

from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort


class MockDbFilterLLM(LLMPort):
    """
    Mock LLM for DB filter generation.

    Simulates LLM responses without calling external APIs.
    """


    async def generate(self, prompt: Prompt) -> LLMResponse:

        text = prompt.prompt.lower()


        # iphone example
        if "iphone" in text and "under" in text:
            return LLMResponse(
                raw=json.dumps({
                    "name": "iphone",
                    "max_price": 600
                })
            )


        # samsung phone example
        if "samsung" in text:
            return LLMResponse(
                raw=json.dumps({
                    "name": "samsung phone",
                    "max_price": 500
                })
            )


        # explicit product categories
        if "phone" in text:
            result = {}

            if "under 600" in text:
                result["max_price"] = 600

            result["name"] = "phone"

            return LLMResponse(
                raw=json.dumps(result)
            )


        # price extraction only
        if "under 600" in text:
            return LLMResponse(
                raw=json.dumps({
                    "max_price": 600
                })
            )


        if "above 200" in text:
            return LLMResponse(
                raw=json.dumps({
                    "min_price": 200
                })
            )


        # vague query
        if (
            "good camera" in text
            or "good battery" in text
            or "gaming" in text
            or "performance" in text
        ):
            return LLMResponse(
                raw=json.dumps({})
            )


        # default
        return LLMResponse(
            raw=json.dumps({})
        )