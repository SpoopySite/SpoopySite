import json
import aiohttp
import logging
from urllib.parse import urlparse, ParseResult

import validators.url

log = logging.getLogger(__name__)


async def redirect_gatherer(url: str, session: aiohttp.client.ClientSession):
    async with session.get(url) as resp:
        return [str(x.url) for x in resp.history]


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


async def open_blacklist():
    with open("api/blacklist.json", "r") as file:
        data = json.load(file)
    return data


async def blacklist_check(url: str):
    blacklist = await open_blacklist()
    return url in blacklist["blacklist"]


async def parse_phistank(url: str, phishtank_data):
    url_netloc = await url_splitter(url)
    url_netloc = url_netloc.netloc

    for phish in phishtank_data:
        parsed_phish = await url_splitter(phish["url"])
        netloc = parsed_phish.netloc

        if url_netloc == netloc:
            log.info("Found")
            return True
    return False

