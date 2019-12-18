import logging

import sanic
import sanic.request
import sanic.response
from sanic import Blueprint

bp = Blueprint("spoopy_fetching")
log = logging.getLogger(__name__)


@bp.route("/spoopy/<url:path>", methods=["GET"])
async def get_spoopy(request: sanic.request.Request, url: str):
    log.info(url + " 1")
    return await sanic.response.file("public/spoopy.html")


@bp.route("/spoopy/http://<url:path>", methods=["GET"])
async def get_spoopy(request: sanic.request.Request, url: str):
    log.info(url + " 2")
    return await sanic.response.file("public/spoopy.html")


@bp.route("/spoopy/https://<url:path>", methods=["GET"])
async def get_spoopy(request: sanic.request.Request, url: str):
    log.info(url + " 3")
    return await sanic.response.file("public/spoopy.html")
