import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def brave_search(query: str, api_key: str, count: int = 10):
    """
    Perform a Brave Search query and return the top result URLs.

    :param query: Search keyword or question
    :param api_key: Your Brave Search API key
    :param count: Number of results to return (default 10)
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    
    params = {
        "q": query,
        "count": count
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Extract URLs from search results
    urls = [item["url"] for item in data.get("web", {}).get("results", [])]
    return urls

if __name__ == "__main__":
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    query = "latest AI news"
    
    results = brave_search(query, BRAVE_API_KEY)
    print("Top 10 URLs:")
    for i, url in enumerate(results, start=1):
        print(f"{i}. {url}")
