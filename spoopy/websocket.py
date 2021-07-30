import json
import logging

import aiohttp.client
import aiohttp.client_exceptions
import asyncpg.pool
import sanic.request
import sanic.response
import websockets.legacy.protocol
from sanic import Blueprint
import urllib.parse

import api.helpers

bp = Blueprint("spoopy_websocket")
log = logging.getLogger(__name__)


async def get_check_website(url: str, session: aiohttp.client.ClientSession, db: asyncpg.pool.Pool, fish: list):
    async with session.get(url, allow_redirects=False) as resp:
        status = resp.status
        headers = resp.headers
        text = await resp.text("utf-8")
        resp.close()

    log.info(f"Status: {status}")

    reasons = []
    safety = True

    parsed_url = await api.helpers.url_splitter(url)
    hsts_check = await api.helpers.hsts_check(parsed_url.netloc, session, db)
    blacklist_check = await api.helpers.blacklist_check(parsed_url.netloc)
    webrisk_check = await api.helpers.webrisk_check(url, session, db)
    refresh_redirect = api.helpers.refresh_header_finder(text)

    if blacklist_check:
        safety = False
        reasons.append(f"Blacklisted: {blacklist_check['reason']} by {blacklist_check['source']}")

    webrisk_reasons = []
    for key in webrisk_check:
        if webrisk_check.get(key):
            webrisk_reasons.append(key)

    if webrisk_reasons:
        safety = False
        reasons.append(f"WebRisk Flagged: {', '.join(webrisk_reasons)}")

    # if url.startswith("https"):
    #     if not hsts_check == "preloaded":
    #         safety = False

    if await api.helpers.parse_phistank(url, fish):
        safety = False
        reasons.append("Phishtank")

    return status, headers.get("location"), safety, reasons, refresh_redirect


@bp.websocket("/ws")
async def ws_spoopy(request: sanic.request.Request, ws: websockets.legacy.protocol.WebSocketCommonProtocol):
    url = await ws.recv()
    log.debug(f"New URL: {url}")

    if not await api.helpers.validate_url(url):
        await ws.send(json.dumps({"error": "Invalid URL"}))
        await ws.close()
        return

    url_pool = [url]
    youtube_check = False
    bitly_warning = False

    for url in url_pool:
        parsed = urllib.parse.urlparse(url)

        if "spoopy.oceanlord.me" in url:
            await ws.send(json.dumps({"error": "No."}))
            await ws.close()

        try:
            status, location, safety, reasons, refresh_redirect = await get_check_website(url, request.app.session, request.app.db, request.app.fish)
        except aiohttp.client_exceptions.ClientConnectorError:
            log.warning(f"Error connecting to {url} on WS")
            await ws.send(json.dumps({"error": f"Could not establish a connection to {url}"}))
            await ws.close()
            return
        except aiohttp.client_exceptions.ClientConnectorSSLError as err:
            log.warning(f"Error connect to {url} on WS due to error")
            log.error(err)
            await ws.send(json.dumps({"error": f"Could not support the protocol version that {url} uses"}))
            await ws.close()
            return

        if "youtube.com" in parsed.netloc and parsed.path == "/redirect":
            if "q" in urllib.parse.parse_qs(parsed.query):
                url_pool.append(urllib.parse.parse_qs(parsed.query).get("q")[0])
                youtube_check = True
        elif "google.com" in parsed.netloc and parsed.path == "/url":
            if "url" in urllib.parse.parse_qs(parsed.query):
                url_pool.append(urllib.parse.parse_qs(parsed.query).get("url")[0])
        elif "bitly.com" in parsed.netloc and parsed.path == "/a/warning":
            if "url" in urllib.parse.parse_qs(parsed.query):
                url_pool.append(urllib.parse.parse_qs(parsed.query).get("url")[0])
                bitly_warning = True

        await ws.send(json.dumps({"url": url,
                                  "safety": safety,
                                  "reasons": reasons,
                                  "youtube": youtube_check,
                                  "bitly_warning": bitly_warning}))
        youtube_check = False
        bitly_warning = False

        if status in [300, 301, 302, 303, 307, 308]:
            if location.startswith("/"):
                url_pool.append(f"{parsed.scheme}://{parsed.netloc}/{location}")
            else:
                url_pool.append(location)
        if refresh_redirect:
            url_pool.append(refresh_redirect)
    await ws.send(json.dumps({"end": True}))
    await ws.close()
    return
