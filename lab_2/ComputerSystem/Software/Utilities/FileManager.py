from typing import List

class FileManager:
    def __init__(self):
        self.current_directory = "/"
        self.file_system = None
        self.search_engine = None

    def list_files(self, directory: str = None) -> List[str]:
        """Список файлов в директории"""
        dir_path = directory or self.current_directory
        return ["file1.txt", "file2.doc", "file3.pdf"]

    def create_directory(self, name: str):
        """Создание директории"""
        return f"Создана директория: {name}"

    def delete_file(self, filename: str):
        """Удаление файла"""
        return f"Удален файл: {filename}"