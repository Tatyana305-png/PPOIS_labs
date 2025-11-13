class SystemCleaner:
    def __init__(self):
        self.temp_files = []
        self.cache_directories = []
        self.log_files = []

    def scan_system(self):
        """Сканирование системы на ненужные файлы"""
        self.temp_files = ["/tmp/file1.tmp", "/tmp/file2.tmp"]
        self.cache_directories = ["/cache/browser", "/cache/System"]
        return len(self.temp_files) + len(self.cache_directories)

    def clean_system(self):
        """Очистка системы"""
        cleaned = len(self.temp_files) + len(self.cache_directories)
        self.temp_files.clear()
        self.cache_directories.clear()
        return cleaned