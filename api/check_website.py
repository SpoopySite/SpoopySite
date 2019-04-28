import logging

import sanic
import sanic.response
from sanic import Blueprint

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
    redirects = await api.helpers.redirect_gatherer(url, request.app.session)

    checks = {
        "urls": {},
        "redirects": redirects
    }

    for redirect_url in redirects:
        checks["urls"][redirect_url] = {"safety": 0}

        parsed_url = await api.helpers.url_splitter(url)
        hsts_check = await api.helpers.hsts_check(parsed_url.netloc, request.app.session)
        blacklist_check = await api.helpers.blacklist_check(parsed_url.netloc)

        if not hsts_check["status"] == "preloaded":
            checks["urls"][redirect_url]["safety"] -= 1
        checks["urls"][redirect_url]["hsts"] = hsts_check["status"] if hsts_check["status"] == "preloaded" else "NO_HSTS"
        checks["urls"][redirect_url]["blacklist"] = blacklist_check
        checks["urls"][redirect_url]["phishtank"] = await api.helpers.parse_phistank(url, request.app.fish)
    # log.info(await api.helpers.redirect_gatherer(url, request.app.session))
    # checks[url]["redirects"] = await api.helpers.redirect_gatherer(url, request.app.session)

    return sanic.response.json({"processed": checks})


@bp.route("/check_redirect", methods=["GET"])
async def get_check_redirect(request):
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

    checks = await api.helpers.redirect_gatherer(url, request.app.session)
    log.info(checks)
    for x in checks:
        log.info(x)
        log.info(type(x))

    return sanic.response.json({"processed": checks})
