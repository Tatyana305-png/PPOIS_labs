import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from models.audio_models import Song, Podcast, Audiobook
from models.user_models import User, UserProfile, Subscription
from models.playlist_models import Playlist, SmartPlaylist
from models.library_models import MusicLibrary, Artist, Album
from models.player_models import PlayerState, Equalizer, PlaybackQueue

from behaviors.audio_behaviors import AudioFileManager, AudioAnalyzer
from behaviors.playlist_behaviors import PlaylistManager, SmartPlaylistGenerator
from behaviors.user_behaviors import UserManager, SubscriptionManager
from behaviors.player_behaviors import PlaybackController, EqualizerController

from exceptions.audio_exceptions import InvalidAudioFormatException, AudioFileNotFoundException
from exceptions.playlist_exceptions import PlaylistEmptyException, DuplicateSongException
from exceptions.user_exceptions import UserNotFoundException, SubscriptionExpiredException

from utils.helpers import Logger, Validator, Formatter


def demonstrate_associations():
    """Демонстрация 30 ассоциаций классов"""
    logger = Logger()

    # 1. User имеет UserProfile
    user = User("user1", "john_doe", "john@example.com")
    profile = UserProfile(user)

    # 2. User имеет Subscription
    subscription = Subscription(user)

    # 3. Playlist имеет creator (User)
    playlist = Playlist("pl1", "My Playlist", user)

    # 4. Song в Playlist
    song = Song("/music/song1.mp3", "Beautiful Song", 240, "Artist1", "Album1")
    playlist.add_song(song)

    # 5. Album имеет Artist
    artist = Artist("art1", "Famous Artist")
    album = Album("alb1", "Great Album", artist)

    # 6. MusicLibrary имеет owner (User)
    library = MusicLibrary(user)

    # 7. PlayerState имеет current_song (Song)
    player_state = PlayerState()
    player_state.current_song = song

    # 8. PlaybackQueue имеет songs (List[Song])
    queue = PlaybackQueue()
    queue.songs = [song]

    # 9. Equalizer имеет presets (Dict)
    equalizer = Equalizer()

    # 10. SmartPlaylist имеет criteria (Dict)
    smart_pl = SmartPlaylist("spl1", "Smart Mix", user, {"genre": "rock"})

    # 11. AudioFileManager работает с Song
    audio_manager = AudioFileManager()
    loaded_song = audio_manager.load_audio_file("/music/song1.mp3")

    # 12. AudioAnalyzer анализирует Song
    analyzer = AudioAnalyzer()
    bpm = analyzer.analyze_bpm(song)

    # 13. PlaylistManager создает Playlist
    playlist_manager = PlaylistManager()
    new_playlist = playlist_manager.create_playlist("New Playlist", user)

    # 14. SmartPlaylistGenerator создает SmartPlaylist
    smart_generator = SmartPlaylistGenerator()
    rock_playlist = smart_generator.generate_by_genre("rock", library, 50)

    # 15. UserManager управляет User
    user_manager = UserManager()
    registered_user = user_manager.register_user("new_user", "new@example.com", "password")

    # 16. SubscriptionManager управляет Subscription
    sub_manager = SubscriptionManager()
    new_subscription = sub_manager.create_subscription(user, "premium")

    # 17. PlaybackController управляет PlayerState
    playback_controller = PlaybackController()
    playback_controller.play(song)

    # 18. EqualizerController управляет Equalizer
    eq_controller = EqualizerController()
    eq_controller.set_preset("rock")

    # 19. Logger логирует действия с различными объектами
    logger.log(f"User {user.username} created playlist {playlist.name}")

    # 20. Validator проверяет различные объекты
    is_valid = Validator.validate_email(user.email)

    # 21. Formatter форматирует данные из различных объектов
    duration_str = Formatter.format_duration(song.duration)

    # 22. CollaborativePlaylist имеет collaborators (List[User])
    from models.playlist_models import CollaborativePlaylist
    collab_playlist = CollaborativePlaylist("cpl1", "Collaborative", user)
    collab_playlist.collaborators.append(registered_user)

    # 23. ListeningHistory связан с User
    from models.user_models import ListeningHistory
    history = ListeningHistory(user)

    # 24. UserStatistics связан с User
    from models.user_models import UserStatistics
    stats = UserStatistics(user)

    # 25. PlaylistStatistics связан с Playlist
    from models.playlist_models import PlaylistStatistics
    pl_stats = PlaylistStatistics(playlist)

    # 26. LibraryScanner работает с MusicLibrary
    from models.library_models import LibraryScanner
    scanner = LibraryScanner(library)

    # 27. AudioDevice в PlayerSettings
    from models.player_models import AudioDevice, PlayerSettings
    device = AudioDevice("dev1", "Speakers")
    player_settings = PlayerSettings()
    player_settings.audio_device = device

    # 28. Podcast наследуется от AudioFile
    podcast = Podcast("/podcasts/ep1.mp3", "Tech Talk", 3600, "Host1", 1)

    # 29. Audiobook наследуется от AudioFile
    audiobook = Audiobook("/books/book1.mp3", "Great Novel", 7200, "Author1", "Narrator1")

    # 30. PlaylistFolder содержит Playlist
    from models.playlist_models import PlaylistFolder
    folder = PlaylistFolder("f1", "My Folders", user)
    folder.playlists.append(playlist)

    logger.log("All associations demonstrated successfully")


def demonstrate_exceptions():
    """Демонстрация обработки исключений"""
    logger = Logger()

    try:
        # 1. InvalidAudioFormatException
        song = Song("/music/song.xyz", "Test", 120, "Artist", "Album")
        song.format = "xyz"
        song.validate_format()
    except InvalidAudioFormatException as e:
        logger.log(f"Audio format error: {e}", "ERROR")

    try:
        # 2. AudioFileNotFoundException
        audio_manager = AudioFileManager()
        audio_manager.load_audio_file("/nonexistent/file.mp3")
    except AudioFileNotFoundException as e:
        logger.log(f"Audio file not found: {e}", "ERROR")

    try:
        # 3. PlaylistEmptyException
        playlist = Playlist("pl1", "Empty Playlist", None)
        playlist.remove_song(Song("/test.mp3", "Test", 120, "A", "B"))
    except PlaylistEmptyException as e:
        logger.log(f"Playlist error: {e}", "ERROR")

    try:
        # 4. DuplicateSongException
        playlist = Playlist("pl2", "Test Playlist", None)
        song = Song("/test.mp3", "Test", 120, "A", "B")
        playlist.add_song(song)
        playlist.add_song(song)  # Дублирование
    except DuplicateSongException as e:
        logger.log(f"Duplicate song: {e}", "ERROR")

    try:
        # 5. UserNotFoundException
        user_manager = UserManager()
        # Симуляция ситуации, когда пользователь не найден
        raise UserNotFoundException("User not found in database")
    except UserNotFoundException as e:
        logger.log(f"User error: {e}", "ERROR")

    try:
        # 6. SubscriptionExpiredException
        user = User("user1", "test", "test@example.com")
        subscription = Subscription(user)
        subscription.end_date = datetime(2020, 1, 1)  # Прошедшая дата
        subscription.check_validity()
    except SubscriptionExpiredException as e:
        logger.log(f"Subscription error: {e}", "ERROR")


if __name__ == "__main__":
    print("Музыкальный проигрыватель - Демонстрация")
    print("=" * 50)

    demonstrate_associations()
    demonstrate_exceptions()

    print("\nПрограмма успешно завершена!")