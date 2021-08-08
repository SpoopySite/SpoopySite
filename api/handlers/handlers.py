from urllib.parse import ParseResult

import bitly
import google
import youtube


def handlers(parsed: ParseResult):
    youtube_check = False
    bitly_warning = False
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

    return {"url": url, "youtube": youtube_check, "bitly": bitly_warning}
