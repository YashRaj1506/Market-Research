import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def url_addition(self, key: str, value: str):
        try:
            self.client.sadd(key, value)
            return True
        except Exception as e:
            print(f"[!] Error adding URL to Redis: {e}")
            return False

    def url_deletion(self, key: str, value: str):
        try:
            self.client.srem(key, value)
            return True
        except Exception as e:
            print(f"[!] Error removing URL from Redis: {e}")
            return False

    def url_check(self, key: str, value: str) -> bool:
        try:
            return self.client.sismember(key, value)
        except Exception as e:
            print(f"[!] Error checking URL in Redis: {e}")
            return False

    def url_retrieval(self, key: str):
        try:
            return self.client.spop(key)
        except Exception as e:
            print(f"[!] Error retrieving URL from Redis: {e}")
            return None

    def url_count(self, key: str) -> int:
        try:
            return self.client.scard(key)
        except Exception as e:
            print(f"[!] Error counting URLs in Redis: {e}")
            return 0

    def bulk_url_addition(self, key: str, values: list):
        try:
            self.client.sadd(key, *values)
            return True
        except Exception as e:
            print(f"[!] Error adding multiple URLs to Redis: {e}")
            return False

    def connectivity_test(self) -> bool:
        try:
            return self.client.ping()
        except Exception as e:
            print(f"[!] Error connecting to Redis: {e}")
            return False

    def connectivity_close(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"[!] Error closing Redis connection: {e}")


class URLManager:
    PENDING = "scraper:urls:pending"
    SEEN = "scraper:urls:seen"
    FAILED = "scraper:urls:failed"

    def __init__(self):
        self.redis = RedisClient()
        if not self.redis.connectivity_test():
            raise ConnectionError("Cannot connect to Redis server")
        print("[+] Connected to Redis")

    def add_url(self, url: str):
        """Add URL to pending queue if not seen before"""
        if not self.redis.url_check(self.SEEN, url):
            self.redis.url_addition(self.PENDING, url)
            self.redis.url_addition(self.SEEN, url)
            return True
        return False

    def add_bulk_urls(self, urls: list):
        """Add multiple URLs, filtering out already seen ones"""
        unseen = [u for u in urls if not self.redis.url_check(self.SEEN, u)]
        if unseen:
            self.redis.bulk_url_addition(self.PENDING, unseen)
            self.redis.bulk_url_addition(self.SEEN, unseen)
            print(f"[+] Added {len(unseen)} new URLs")
        return len(unseen)

    def get_next_url(self):
        """Get next URL from pending queue"""
        return self.redis.url_retrieval(self.PENDING)

    def mark_failed(self, url: str):
        """Mark URL as failed"""
        self.redis.url_addition(self.FAILED, url)

    def pending_count(self):
        """Count URLs in pending queue"""
        return self.redis.url_count(self.PENDING)

    def seen_count(self):
        """Count total URLs seen"""
        return self.redis.url_count(self.SEEN)

    def failed_count(self):
        """Count failed URLs"""
        return self.redis.url_count(self.FAILED)

    def close(self):
        """Close Redis connection"""
        self.redis.connectivity_close()


if __name__ == "__main__":
    manager = URLManager()

    print("\n[Testing URL Manager]")
    manager.add_url("https://example.com")
    manager.add_url("https://example.com")

    manager.add_bulk_urls([
        "https://google.com",
        "https://github.com",
        "https://google.com"
    ])

    print(f"Pending: {manager.pending_count()}")
    print(f"Seen: {manager.seen_count()}")

    url = manager.get_next_url()
    print(f"Next URL: {url}")
    print(f"Pending after pop: {manager.pending_count()}")

    manager.close()
