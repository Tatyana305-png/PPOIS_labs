from typing import Dict

class AudioMetadata:
    def __init__(self):
        self.id3_tags = {}
        self.artwork = None
        self.copyright = ""
        self.encoder = ""
        self.comments = ""

    def add_id3_tag(self, key: str, value: str) -> None:
        """Добавляет ID3 тег"""
        if key and value:
            self.id3_tags[key] = value

    def get_id3_tag(self, key: str) -> str:
        """Возвращает значение ID3 тега"""
        return self.id3_tags.get(key, "")

    def has_artwork(self) -> bool:
        """Проверяет, есть ли обложка"""
        return self.artwork is not None

    def get_metadata_summary(self) -> Dict:
        """Возвращает сводку метаданных"""
        return {
            'total_id3_tags': len(self.id3_tags),
            'has_artwork': self.has_artwork(),
            'has_copyright': bool(self.copyright),
            'encoder': self.encoder
        }

    def clear_id3_tags(self) -> None:
        """Очищает все ID3 теги"""
        self.id3_tags.clear()