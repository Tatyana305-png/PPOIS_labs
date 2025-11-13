from typing import List, Dict
from .Application import Application

class TextEditor(Application):
    def __init__(self):
        super().__init__("TextEditor", "1.0")
        self.open_files = []
        self.current_file = None
        self.spell_checker = None

    def open_file(self, filename: str):
        self.current_file = filename
        self.open_files.append(filename)
        return f"Открыт файл: {filename}"

    def save_file(self, content: str):
        if self.current_file:
            return f"Файл {self.current_file} сохранен"
        return "Нет открытого файла для сохранения"

    def spell_check(self, text: str) -> List[str]:
        if self.spell_checker:
            return self.spell_checker.check(text)
        return []