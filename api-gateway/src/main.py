import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.components.cache_infrastructure import CacheInfrastructure
from src.components.task_bus_infrastructure import TaskBusInfrastructure
# Import your new Cache Infrastructure (Adjust the path to match where you saved it)
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

# Initialize system infrastructure once (composition root)
task_bus_infras = TaskBusInfrastructure()
cache_infras = CacheInfrastructure() # Initialize the cache here!

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
    
    # 1. Create the Query object early so we can hash it for the cache
    query = Query(text=req.query)

    # ---------------------------------------------------------
    # 2. EDGE CACHE INTERCEPTION
    # ---------------------------------------------------------
    try:
        cached_response = await cache_infras.cache.get_answer(query)
        if cached_response:
            # Tag it so the frontend knows it was lightning fast
            metadata = cached_response.metadata or {}
            metadata['gateway_cached'] = True

            return SearchResponseModel(
                success=cached_response.success,
                # Make sure the '.answer' property matches your SearchAnswer dataclass
                answer={"text": cached_response.answer.answer} if cached_response.answer else None,
                error=cached_response.error,
                metadata=metadata
            )
    except Exception as e:
        # Raise the cache exception immediately to expose connection issues
        raise HTTPException(status_code=500, detail=f"Cache Error: {str(e)}")
    # ---------------------------------------------------------

    # 3. Generate a globally unique ID for this specific web request
    request_id = RequestID(value=str(uuid.uuid4()))
    
    # 4. Package the domain task
    task = SearchTask(
        request_id=request_id,
        query=query
    )

    try:
        # 5. Push to the Worker Queue
        await task_bus_infras.task_bus.push_task(task)
        
        # 6. Suspend this HTTP request and wait for the Worker's broadcast
        bus_result = await task_bus_infras.task_bus.subscribe(request_id, timeout_seconds=500)
        
        # ---------------------------------------------------------
        # NEW: SAVE TO EDGE CACHE
        # ---------------------------------------------------------
        # Only cache the result if it was actually successful
        if bus_result.success:
            try:
                await cache_infras.cache.set_answer(query, bus_result)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Cache Write Error: {str(e)}")
        # ---------------------------------------------------------
        
        # 7. Map the internal Bus Response back to the external HTTP Response
        return SearchResponseModel(
            success=bus_result.success,
            answer={"text": bus_result.answer.answer} if bus_result.answer else None,
            error=bus_result.error,
            metadata=bus_result.metadata 
        )

    except TimeoutError as e:
        # If the timeout is breached, return a 504 Gateway Timeout
        raise HTTPException(status_code=504, detail=str(e))
        
    except HTTPException:
        raise
        
    except Exception as e:
        # Catch any Redis connection failures or unexpected crashes and raise them explicitly
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")