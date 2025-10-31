import unittest
import sys
import os


def run_all_tests():
    """Запуск всех тестов музыкального проигрывателя"""
    print("🎵 Запуск тестов музыкального проигрывателя")
    print("=" * 60)

    # Добавляем текущую директорию в путь для импортов
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

    # Находим все тестовые файлы
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')

    # Запускаем тесты
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # Статистика
    print("=" * 60)
    print(f"Тестов запущено: {result.testsRun}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Провалов: {len(result.failures)}")

    if result.wasSuccessful():
        print("🎉 Все тесты прошли успешно! Музыкальный проигрыватель работает корректно.")
        return True
    else:
        print("❌ Есть проблемы в коде, требующие исправления.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)