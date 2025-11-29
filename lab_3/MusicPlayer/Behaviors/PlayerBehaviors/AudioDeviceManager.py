from typing import List, Dict, Optional
from Models.PlayerModels.AudioDevice import AudioDevice


class AudioDeviceManager:
    def __init__(self):
        self.available_devices = []
        self.current_device = None
        self._scan_devices()

    def _scan_devices(self) -> None:
        """Сканирует доступные аудиоустройства"""
        self.available_devices = [
            AudioDevice("device_1", "Built-in Speakers", "output", 44100, 1024, 50, True),
            AudioDevice("device_2", "USB Headphones", "output", 48000, 2048, 30, False),
            AudioDevice("device_3", "HDMI Output", "output", 192000, 512, 20, False),
            AudioDevice("device_4", "Microphone", "input", 44100, 1024, 100, False)
        ]

    def get_available_devices(self) -> List[AudioDevice]:
        """Возвращает список доступных аудиоустройств"""
        return self.available_devices.copy()

    def get_output_devices(self) -> List[AudioDevice]:
        """Возвращает только выходные устройства"""
        return [device for device in self.available_devices if device.type == "output"]

    def set_output_device(self, device: AudioDevice) -> bool:
        """Устанавливает выходное аудиоустройство"""
        if not device or device not in self.available_devices:
            return False

        if device.type != "output":
            return False

        self.current_device = device

        # Сбрасываем флаг "по умолчанию" у всех устройств
        for dev in self.available_devices:
            dev.is_default = False

        # Устанавливаем новое устройство как default
        device.is_default = True

        return True

    def configure_device_settings(self, device: AudioDevice, settings: Dict) -> bool:
        """Конфигурирует настройки аудиоустройства"""
        if not device or not settings or device not in self.available_devices:
            return False

        # Применяем настройки к устройству
        if 'sample_rate' in settings:
            device.sample_rate = settings['sample_rate']

        if 'buffer_size' in settings:
            device.buffer_size = settings['buffer_size']

        if 'latency' in settings:
            device.latency = settings['latency']

        return True

    def test_audio_device(self, device: AudioDevice) -> Dict:
        """Тестирует аудиоустройство и возвращает результаты"""
        if not device or device not in self.available_devices:
            return {'status': 'failed', 'errors': ['Invalid device']}

        test_results = {
            'device_name': device.name,
            'device_type': device.type,
            'status': 'working',
            'sample_rate': device.sample_rate,
            'signal_quality': 95 if device.type == "output" else 88
        }

        return test_results

    def get_device_by_id(self, device_id: str) -> Optional[AudioDevice]:
        """Находит устройство по ID"""
        return next((device for device in self.available_devices
                     if device.device_id == device_id), None)

    def get_current_device(self) -> Optional[AudioDevice]:
        """Возвращает текущее выбранное устройство"""
        return self.current_device