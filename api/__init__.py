from sanic import Blueprint

import api.check_website

bp_group = Blueprint.group(check_website.bp,
                           url_prefix="/api")
