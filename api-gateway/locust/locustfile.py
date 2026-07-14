from locust import HttpUser, task, between
import random

from queries import SEARCH_QUERIES


class OrionUser(HttpUser):

    host = "http://localhost:8000"

    wait_time = between(1, 3)


    @task
    def search_request(self):

        query = random.choice(
            SEARCH_QUERIES
        )

        response = self.client.post(
            "/search",
            json={
                "query": query
            },
            name="/search"
        )


        if response.status_code != 200:
            print(
                "Failed:",
                response.status_code,
                response.text
            )