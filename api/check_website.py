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

    checks = {
        url: {
            "safety": 0
        }
    }

    parsed_url = await api.helpers.url_splitter(url)
    hsts_check = await api.helpers.hsts_check(parsed_url.netloc, request.app.session)

    if not hsts_check["status"] == "preloaded":
        checks[search_query]["safety"] -= 1
    checks[search_query]["hsts"] = hsts_check["status"] if hsts_check["status"] == "preloaded" else "NO_HSTS"

    return sanic.response.json({"processed": checks})
