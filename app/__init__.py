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
import logging
import os

import aiohttp
import sanic
import sanic.exceptions
import sanic.request
import sanic.response

import api
from .config import Config

log = logging.getLogger(__name__)


async def ignore_404s(request, exception):
    log.warning(f"File/URL not found: {request.url}")
    return sanic.response.text(f"404. `{request.url}` not found.", status=404)


async def ignore_methods(request, exception):
    request: sanic.request.Request
    log.warning(f"Method {request.method} not supported for {request.url}")
    return sanic.response.text(f"Method: {request.method}, is not supported for {request.url}", status=405)


class Server:
    def __init__(self, config, *, loop=None):
        self.app = app = sanic.Sanic(__name__, configure_logging=False)
        self.config = app.cfg = config

        self.loop = loop = loop or asyncio.get_event_loop()

        self.session = app.session = None

        app.config['LOGO'] = None

        app.blueprint(api.bp_group)
        app.static("/", "./static/index.html")
        app.static("/", "./static")

        app.error_handler.add(sanic.exceptions.NotFound, ignore_404s)
        app.error_handler.add(sanic.exceptions.MethodNotSupported, ignore_methods)

        # Register middleware which starts database connections
        app.register_listener(self.worker_stop, 'after_server_stop')
        app.register_listener(self.worker_init, 'before_server_start')

    @classmethod
    def with_config(cls, path='config.yaml', *, loop=None):
        return cls(Config.from_file(path), loop=loop)

    def run(self, host='0.0.0.0', port=8000, debug=False, workers=None, **kwargs):
        """
        Run the App, this calls `sanic.Sanic.run` with the given arguments.

        The App will start one worker per available cpu core unless otherwise specified.
        """

        workers = workers or os.cpu_count() or 1

        self.app.run(host=host, port=port, debug=debug, workers=workers, **kwargs)

    async def worker_init(self, app, loop):
        self.session = app.session = aiohttp.ClientSession()

    async def worker_stop(self, app, loop):
        await self.session.close()
