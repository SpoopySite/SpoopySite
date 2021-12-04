import aiohttp.client
from urllib.parse import ParseResult

from pbincli.format import Paste

from api.helpers import validate_url
from app.useragents import get_random_user_agent


async def textbin(parsed: ParseResult, session: aiohttp.client.ClientSession):
    headers = {
        "user-agent": get_random_user_agent(),
        "X-Requested-With": "JSONHttpRequest"
    }
    async with session.get(f"https://textbin.xyz?{parsed.query}", headers=headers) as resp:
        result: dict = await resp.json()

    paste = Paste()
    version = result['v'] if 'v' in result else 1
    paste.setVersion(version)
    paste.setHash(parsed.fragment)
    paste.loadJSON(result)
    paste.decrypt()
    text = paste.getText()
    text = text.decode('utf-8')

    urls = []
    for url in text.split():
        if validate_url(url):
            urls.append(url)

    if len(urls) == 1:
        return urls[0]
    return False
