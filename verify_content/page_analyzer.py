import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class PageAnalyzer:
    def __init__(self, url: str):
        self.url = url
        self.html_content = None

    def fetch_initial_html(self):
        """Fetch raw HTML without executing JavaScript"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            self.html_content = response.text
            return True
        except Exception as e:
            print(f"[!] Error fetching page: {e}")
            return False

    def requires_js_rendering(self):
        """Determine if page needs JavaScript rendering"""
        if not self.html_content:
            if not self.fetch_initial_html():
                return None

        soup = BeautifulSoup(self.html_content, 'html.parser')

        js_indicators = {
            'react': False,
            'vue': False,
            'angular': False,
            'heavy_scripts': False,
            'spa_patterns': False,
            'minimal_content': False
        }

        scripts = soup.find_all('script')
        script_count = len(scripts)

        for script in scripts:
            script_text = script.get_text().lower() if script.string else ''
            src = script.get('src', '').lower()

            if 'react' in src or 'react' in script_text:
                js_indicators['react'] = True
            if 'vue' in src or 'vue' in script_text:
                js_indicators['vue'] = True
            if 'angular' in src or 'angular' in script_text:
                js_indicators['angular'] = True

        if script_count > 10:
            js_indicators['heavy_scripts'] = True

        root_div = soup.find('div', id=['root', 'app', '__next'])
        if root_div and len(root_div.get_text(strip=True)) < 100:
            js_indicators['spa_patterns'] = True

        body = soup.find('body')
        if body:
            text_content = body.get_text(strip=True)
            if len(text_content) < 200 and script_count > 3:
                js_indicators['minimal_content'] = True

        needs_js = any([
            js_indicators['react'],
            js_indicators['vue'],
            js_indicators['angular'],
            js_indicators['spa_patterns'],
            js_indicators['minimal_content']
        ])

        return {
            'needs_js': needs_js,
            'indicators': js_indicators,
            'script_count': script_count,
            'recommendation': 'js_scraper' if needs_js else 'html_scraper'
        }

if __name__ == "__main__":
    test_urls = [
        # "https://example.com",
        "https://react.dev",
        # "https://news.ycombinator.com"
    ]

    analyzer = PageAnalyzer(url)

    js_analysis = analyzer.requires_js_rendering()
    if js_analysis:
        print(f"\n[JS Analysis]")
        print(f"Needs JavaScript: {js_analysis['needs_js']}")
        print(f"Recommendation: Use {js_analysis['recommendation']}")
        print(f"Script Count: {js_analysis['script_count']}")
        print(f"Indicators: {js_analysis['indicators']}")
