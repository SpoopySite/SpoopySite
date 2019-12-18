import json
import logging

import aiohttp.client
import asyncpg.pool
import sanic
import sanic.request
import sanic.response
import websockets.protocol
from sanic import Blueprint

import api.helpers

bp = Blueprint("spoopy_websocket")
log = logging.getLogger(__name__)


async def get_check_website(url: str, session: aiohttp.client.ClientSession, db: asyncpg.pool.Pool, fish: list):
    async with session.get(url, allow_redirects=False) as resp:
        status = resp.status
        headers = resp.headers

    log.info(status)
    log.info(headers)

    reasons = []
    safety = True

    parsed_url = await api.helpers.url_splitter(url)
    hsts_check = await api.helpers.hsts_check(parsed_url.netloc, session, db)
    blacklist_check = await api.helpers.blacklist_check(parsed_url.netloc)
    if blacklist_check:
        safety = False
        reasons.append("Blacklisted")


    # if url.startswith("https"):
    #     if not hsts_check == "preloaded":
    #         safety = False

    if await api.helpers.parse_phistank(url, fish):
        safety = False
        reasons.append("Phishtank")

    return status, headers.get("location"), safety, reasons


@bp.websocket("/ws/<url:path>")
async def ws_spoopy(request: sanic.request.Request, ws: websockets.protocol.WebSocketCommonProtocol, url):
    log.info(url + "48")

    url_pool = [url]
    for url in url_pool:
        await ws.ping()
        status, location, safety, reasons = await get_check_website(url, request.app.session, request.app.db, request.app.fish)
        await ws.ping()
        log.info(status)
        log.info(location)
        await ws.send(json.dumps({"url": url, "safety": safety, "reasons": reasons}))

        if status in [302]:
            url_pool.append(location)
    await ws.send(json.dumps({"end": True}))
    return


@bp.websocket("/ws/http://<url:path>")
async def ws_spoopy(request: sanic.request.Request, ws: websockets.protocol.WebSocketCommonProtocol, url):
    log.info(url + "68")
    await ws.close()
    return


@bp.websocket("/ws/https://<url:path>")
async def ws_spoopy(request: sanic.request.Request, ws: websockets.protocol.WebSocketCommonProtocol, url):
    log.info(url + "75")
    await ws.send(json.dumps({"test": "hi3"}))

    url_pool = [url]
    for url in url_pool:
        await ws.ping()
        log.warning("hi")
        checks, status, location = await get_check_website(url, request.app.session, request.app.db, request.app.fish)
        await ws.ping()
        log.info(checks)
        log.info(type(status))
        log.info(status)
        log.info(repr(status))
        log.info(location)
        await ws.send("test")
        await ws.send(checks)

        if status in [302]:
            url_pool.append(location)
    return
