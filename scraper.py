import requests
from bs4 import BeautifulSoup


def fetch_page(url:str) -> tuple:
    """Fetches the HTML content of a page. Returns a tuple with the raw HTML text and the HTTP status code."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text, response.status_code

if __name__ == "__main__":
    html, status = fetch_page("https://weworkremotely.com/categories/remote-design-jobs")
    print("Status:", status)
    print("HTML length:", len(html))


    