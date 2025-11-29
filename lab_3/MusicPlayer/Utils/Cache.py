import time
from typing import Any

class Cache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}

    def get(self, key: str) -> Any:
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None

    def set(self, key: str, value: Any):
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = value
        self.access_times[key] = time.time()

    def _evict_oldest(self):
        oldest_key = min(self.access_times, key=self.access_times.get)
        del self.cache[oldest_key]
        del self.access_times[oldest_key]