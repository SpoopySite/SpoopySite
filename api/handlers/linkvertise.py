import base64
import json
import logging
import time
from urllib.parse import ParseResult, urlunparse

import aiohttp

from api.handlers.handler_exceptions import Linkvertise
from app.useragents import get_random_user_agent

log = logging.getLogger(__name__)


def headers():
    return {
        "accept": "application/json",
        "user-agent": get_random_user_agent(),
        "referer": "https://linkvertise.com/",
        "origin": "https://linkvertise.com",
    }


def linkvertise_domains():
    with open("api/handlers/data/linkvertise.json", "r") as file:
        data = json.load(file)
    return data


async def get_link_id(parsed: ParseResult, session: aiohttp.client.ClientSession, url: str):
    async with session.get(f"https://publisher.linkvertise.com/api/v1/redirect/link/static/{url}",
                           headers=headers(),
                           allow_redirects=False
                           ) as resp:
        json_content: dict = await resp.json()
    if json_content["success"]:
        return json_content["data"]["link"]["id"]
    raise Linkvertise(f"Got errors from {urlunparse(parsed)}: {', '.join(json_content['messages'])}")


def get_serial(link_id: int):
    internal_time = int(time.time() * 1000)
    data = {
        "timestamp": str(internal_time),
        "random": "6548307",
        "link_id": link_id
    }

    data_string = json.dumps(data).encode("utf-8")

    return base64.b64encode(data_string).decode("utf-8")


async def get_target(link_id: int, session: aiohttp.client.ClientSession, parsed: ParseResult, url: str):
    serial = get_serial(link_id)
    async with session.post(f"https://publisher.linkvertise.com/api/v1/redirect/link/{url}/target", json={
        "serial": serial
    }, headers=headers()) as resp:
        json_content: dict = await resp.json()
    return json_content


async def linkvertise(parsed: ParseResult, session: aiohttp.client.ClientSession):
    url = parsed.path

    url = url.lstrip("/download/")
    url = url.lstrip("/")

    url = "/".join(url.split("/")[:2])

    log.info(url)

    link_id = await get_link_id(parsed, session, url)
    fetch_target = await get_target(link_id, session, parsed, url)
    log.info(f"FT: {fetch_target}")
    return fetch_target["data"]["target"]
