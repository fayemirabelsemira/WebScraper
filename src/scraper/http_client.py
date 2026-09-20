import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import (
    HEADERS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF_FACTOR,
    RETRY_STATUS_CODES,
)


class HTTPClient:
    """Handles HTTP requests for the web scraper."""

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            HEADERS
        )

        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=RETRY_STATUS_CODES,
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        self.session.mount(
            "http://",
            adapter
        )

        self.session.mount(
            "https://",
            adapter
        )

    def fetch(self, url: str) -> str:
        """Fetch HTML content from a URL."""

        response = self.session.get(
            url,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.text

    def close(self):
        """Close the HTTP session."""

        self.session.close()