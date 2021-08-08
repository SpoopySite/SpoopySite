import urllib.parse
from urllib.parse import ParseResult


def youtube(parsed: ParseResult):
    if "q" in urllib.parse.parse_qs(parsed.query):
        return urllib.parse.parse_qs(parsed.query).get("q")[0], True
