import requests
from bs4 import BeautifulSoup

class HTMLScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.session = requests.Session()
        self.session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
})

    def fetch_html(self):
        response = self.session.get(self.url, timeout=10)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')
        print(f"[+] HTML fetched from {self.url}")

    def get_content(self):
        if self.soup is None:
            self.fetch_html()
        return self.soup.get_text(strip=True)


if __name__ == "__main__":
    scraper = HTMLScraper("https://example.com")
    scraper.fetch_html()
    print(scraper.get_content()[:500])