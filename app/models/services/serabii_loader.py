import bs4
import requests

from config.default import URL_BASE


def get_soup(url: str) -> bs4.BeautifulSoup:
    url = f"{URL_BASE}{url}"
    data = requests.get(url)
    return bs4.BeautifulSoup(data.text, 'html.parser')
