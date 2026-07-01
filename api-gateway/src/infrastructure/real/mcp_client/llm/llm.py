from typing import Dict, Any

from src.infrastructure.real.mcp_client.llm.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.config.settings import settings


class LLM(LLMPort):
    def __init__(self, http_client: HttpClientPort):
        self.http_client = http_client

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
                "temperature": 0.2
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
            raw_text = response["choices"][0]["message"]["content"]

            return LLMResponse(raw=raw_text)

        except Exception as e:
            return LLMResponse(
                raw="",
                error=str(e)
            )