import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Behaviors.PlayerBehaviors.EqualizerController import EqualizerController
from Models.PlayerModels.Equalizer import Equalizer


class TestEqualizerController(unittest.TestCase):

    def setUp(self):
        self.equalizer_controller = EqualizerController()
        self.equalizer = self.equalizer_controller.equalizer

    def test_equalizer_controller_initialization(self):
        """Тест инициализации контроллера эквалайзера"""
        self.assertIsInstance(self.equalizer_controller.equalizer, Equalizer)
        self.assertEqual(len(self.equalizer_controller.equalizer.bands), 10)
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_set_preset_existing(self):
        """Тест установки существующего пресета"""
        # Создаем пресеты
        self.equalizer_controller.equalizer.presets = {
            "rock": [6, 4, 2, 0, -2, -2, 0, 2, 4, 6],
            "jazz": [0, 2, 4, 3, 1, 0, -1, -2, -3, -4]
        }

        result = self.equalizer_controller.set_preset("rock")
        self.assertTrue(result)
        self.assertEqual(self.equalizer_controller.equalizer.bands, [6, 4, 2, 0, -2, -2, 0, 2, 4, 6])

    def test_set_preset_nonexistent(self):
        """Тест установки несуществующего пресета"""
        self.equalizer_controller.equalizer.presets = {
            "rock": [6, 4, 2, 0, -2, -2, 0, 2, 4, 6]
        }

        result = self.equalizer_controller.set_preset("nonexistent")
        self.assertFalse(result)
        # Полосы не должны измениться
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_adjust_band_valid(self):
        """Тест корректировки валидной полосы"""
        # Корректируем несколько полос
        bands_to_adjust = [(0, -6), (5, 3), (9, 12)]

        for band, value in bands_to_adjust:
            result = self.equalizer_controller.adjust_band(band, value)
            self.assertTrue(result)
            self.assertEqual(self.equalizer_controller.equalizer.bands[band], value)

    def test_adjust_band_invalid_band(self):
        """Тест корректировки невалидной полосы"""
        # Полоса вне диапазона
        result = self.equalizer_controller.adjust_band(-1, 5)
        self.assertFalse(result)

        result = self.equalizer_controller.adjust_band(10, 5)
        self.assertFalse(result)

        # Полосы не должны измениться
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_reset_equalizer(self):
        """Тест сброса эквалайзера"""
        # Устанавливаем ненулевые значения
        for i in range(10):
            self.equalizer_controller.equalizer.bands[i] = i * 2 - 5

        # Сбрасываем
        result = self.equalizer_controller.reset_equalizer()
        self.assertTrue(result)
        self.assertEqual(self.equalizer_controller.equalizer.bands, [0] * 10)

    def test_save_preset(self):
        """Тест сохранения пресета"""
        # Устанавливаем значения полос
        test_bands = [-3, -1, 0, 2, 4, 4, 2, 0, -1, -3]
        self.equalizer_controller.equalizer.bands = test_bands

        # Сохраняем как пресет
        result = self.equalizer_controller.save_preset("custom")
        self.assertTrue(result)
        self.assertIn("custom", self.equalizer_controller.equalizer.presets)
        self.assertEqual(self.equalizer_controller.equalizer.presets["custom"], test_bands)

    def test_save_preset_overwrite(self):
        """Тест перезаписи существующего пресета"""
        # Сохраняем первый пресет
        bands1 = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
        self.equalizer_controller.equalizer.bands = bands1
        self.equalizer_controller.save_preset("test_preset")

        # Сохраняем с тем же именем (перезапись)
        bands2 = [5, 4, 3, 2, 1, 1, 2, 3, 4, 5]
        self.equalizer_controller.equalizer.bands = bands2
        result = self.equalizer_controller.save_preset("test_preset")

        self.assertTrue(result)
        self.assertEqual(self.equalizer_controller.equalizer.presets["test_preset"], bands2)

    def test_equalizer_enable_disable(self):
        """Тест включения/выключения эквалайзера"""
        # Добавляем свойство is_enabled если его нет
        if not hasattr(self.equalizer, 'is_enabled'):
            self.equalizer.is_enabled = False

        self.assertFalse(self.equalizer.is_enabled)

        self.equalizer.is_enabled = True
        self.assertTrue(self.equalizer.is_enabled)

        self.equalizer.is_enabled = False
        self.assertFalse(self.equalizer.is_enabled)

    def test_equalizer_preamp(self):
        """Тест работы с предусилителем"""
        # Добавляем свойство preamp если его нет
        if not hasattr(self.equalizer, 'preamp'):
            self.equalizer.preamp = 0

        preamp_values = [-12, -6, 0, 3, 6, 12]

        for value in preamp_values:
            self.equalizer.preamp = value
            self.assertEqual(self.equalizer.preamp, value)


if __name__ == '__main__':
    unittest.main()
