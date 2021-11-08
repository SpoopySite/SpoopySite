from bs4 import BeautifulSoup


def goo_su(text: str):
    soup = BeautifulSoup(text, features="html.parser")
    delay_page = soup.find(id="delay-page")
    if delay_page:
        return delay_page.attrs.get("data-url", None)
