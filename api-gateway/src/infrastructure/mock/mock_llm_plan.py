import json
import random

from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort


class MockPlanLLM(LLMPort):

    def __init__(self):
        self.plans = [
            # -----------------------------
            # Plan 1:
            # Semantic search pipeline
            # START
            #  |
            # VECTOR_SEARCH
            #  |
            # METADATA_FILTER
            #  |
            # END
            # -----------------------------
            {
                "edges": [
                    ["START", "VECTOR_SEARCH_TOOL"],
                    ["VECTOR_SEARCH_TOOL", "METADATA_FILTER_TOOL"],
                    ["METADATA_FILTER_TOOL", "END"],
                ]
            },

            # -----------------------------
            # Plan 2:
            # Structured database query
            # START
            #  |
            # DB_FILTER
            #  |
            # END
            # -----------------------------
            {
                "edges": [
                    ["START", "DB_FILTER_TOOL"],
                    ["DB_FILTER_TOOL", "END"],
                ]
            },

            # -----------------------------
            # Plan 3:
            # Web search
            # START
            #  |
            # WEB_SEARCH
            #  |
            # END
            # -----------------------------
            {
                "edges": [
                    ["START", "WEB_SEARCH_TOOL"],
                    ["WEB_SEARCH_TOOL", "END"],
                ]
            },
        ]


    async def generate(self, prompt: Prompt) -> LLMResponse:

        plan = random.choice(self.plans)

        return LLMResponse(
            raw=json.dumps(plan),
            error=None
        )