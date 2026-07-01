from abc import ABC, abstractmethod

from infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from infrastructure.real.mcp_client.planning.prompt import Prompt



class LLMPort(ABC):
    @abstractmethod
    async def generate(self, prompt: Prompt) -> LLMResponse:
        pass
