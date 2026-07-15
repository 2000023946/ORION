import requests
from typing import List

# Import your abstract port interface
from src.infrastructure.real.mcp_server.tools.vector_search.embedding.embedding_port import EmbeddingPort

Vector = List[float]

class TeiEmbeddingAdapter(EmbeddingPort):
    """
    Adapter for the official Hugging Face Text Embeddings Inference (TEI) image.
    Uses standard HTTP REST calls to communicate with the Rust backend.
    """
    def __init__(self, target_url: str = "http://localhost:8080"):
        # Defensive check: Ensure the URL starts with http:// or https://
        if not target_url.startswith(("http://", "https://")):
            target_url = f"http://{target_url}"
            
        # TEI exposes the embeddings route natively at /embed
        self.endpoint = f"{target_url.rstrip('/')}/embed"

    def embed(self, text: str) -> Vector:
        response = requests.post(self.endpoint, json={"inputs": text})
        response.raise_for_status()
        data = response.json()
        
        # TEI returns a nested array (e.g., [[0.1, 0.2, ...]]) even for single strings
        if isinstance(data[0], list):
            return data[0]
        return data

    def embed_batch(self, texts: List[str]) -> List[Vector]:
        response = requests.post(self.endpoint, json={"inputs": texts})
        response.raise_for_status()
        
        # Returns a clean list of lists: [[0.1...], [0.2...], ...]
        return response.json()