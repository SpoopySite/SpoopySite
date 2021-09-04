import logging
from urllib.parse import ParseResult, parse_qs

import aiohttp
import multidict

from . import bitly, youtube, google, adfly, duckduckgo

log = logging.getLogger(__name__)


async def handlers(parsed: ParseResult, text: str, headers: multidict.CIMultiDictProxy,
                   session: aiohttp.client.ClientSession):
    youtube_check = False
    bitly_warning = False
    adfly_warning = False
    duckduckgo_warning = False
    url = None

    query_parse = parse_qs(parsed.query)

    if "youtube.com" in parsed.netloc and parsed.path == "/redirect":
        check = youtube.youtube(parsed)
        if check:
            url = check[0]
            youtube_check = True
    elif "google.com" in parsed.netloc and parsed.path == "/url":
        check = google.google(parsed)
        if check:
            url = check
    elif "bitly.com" in parsed.netloc and parsed.path == "/a/warning":
        check = bitly.bitly(parsed)
        if check:
            url = check[0]
            bitly_warning = True
    elif headers.get("x-powered-by") == "adfly" and len(parsed.path) > 0:
        check = adfly.adfly(text)
        if check:
            url = check
            adfly_warning = True
    elif "duckduckgo.com" in parsed.netloc and "q" in query_parse.keys():
        check = await duckduckgo.duckduckgo(parsed, session)
        if check:
            url = check
            duckduckgo_warning = True

    return {"url": url, "youtube": youtube_check, "bitly": bitly_warning, "adfly": adfly_warning}
