from .Playlist import Playlist

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, creator):
        super().__init__(playlist_id, name, creator)
        self.collaborators = []
        self.edit_permissions = "all"
        self.approval_required = False

    def add_collaborator(self, user) -> bool:
        """Добавляет collaborator'а в плейлист"""
        if user and user not in self.collaborators:
            self.collaborators.append(user)
            return True
        return False

    def remove_collaborator(self, user) -> bool:
        """Удаляет collaborator'а из плейлиста"""
        if user in self.collaborators:
            self.collaborators.remove(user)
            return True
        return False

    def can_user_edit(self, user) -> bool:
        """Проверяет, может ли пользователь редактировать плейлист"""
        if user == self.creator:
            return True

        if self.edit_permissions == "all" and user in self.collaborators:
            return True

        if self.edit_permissions == "approved" and user in self.collaborators and not self.approval_required:
            return True

        return False

    def get_collaborator_count(self) -> int:
        """Возвращает количество collaborator'ов"""
        return len(self.collaborators)

    def is_collaborative(self) -> bool:
        """Проверяет, является ли плейлист collaborative"""
        return len(self.collaborators) > 0