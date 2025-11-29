from datetime import datetime
from typing import Dict
from .MusicLibrary import MusicLibrary

class LibraryScanner:
    def __init__(self, library: MusicLibrary):
        self.library = library
        self.supported_formats = ["mp3", "wav", "flac", "aac"]
        self.scan_progress = 0
        self.last_scan = None

    def scan_library(self) -> bool:
        """Запускает сканирование библиотеки"""
        self.scan_progress = 0
        # Симуляция сканирования
        self.scan_progress = 100
        self.last_scan = datetime.now()
        return True

    def is_format_supported(self, file_extension: str) -> bool:
        """Проверяет поддержку формата файла"""
        return file_extension.lower() in self.supported_formats

    def get_supported_formats_info(self) -> Dict:
        """Возвращает информацию о поддерживаемых форматах"""
        return {
            'total_formats': len(self.supported_formats),
            'formats': self.supported_formats,
            'lossless_formats': [fmt for fmt in self.supported_formats if fmt in ['wav', 'flac']]
        }

    def reset_scan(self) -> None:
        """Сбрасывает состояние сканирования"""
        self.scan_progress = 0
        self.last_scan = None