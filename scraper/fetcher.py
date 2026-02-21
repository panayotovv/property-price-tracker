import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Request failed:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("div", class_="panel rel shadow offer")