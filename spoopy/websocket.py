import json
import logging
import urllib.parse
from urllib.parse import ParseResult

import aiohttp.client
import aiohttp.client_exceptions
import sanic.request
import sanic.response
import websockets.legacy.protocol
from sanic import Blueprint

import api.checkers.cloudflare
import api.checkers.luma
import api.handlers.handlers
import api.helpers
from api.tool_check_website_wrapper import get_check_website

bp = Blueprint("spoopy_websocket")
log = logging.getLogger(__name__)


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
    adfly = False

    for url in url_pool:
        parsed: ParseResult = urllib.parse.urlparse(url)

        if "spoopy.oceanlord.me" in url:
            await ws.send(json.dumps({"error": "No."}))
            await ws.close()

        try:
            status, location, safety, reasons, refresh_redirect, text, headers = await get_check_website(url,
                                                                                                         request.app.session,
                                                                                                         request.app.db,
                                                                                                         request.app.fish)
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

        handler_check = api.handlers.handlers.handlers(parsed, text, headers)
        if handler_check["url"]:
            url_pool.append(handler_check.get("url"))
            youtube_check = handler_check.get("youtube")
            bitly_warning = handler_check.get("bitly")
            adfly = handler_check.get("adfly")

        await ws.send(json.dumps({"url": url,
                                  "safety": safety,
                                  "reasons": reasons,
                                  "youtube": youtube_check,
                                  "bitly_warning": bitly_warning,
                                  "adfly": adfly}))
        youtube_check = False
        bitly_warning = False
        adfly = False

        if status in [300, 301, 302, 303, 307, 308]:
            if location.startswith("/"):
                url_pool.append(f"{parsed.scheme}://{parsed.netloc}/{location}")
            else:
                if location not in url_pool:
                    url_pool.append(location)
        if refresh_redirect:
            url_pool.append(refresh_redirect)
    await ws.send(json.dumps({"end": True}))
    await ws.close()
    return
