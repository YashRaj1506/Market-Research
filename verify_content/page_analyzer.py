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
        try:
            if not self.html_content:
                if not self.fetch_initial_html():
                    return None

            soup = BeautifulSoup(self.html_content, 'html.parser')

            js_indicators = {
                'empty_spa_root': False,
                'minimal_content': False,
                'has_noscript_content': False,
                'has_semantic_content': False
            }

            # Check for empty SPA root divs
            try:
                root_div = soup.find('div', id=['root', 'app', '__next'])
                if root_div:
                    root_text = root_div.get_text(strip=True)
                    if len(root_text) < 100:
                        js_indicators['empty_spa_root'] = True
            except Exception as e:
                print(f"[!] Error checking SPA root: {e}")

            # Check for noscript tags with content
            try:
                noscript_tags = soup.find_all('noscript')
                noscript_content = ''.join([tag.get_text(strip=True) for tag in noscript_tags])
                if len(noscript_content) > 100:
                    js_indicators['has_noscript_content'] = True
            except Exception as e:
                print(f"[!] Error checking noscript tags: {e}")

            # Check for semantic HTML content
            try:
                semantic_tags = soup.find_all(['p', 'article', 'section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                semantic_text = ''.join([tag.get_text(strip=True) for tag in semantic_tags])
                if len(semantic_text) > 300:
                    js_indicators['has_semantic_content'] = True
            except Exception as e:
                print(f"[!] Error checking semantic content: {e}")

            # Check body content
            try:
                body = soup.find('body')
                if body:
                    body_text = body.get_text(strip=True)
                    if len(body_text) < 300:
                        js_indicators['minimal_content'] = True
            except Exception as e:
                print(f"[!] Error checking body content: {e}")

            # Decision logic: needs JS if it looks like SPA with no real content
            needs_js = (
                (js_indicators['empty_spa_root'] or js_indicators['minimal_content'])
                and not js_indicators['has_semantic_content']
                and not js_indicators['has_noscript_content']
            )

            return {
                'needs_js': needs_js,
                'indicators': js_indicators,
                'recommendation': 'js_scraper' if needs_js else 'html_scraper'
            }
        except Exception as e:
            print(f"[!] Error analyzing page: {e}")
            # Default to html_scraper if analysis fails
            return {
                'needs_js': False,
                'indicators': {},
                'recommendation': 'html_scraper'
            }

if __name__ == "__main__":
    url = "https://www.iea.org/reports/global-ev-outlook-2024/trends-in-electric-cars"

    analyzer = PageAnalyzer(url)

    try:
        js_analysis = analyzer.requires_js_rendering()
        if js_analysis:
            print(f"\n[JS Analysis]")
            print(f"Needs JavaScript: {js_analysis['needs_js']}")
            print(f"Recommendation: Use {js_analysis['recommendation']}")
            print(f"Script Count: {js_analysis['script_count']}")
            print(f"Indicators: {js_analysis['indicators']}")
    except Exception as e:
        print(f"[!] Error during analysis: {e}")
