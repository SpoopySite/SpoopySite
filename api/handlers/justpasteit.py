from bs4 import BeautifulSoup


def justpasteit(text: str):
    soup = BeautifulSoup(text, features="html.parser")
    href_block = soup.find(class_="redirectLinkBlock")
    return href_block.a.get("href")
