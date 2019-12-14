import datetime
import json
import logging
from urllib.parse import urlparse

import aiohttp
import asyncpg
import validators.url

log = logging.getLogger(__name__)


async def redirect_gatherer(url: str, session: aiohttp.client.ClientSession):
    async with session.get(url) as resp:
        return [str(x.url) for x in resp.history]


async def validate_url(url: str):
    a = validators.url(url)
    if not isinstance(a, validators.ValidationFailure):
        return True
    return False


async def url_splitter(url: str):
    return urlparse(url)


async def check_hsts(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        check = await conn.fetchval("""
        SELECT EXISTS(
        SELECT 1
        FROM hsts
        WHERE url = $1
        )
        """, url)
    return check


async def fetch_hsts(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        value = await conn.fetchval("""
        SELECT status
        FROM hsts
        WHERE url = $1
        """, url)
    return value


async def fetch_updated_at(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        value = await conn.fetchval("""
        SELECT updated_at
        FROM hsts
        WHERE url = $1
        """, url)
    return value


async def insert_hsts(pool: asyncpg.pool.Pool, url: str, status: str):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO hsts (url, status)
        VALUES($1, $2) 
        """, url, status)


async def update_hsts(session: aiohttp.client.ClientSession, url, pool: asyncpg.pool.Pool):
    log.info("Updating HSTS status for: {}".format(url))
    async with session.get("https://hstspreload.org/api/v2/status",
                           params={"domain": url}) as resp:
        json_data = await resp.json()
        status = json_data.get("status")
        await insert_hsts(pool, url, status)
    return status


async def hsts_check(url: str, session: aiohttp.client.ClientSession, pool: asyncpg.pool.Pool):
    if await check_hsts(pool, url):
        updated_at = await fetch_updated_at(pool, url)
        if (updated_at + datetime.timedelta(days=7)) > datetime.datetime.now():
            return await fetch_hsts(pool, url)
        else:
            return await update_hsts(session, url, pool)
    else:
        return await update_hsts(session, url, pool)


async def open_blacklist():
    with open("api/blacklist.json", "r") as file:
        data = json.load(file)
    return data


async def blacklist_check(url: str):
    blacklist = await open_blacklist()
    return url in blacklist["blacklist"]


async def parse_phistank(url: str, phishtank_data):
    url_netloc = await url_splitter(url)
    url_netloc = url_netloc.netloc

    for phish in phishtank_data:
        parsed_phish = await url_splitter(phish["url"])
        netloc = parsed_phish.netloc

        if url_netloc == netloc:
            log.info("Found")
            return True
    return False
