import aiohttp
import logging
from urllib.parse import urlparse

import validators.url

log = logging.getLogger(__name__)


async def validate_url(url: str):
    a = validators.url(url)
    if not isinstance(a, validators.ValidationFailure):
        return True
    return False


async def url_splitter(url: str):
    return urlparse(url)


async def hsts_check(url: str, session: aiohttp.client.ClientSession):
    async with session.get("https://hstspreload.org/api/v2/status",
                           params={"domain": url}) as resp:
        json = await resp.json()
        status = resp.status

    return json
