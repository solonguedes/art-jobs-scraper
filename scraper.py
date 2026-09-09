import requests
from bs4 import BeautifulSoup


def fetch_page(url:str) -> tuple:
    """Fetches the HTML content of a page. Returns a tuple with the raw HTML text and the HTTP status code."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text, response.status_code


def parse_listings (html: str) -> list:
    """Parses the HTML and returns a list of job listing elements found on the page."""
    soup = BeautifulSoup(html,"html.parser")
    listings = soup.find_all("li", class_="new-listing-container")
    return listings


if __name__ == "__main__":
    html, status = fetch_page("https://weworkremotely.com/categories/remote-design-jobs")
    print("Status:", status)
    print("HTML length:", len(html))
    
    listings = parse_listings(html)
    print("Listings found:", len(listings))
    
    for listing in listings:
        title_element = listing.find("span", class_="new-listing__header__title__text")
        if not title_element:
            print("- (no title found)")
            continue
    
        print("-", title_element.text)
            
            
    


    