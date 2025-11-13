from typing import Dict
import urllib.parse


class WebClient:
    def __init__(self):
        self.cookies = {}
        self.user_agent = "WebClient/1.0"
        self.download_manager = None
        self.cache_manager = None

    def get_request(self, url: str) -> str:
        """GET запрос"""
        parsed_url = urllib.parse.urlparse(url)
        return f"GET {parsed_url.path} HTTP/1.1\nHost: {parsed_url.netloc}\nUser-Agent: {self.user_agent}"

    def post_request(self, url: str, data: Dict) -> str:
        """POST запрос"""
        parsed_url = urllib.parse.urlparse(url)
        post_data = "&".join([f"{k}={v}" for k, v in data.items()])
        return f"POST {parsed_url.path} HTTP/1.1\nHost: {parsed_url.netloc}\nContent-Type: application/x-www-form-urlencoded\n\n{post_data}"