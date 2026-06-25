from src.ports.http_port import HttpPort


class DummyHttpAdapter(HttpPort):

    def get(self, url: str, headers: dict | None = None) -> dict:
        return {
            "url": url,
            "method": "GET",
            "content": "dummy get response",
            "score": 1.0
        }

    def post(
        self,
        url: str,
        body: dict,
        headers: dict | None = None
    ) -> dict:
        return {
            "url": url,
            "method": "POST",
            "request_body": body,
            "content": f"dummy search result for '{body.get('query', '')}'",
            "score": 1.0
        }