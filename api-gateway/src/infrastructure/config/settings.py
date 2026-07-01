import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # LLM
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    # HTTP
    http_timeout: int = int(os.getenv("HTTP_TIMEOUT", "30"))

    # Debug
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()