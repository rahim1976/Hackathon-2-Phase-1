import httpx
from typing import Any

DAEMON_URL = "http://127.0.0.1:8000"

class DaemonConnectionError(Exception):
    """Raised when the client cannot connect to the daemon."""
    pass

class TodoClient:
    def __init__(self, base_url: str = DAEMON_URL):
        self.base_url = base_url

    def _get_url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    async def get(self, path: str) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self._get_url(path))
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError as e:
            raise DaemonConnectionError("Could not connect to the background daemon.") from e

    async def post(self, path: str, json: dict | None = None) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self._get_url(path), json=json)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError as e:
            raise DaemonConnectionError("Could not connect to the background daemon.") from e

    async def patch(self, path: str, json: dict) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(self._get_url(path), json=json)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError as e:
            raise DaemonConnectionError("Could not connect to the background daemon.") from e

    async def delete(self, path: str) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(self._get_url(path))
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError as e:
            raise DaemonConnectionError("Could not connect to the background daemon.") from e

client = TodoClient()
