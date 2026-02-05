from typing import Any

from aiohttp import ClientSession, ClientTimeout
from pydantic import HttpUrl

TIMEOUT = 5.0


async def fetch(url: HttpUrl, params: dict[str, Any] = {}) -> dict:
    url_encoded = url.encoded_string()

    async with ClientSession(timeout=ClientTimeout(total=TIMEOUT)) as session:
        async with session.get(url_encoded, params=params) as response:
            json = await response.json()

    return json
