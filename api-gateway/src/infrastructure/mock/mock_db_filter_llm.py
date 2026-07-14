import asyncio
import json
import random
import re

from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort


class MockDbFilterLLM(LLMPort):

    async def generate(self, prompt: Prompt) -> LLMResponse:
        await asyncio.sleep(random.uniform(0.2, 0.4))  # DB Filter LLM

        text = prompt.prompt.lower()

        result = {}


        # -------------------------
        # Name rules
        # -------------------------

        if "iphone" in text:
            result["name"] = "iphone"

        elif "samsung" in text and "phone" in text:
            result["name"] = "samsung phone"


        # -------------------------
        # Price extraction
        # -------------------------

        under_match = re.search(
            r"(?:under|below)\s+(\d+)",
            text
        )

        if under_match:
            result["max_price"] = int(
                under_match.group(1)
            )


        above_match = re.search(
            r"(?:above|over)\s+(\d+)",
            text
        )

        if above_match:
            result["min_price"] = int(
                above_match.group(1)
            )


        return LLMResponse(
            raw=json.dumps(result)
        )