import requests
from bs4 import BeautifulSoup, Tag
import json


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
    """Parses title, company, location and link"""
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

def get_all_jobs(url:str) -> list:
    """Fetches, parses and extracts all valid job listings from a page. Returns a list of job dictionaries."""
    html, _ = fetch_page(url)
    listings = parse_listings(html)
    final_listing = []
    for listing in listings:
        extraction = extract_job(listing)
        if not extraction:
            continue
        final_listing.append(extraction)
    return final_listing

def save_jobs(jobs:list, file_path:str) -> None:
    """Saves the list of jobs to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(jobs, file, ensure_ascii=False, indent=2)  
                
                
def load_jobs(file_path:str) -> list:
    """Loads the list of jobs from a JSON file. Returns an empty list if the file doesn't exist."""
    try:
        with open(file_path,"r", encoding="utf-8") as file:
            job_list = json.load(file)
            return job_list
    except FileNotFoundError:
        return []
                     
    
        
if __name__ == "__main__":
    jobs = get_all_jobs("https://weworkremotely.com/categories/remote-design-jobs")
    print("Jobs found:", len(jobs))
    
    save_jobs(jobs, "jobs.json")
    print("Jobs saved!")

    reloaded_jobs = load_jobs("jobs.json")
    print("Jobs reloaded:", len(reloaded_jobs))
            
            
    


    