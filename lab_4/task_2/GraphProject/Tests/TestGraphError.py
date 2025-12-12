import unittest
import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GraphError import GraphError


class TestGraphError(unittest.TestCase):
    """Тесты для класса GraphError"""

    def test_exception_creation(self):
        """Тест создания исключения"""
        error = GraphError("Test error message")
        self.assertEqual(str(error), "Test error message")

    def test_exception_inheritance(self):
        """Тест наследования от Exception"""
        error = GraphError("Test")
        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, GraphError)

    def test_exception_with_different_messages(self):
        """Тест исключений с разными сообщениями"""
        messages = [
            "Vertex not found",
            "Edge already exists",
            "Invalid weight",
            "Graph is empty"
        ]

        for msg in messages:
            error = GraphError(msg)
            self.assertEqual(str(error), msg)

    def test_exception_raising(self):
        """Тест возбуждения исключения"""
        with self.assertRaises(GraphError) as context:
            raise GraphError("Test error")

        self.assertEqual(str(context.exception), "Test error")


if __name__ == '__main__':
    unittest.main()