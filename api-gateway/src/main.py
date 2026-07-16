import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.components.task_bus_infrastructure import TaskBusInfrastructure
from src.metrics.decorator import measure

# Import your domain and bus models
from src.domain.query import Query
from src.application.bus.request_id import RequestID
from src.application.bus.search_task import SearchTask

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

# -----------------------------
# Prometheus metrics endpoint
# -----------------------------

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# initialize system once (composition root)
task_bus_infras = TaskBusInfrastructure()

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
@measure("search_request")
@app.post("/search", response_model=SearchResponseModel)
async def search(req: SearchRequest):
    print("got a request")
    # 1. Generate a globally unique ID for this specific web request
    request_id = RequestID(value=str(uuid.uuid4()))
    
    # 2. Package the domain task
    task = SearchTask(
        request_id=request_id,
        query=Query(text=req.query)
    )

    try:
        # 3. Push to the Worker Queue
        print("pushing the task now", task)
        await task_bus_infras.task_bus.push_task(task)
        
        # 4. Suspend this HTTP request and wait for the Worker's broadcast
        # The timeout ensures the client doesn't hang forever if the queue is overloaded
        bus_result = await task_bus_infras.task_bus.subscribe(request_id, timeout_seconds=500)
        print("got the result", bus_result)
        # 5. Map the internal Bus Response back to the external HTTP Response
        return SearchResponseModel(
            success=bus_result.success,
            answer={"text": bus_result.answer.answer} if bus_result.answer else None,
            error=bus_result.error,
            metadata=bus_result.metadata  # Can be populated if you pass metadata through the bus later
        )

    except TimeoutError as e:
        # If the 60s timeout is breached, return a 504 Gateway Timeout
        raise HTTPException(status_code=504, detail=str(e))
        
    except Exception as e:
        # Catch any Redis connection failures or unexpected crashes
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")