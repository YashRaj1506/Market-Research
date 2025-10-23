from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class JSScraper:
    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=self.options)
        print(f"[+] Browser started for {self.url}")

    def fetch_page(self, wait_time: int = 3):
        try:
            self.driver.get(self.url)
            time.sleep(wait_time)
            print("[+] Page loaded with JS rendering")
            return self.driver.page_source
        except Exception as e:
            print(f"[!] Error: {e}")
            return None

    def get_content(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(strip=True)

    def close(self):
        self.driver.quit()
        print("[+] Browser closed")


if __name__ == "__main__":
    scraper = JSScraper("https://react.dev", headless=True)
    scraper.fetch_page(wait_time=5)
    print(scraper.get_content()[:500])
    scraper.close()
