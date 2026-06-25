import requests

from src.ports.http_port import HttpPort


class RequestsHttpAdapter(HttpPort):

    def get(self, url, headers=None) -> dict:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, url, body, headers=None) -> dict:
        response = requests.post(
            url,
            json=body,
            headers=headers
        )
        response.raise_for_status()
        return response.json()