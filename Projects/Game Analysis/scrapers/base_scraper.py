import time
import requests
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, base_url, headers=None, delay=1.5, timeout=10, retries=3):
        self.base_url = base_url
        self.headers = headers or {}
        self.delay = delay
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()

    def get(self, url, params=None):
        attempt = 0

        while attempt < self.retries:
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=self.timeout
                )

                response.raise_for_status()
                time.sleep(self.delay)
                return response

            except requests.RequestException:
                attempt += 1
                time.sleep(1)

        return None

    @abstractmethod
    def scrape(self):
        pass
