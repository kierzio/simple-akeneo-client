from __future__ import annotations
from dataclasses import dataclass
import base64
import time
import httpx
from .config import get_settings

TOKEN_PATH = "/api/oauth/v1/token"

@dataclass
class Token:
    access_token: str
    refresh_token: str
    expires_at: float  # epoch seconds

    def is_expired(self) -> bool:
        # refresh 2 minutes early
        return time.time() >= (self.expires_at - 120)

async def obtain_token(client: httpx.AsyncClient) -> Token:
    s = get_settings()
    auth = base64.b64encode(f"{s.client_id}:{s.client_secret}".encode()).decode()
    payload = {
        "grant_type": "password",
        "username": s.username,
        "password": s.password,
    }
    r = await client.post(
        TOKEN_PATH,
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        json=payload,
    )
    r.raise_for_status()
    data = r.json()
    return Token(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_at=time.time() + int(data.get("expires_in", 3600)),
    )

async def refresh_token(client: httpx.AsyncClient, refresh_token: str) -> Token:
    s = get_settings()
    auth = base64.b64encode(f"{s.client_id}:{s.client_secret}".encode()).decode()
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    r = await client.post(
        TOKEN_PATH,
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        json=payload,
    )
    r.raise_for_status()
    data = r.json()
    return Token(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_at=time.time() + int(data.get("expires_in", 3600)),
    )
