from datetime import datetime
from typing import Dict

class PlaylistFolder:
    def __init__(self, folder_id: str, name: str, owner):
        self.folder_id = folder_id
        self.name = name
        self.owner = owner
        self.playlists = []
        self.description = ""
        self.creation_date = datetime.now()

    def add_playlist(self, playlist) -> bool:
        """Добавляет плейлист в папку"""
        if playlist and playlist not in self.playlists:
            self.playlists.append(playlist)
            return True
        return False

    def remove_playlist(self, playlist) -> bool:
        """Удаляет плейлист из папки"""
        if playlist in self.playlists:
            self.playlists.remove(playlist)
            return True
        return False

    def get_playlist_count(self) -> int:
        """Возвращает количество плейлистов в папке"""
        return len(self.playlists)

    def is_empty(self) -> bool:
        """Проверяет, пустая ли папка"""
        return len(self.playlists) == 0

    def get_folder_info(self) -> Dict:
        """Возвращает информацию о папке"""
        return {
            'name': self.name,
            'playlist_count': self.get_playlist_count(),
            'creation_date': self.creation_date.strftime("%Y-%m-%d"),
            'description': self.description
        }