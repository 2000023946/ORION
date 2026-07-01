from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class HttpClientPort(ABC):

    @abstractmethod
    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Perform HTTP GET request."""
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Perform HTTP POST request."""
        pass

    @abstractmethod
    async def put(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Perform HTTP PUT request."""
        pass

    @abstractmethod
    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Perform HTTP DELETE request."""
        pass