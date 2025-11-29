from typing import Optional

class Equalizer:
    def __init__(self):
        self.bands = [0] * 10
        self.presets = {}
        self.is_enabled = False
        self.preamp = 0

    def set_band(self, band_index: int, value: float) -> bool:
        """Устанавливает значение для полосы эквалайзера"""
        if 0 <= band_index < len(self.bands) and -12 <= value <= 12:
            self.bands[band_index] = value
            return True
        return False

    def get_band_value(self, band_index: int) -> Optional[float]:
        """Возвращает значение полосы эквалайзера"""
        if 0 <= band_index < len(self.bands):
            return self.bands[band_index]
        return None

    def reset_bands(self) -> None:
        """Сбрасывает все полосы эквалайзера к нулю"""
        self.bands = [0] * len(self.bands)

    def apply_preset(self, preset_name: str) -> bool:
        """Применяет сохраненный пресет"""
        if preset_name in self.presets:
            self.bands = self.presets[preset_name].copy()
            return True
        return False

    def save_preset(self, preset_name: str) -> bool:
        """Сохраняет текущие настройки как пресет"""
        if preset_name:
            self.presets[preset_name] = self.bands.copy()
            return True
        return False