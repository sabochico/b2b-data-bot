import requests
from bs4 import BeautifulSoup
import csv

def scrape_companies():
    url = "https://find-and-update.company-information.service.gov.uk/search/companies?q=design"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    data = []
    for item in soup.select(".type-search-result"):
        name = item.select_one("a").get_text(strip=True)
        link = "https://find-and-update.company-information.service.gov.uk" + item.select_one("a")["href"]
        status_el = item.select_one(".company-status")
        status = status_el.get_text(strip=True) if status_el else "Unknown"
        data.append({
            "name": name,
            "status": status,
            "url": link
        })
    
    with open("output.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "status", "url"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    scrape_companies()
