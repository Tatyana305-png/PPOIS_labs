import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from VertexWrapper import VertexWrapper


class TestVertexWrapper(unittest.TestCase):
    """Тесты для класса VertexWrapper"""

    def test_vertex_creation(self):
        """Тест создания вершины"""
        vertex = VertexWrapper("A", 0)
        self.assertEqual(vertex.value, "A")
        self.assertEqual(vertex.index, 0)
        self.assertIsNone(vertex.first_edge)

    def test_vertex_creation_with_different_types(self):
        """Тест создания вершин с разными типами значений"""
        test_cases = [
            (1, 0),  # int
            ("vertex1", 1),  # str
            (3.14, 2),  # float
            ((1, 2), 3),  # tuple
            (None, 4),  # None
        ]

        for value, index in test_cases:
            vertex = VertexWrapper(value, index)
            self.assertEqual(vertex.value, value)
            self.assertEqual(vertex.index, index)

    def test_vertex_equality(self):
        """Тест сравнения вершин"""
        vertex1 = VertexWrapper("A", 0)
        vertex2 = VertexWrapper("A", 0)
        vertex3 = VertexWrapper("B", 0)
        vertex4 = VertexWrapper("A", 1)

        # Равенство по значению и индексу
        self.assertEqual(vertex1, vertex2)

        # Неравенство по значению
        self.assertNotEqual(vertex1, vertex3)

        # Неравенство по индексу
        self.assertNotEqual(vertex1, vertex4)

        # Сравнение с неверным типом
        self.assertNotEqual(vertex1, "not a vertex")
        self.assertNotEqual(vertex1, None)

    def test_vertex_hash(self):
        """Тест хэширования вершин"""
        vertex1 = VertexWrapper("A", 0)
        vertex2 = VertexWrapper("A", 0)
        vertex3 = VertexWrapper("B", 0)

        # Одинаковые вершины должны иметь одинаковый хэш
        self.assertEqual(hash(vertex1), hash(vertex2))

        # Разные вершины должны иметь разные хэши
        self.assertNotEqual(hash(vertex1), hash(vertex3))

    def test_vertex_repr(self):
        """Тест строкового представления"""
        vertex = VertexWrapper("TestVertex", 5)
        expected_repr = "Vertex(TestVertex)"
        self.assertEqual(repr(vertex), expected_repr)

    def test_vertex_with_first_edge(self):
        """Тест вершины с установленным first_edge"""
        vertex = VertexWrapper("A", 0)

        # Создаем mock edge
        class MockEdge:
            def __repr__(self):
                return "MockEdge"

        edge = MockEdge()
        vertex.first_edge = edge

        self.assertIs(vertex.first_edge, edge)
        self.assertEqual(repr(vertex.first_edge), "MockEdge")


if __name__ == '__main__':
    unittest.main()