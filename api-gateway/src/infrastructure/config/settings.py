import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # ----------------------------
    # LLM
    # ----------------------------
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    # ----------------------------
    # HTTP
    # ----------------------------
    http_timeout: int = int(os.getenv("HTTP_TIMEOUT", "30"))

    # ----------------------------
    # Web search API
    # ----------------------------
    web_api_key: str = os.getenv("WEB_API_KEY", "")
    web_api_url: str = os.getenv("WEB_API_URL", "")
    # ----------------------------
    # Embeddings
    # ----------------------------
    embedding_api: str = os.getenv("EMBEDDING_API", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # ----------------------------
    # Vector DB (FAISS / Pinecone / Weaviate)
    # ----------------------------
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "faiss")

    vector_db_api_key: str = os.getenv("VECTOR_DB_API_KEY", "")
    vector_db_url: str = os.getenv("VECTOR_DB_URL", "")
    vector_db_index: str = os.getenv("VECTOR_DB_INDEX", "main-index")

    vector_top_k: int = int(os.getenv("VECTOR_TOP_K", "5"))

    # ----------------------------
    # 📄 Metadata / Document DB (NEW)
    # ----------------------------
    metadata_db_type: str = os.getenv("METADATA_DB_TYPE", "mongo")  # mongo | elastic | postgres

    metadata_db_api_key: str = os.getenv("METADATA_DB_API_KEY", "")
    metadata_db_url: str = os.getenv("METADATA_DB_URL", "")
    metadata_db_index: str = os.getenv("METADATA_DB_INDEX", "documents")

    metadata_batch_size: int = int(os.getenv("METADATA_BATCH_SIZE", "10"))

    # ----------------------------
    # Debug
    # ----------------------------
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()