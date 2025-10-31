from typing import List, Optional
from models.player_models import PlayerState, Equalizer, PlaybackQueue
from models.audio_models import Song


class PlaybackController:
    def __init__(self):
        self.state = PlayerState()
        self.queue = PlaybackQueue()

    def play(self, song: Song) -> bool:
        self.state.current_song = song
        self.state.is_playing = True
        return True

    def pause(self) -> bool:
        self.state.is_playing = False
        return True

    def resume(self) -> bool:
        self.state.is_playing = True
        return True

    def stop(self) -> bool:
        self.state.is_playing = False
        self.state.current_time = 0
        return True

    def next_track(self) -> bool:
        if self.queue.songs:
            self.queue.current_index = (self.queue.current_index + 1) % len(self.queue.songs)
            self.state.current_song = self.queue.songs[self.queue.current_index]
            return True
        return False

    def previous_track(self) -> bool:
        if self.queue.songs:
            self.queue.current_index = (self.queue.current_index - 1) % len(self.queue.songs)
            self.state.current_song = self.queue.songs[self.queue.current_index]
            return True
        return False

    def seek(self, position: float) -> bool:
        self.state.current_time = position
        return True

    def set_volume(self, volume: int) -> bool:
        self.state.volume = max(0, min(100, volume))
        return True

    def set_repeat_mode(self, mode: str) -> bool:
        self.state.repeat_mode = mode
        return True

    def toggle_shuffle(self) -> bool:
        self.state.shuffle = not self.state.shuffle
        return True


class QueueManager:
    def add_to_queue(self, song: Song) -> bool:
        self.queue.songs.append(song)
        return True

    def remove_from_queue(self, song: Song) -> bool:
        if song in self.queue.songs:
            self.queue.songs.remove(song)
            return True
        return False

    def clear_queue(self) -> bool:
        self.queue.songs.clear()
        return True

    def move_in_queue(self, old_index: int, new_index: int) -> bool:
        if 0 <= old_index < len(self.queue.songs) and 0 <= new_index < len(self.queue.songs):
            song = self.queue.songs.pop(old_index)
            self.queue.songs.insert(new_index, song)
            return True
        return False

    def save_queue_as_playlist(self, name: str) -> bool:
        return True


class EqualizerController:
    def __init__(self):
        self.equalizer = Equalizer()

    def set_preset(self, preset_name: str) -> bool:
        if preset_name in self.equalizer.presets:
            self.equalizer.bands = self.equalizer.presets[preset_name]
            return True
        return False

    def adjust_band(self, band: int, value: float) -> bool:
        if 0 <= band < len(self.equalizer.bands):
            self.equalizer.bands[band] = value
            return True
        return False

    def reset_equalizer(self) -> bool:
        self.equalizer.bands = [0] * 10
        return True

    def save_preset(self, name: str) -> bool:
        self.equalizer.presets[name] = self.equalizer.bands.copy()
        return True


class AudioDeviceManager:
    def get_available_devices(self) -> List:
        return []

    def set_output_device(self, device) -> bool:
        return True

    def configure_device_settings(self, device, settings: dict) -> bool:
        return True

    def test_audio_device(self, device) -> bool:
        return True