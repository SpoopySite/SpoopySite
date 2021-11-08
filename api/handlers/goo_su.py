from bs4 import BeautifulSoup


def goo_su(text: str):
    soup = BeautifulSoup(text, features="html.parser")
    return soup.find(id="delay-page").attrs.get("data-url", None)
