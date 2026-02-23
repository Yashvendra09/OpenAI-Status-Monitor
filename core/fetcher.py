import httpx
from typing import Optional


class HTTPFetcher:
    """
    Handles HTTP requests with ETag-based conditional fetching.
    Prevents unnecessary data transfer.
    """

    def __init__(self):
        self._etag_cache = {}

    async def fetch_json(self, url: str) -> Optional[dict]:
        headers = {}

        # Send ETag if we have one
        if url in self._etag_cache:
            headers["If-None-Match"] = self._etag_cache[url]

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)

            # If nothing changed
            if response.status_code == 304:
                return None

            response.raise_for_status()

            # Store ETag for future conditional requests
            if "etag" in response.headers:
                self._etag_cache[url] = response.headers["etag"]

            return response.json()