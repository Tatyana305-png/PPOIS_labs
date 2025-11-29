from Models.PlayerModels.Equalizer import Equalizer

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