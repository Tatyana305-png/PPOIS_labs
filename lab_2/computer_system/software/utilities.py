import zipfile
import tempfile
from typing import List


class FileManager:
    def __init__(self):
        self.current_directory = "/"
        self.file_system = None
        self.search_engine = None

    def list_files(self, directory: str = None) -> List[str]:
        """Список файлов в директории"""
        dir_path = directory or self.current_directory
        # Имитация списка файлов
        return ["file1.txt", "file2.doc", "file3.pdf"]

    def create_directory(self, name: str):
        """Создание директории"""
        return f"Создана директория: {name}"

    def delete_file(self, filename: str):
        """Удаление файла"""
        return f"Удален файл: {filename}"


class CompressionUtility:
    def __init__(self):
        self.compression_level = 6
        self.supported_formats = ['zip', 'tar', 'gz']

    def compress_files(self, files: List[str], archive_name: str) -> bool:
        """Сжатие файлов"""
        try:
            # Имитация сжатия
            print(f"Сжатие файлов {files} в архив {archive_name}")
            return True
        except Exception:
            return False

    def extract_files(self, archive_name: str, extract_path: str) -> bool:
        """Извлечение файлов из архива"""
        try:
            # Имитация извлечения
            print(f"Извлечение архива {archive_name} в {extract_path}")
            return True
        except Exception:
            return False


class SystemCleaner:
    def __init__(self):
        self.temp_files = []
        self.cache_directories = []
        self.log_files = []

    def scan_system(self):
        """Сканирование системы на ненужные файлы"""
        # Имитация сканирования
        self.temp_files = ["/tmp/file1.tmp", "/tmp/file2.tmp"]
        self.cache_directories = ["/cache/browser", "/cache/system"]
        return len(self.temp_files) + len(self.cache_directories)

    def clean_system(self):
        """Очистка системы"""
        cleaned = len(self.temp_files) + len(self.cache_directories)
        self.temp_files.clear()
        self.cache_directories.clear()
        return cleaned