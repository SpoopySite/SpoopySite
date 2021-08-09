import base64
import logging

from bs4 import BeautifulSoup
from bs4.element import Tag

log = logging.getLogger(__name__)


def script_to_list(script: Tag):
    script_list = []
    if not script.string:
        return
    for line in script.string.split("\n"):
        stripped = line.strip()
        if len(stripped) > 0:
            script_list.append(stripped)
    return script_list


def ysmm_finder(script_list: [str]):
    for line in script_list:
        line: str
        if line.startswith("var ysmm"):
            ysmm = line.split(" ")[-1]
            ysmm = ysmm.replace("\'", "").replace(";", "")
            return ysmm


# Sourced from https://github.com/jkehler/unshortenit/blob/master/unshortenit/modules/adfly.py
def ysmm_to_url(ysmm: str):
    left = ""
    right = ""
    for c in [ysmm[i:i + 2] for i in range(0, len(ysmm), 2)]:
        left += c[0]
        right = c[1] + right
    encoded_uri = list(left + right)
    numbers = ((i, n) for i, n in enumerate(encoded_uri) if str.isdigit(n))
    for first, second in zip(numbers, numbers):
        xor = int(first[1]) ^ int(second[1])
        if xor < 10:
            encoded_uri[first[0]] = str(xor)
    decoded_uri = base64.b64decode("".join(encoded_uri).encode())[16:-16].decode()
    return decoded_uri


def adfly(text: str):
    soup = BeautifulSoup(text, features="html.parser")
    scripts = soup.findAll("script")
    ysmm = ""
    for script in scripts:
        script_list = script_to_list(script)
        if not script_list:
            continue
        check = ysmm_finder(script_list)
        if check:
            ysmm = check
            break

    if not ysmm:
        return

    ysmm_string = ysmm_to_url(ysmm)
    return ysmm_string
