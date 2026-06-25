from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Config:
    WEB_API: str
    VECTOR_DB_API: str
    METADATA_API: str
    SYNTHESIS_LLM: str
    PLANNING_LLM: str


config = Config(
    WEB_API=os.getenv("WEB_API", ""),
    VECTOR_DB_API=os.getenv("VECTOR_DB_API", ""),
    METADATA_API=os.getenv("METADATA_API", ""),
    SYNTHESIS_LLM=os.getenv("SYNTHESIS_LLM", ""),
    PLANNING_LLM=os.getenv("PLANNING_LLM", ""),
)