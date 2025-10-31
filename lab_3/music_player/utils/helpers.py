import time
from typing import Any, List
from datetime import datetime


class Logger:
    def __init__(self):
        self.log_file = "music_player.log"

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        print(log_entry)
        with open(self.log_file, "a") as f:
            f.write(log_entry)


class Validator:
    @staticmethod
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email

    @staticmethod
    def validate_audio_file(file_path: str) -> bool:
        return file_path.endswith(('.mp3', '.wav', '.flac', '.aac'))

    @staticmethod
    def validate_playlist_name(name: str) -> bool:
        return len(name) >= 1 and len(name) <= 100


class Formatter:
    @staticmethod
    def format_duration(seconds: float) -> str:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    @staticmethod
    def format_file_size(bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"


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