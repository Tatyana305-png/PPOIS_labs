class Monitor:
    def __init__(self, resolution: tuple, refresh_rate: int):
        self.resolution = resolution
        self.refresh_rate = refresh_rate
        self.current_resolution = resolution
        self.brightness = 50
        self.graphics_card = None
        self.monitor_type = "IPS"
        self.screen_size = 27
        self.hdr_support = True

    def set_resolution(self, width: int, height: int):
        """Установка разрешения"""
        self.current_resolution = (width, height)
        print(f"Разрешение установлено: {width}x{height}")

    def adjust_brightness(self, level: int):
        """Регулировка яркости"""
        self.brightness = max(0, min(100, level))
        print(f"Яркость установлена: {self.brightness}%")

    def set_refresh_rate(self, rate: int):
        """Установка частоты обновления"""
        self.refresh_rate = rate
        print(f"Частота обновления установлена: {rate}Hz")

    def enable_hdr(self):
        """Включение HDR"""
        if self.hdr_support:
            print("HDR включен")
        else:
            print("Монитор не поддерживает HDR")

    def disable_hdr(self):
        """Выключение HDR"""
        print("HDR выключен")

    def get_monitor_info(self) -> dict:
        """Получение информации о мониторе"""
        return {
            'resolution': self.resolution,
            'current_resolution': self.current_resolution,
            'refresh_rate': self.refresh_rate,
            'brightness': self.brightness,
            'monitor_type': self.monitor_type,
            'screen_size': self.screen_size,
            'hdr_support': self.hdr_support
        }

    def calibrate_colors(self):
        """Калибровка цветов"""
        print("Выполняется калибровка цветов монитора...")

    def power_save_mode(self, enable: bool):
        """Режим энергосбережения"""
        mode = "включен" if enable else "выключен"
        print(f"Режим энергосбережения {mode}")