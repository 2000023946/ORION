import asyncio

from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.planning.prompt import Prompt


class MockAnswerLLM(LLMPort):

    async def generate(self, prompt: Prompt) -> LLMResponse:
        """
        Mock final answer generator.

        Receives:
        - User query
        - Tool execution results

        Returns:
        - Natural language answer
        """

        await asyncio.sleep(2.5)   

        text = prompt.prompt.lower()

        # Mock DB result case
        if "iphone" in text:
            return LLMResponse(
                raw=(
                    "I found an iPhone matching your requirements. "
                    "The available product is an iPhone with the requested price constraints."
                )
            )

        # Mock web search case
        if "stock market" in text:
            return LLMResponse(
                raw=(
                    "Based on the provided market search results, "
                    "the stock market is currently trading lower. "
                    "The S&P 500 and major indexes show negative movement."
                )
            )

        # Mock vector search case
        if "documents" in text or "products" in text:
            return LLMResponse(
                raw=(
                    "I found relevant documents from the search results "
                    "that may answer your query."
                )
            )

        # Default fallback
        return LLMResponse(
            raw=(
                "I could not find enough information in the provided context "
                "to answer the question."
            )
        )