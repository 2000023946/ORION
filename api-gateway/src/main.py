from typing import Any

from fastapi import FastAPI # type: ignore
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.components.app import App
from src.metrics.decorator import measure

from prometheus_client import make_asgi_app


# -------------------------
# FastAPI app
# -------------------------

app = FastAPI(title="MCP DAG Agent")


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Prometheus metrics endpoint
# -------------------------

metrics_app = make_asgi_app()

app.mount(
    "/metrics",
    metrics_app
)
# initialize system once (composition root)
system = App(mock=True)



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
# API endpoint
# -------------------------
@measure("search_requeset")
@app.post("/search", response_model=SearchResponseModel)
async def search(req: SearchRequest):
    print("comuniting to executor the name of ", system.graph_executor_infras.grpc_graph_executor.target_address)
    result = await system.run(req.query)
    return SearchResponseModel(
        success=result.success,
        answer=result.answer.to_dict() if result.answer else None,
        error=result.error,
        metadata=result.metadata
    )
    
    
