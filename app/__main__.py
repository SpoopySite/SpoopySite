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

import sentry_sdk
import uvloop
from sentry_sdk.integrations.sanic import SanicIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from . import Server
from .logging import fix_access_log, setup_logging

sentry_sdk.init(
    dsn="https://a2ab246b56f34179a4e2d2d54f0597d7@o970585.ingest.sentry.io/5921973",
    integrations=[SanicIntegration(), AioHttpIntegration()],
    request_bodies="always",
    traces_sample_rate=1.0
)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

with setup_logging():
    fix_access_log()

    Server.with_config().run()
