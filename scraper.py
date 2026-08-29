import requests
from bs4 import BeautifulSoup


def fetch_page(url:str) -> str:
    """Fetches the HTML content of a page. Returns the raw HTML as text"""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


    