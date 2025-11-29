from .AudioFile import AudioFile
from typing import Dict

class Audiobook(AudioFile):
    def __init__(self, file_path: str, title: str, duration: float, author: str, narrator: str):
        super().__init__(file_path, title, duration)
        self.author = author
        self.narrator = narrator
        self.chapter = 1
        self.total_chapters = 10
        self.publisher = ""
        self.isbn = ""

    def get_progress_percentage(self) -> float:
        """Возвращает процент прослушанного"""
        if self.total_chapters == 0:
            return 0.0
        return (self.chapter / self.total_chapters) * 100

    def move_to_next_chapter(self) -> bool:
        """Переходит к следующей главе"""
        if self.chapter < self.total_chapters:
            self.chapter += 1
            return True
        return False

    def move_to_previous_chapter(self) -> bool:
        """Возвращается к предыдущей главе"""
        if self.chapter > 1:
            self.chapter -= 1
            return True
        return False

    def get_chapter_info(self) -> Dict:
        """Возвращает информацию о текущей главе"""
        return {
            'current_chapter': self.chapter,
            'total_chapters': self.total_chapters,
            'progress': f"{self.get_progress_percentage():.1f}%",
            'author': self.author,
            'narrator': self.narrator
        }

    def is_finished(self) -> bool:
        """Проверяет, завершена ли аудиокнига"""
        return self.chapter >= self.total_chapters

    def set_total_chapters(self, chapters: int) -> None:
        """Устанавливает общее количество глав"""
        if chapters > 0:
            self.total_chapters = chapters