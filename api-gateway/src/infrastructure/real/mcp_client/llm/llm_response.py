from dataclasses import dataclass
from typing import Optional

from src.infrastructure.real.http.http_response import HttpResponse
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter


@dataclass
class LLMResponse:
    """
    Simple wrapper for raw LLM output only.
    """
    raw: str
    error: Optional[str] = None

    def is_error(self) -> bool:
        return self.error is not None
    
    def get_response(self) -> str:
        if self.is_error():
            raise ValueError(f"Failed to create response due to: {self.error}")
        return self.raw

    @classmethod
    def create(cls, response: HttpResponse, json_parser: JsonAdapter) -> "LLMResponse":
        try:
            # 1. Parse HTTP body → dict
            data = json_parser.to_json(response.body)

            # 2. Handle API-level errors (Groq/OpenAI style)
            if "error" in data:
                return cls(
                    raw="",
                    error=data["error"].get("message", str(data["error"]))
                )

            # 3. Extract choices safely
            choices = data.get("choices")
            if not choices:
                return cls(
                    raw="",
                    error=f"No choices in LLM response: {data}"
                )

            message = choices[0].get("message", {})
            content = message.get("content")

            if content is None:
                return cls(
                    raw="",
                    error=f"No content in LLM response: {data}"
                )

            return cls(
                raw=content,
                error=None
            )

        except Exception as e:
            return cls(
                raw="",
                error=str(e)
            )