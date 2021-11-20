import datetime
import asyncpg


async def insert_into_cache(url: str, result: str, pool: asyncpg.pool.Pool):
    if await check_if_cached(url, pool):
        await update_cache(url, result, pool)
    else:
        async with pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO past_checks (url, data)
            VALUES ($1, $2)
            """, url, result)


async def update_cache(url: str, result: str, pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:
        await conn.execute("""
        UPDATE past_checks
        SET data = $1, created_at = NOW()
        WHERE url = $2
        """, result, url)


async def cached(url: str, pool: asyncpg.pool.Pool):
    if await check_if_cached(url, pool):
        updated_at = await fetch_updated_at(pool, url)
        if (updated_at + datetime.timedelta(hours=1)) > datetime.datetime.now():
            return await fetch_cached_result(url, pool)
        else:
            return False
    return False


async def fetch_cached_result(url: str, pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:
        result = await conn.fetchval("""
        SELECT data
        FROM past_checks
        WHERE url = $1
        """, url)
    return result


async def fetch_updated_at(pool: asyncpg.pool.Pool, url: str):
    async with pool.acquire() as conn:
        updated_at = await conn.fetchval("""
        SELECT created_at
        FROM past_checks
        WHERE url = $1
        """, url)
    return updated_at


async def check_if_cached(url: str, pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:
        check = await conn.fetchval("""
        SELECT EXISTS(
        SELECT 1
        FROM past_checks
        WHERE url = $1
        )
        """, url)
    return check
