import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode


class TestEdgeNode(unittest.TestCase):
    """Тесты для класса EdgeNode"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.vertex1 = VertexWrapper("A", 0)
        self.vertex2 = VertexWrapper("B", 1)

    def test_edge_node_creation(self):
        """Тест создания узла ребра"""
        edge = EdgeNode(self.vertex1, self.vertex2, 2.5)

        self.assertEqual(edge.vertex, self.vertex1)
        self.assertEqual(edge.other_vertex, self.vertex2)
        self.assertEqual(edge.weight, 2.5)
        self.assertIsNone(edge.next)
        self.assertIsNone(edge.twin)


    def test_edge_node_with_next(self):
        """Тест узла ребра со ссылкой next"""
        edge1 = EdgeNode(self.vertex1, self.vertex2, 1.0)
        edge2 = EdgeNode(self.vertex1, VertexWrapper("C", 2), 2.0)

        edge1.next = edge2

        self.assertIs(edge1.next, edge2)
        self.assertIsNone(edge2.next)

    def test_edge_node_with_twin(self):
        """Тест узла ребра со ссылкой twin"""
        edge1 = EdgeNode(self.vertex1, self.vertex2, 1.5)
        edge2 = EdgeNode(self.vertex2, self.vertex1, 1.5)

        edge1.twin = edge2
        edge2.twin = edge1

        self.assertIs(edge1.twin, edge2)
        self.assertIs(edge2.twin, edge1)

    def test_edge_node_repr(self):
        """Тест строкового представления"""
        edge = EdgeNode(self.vertex1, self.vertex2, 3.0)
        expected_repr = "EdgeNode(A-B, w=3.0)"
        self.assertEqual(repr(edge), expected_repr)

    def test_edge_node_different_weights(self):
        """Тест узлов ребра с разными весами"""
        weights = [0.5, 1.0, 2.5, 10.0, 100.5]

        for weight in weights:
            edge = EdgeNode(self.vertex1, self.vertex2, weight)
            self.assertEqual(edge.weight, weight)

    def test_edge_node_chain(self):
        """Тест цепочки узлов ребер"""
        vertex3 = VertexWrapper("C", 2)

        edge1 = EdgeNode(self.vertex1, self.vertex2, 1.0)
        edge2 = EdgeNode(self.vertex1, vertex3, 2.0)
        edge3 = EdgeNode(self.vertex1, VertexWrapper("D", 3), 3.0)

        edge1.next = edge2
        edge2.next = edge3

        # Проверяем цепочку
        self.assertIs(edge1.next, edge2)
        self.assertIs(edge2.next, edge3)
        self.assertIsNone(edge3.next)


if __name__ == '__main__':
    unittest.main()