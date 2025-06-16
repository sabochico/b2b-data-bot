import requests
from bs4 import BeautifulSoup
import csv

def scrape_companies():
    url = "https://find-and-update.company-information.service.gov.uk/search/companies?q=design"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    data = []
    results = soup.select(".type-search-result")
    if not results:
        print("No results found — check selectors or site blocking")
    for item in results:
        a_tag = item.select_one("a")
        if not a_tag:
            continue
        name = a_tag.get_text(strip=True)
        link = "https://find-and-update.company-information.service.gov.uk" + a_tag["href"]
        status_el = item.select_one(".company-status")
        status = status_el.get_text(strip=True) if status_el else "Unknown"
        data.append({
            "name": name,
            "status": status,
            "url": link
        })

    if not data:
        print("Scraper ran, but no data collected.")
    else:
        print(f"Scraped {len(data)} companies")

    with open("output.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "status", "url"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    scrape_companies()
