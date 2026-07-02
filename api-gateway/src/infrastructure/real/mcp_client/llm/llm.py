from typing import Dict, Any

from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.config.settings import settings


class LLM(LLMPort):
    def __init__(self, http_client: HttpClientPort, json_parser: JsonAdapter):
        self.http_client = http_client
        self.json_parser = json_parser

    async def generate(self, prompt: Prompt) -> LLMResponse:
        try:
            payload: Dict[str, Any] = {
                "model": settings.llm_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt.prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": settings.llm_max_tokens
            }

            headers = {
                "Authorization": f"Bearer {settings.llm_api_key}",
                "Content-Type": "application/json"
            }

            response = await self.http_client.post(
                url=f"{settings.llm_base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=settings.http_timeout
            )
            

            # OpenAI-style response parsing
            return LLMResponse.create(response, self.json_parser)

        except Exception as e:
            return LLMResponse(
                raw="",
                error=str(e)
            )