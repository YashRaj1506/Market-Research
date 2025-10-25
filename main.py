from Scraper.html_scraper import HTMLScraper
from Scraper.js_scraper import JSScraper
from verify_content.page_analyzer import PageAnalyzer
from Scraper.url_manager import URLManager, RedisClient
from browser_search import brave_search
from web_query import generate_search_queries
import logging
import os

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

        try:
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

            with open("scraped_contents.txt", "a", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                f.write(content)
                f.write("\n\n" + "="*80 + "\n\n")
        except Exception as e:
            logger.error(f"[!] Error scraping {url}: {e}")
            self.url_manager.mark_failed(url)
            return None
        
        

        # print(f"[+] Scraped content from {url} (length: {len(content)})")
        logger.info(f"[+] Scraped content from {url} (length: {len(content)})")
        return content

    def start_scraping(self, urls: list):
        for url in urls:
            self.scrape_url(url)

    def close(self):
        self.url_manager.close()

if __name__ == "__main__":

    brave_api_key = os.getenv("BRAVE_API_KEY")

    main_scraper = MainScraper()

    url_to_fetch = []

    # search_queries = generate_search_queries("latest trends in electric vehicles 2024")
    # for query in search_queries:
    #     urls = brave_search(query, brave_api_key)
    #     url_to_fetch.extend(urls)

    # main_scraper.url_manager.add_bulk_urls(url_to_fetch)

    # print(url_to_fetch)

    dummy_urls = ['https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-cars', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-the-electric-vehicle-industry', 'https://www.coxautoinc.com/market-insights/q4-2024-ev-sales/', 'https://about.bnef.com/electric-vehicle-outlook/', 'https://www.iea.org/reports/global-ev-outlook-2024', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-cars', 'https://www.virta.global/global-electric-vehicle-market', 'https://www.iea.org/reports/global-ev-outlook-2024', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-the-electric-vehicle-industry', 'https://www.coxautoinc.com/market-insights/q4-2024-ev-sales/#:~:text=Sales in 2024 (1,301,411) were,of total new-vehicle sales.', 'https://about.bnef.com/insights/clean-transport/electric-vehicle-outlook/', 'https://www.iea.org/reports/global-ev-outlook-2025', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-cars', 'https://ev-volumes.com/', 'https://theicct.org/publication/us-passenger-ev-sales-and-model-availability-through-2024-apr25/', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-cars', 'https://about.bnef.com/insights/clean-transport/electric-vehicle-outlook/', 'https://www.recurrentauto.com/research/states-leading-the-ev-revolution', 'https://www.recurrentauto.com/research/ev-adoption-us', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-the-electric-vehicle-industry', 'https://afdc.energy.gov/fuels/electricity-infrastructure-trends', 'https://www.iea.org/reports/global-ev-outlook-2024/outlook-for-electric-vehicle-charging-infrastructure', 'https://driveelectric.gov/news/', 'https://theicct.org/publication/us-charging-infrastructure-deployment-through-2024-apr25/', 'https://afdc.energy.gov/files/u/publication/electric_vehicle_charging_infrastructure_trends_first_quarter_2024.pdf', 'https://www.autobodynews.com/news/ces-2024-unveils-future-of-transportation-autonomous-electric-high-tech-mobility-innovations', 'https://firstignite.com/exploring-the-latest-autonomous-vehicles-advancements-in-2024/', 'https://www.bain.com/insights/electric-and-autonomous-vehicles-the-future-is-now/', 'https://www.gdsonline.tech/autonomous-vehicle-trends-whats-next/', 'https://www.bloomberg.com/news/newsletters/2024-02-27/autonomous-electric-vehicles-will-guzzle-power-instead-of-gas', 'https://www.greencars.com/greencars-101/the-future-of-ev-batteries', 'https://sodiumbatteryhub.com/2024/11/23/whats-new-in-ev-battery-technology-for-2024/', 'https://www.leadintelligent.com/en/top-global-ev-trends-for-2025-and-beyond/', 'https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-vehicle-batteries', 'https://www.altenergymag.com/story/2024/08/the-5-most-impactful-battery-innovations-in-2024/42754/', 'https://www.e-motec.net/top-5-ev-innovations-in-fleet-technology-in-2024/', 'https://prismecs.com/blog/driving-towards-sustainability-the-rise-of-electric-vehicles', 'https://bydpampanga.com/articles/the-future-of-electric-vehicles-9-latest-trends-and-innovations', 'https://www.greenmountainenergy.com/en/blog/electric-vehicle/electric-vehicle-technology-innovations-2025', 'https://statzon.com/insights/electric-mobility-trends-2024', 'https://www.statista.com/statistics/541390/global-sales-of-plug-in-electric-vehicle-manufacturers/', 'https://theicct.org/publication/us-passenger-ev-sales-and-model-availability-through-2024-apr25/', 'https://www.virta.global/global-electric-vehicle-market', 'https://www.fortunebusinessinsights.com/industry-reports/electric-vehicle-market-101678', 'https://www.eia.gov/todayinenergy/detail.php?id=62924', 'https://www.iea.org/reports/global-ev-outlook-2024', 'https://www.gridserve.com/how-government-incentives-shape-ev-adoption-worldwide/', 'https://www.forbes.com/sites/energyinnovation/2025/02/09/electric-vehicles-set-records-smart-policy-can-ensure-america-leads-global-markets/', 'https://www.iea.org/reports/global-ev-outlook-2021/policies-to-promote-electric-vehicle-deployment', 'https://iea.blob.core.windows.net/assets/a9e3544b-0b12-4e15-b407-65f5c8ce1b5f/GlobalEVOutlook2024.pdf']

    main_scraper.start_scraping(dummy_urls)

    # main_scraper.scrape_url(test_url)
    # main_scraper.close()