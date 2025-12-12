import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Запуск всех тестов"""
    test_loader = unittest.TestLoader()

    test_suites = [
        test_loader.loadTestsFromName('Tests.TestGraphError'),
        test_loader.loadTestsFromName('Tests.TestVertexWrapper'),
        test_loader.loadTestsFromName('Tests.TestEdgeNode'),
        test_loader.loadTestsFromName('Tests.TestEdgeWrapper'),

        test_loader.loadTestsFromName('Tests.TestBaseIterator'),
        test_loader.loadTestsFromName('Tests.TestGraphIterator'),
        test_loader.loadTestsFromName('Tests.TestReverseGraphIterator'),
        test_loader.loadTestsFromName('Tests.TestConstGraphIterator'),
        test_loader.loadTestsFromName('Tests.TestBidirectionalIterator'),
        test_loader.loadTestsFromName('Tests.TestIteratorUtils'),

        test_loader.loadTestsFromName('Tests.TestWirthGraphOperations'),
        test_loader.loadTestsFromName('Tests.TestWirthIteratorsProvider'),
        test_loader.loadTestsFromName('Tests.TestWirthGraphComparator'),
        test_loader.loadTestsFromName('Tests.TestWirthAdjacencyListGraph'),

        test_loader.loadTestsFromName('Tests.TestIntegration'),
    ]

    all_tests = unittest.TestSuite(test_suites)

    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(all_tests)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("Запуск всех unit-тестов для графа с модифицированной структурой Вирта")
    print("=" * 70)

    success = run_all_tests()

    print("\n" + "=" * 70)
    if success:
        print(" Все тесты пройдены успешно!")
    else:
        print(" Некоторые тесты не пройдены")

    sys.exit(0 if success else 1)