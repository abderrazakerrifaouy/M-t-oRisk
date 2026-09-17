import requests


class APIClient:

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, params):
        response = requests.get(
            self.base_url,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()
    