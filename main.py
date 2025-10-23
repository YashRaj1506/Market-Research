import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def url_addition(self, key: str, value: str):
        """Add a URL to a Redis set"""
        try:
            self.client.sadd(key, value)
            return True
        except Exception as e:
            print(f"[!] Error adding URL to Redis: {e}")
            return False
        
    def url_deletion(self, key: str, value: str):
        """Remove a URL from a Redis set"""
        try:
            self.client.srem(key, value)
            return True
        except Exception as e:
            print(f"[!] Error removing URL from Redis: {e}")
            return False
    
    def url_check(self, key: str, value: str) -> bool:
        """Check if a URL exists in a Redis set"""
        try:
            return self.client.sismember(key, value)
        except Exception as e:
            print(f"[!] Error checking URL in Redis: {e}")
            return False
        
    def url_retrieval(self, key: str):
        """Retrieve a URL from a Redis set"""
        try:
            return self.client.spop(key)
        except Exception as e:
            print(f"[!] Error retrieving URLs from Redis: {e}")
            return None
        
    def url_count(self, key: str) -> int:
        """Get the count of URLs in a Redis set"""
        try:
            return self.client.scard(key)
        except Exception as e:
            print(f"[!] Error counting URLs in Redis: {e}")
            return 0
        
    def bulk_urls_addition(self, key: str, values: list):
        """Add multiple URLs to a Redis set"""
        try:
            self.client.sadd(key, *values)
            return True
        except Exception as e:
            print(f"[!] Error adding multiple URLs to Redis: {e}")
            return False
        
    def connectivity_test(self) -> bool:
        """Test connectivity to Redis server"""
        try:
            return self.client.ping()
        except Exception as e:
            print(f"[!] Error connecting to Redis: {e}")
            return False
    
    def connectivity_close(self):
        """Close the Redis connection"""
        try:
            self.client.close()
        except Exception as e:
            print(f"[!] Error closing Redis connection: {e}")