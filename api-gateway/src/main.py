from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from src.components.app import App


# -------------------------
# Request / Response models
# -------------------------

class SearchRequest(BaseModel):
    query: str


class SearchResponseModel(BaseModel):
    success: bool
    answer: dict[str, Any] | None = None
    error: str | None = None
    metadata: dict[str, Any] | None = None


# -------------------------
# FastAPI app
# -------------------------

app = FastAPI(title="MCP DAG Agent")

# initialize system once (composition root)
system = App()


# -------------------------
# API endpoint
# -------------------------

@app.post("/search", response_model=SearchResponseModel)
async def search(req: SearchRequest):
    
    result = await system.run(req.query)
    return SearchResponseModel(
        success=result.success,
        answer=result.answer.to_dict() if result.answer else None,
        error=result.error,
        metadata=result.metadata
    )

    
    
