import requests
from bs4 import BeautifulSoup, Tag


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

def extract_job(listing: Tag) -> dict:
    job_title = listing.find("span", class_="new-listing__header__title__text")
    if not job_title:
        return None
    title_text = job_title.text
    
    company_name = listing.find("p", class_="new-listing__company-name")
    if not company_name:
        return None
    company_text = company_name.text
    
    location_name = listing.find("p", class_="new-listing__company-headquarters")
    location_status = location_name.text if location_name else "Not specified"
    
    link_element = listing.find("a", class_="listing-link--unlocked")
    job_url = link_element["href"]
    full_url = f"https://weworkremotely.com{job_url}"
    
    extracted_job = {
        "title": title_text.strip(),
        "company": company_text.strip(),
        "location": location_status.strip(),
        "link": full_url.strip()
    }
    return extracted_job
        

if __name__ == "__main__":
    html, status = fetch_page("https://weworkremotely.com/categories/remote-design-jobs")
    print("Status:", status)
    print("HTML length:", len(html))
    
    listings = parse_listings(html)
    print("Listings found:", len(listings))
    
    for listing in listings:
        job = extract_job(listing)
        if not job:
            continue
        print(job)
            
            
    


    