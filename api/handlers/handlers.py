import logging
from urllib.parse import ParseResult
import multidict

from . import bitly, youtube, google, adfly

log = logging.getLogger(__name__)


def handlers(parsed: ParseResult, text: str, headers: multidict.CIMultiDictProxy):
    youtube_check = False
    bitly_warning = False
    adfly_warning = False
    url = None

    if "youtube.com" in parsed.netloc and parsed.path == "/redirect":
        check = youtube.youtube(parsed)
        if check:
            url = check[0]
            youtube_check = True
    elif "google.com" in parsed.netloc and parsed.path == "/url":
        check = google.google(parsed)
        if check:
            url = check
    elif "bitly.com" in parsed.netloc and parsed.path == "/a/warning":
        check = bitly.bitly(parsed)
        if check:
            url = check[0]
            bitly_warning = True
    elif headers.get("x-powered-by") == "adfly" and len(parsed.path) > 0:
        check = adfly.adfly(text)
        if check:
            url = check
            adfly_warning = True

    return {"url": url, "youtube": youtube_check, "bitly": bitly_warning, "adfly": adfly_warning}
