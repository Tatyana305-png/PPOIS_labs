from typing import Dict

class AudioQuality:
    def __init__(self):
        self.bit_depth = 16
        self.dynamic_range = 0
        self.frequency_response = ""
        self.signal_noise_ratio = 0

    def is_high_quality(self) -> bool:
        """Проверяет, является ли качество высоким"""
        return (self.bit_depth >= 24 and
                self.signal_noise_ratio >= 90 and
                self.dynamic_range >= 10)

    def get_quality_rating(self) -> str:
        """Возвращает рейтинг качества"""
        if self.is_high_quality():
            return "High"
        elif self.bit_depth >= 16 and self.signal_noise_ratio >= 80:
            return "Medium"
        else:
            return "Low"

    def set_high_quality_preset(self) -> None:
        """Устанавливает настройки высокого качества"""
        self.bit_depth = 24
        self.dynamic_range = 12
        self.signal_noise_ratio = 96
        self.frequency_response = "20-20000Hz"

    def get_technical_specs(self) -> Dict:
        """Возвращает технические характеристики"""
        return {
            'bit_depth': f"{self.bit_depth}-bit",
            'dynamic_range': f"{self.dynamic_range} dB",
            'signal_noise_ratio': f"{self.signal_noise_ratio} dB",
            'frequency_response': self.frequency_response,
            'quality_rating': self.get_quality_rating()
        }