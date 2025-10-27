from __future__ import annotations
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception, retry_if_exception_type
from .config import get_settings
from .auth import Token, obtain_token, refresh_token

class AkeneoClient:
    def __init__(self):
        s = get_settings()
        self.client = httpx.AsyncClient(base_url=s.base_url, timeout=30.0)
        self._token: Token | None = None

    async def _ensure_token(self):
        if self._token is None:
            self._token = await obtain_token(self.client)
        elif self._token.is_expired():
            self._token = await refresh_token(self.client, self._token.refresh_token)

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        await self._ensure_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._token.access_token}"
        r = await self.client.request(method, url, headers=headers, **kwargs)
        if r.status_code == 401:
            # Try one refresh then retry once
            self._token = await refresh_token(self.client, self._token.refresh_token)  # type: ignore
            headers["Authorization"] = f"Bearer {self._token.access_token}"
            r = await self.client.request(method, url, headers=headers, **kwargs)
        r.raise_for_status()
        return r

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("GET", url, **kwargs)

    async def close(self):
        await self.client.aclose()
