"""
Music Player Application
A comprehensive modular music player with 50 classes, 150+ fields, and 100+ behaviors.
"""

__version__ = "1.0.0"
__author__ = "Music Player Team"
__description__ = "Advanced modular music player application"

# Import key classes for easy access
from .models.audio_models import Song, Podcast, Audiobook
from .models.user_models import User, UserProfile, Subscription
from .models.playlist_models import Playlist, SmartPlaylist
from .models.library_models import MusicLibrary, Artist, Album
from .models.player_models import PlayerState, Equalizer

from .behaviors.audio_behaviors import AudioFileManager, AudioAnalyzer
from .behaviors.playlist_behaviors import PlaylistManager, SmartPlaylistGenerator
from .behaviors.user_behaviors import UserManager, SubscriptionManager
from .behaviors.player_behaviors import PlaybackController, EqualizerController

from .exceptions.audio_exceptions import (
    AudioException,
    InvalidAudioFormatException,
    AudioFileNotFoundException
)
from .exceptions.playlist_exceptions import (
    PlaylistException,
    PlaylistNotFoundException,
    PlaylistEmptyException
)
from .exceptions.user_exceptions import (
    UserException,
    UserNotFoundException,
    SubscriptionExpiredException
)

from .utils.helpers import Logger, Validator, Formatter


# Package-level initialization
def initialize_app():
    """Initialize the music player application"""
    logger = Logger()
    logger.log("Music Player application initialized")
    return True


def get_system_info():
    """Return system information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "modules": [
            "models",
            "behaviors",
            "exceptions",
            "utils"
        ]
    }


# Export main components for easy importing
__all__ = [
    # Models
    'Song', 'Podcast', 'Audiobook',
    'User', 'UserProfile', 'Subscription',
    'Playlist', 'SmartPlaylist',
    'MusicLibrary', 'Artist', 'Album',
    'PlayerState', 'Equalizer',

    # Behaviors
    'AudioFileManager', 'AudioAnalyzer',
    'PlaylistManager', 'SmartPlaylistGenerator',
    'UserManager', 'SubscriptionManager',
    'PlaybackController', 'EqualizerController',

    # Exceptions
    'AudioException', 'InvalidAudioFormatException', 'AudioFileNotFoundException',
    'PlaylistException', 'PlaylistNotFoundException', 'PlaylistEmptyException',
    'UserException', 'UserNotFoundException', 'SubscriptionExpiredException',

    # Utilities
    'Logger', 'Validator', 'Formatter',

    # Functions
    'initialize_app', 'get_system_info'
]

# Initialize when package is imported
app_initialized = initialize_app()