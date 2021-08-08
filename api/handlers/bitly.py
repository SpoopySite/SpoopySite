import urllib.parse
from urllib.parse import ParseResult


def bitly(parsed: ParseResult):
    if "url" in urllib.parse.parse_qs(parsed.query):
        return urllib.parse.parse_qs(parsed.query).get("url")[0], True
