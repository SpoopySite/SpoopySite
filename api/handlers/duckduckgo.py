import logging
import urllib.parse
from urllib.parse import ParseResult

import aiohttp

log = logging.getLogger(__name__)


async def duckduckgo(parsed: ParseResult, session: aiohttp.client.ClientSession):
    if "q" in urllib.parse.parse_qs(parsed.query):
        ddg_query = urllib.parse.parse_qs(parsed.query).get("q")[0]
        if ddg_query.startswith("! site:"):
            async with session.get("https://api.duckduckgo.com/", params={"q": ddg_query, "format": "json", "no_redirect": 1}) as resp:
                json_content: dict = await resp.json(content_type="application/x-javascript")
            return json_content["Redirect"]
        else:
            log.warning(f"DDG: Unknown query string: {ddg_query}")
            return {"error": "Unknown query string"}
