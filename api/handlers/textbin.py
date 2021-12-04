from urllib.parse import ParseResult

from pbincli.api import PrivateBin
from pbincli.format import Paste

from api.helpers import validate_url


def textbin(parsed: ParseResult):
    api_client = PrivateBin({"server": "https://textbin.xyz",
                             'proxy': None,
                             'short_api': None,
                             'short_url': None,
                             'short_user': None,
                             'short_pass': None,
                             'short_token': None,
                             'no_check_certificate': False,
                             'no_insecure_warning': False})

    paste = Paste()
    result = api_client.get(parsed.query)
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
