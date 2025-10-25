from Scraper.html_scraper import HTMLScraper
from Scraper.js_scraper import JSScraper
from verify_content.page_analyzer import PageAnalyzer
from Scraper.url_manager import URLManager, RedisClient
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger =logging.getLogger(__name__)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

#File handler
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

class MainScraper:
    def __init__(self):
        self.url_manager = URLManager()

    def scrape_url(self, url: str):
        analyzer = PageAnalyzer(url)
        analysis = analyzer.requires_js_rendering()

        if analysis and analysis['recommendation'] == 'js_scraper':
            scraper = JSScraper(url)
            scraper.fetch_page()
            content = scraper.get_content()
            print(content)
            scraper.close()
        else:
            scraper = HTMLScraper(url)
            scraper.fetch_html()
            content = scraper.get_content()
            print(content)

        # print(f"[+] Scraped content from {url} (length: {len(content)})")
        logger.info(f"[+] Scraped content from {url} (length: {len(content)})")
        return content

    def close(self):
        self.url_manager.close()

if __name__ == "__main__":

    main_scraper = MainScraper()
    test_url = "https://scale.com/enterprise/agentic-solutions"
    # test_url = "https://example.com"
    main_scraper.scrape_url(test_url)
    main_scraper.close()