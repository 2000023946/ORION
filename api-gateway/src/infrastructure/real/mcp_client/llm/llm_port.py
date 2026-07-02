from abc import ABC, abstractmethod

from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse



class LLMPort(ABC):
    @abstractmethod
    async def generate(self, prompt: Prompt) -> LLMResponse:
        pass
