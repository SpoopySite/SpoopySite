# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2018 - 2019 SnowyLuma

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

__all__ = ('create_pgsql_pool',)

import asyncio
import functools
import json
import logging

import asyncpg


log = logging.getLogger(__name__)


async def _set_codecs(conn, init=None):
    if init is not None:
        await init(conn)

    await conn.set_type_codec(typename='jsonb', schema='pg_catalog', encoder=json.dumps, decoder=json.loads)


async def create_pgsql_pool(*args, command_timeout=120, init=None, **kwargs):
    """
    Invokes `asyncpg.create_pool` with the given arguments, adding a jsonb codec to allow working with json easier.

    To allow easier usage within Docker 5 attempts are made at establishing a connection.
    """

    if init is None:
        init_conn = _set_codecs
    else:
        init_conn = functools.partial(_set_codecs, init)

    error = None

    for attempt in range(5):
        try:
            return await asyncpg.create_pool(*args, command_timeout=command_timeout, init=init_conn, **kwargs)
        except (ConnectionRefusedError, asyncpg.CannotConnectNowError) as error:
            if attempt < 5:
                delay = (attempt + 1) ** 2
                log.warning(f'Retrying connection in {delay} due to {error.__class__.__name__}: {error}')

                await asyncio.sleep(delay)

    raise error
