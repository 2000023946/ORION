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
    answer: dict | None = None
    error: str | None = None


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
    print('res', result)
    return SearchResponseModel(
        success=result.success,
        answer=result.answer.to_dict() if result.answer else None,
        error=result.error
    )