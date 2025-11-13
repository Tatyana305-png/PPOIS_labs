from typing import List

class CompressionUtility:
    def __init__(self):
        self.compression_level = 6
        self.supported_formats = ['zip', 'tar', 'gz']

    def compress_files(self, files: List[str], archive_name: str) -> bool:
        """Сжатие файлов"""
        try:
            print(f"Сжатие файлов {files} в архив {archive_name}")
            return True
        except Exception:
            return False

    def extract_files(self, archive_name: str, extract_path: str) -> bool:
        """Извлечение файлов из архива"""
        try:
            print(f"Извлечение архива {archive_name} в {extract_path}")
            return True
        except Exception:
            return False