import logging
import urllib.parse

import aiohttp.client_exceptions
import sanic
import sanic.response
from sanic import Blueprint

import api.checkers.cloudflare
import api.checkers.luma
import api.helpers

bp = Blueprint("check_website")
log = logging.getLogger(__name__)


@bp.route("/check_website", methods=["GET"])
async def get_check_website(request):
    try:
        if "website" in request.args:
            search_query = request.args["website"][0]
        else:
            search_query = None
        if search_query is None or search_query == "":
            search_query = request.json.get("website")
    except (AttributeError, KeyError):
        error = (
            "Please specify the search query under the 'website' key."
        )
        return sanic.response.json({"error": error}, status=400)

    if not await api.helpers.validate_url(search_query):
        return sanic.response.json({"status": "Invalid URL"},
                                   status=400)

    url = search_query

    if "spoopy.oceanlord.me" in url:
        return sanic.response.json({"error": "Go away."})

    try:
        redirects = await api.helpers.redirect_gatherer(url, request.app.session)
    except aiohttp.client_exceptions.ClientConnectorError:
        log.warning(f"Error connecting to {url}")
        return sanic.response.json({"error": f"Could not establish a connection to {url}"}, status=400)

    if len(redirects) == 0:
        redirects.append(url)
    log.info(redirects)

    async with request.app.session.get(redirects[-1], allow_redirects=False) as resp:
        text = await resp.text("utf-8")
        resp.close()
    refresh_header = api.helpers.refresh_header_finder(text)
    if refresh_header:
        redirects.append(refresh_header)

    checks = {
        "urls": {},
    }

    parsed_url = urllib.parse.urlparse(redirects[-1])
    if "youtube.com" in parsed_url.netloc and parsed_url.path == "/redirect":
        if "q" in urllib.parse.parse_qs(parsed_url.query):
            redirects.append(urllib.parse.parse_qs(parsed_url.query).get("q")[0])
    elif "google.com" in parsed_url.netloc and parsed_url.path == "/url":
        if "url" in urllib.parse.parse_qs(parsed_url.query):
            redirects.append(urllib.parse.parse_qs(parsed_url.query).get("url")[0])
    elif "bitly.com" in parsed_url.netloc and parsed_url.path == "/a/warning":
        if "url" in urllib.parse.parse_qs(parsed_url.query):
            redirects.append(urllib.parse.parse_qs(parsed_url.query).get("url")[0])

    for redirect_url in redirects:
        checks["urls"][redirect_url] = {"safety": 0}

        parsed_url = await api.helpers.url_splitter(url)
        hsts_check = await api.helpers.hsts_check(parsed_url.netloc, request.app.session, request.app.db)
        blacklist_check = await api.helpers.blacklist_check(parsed_url.netloc)
        phishtank_check = await api.helpers.parse_phistank(url, request.app.fish)
        webrisk_check = await api.helpers.webrisk_check(url, request.app.session, request.app.db)
        cloudflare_check = await api.checkers.cloudflare.check(parsed_url.netloc)
        luma_check = await api.checkers.luma.check(parsed_url.netloc, request.app.session)

        if not hsts_check == "preloaded":
            checks["urls"][redirect_url]["safety"] -= 1
        checks["urls"][redirect_url]["hsts"] = hsts_check if hsts_check == "preloaded" else "NO_HSTS"
        checks["urls"][redirect_url]["blacklist"] = blacklist_check
        checks["urls"][redirect_url]["phishtank"] = phishtank_check
        checks["urls"][redirect_url]["webrisk"] = []

        for key in webrisk_check:
            if webrisk_check.get(key):
                checks["urls"][redirect_url]["webrisk"].append(key)
        if not checks["urls"][redirect_url]["webrisk"]:
            checks["urls"][redirect_url].pop("webrisk")

        if blacklist_check:
            checks["urls"][redirect_url]["safe"] = False
        elif phishtank_check:
            checks["urls"][redirect_url]["safe"] = False
        elif "webrisk" in checks["urls"][redirect_url]:
            checks["urls"][redirect_url]["safe"] = False
        elif str(cloudflare_check[0]) == "0.0.0.0":
            checks["urls"][redirect_url]["safe"] = False
        elif luma_check:
            checks["urls"][redirect_url]["safe"] = False
        else:
            checks["urls"][redirect_url]["safe"] = True

    # log.info(await api.helpers.redirect_gatherer(url, request.app.session))
    # checks[url]["redirects"] = await api.helpers.redirect_gatherer(url, request.app.session)

    return sanic.response.json({"processed": checks})
