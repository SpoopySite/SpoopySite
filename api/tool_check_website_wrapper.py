import json
import logging

import aiohttp
import aiohttp.client_exceptions
import asyncpg
import tld

import api.cached
import api.checkers
import api.helpers
from app.useragents import get_random_user_agent

log = logging.getLogger(__name__)


async def get_check_website(url: str, session: aiohttp.client.ClientSession, db: asyncpg.pool.Pool, fish: list):
    text = None
    partial_info = False
    cached = False

    cached_data = await api.cached.cached(url, db)
    if cached_data:
        log.info(f"Serving {url} from cache")
        data = json.loads(cached_data)
        cached = True
        status, location, safety, reasons, refresh_redirect, text, headers, hsts_check, js_redirect, query_redirect, \
        partial_info = data
        return status, location, safety, reasons, refresh_redirect, text, headers, hsts_check, js_redirect, \
               query_redirect, partial_info, cached

    try:
        async with session.get(url, allow_redirects=False, headers={"User-Agent": get_random_user_agent()}) as resp:
            status = resp.status
            headers = resp.headers
            if not headers.get("Content-Type", "").startswith("image") and not headers.get("Content-Type", "").startswith("video"):
                text = await resp.text("utf-8")
            resp.close()
    except aiohttp.client_exceptions.ClientConnectorError:
        log.warning(f"Error connecting to {url} on API")
        partial_info = True
        status = None
        headers = {}

    log.info(f"Status: {status}")

    reasons = []
    safety = True

    parsed_url = await api.helpers.url_splitter(url)
    tld_parsed_url = tld.get_tld(url, as_object=True)
    hsts_check = await api.helpers.hsts_check(parsed_url.netloc, session, db)
    blacklist_check = await api.helpers.blacklist_check(parsed_url.netloc)
    webrisk_check = await api.helpers.webrisk_check(url, session, db)
    cloudflare_check = await api.checkers.cloudflare.check(parsed_url.netloc)
    luma_check = await api.checkers.luma.check(tld_parsed_url.fld, session)
    if not luma_check:
        luma_check = await api.checkers.luma.check(parsed_url.netloc, session)
    query_redirect = api.helpers.query_redirect(parsed_url)

    if text is not None:
        refresh_redirect = api.helpers.refresh_header_finder(text, parsed_url)
        js_redirect = api.helpers.js_script_check(text)
    else:
        refresh_redirect = None
        js_redirect = None

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

    if cloudflare_check:
        if str(cloudflare_check[0]) == "0.0.0.0":
            safety = False
            reasons.append("Cloudflare")

    if luma_check:
        safety = False
        reasons.append("🐟🐠: Phishing Detection")

    location = headers.get("location")
    if not location:
        location = headers.get("Location")

    data = [status, location, safety, reasons, refresh_redirect, text, dict(headers), hsts_check, js_redirect,
            query_redirect, partial_info]
    data = json.dumps(data)
    await api.cached.insert_into_cache(url, data, db)

    return status, location, safety, reasons, refresh_redirect, text, headers, hsts_check, js_redirect, query_redirect, partial_info, cached
