from .Application import Application
from .WebTab import WebTab

class WebBrowser(Application):
    def __init__(self):
        super().__init__("WebBrowser", "2.0")
        self.open_tabs = []
        self.current_tab = None
        self.download_manager = None
        self.cookie_manager = None

    def open_tab(self, url: str):
        tab = WebTab(url)
        self.open_tabs.append(tab)
        self.current_tab = tab
        return tab

    def close_tab(self, tab):
        if tab in self.open_tabs:
            self.open_tabs.remove(tab)
            if self.current_tab == tab:
                self.current_tab = self.open_tabs[0] if self.open_tabs else None