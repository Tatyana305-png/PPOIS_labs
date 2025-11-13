import datetime

class WebTab:
    def __init__(self, url: str):
        self.url = url
        self.history = []
        self.cookies = {}
        self.load_time = datetime.datetime.now()

    def navigate(self, new_url: str):
        self.history.append(self.url)
        self.url = new_url

    def go_back(self):
        if self.history:
            self.url = self.history.pop()