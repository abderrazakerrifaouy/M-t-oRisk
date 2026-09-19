import requests
from requests import RequestException

from src.exceptions import ExtractionError


class APIClient:

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, params):
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except RequestException as exc:
            raise ExtractionError(
                f"Weather API request failed: {self.base_url}"
            ) from exc
        except ValueError as exc:
            raise ExtractionError("Weather API returned invalid JSON") from exc

    