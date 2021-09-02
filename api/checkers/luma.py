import datetime
import logging
import os.path
import pickle

import aiohttp

from app.config import Config

config = Config.from_file()
log = logging.getLogger(__name__)


async def update(session: aiohttp.client.ClientSession) -> dict:
    log.info("Updating 🐟🐠")
    async with session.get("https://http://api.phish.surf:5000/gimme-domains") as resp:
        json_content: dict = await resp.json()
    return {"fetch_time": datetime.datetime.now(), "list": json_content}


def save(json_content: dict):
    with open("luma.pickle", "wb") as f:
        pickle.dump(json_content, f, pickle.HIGHEST_PROTOCOL)


def load() -> dict:
    with open("luma.pickle", "rb") as f:
        return pickle.load(f)


async def check(url: str, session: aiohttp.client.ClientSession):
    log.info(f"🐟🐠 checking: {url}")
    if os.path.isfile("luma.pickle"):
        json = load()
        if (json.get("fetch_time") + datetime.timedelta(minutes=5)) > datetime.datetime.now():
            return url in json.get("list")
        else:
            json = await update(session)
            save(json)
            return url in json.get("list")
    else:
        json = await update(session)
        save(json)
        return url in json.get("list")
