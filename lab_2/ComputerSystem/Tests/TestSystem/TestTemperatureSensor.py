import pytest
import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from System.Cooling import TemperatureSensor, CoolingSystem


class TestTemperatureSensor:

    def test_sensor_initialization(self):
        """Тест инициализации датчика"""
        sensor = TemperatureSensor("CPU")

        assert sensor.location == "CPU"
        assert sensor.current_temp == 25.0

    def test_update_temperature(self):
        """Тест обновления температуры"""
        sensor = TemperatureSensor("Test")

        sensor.update_temperature(35.5)
        assert sensor.current_temp == 35.5

    def test_calibrate_sensor(self):
        """Тест калибровки датчика"""
        sensor = TemperatureSensor("Test")

        sensor.calibrate(-1.5)
        assert sensor.calibration_offset == -1.5

    def test_simulate_temperature_change(self):
        """Тест симуляции изменения температуры"""
        sensor = TemperatureSensor("Test")
        random.seed(42)

        new_temp = sensor.simulate_temperature_change(25.0, 2.0)
        assert sensor.current_temp == new_temp

    def test_get_trend(self):
        """Тест определения тренда"""
        sensor = TemperatureSensor("Test")

        # Просто проверяем что метод существует
        trend = sensor.get_trend()
        assert isinstance(trend, str)

    def test_reset_sensor(self):
        """Тест сброса датчика"""
        sensor = TemperatureSensor("Test")
        sensor.current_temp = 80.0
        sensor.calibration_offset = 2.0

        sensor.reset_sensor()

        assert sensor.current_temp == 25.0

    def test_enable_disable_sensor(self):
        """Тест включения/отключения датчика"""
        sensor = TemperatureSensor("Test")

        sensor.disable()
        assert sensor.is_active == False

        sensor.enable()
        assert sensor.is_active == True

    def test_get_stats(self):
        """Тест получения статистики"""
        sensor = TemperatureSensor("Test")

        stats = sensor.get_stats()
        assert isinstance(stats, dict)

    def test_set_thresholds(self):
        """Тест установки пороговых значений"""
        sensor = TemperatureSensor("Test")

        sensor.set_thresholds(60.0, 85.0)
        assert sensor.warning_threshold == 60.0
        assert sensor.critical_threshold == 85.0

    def test_sensor_integration_with_cooling_system(self):
        """Интеграционный тест"""
        cooling_system = CoolingSystem()
        sensor = TemperatureSensor("CPU")

        cooling_system.temperature_sensors.append(sensor)
        sensor.update_temperature(65.0)

        assert len(cooling_system.temperature_sensors) == 1
        assert cooling_system.temperature_sensors[0].current_temp == 65.0

    def test_temperature_history(self):
        """Тест истории температуры"""
        sensor = TemperatureSensor("Test")

        sensor.update_temperature(30.0)
        sensor.update_temperature(35.0)

        assert len(sensor.temperature_history) == 2
        assert sensor.temperature_history[0][1] == 30.0
        assert sensor.temperature_history[1][1] == 35.0


    def test_sensor_location(self):
        """Тест расположения датчика"""
        sensor = TemperatureSensor("GPU_Fan")
        assert sensor.location == "GPU_Fan"

    def test_multiple_calibrations(self):
        """Тест множественных калибровок"""
        sensor = TemperatureSensor("Test")

        sensor.calibrate(2.0)
        assert sensor.calibration_offset == 2.0

        sensor.calibrate(-1.0)
        assert sensor.calibration_offset == -1.0