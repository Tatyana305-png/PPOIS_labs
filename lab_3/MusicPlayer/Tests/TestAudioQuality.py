import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.AudioModels.AudioQuality import AudioQuality


class TestAudioQuality(unittest.TestCase):

    def setUp(self):
        """Настройка тестового окружения перед каждым тестом"""
        self.quality = AudioQuality()

    def test_initial_state(self):
        """Тест начального состояния объекта AudioQuality"""
        self.assertEqual(self.quality.bit_depth, 16)
        self.assertEqual(self.quality.dynamic_range, 0)
        self.assertEqual(self.quality.frequency_response, "")
        self.assertEqual(self.quality.signal_noise_ratio, 0)

    def test_is_high_quality_initial(self):
        """Тест проверки высокого качества для начального состояния"""
        self.assertFalse(self.quality.is_high_quality())

    def test_is_high_quality_high_quality(self):
        """Тест проверки высокого качества для настроек высокого качества"""
        # Устанавливаем параметры высокого качества
        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 95
        self.quality.dynamic_range = 15
        self.assertTrue(self.quality.is_high_quality())

    def test_is_high_quality_edge_cases(self):
        """Тест проверки высокого качества для граничных случаев"""
        # Минимальные значения для высокого качества
        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 90
        self.quality.dynamic_range = 10
        self.assertTrue(self.quality.is_high_quality())

        # Ниже минимальных значений
        self.quality.bit_depth = 23
        self.quality.signal_noise_ratio = 90
        self.quality.dynamic_range = 10
        self.assertFalse(self.quality.is_high_quality())

        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 89
        self.quality.dynamic_range = 10
        self.assertFalse(self.quality.is_high_quality())

        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 90
        self.quality.dynamic_range = 9
        self.assertFalse(self.quality.is_high_quality())

    def test_get_quality_rating_high(self):
        """Тест получения рейтинга 'High' качества"""
        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 95
        self.quality.dynamic_range = 12
        self.assertEqual(self.quality.get_quality_rating(), "High")

    def test_get_quality_rating_medium(self):
        """Тест получения рейтинга 'Medium' качества"""
        # Вариант 1: битовая глубина 16, хорошее SNR
        self.quality.bit_depth = 16
        self.quality.signal_noise_ratio = 85
        self.assertEqual(self.quality.get_quality_rating(), "Medium")

        # Вариант 2: битовая глубина 24, но низкий SNR (не подходит для High)
        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 85
        self.quality.dynamic_range = 5
        self.assertEqual(self.quality.get_quality_rating(), "Medium")

    def test_get_quality_rating_low(self):
        """Тест получения рейтинга 'Low' качества"""
        # Низкая битовая глубина
        self.quality.bit_depth = 8
        self.quality.signal_noise_ratio = 85
        self.assertEqual(self.quality.get_quality_rating(), "Low")

        # Низкий SNR
        self.quality.bit_depth = 16
        self.quality.signal_noise_ratio = 75
        self.assertEqual(self.quality.get_quality_rating(), "Low")

        # Оба параметра низкие
        self.quality.bit_depth = 8
        self.quality.signal_noise_ratio = 70
        self.assertEqual(self.quality.get_quality_rating(), "Low")

    def test_get_quality_rating_edge_cases(self):
        """Тест получения рейтинга качества для граничных значений"""
        # Граница между Medium и High (должен быть Medium, т.к. dynamic_range недостаточен)
        self.quality.bit_depth = 24
        self.quality.signal_noise_ratio = 90
        self.quality.dynamic_range = 9  # Меньше 10
        self.assertEqual(self.quality.get_quality_rating(), "Medium")

        # Граница между Low и Medium
        self.quality.bit_depth = 16
        self.quality.signal_noise_ratio = 80
        self.assertEqual(self.quality.get_quality_rating(), "Medium")

        self.quality.bit_depth = 16
        self.quality.signal_noise_ratio = 79
        self.assertEqual(self.quality.get_quality_rating(), "Low")

        self.quality.bit_depth = 15
        self.quality.signal_noise_ratio = 80
        self.assertEqual(self.quality.get_quality_rating(), "Low")

    def test_set_high_quality_preset(self):
        """Тест установки пресета высокого качества"""
        self.quality.set_high_quality_preset()

        self.assertEqual(self.quality.bit_depth, 24)
        self.assertEqual(self.quality.dynamic_range, 12)
        self.assertEqual(self.quality.signal_noise_ratio, 96)
        self.assertEqual(self.quality.frequency_response, "20-20000Hz")

        # Проверяем, что качество действительно высокое
        self.assertTrue(self.quality.is_high_quality())
        self.assertEqual(self.quality.get_quality_rating(), "High")

    def test_set_high_quality_preset_overwrites_existing(self):
        """Тест, что пресет высокого качества перезаписывает существующие значения"""
        # Устанавливаем какие-то значения
        self.quality.bit_depth = 8
        self.quality.dynamic_range = 5
        self.quality.signal_noise_ratio = 70
        self.quality.frequency_response = "custom"

        # Применяем пресет
        self.quality.set_high_quality_preset()

        # Проверяем, что значения перезаписаны
        self.assertEqual(self.quality.bit_depth, 24)
        self.assertEqual(self.quality.dynamic_range, 12)
        self.assertEqual(self.quality.signal_noise_ratio, 96)
        self.assertEqual(self.quality.frequency_response, "20-20000Hz")

    def test_get_technical_specs_initial(self):
        """Тест получения технических характеристик для начального состояния"""
        specs = self.quality.get_technical_specs()

        expected = {
            'bit_depth': "16-bit",
            'dynamic_range': "0 dB",
            'signal_noise_ratio': "0 dB",
            'frequency_response': "",
            'quality_rating': "Low"
        }
        self.assertEqual(specs, expected)

    def test_get_technical_specs_high_quality(self):
        """Тест получения технических характеристик для высокого качества"""
        self.quality.set_high_quality_preset()
        specs = self.quality.get_technical_specs()

        expected = {
            'bit_depth': "24-bit",
            'dynamic_range': "12 dB",
            'signal_noise_ratio': "96 dB",
            'frequency_response': "20-20000Hz",
            'quality_rating': "High"
        }
        self.assertEqual(specs, expected)

    def test_get_technical_specs_medium_quality(self):
        """Тест получения технических характеристик для среднего качества"""
        self.quality.bit_depth = 16
        self.quality.signal_noise_ratio = 85
        self.quality.dynamic_range = 8
        self.quality.frequency_response = "50-15000Hz"

        specs = self.quality.get_technical_specs()

        expected = {
            'bit_depth': "16-bit",
            'dynamic_range': "8 dB",
            'signal_noise_ratio': "85 dB",
            'frequency_response': "50-15000Hz",
            'quality_rating': "Medium"
        }
        self.assertEqual(specs, expected)

    def test_get_technical_specs_formatting(self):
        """Тест форматирования значений в технических характеристиках"""
        # Проверяем форматирование различных числовых значений
        self.quality.bit_depth = 32
        self.quality.dynamic_range = 15
        self.quality.signal_noise_ratio = 100
        self.quality.frequency_response = "10-40000Hz"

        specs = self.quality.get_technical_specs()

        self.assertEqual(specs['bit_depth'], "32-bit")
        self.assertEqual(specs['dynamic_range'], "15 dB")
        self.assertEqual(specs['signal_noise_ratio'], "100 dB")
        self.assertEqual(specs['frequency_response'], "10-40000Hz")

    def test_quality_rating_consistency(self):
        """Тест согласованности между is_high_quality и get_quality_rating"""
        test_cases = [
            # (bit_depth, snr, dynamic_range, expected_high_quality, expected_rating)
            (24, 95, 12, True, "High"),
            (24, 90, 10, True, "High"),
            (24, 90, 9, False, "Medium"),
            (16, 85, 8, False, "Medium"),
            (16, 75, 5, False, "Low"),
            (8, 70, 3, False, "Low"),
        ]

        for bit_depth, snr, dynamic_range, expected_high, expected_rating in test_cases:
            with self.subTest(bit_depth=bit_depth, snr=snr, dynamic_range=dynamic_range):
                self.quality.bit_depth = bit_depth
                self.quality.signal_noise_ratio = snr
                self.quality.dynamic_range = dynamic_range

                self.assertEqual(self.quality.is_high_quality(), expected_high)
                self.assertEqual(self.quality.get_quality_rating(), expected_rating)

    def test_negative_values(self):
        """Тест обработки отрицательных значений"""
        self.quality.bit_depth = -16
        self.quality.dynamic_range = -5
        self.quality.signal_noise_ratio = -10

        # Проверяем, что методы не падают с отрицательными значениями
        self.assertFalse(self.quality.is_high_quality())
        self.assertEqual(self.quality.get_quality_rating(), "Low")

        specs = self.quality.get_technical_specs()
        self.assertEqual(specs['bit_depth'], "-16-bit")
        self.assertEqual(specs['dynamic_range'], "-5 dB")
        self.assertEqual(specs['signal_noise_ratio'], "-10 dB")

    def test_extreme_values(self):
        """Тест обработки экстремальных значений"""
        # Очень высокие значения
        self.quality.bit_depth = 64
        self.quality.signal_noise_ratio = 200
        self.quality.dynamic_range = 50

        self.assertTrue(self.quality.is_high_quality())
        self.assertEqual(self.quality.get_quality_rating(), "High")

        # Нулевые значения (кроме bit_depth, который по умолчанию 16)
        self.quality.bit_depth = 0
        self.quality.signal_noise_ratio = 0
        self.quality.dynamic_range = 0

        self.assertFalse(self.quality.is_high_quality())
        self.assertEqual(self.quality.get_quality_rating(), "Low")

    def test_frequency_response_does_not_affect_quality(self):
        """Тест, что frequency_response не влияет на оценку качества"""
        # Сохраняем одинаковые параметры качества, меняем только frequency_response
        base_bit_depth = 24
        base_snr = 95
        base_dynamic_range = 12

        test_responses = ["", "20-20000Hz", "custom response", "10-40000Hz"]

        for response in test_responses:
            with self.subTest(frequency_response=response):
                self.quality.bit_depth = base_bit_depth
                self.quality.signal_noise_ratio = base_snr
                self.quality.dynamic_range = base_dynamic_range
                self.quality.frequency_response = response

                # Качество должно оставаться высоким независимо от frequency_response
                self.assertTrue(self.quality.is_high_quality())
                self.assertEqual(self.quality.get_quality_rating(), "High")

    def test_technical_specs_immutability(self):
        """Тест, что возвращаемые технические характеристики не связаны с оригинальным объектом"""
        specs = self.quality.get_technical_specs()
        original_rating = specs['quality_rating']

        # Изменяем качество
        self.quality.set_high_quality_preset()

        # Старая сводка не должна измениться
        self.assertEqual(specs['quality_rating'], original_rating)

        # Новая сводка должна отражать изменения
        new_specs = self.quality.get_technical_specs()
        self.assertEqual(new_specs['quality_rating'], "High")


if __name__ == '__main__':
    unittest.main()