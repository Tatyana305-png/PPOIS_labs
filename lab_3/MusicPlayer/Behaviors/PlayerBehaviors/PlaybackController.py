from Models.PlayerModels.PlayerState import PlayerState
from Models.PlayerModels.PlaybackQueue import PlaybackQueue
from Models.AudioModels.Song import Song


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