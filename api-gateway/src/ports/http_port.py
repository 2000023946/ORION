# ports/http_port.py

from abc import ABC, abstractmethod

class HttpPort(ABC):

    @abstractmethod
    def get(self, url: str, headers: dict | None = None) -> dict:
        pass

    @abstractmethod
    def post(
        self,
        url: str,
        body: dict,
        headers: dict | None = None
    ) -> dict:
        pass