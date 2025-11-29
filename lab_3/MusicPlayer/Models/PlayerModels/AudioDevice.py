class AudioDevice:
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name
        self.type = "output"
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.latency = 0
        self.is_default = False

    def is_output_device(self) -> bool:
        """Проверяет, является ли устройство выходным"""
        return self.type == "output"

    def is_input_device(self) -> bool:
        """Проверяет, является ли устройство входным"""
        return self.type == "input"

    def supports_high_quality(self) -> bool:
        """Проверяет поддержку высокого качества"""
        return self.sample_rate >= 48000

    def get_device_info(self) -> dict:
        """Возвращает информацию об устройстве"""
        return {
            'name': self.name,
            'type': self.type,
            'sample_rate': f"{self.sample_rate} Hz",
            'buffer_size': self.buffer_size,
            'latency': f"{self.latency} ms",
            'is_default': self.is_default
        }

    def set_as_default(self) -> None:
        """Устанавливает устройство как используемое по умолчанию"""
        self.is_default = True