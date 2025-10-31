from typing import List, Optional
from datetime import datetime


class PlayerState:
    def __init__(self):
        self.current_song = None
        self.is_playing = False
        self.current_time = 0
        self.volume = 50
        self.repeat_mode = "none"
        self.shuffle = False
        self.playback_speed = 1.0


class Equalizer:
    def __init__(self):
        self.bands = [0] * 10
        self.presets = {}
        self.is_enabled = False
        self.preamp = 0


class AudioDevice:
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name
        self.type = "output"
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.latency = 0
        self.is_default = False


class PlaybackQueue:
    def __init__(self):
        self.songs = []
        self.current_index = 0
        self.history = []
        self.up_next = []
        self.max_history_size = 100


class PlayerSettings:
    def __init__(self):
        self.audio_device = None
        self.volume_normalization = False
        self.gapless_playback = True
        self.crossfade_duration = 0
        self.high_quality_streaming = True
        self.download_quality = "high"