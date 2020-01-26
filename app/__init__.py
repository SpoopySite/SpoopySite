# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2018 Samuel Riches

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import bz2
import json
import json.decoder
import logging
import os
import time
from sanic.websocket import WebSocketProtocol
from .database import create_pgsql_pool
import urllib.parse

import spoopy.spoopy
import spoopy.websocket
import aiohttp
import aiohttp.client_exceptions
import sanic
import sanic.exceptions
import sanic.request
import sanic.response

import api
from .config import Config

log = logging.getLogger(__name__)
config = Config.from_file()


async def ignore_404s(request, exception):
    log.warning(f"File/URL not found: {request.url}")
    if request.path.count("/site/http") > 1:
        return sanic.response.text(f"404. `{request.url}` not found.", status=404)
    elif request.path.startswith("/site/http"):
        return await sanic.response.file("./spoopy-site/build/index.html")
    else:
        return sanic.response.text(f"404. `{request.url}` not found.", status=404)


async def ignore_methods(request, exception):
    request: sanic.request.Request
    log.warning(f"Method {request.method} not supported for {request.url}")
    return sanic.response.text(f"Method: {request.method}, is not supported for {request.url}", status=405)


def json_cleaner(data: [dict]):
    new_data = []
    for data_piece in data:
        data_piece: dict
        data_piece.pop("phish_detail_url")
        data_piece.pop("submission_time")
        data_piece.pop("verification_time")
        data_piece.pop("online")
        data_piece.pop("details")
        data_piece.pop("target")
        data_piece.pop("verified")
        data_piece["url"] = urllib.parse.urlparse(data_piece["url"]).netloc
        new_data.append(data_piece)

    return new_data


async def phish_download(app):
    async with app.session.get(f"https://data.phishtank.com/data/{config.key}/online-valid.json.bz2",
                               headers={"User-Agent": "python-aiohttp"}) as resp:
        log.info(resp.headers)
        status = resp.status
        if status != 200:
            text_data = await resp.text()
            log.warning(status)
            try:
                data = await resp.json()
                log.warning(data)
            except aiohttp.client_exceptions.ContentTypeError:
                log.warning(text_data)
        else:
            data = await resp.read()
            data = bz2.decompress(data)
            data = json.loads(data)
            data = json_cleaner(data)
            with open("api/phishtank.json", "w") as file:
                json.dump(data, file)
            log.info("Downloaded and parsed phishtank")


async def phish_test(app):
    try:
        with open("api/phishtank.json", "r") as _:
            pass
    except FileNotFoundError:
        log.info("Updating phishtank")
        await phish_download(app)


async def download_phish_test(app):
    await phish_test(app)

    while True:
        await asyncio.sleep(86400)

        log.info("Updating phishtank")

        await phish_download(app)


class Server:
    def __init__(self, config, *, loop=None):
        self.app = app = sanic.Sanic(__name__, configure_logging=False)
        self.config = app.cfg = config

        self.loop = loop = loop or asyncio.get_event_loop()

        self.session = app.session = None
        self.fish = app.fish = None
        self.db = app.db = None

        app.config['LOGO'] = None

        app.blueprint(api.bp_group)
        app.blueprint(spoopy.spoopy.bp)
        app.blueprint(spoopy.websocket.bp)

        app.static("/", "./spoopy-site/build/index.html")
        app.static("/static", "./spoopy-site/build/static")
        app.static("/site", "./spoopy-site/build/index.html")
        app.static("/docs", "./spoopy-site/build/index.html")
        app.static("/robots.txt", "./spoopy-site/robots.txt")

        app.error_handler.add(sanic.exceptions.NotFound, ignore_404s)
        app.error_handler.add(sanic.exceptions.MethodNotSupported, ignore_methods)

        # Register middleware which starts database connections
        app.register_listener(self.worker_stop, 'after_server_stop')
        app.register_listener(self.worker_init, 'before_server_start')

        app.add_task(download_phish_test)

    @classmethod
    def with_config(cls, path='config.yaml', *, loop=None):
        return cls(Config.from_file(path), loop=loop)

    def run(self, host='0.0.0.0', port=8000, debug=True, workers=None, **kwargs):
        """
        Run the App, this calls `sanic.Sanic.run` with the given arguments.

        The App will start one worker per available cpu core unless otherwise specified.
        """

        workers = workers or os.cpu_count() or 1

        self.app.run(host=host, port=port, debug=debug, workers=workers, protocol=WebSocketProtocol, **kwargs)

    async def worker_init(self, app, loop):
        self.session = app.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=45))
        self.db = self.app.db = await create_pgsql_pool(**self.config.postgres)
        try:
            with open("api/phishtank.json", "r") as file:
                try:
                    phishtank_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    log.warning("JSON Decode Error. Rebuilding")
                    try:
                        os.remove("api/phishtank.json")
                    except FileNotFoundError:
                        pass
                    await phish_test(app)
                    with open("api/phishtank.json", "r") as file:
                        phishtank_data = json.load(file)
        except FileNotFoundError:
            log.warning("File Not Found. Rebuilding")
            await phish_test(app)
            with open("api/phishtank.json", "r") as file:
                phishtank_data = json.load(file)
        self.fish = app.fish = phishtank_data

    async def worker_stop(self, app, loop):
        await self.session.close()
