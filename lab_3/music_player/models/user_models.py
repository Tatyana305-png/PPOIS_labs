from datetime import datetime, timedelta
from typing import List, Dict
from exceptions.user_exceptions import SubscriptionExpiredException


class User:
    def __init__(self, user_id: str, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.registration_date = datetime.now()
        self.last_login = datetime.now()
        self.is_active = True
        self.preferences = {}
        self.favorite_genres = []
        self.language = "en"
        self.theme = "dark"


class UserProfile:
    def __init__(self, user: User):
        self.user = user
        self.first_name = ""
        self.last_name = ""
        self.birth_date = None
        self.country = ""
        self.city = ""
        self.bio = ""
        self.avatar_url = ""
        self.social_links = {}


class UserPreferences:
    def __init__(self):
        self.audio_quality = "high"
        self.auto_play = True
        self.crossfade_duration = 0
        self.equalizer_preset = "flat"
        self.replay_gain = False
        self.volume_limit = 100
        self.keyboard_shortcuts = {}


class Subscription:
    def __init__(self, user: User):
        self.user = user
        self.plan_type = "free"
        self.start_date = datetime.now()
        self.end_date = datetime.now() + timedelta(days=30)
        self.is_active = True
        self.payment_method = ""
        self.auto_renew = True

    def check_validity(self):
        if datetime.now() > self.end_date:
            raise SubscriptionExpiredException("Subscription has expired")


class ListeningHistory:
    def __init__(self, user: User):
        self.user = user
        self.entries = []
        self.total_listening_time = 0
        self.most_played_songs = []


class UserStatistics:
    def __init__(self, user: User):
        self.user = user
        self.songs_played = 0
        self.artists_discovered = 0
        self.playlists_created = 0
        self.favorites_count = 0
        self.weekly_listening_time = 0