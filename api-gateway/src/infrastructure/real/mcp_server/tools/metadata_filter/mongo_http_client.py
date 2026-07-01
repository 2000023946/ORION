from typing import Any, Optional, Dict

from pymongo import MongoClient

from src.infrastructure.config.settings import settings
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.http.http_response import HttpResponse


class MongoHttpClient(HttpClientPort):
    """
    HttpClientPort implementation backed by MongoDB.

    This acts as a fake HTTP layer so tools can remain unchanged
    while swapping backend implementations.
    """

    def __init__(self, uri: str, db_name: str) -> None:
        self.client: MongoClient[Any] = MongoClient(uri)
        self.db = self.client[db_name]

    # ----------------------------
    # GET
    # ----------------------------
    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        raise NotImplementedError("MongoHttpClient does not support GET yet")

    # ----------------------------
    # POST (MAIN LOGIC)
    # ----------------------------
    async def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:

        json = json or {}

        # ----------------------------
        # Metadata Query endpoint
        # ----------------------------
        if "/query" in url:
            collection_name = settings.metadata_collection_name
            filter_query = json.get("filter", {})


            collection = self.db[collection_name]
            results = list(collection.find(filter_query))

            return HttpResponse(
                status_code=200,
                headers={},
                body={
                    "documents": results
                }
            )

        raise ValueError(f"Unsupported POST route: {url}")

    # ----------------------------
    # PUT
    # ----------------------------
    async def put(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        raise NotImplementedError("MongoHttpClient does not support PUT yet")

    # ----------------------------
    # DELETE
    # ----------------------------
    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        raise NotImplementedError("MongoHttpClient does not support DELETE yet")