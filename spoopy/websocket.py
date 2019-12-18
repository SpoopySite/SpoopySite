import json
import logging

import aiohttp.client
import asyncpg.pool
import sanic
import sanic.request
import sanic.response
import websockets.protocol
from sanic import Blueprint
import urllib.parse

import api.helpers

bp = Blueprint("spoopy_websocket")
log = logging.getLogger(__name__)


async def get_check_website(url: str, session: aiohttp.client.ClientSession, db: asyncpg.pool.Pool, fish: list):
    async with session.get(url, allow_redirects=False) as resp:
        status = resp.status
        headers = resp.headers
        resp.close()

    log.info(status)

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


@bp.websocket("/ws")
async def ws_spoopy(request: sanic.request.Request, ws: websockets.protocol.WebSocketCommonProtocol):
    url = await ws.recv()
    log.info(url)

    url_pool = [url]
    for url in url_pool:
        status, location, safety, reasons = await get_check_website(url, request.app.session, request.app.db, request.app.fish)
        await ws.send(json.dumps({"url": url, "safety": safety, "reasons": reasons}))

        if status in [300, 301, 302, 303, 307, 308]:
            url_pool.append(location)
    await ws.send(json.dumps({"end": True}))
    await ws.close()
    return


@bp.route("/ws")
async def get_ws(request: sanic.request.Request):
    return sanic.response.redirect("/")
