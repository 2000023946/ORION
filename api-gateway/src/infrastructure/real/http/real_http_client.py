import asyncio
from typing import Any, Dict, Optional

import requests

from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.http.http_response import HttpResponse


class RealHttpClient(HttpClientPort):
    """
    Concrete implementation of HttpClientPort using the synchronous
    'requests' library wrapped for async compatibility.
    """

    def __init__(self):
        self._session = requests.Session()

    async def _request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        def do_request():
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                timeout=timeout,
            )

            return HttpResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=response.text,
            )

        return await asyncio.to_thread(do_request)

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        return await self._request(
            "GET",
            url,
            headers=headers,
            params=params,
            timeout=timeout,
        )

    async def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        return await self._request(
            "POST",
            url,
            headers=headers,
            data=data,
            json=json,
            timeout=timeout,
        )

    async def put(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        return await self._request(
            "PUT",
            url,
            headers=headers,
            data=data,
            json=json,
            timeout=timeout,
        )

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        return await self._request(
            "DELETE",
            url,
            headers=headers,
            timeout=timeout,
        )