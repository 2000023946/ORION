import string
import random
from locust import HttpUser, task, between

class OrionUser(HttpUser):

    host = "http://localhost:8000"
    wait_time = between(1, 3)

    @task
    def search_request(self):
        # Generate a random 100-character string to bypass the edge cache
        query = "".join(random.choices(string.ascii_letters + string.digits, k=100))

        # Use catch_response to manually record successes and failures in the Locust UI
        with self.client.post(
            "/search",
            json={
                "query": query
            },
            name="/search",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed: {response.status_code} - {response.text}")
            else:
                response.success()