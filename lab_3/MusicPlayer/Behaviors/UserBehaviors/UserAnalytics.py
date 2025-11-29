from typing import Dict, List
from Models.UserModels.User import User


class UserAnalytics:
    """Аналитика прослушивания пользователя"""

    def get_listening_stats(self, user: User, period: str = "all") -> Dict:
        """Возвращает статистику прослушивания"""
        if not user:
            raise ValueError("User is required")

        if not hasattr(user, 'listening_history'):
            return self._get_empty_stats()

        history = user.listening_history.entries

        if period != "all":
            history = self._filter_by_period(history, period)

        total_time = sum(entry.duration for entry in history if hasattr(entry, 'duration'))
        songs_played = len(history)
        artists_listened = len(set(entry.artist for entry in history if hasattr(entry, 'artist')))

        return {
            'total_time': total_time,
            'songs_played': songs_played,
            'artists_listened': artists_listened,
            'period': period
        }

    def get_favorite_genres(self, user: User) -> List[str]:
        """Возвращает любимые жанры пользователя"""
        if not user or not hasattr(user, 'listening_history'):
            return []

        genre_counter = {}
        for entry in user.listening_history.entries:
            if hasattr(entry, 'genre') and entry.genre:
                genre_counter[entry.genre] = genre_counter.get(entry.genre, 0) + 1

        sorted_genres = sorted(genre_counter.items(), key=lambda x: x[1], reverse=True)
        return [genre for genre, count in sorted_genres[:5]]  # Топ-5 жанров

    def generate_listening_report(self, user: User) -> str:
        """Генерирует текстовый отчет о прослушивании"""
        if not user:
            return "No user data"

        stats = self.get_listening_stats(user)
        favorite_genres = self.get_favorite_genres(user)

        report = f"Listening Report for {user.username}\n"
        report += f"Total listening time: {stats['total_time']} seconds\n"
        report += f"Songs played: {stats['songs_played']}\n"
        report += f"Artists discovered: {stats['artists_listened']}\n"

        if favorite_genres:
            report += f"Favorite genres: {', '.join(favorite_genres)}\n"
        else:
            report += "No genre data available\n"

        return report

    def _filter_by_period(self, history: List, period: str) -> List:
        """Фильтрует историю по периоду (заглушка для демонстрации)"""
        return history

    def _get_empty_stats(self) -> Dict:
        """Возвращает пустую статистику"""
        return {
            'total_time': 0,
            'songs_played': 0,
            'artists_listened': 0,
            'period': 'all'
        }