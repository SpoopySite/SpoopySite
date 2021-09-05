import datetime
import json
import logging
import re
from urllib.parse import urlparse

import aiohttp
import asyncpg
import tld
import validators.url
from bs4 import BeautifulSoup

from app.config import Config
from app.useragents import get_random_user_agent

config = Config.from_file()
log = logging.getLogger(__name__)


def refresh_header_finder(text: str):
    soup = BeautifulSoup(text, features="html.parser")
    if not soup.head:
        return
    meta = soup.head.find_all("meta")
    http_equiv = [x.attrs.get("http-equiv") for x in meta]
    if any(http_equiv):
        for meta_tag in meta:
            if meta_tag.attrs.get("http-equiv") == "refresh":
                content = meta_tag.attrs.get("content")
                if "URL=" in content:
                    return re.search("URL(.*)", content).group(1)[1:]


async def redirect_gatherer(url: str, session: aiohttp.client.ClientSession):
    async with session.get(url, headers={"User-Agent": get_random_user_agent()}) as resp:
        history = [str(x.url) for x in resp.history]
        history.append(str(resp.url))
        return history


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


async def update_db_hsts(pool: asyncpg.pool.Pool, url: str, status: str):
    async with pool.acquire() as conn:
        await conn.execute("""
        UPDATE hsts
        SET status = $1,
        updated_at = NOW()
        WHERE url = $2 
        """, status, url)


async def update_hsts(session: aiohttp.client.ClientSession, url, pool: asyncpg.pool.Pool):
    log.info("Inserting HSTS status for: {}".format(url))
    async with session.get("https://hstspreload.org/api/v2/status",
                           params={"domain": url}) as resp:
        json_data = await resp.json()
        status = json_data.get("status")
        await insert_hsts(pool, url, status)
    return status


async def update_internal_hsts(session: aiohttp.client.ClientSession, url, pool: asyncpg.pool.Pool):
    log.info("Updating HSTS status for: {}".format(url))
    async with session.get("https://hstspreload.org/api/v2/status",
                           params={"domain": url}) as resp:
        json_data = await resp.json()
        status = json_data.get("status")
        await update_db_hsts(pool, url, status)
    return status


async def hsts_check(url: str, session: aiohttp.client.ClientSession, pool: asyncpg.pool.Pool):
    if await check_hsts(pool, url):
        updated_at = await fetch_updated_at(pool, url)
        if (updated_at + datetime.timedelta(days=7)) > datetime.datetime.now():
            return await fetch_hsts(pool, url)
        else:
            return await update_internal_hsts(session, url, pool)
    else:
        return await update_hsts(session, url, pool)


async def open_blacklist():
    with open("api/blacklist.json", "r") as file:
        data = json.load(file)
    return data


async def blacklist_check(url: str):
    blacklist = await open_blacklist()
    url = tld.get_fld(url, fix_protocol=True)
    if url in blacklist["blacklist"]:
        return blacklist["blacklist"][url]
    else:
        return False


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


async def check_webrisk_internal(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        check = await conn.fetchval("""
        SELECT EXISTS(
        SELECT 1
        FROM web_risk
        WHERE url = $1
        )
        """, url)
    return check


async def check_webrisk_expire(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        check = await conn.fetchval("""
        SELECT expire_time
        FROM web_risk
        WHERE url = $1
        """, url)
    return check


async def insert_blank_webrisk(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO web_risk (url, expire_time)
        VALUES ($1, $2)
        """, url, datetime.datetime.now() + datetime.timedelta(minutes=20))


async def insert_webrisk(pool: asyncpg.pool.Pool, url: str, expire_time: datetime,
                         social_engineering: bool = False, malware: bool = False):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO web_risk (url, social_engineering, malware, expire_time) 
        VALUES ($1, $2, $3, $4) 
        """, url, social_engineering, malware, expire_time)


async def update_webrisk(url: str, session: aiohttp.client.ClientSession, pool: asyncpg.pool.Pool):
    log.info(f"Fetching webrisk: {url}")

    params = [
        ("uri", url),
        ("key", config.webrisk_key),
        ("threatTypes", "MALWARE"),
        ("threatTypes", "SOCIAL_ENGINEERING"),
        ("threatTypes", "UNWANTED_SOFTWARE")
    ]
    async with session.get("https://webrisk.googleapis.com/v1/uris:search", params=params) as resp:
        json_content: dict = await resp.json()

    if json_content.get("error"):
        log.info("Error with Google API")
        log.error(json_content)

    if json_content == {}:
        await insert_blank_webrisk(pool, url)
    else:
        parsed_time = datetime.datetime.strptime(json_content["threat"]["expireTime"][:-4], "%Y-%m-%dT%H:%M:%S.%f")
        if json_content["threat"]["threatTypes"] == ["SOCIAL_ENGINEERING"]:
            await insert_webrisk(pool=pool, url=url, social_engineering=True, expire_time=parsed_time)
        elif json_content["threat"]["threatTypes"] == ["MALWARE"]:
            await insert_webrisk(pool=pool, url=url, malware=True, expire_time=parsed_time)
        else:
            await insert_webrisk(pool=pool, url=url, social_engineering=True, malware=True, expire_time=parsed_time)


async def fetch_webrisk(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        data = await conn.fetch("""
        SELECT social_engineering, malware
        FROM web_risk
        WHERE url = $1
        """, url)
    return dict(data[0])


async def delete_webrisk(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        await conn.execute("""
        DELETE FROM web_risk
        WHERE url = $1
        """, url)


async def webrisk_check(url: str, session: aiohttp.client.ClientSession, pool: asyncpg.pool.Pool):
    if await check_webrisk_internal(pool, url):
        expire_time = await check_webrisk_expire(pool, url)
        if expire_time < datetime.datetime.now():
            await delete_webrisk(pool, url)
            await update_webrisk(url, session, pool)
            return await fetch_webrisk(pool, url)
        else:
            return await fetch_webrisk(pool, url)
    else:
        await update_webrisk(url, session, pool)
        return await fetch_webrisk(pool, url)
