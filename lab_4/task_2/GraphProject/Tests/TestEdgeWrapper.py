import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode
from EdgeWrapper import EdgeWrapper


class TestEdgeWrapper(unittest.TestCase):
    """Тесты для класса EdgeWrapper"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.vertex1 = VertexWrapper("A", 0)
        self.vertex2 = VertexWrapper("B", 1)
        self.edge_node1 = EdgeNode(self.vertex1, self.vertex2, 2.5)
        self.edge_node2 = EdgeNode(self.vertex2, self.vertex1, 2.5)
        self.edge_node1.twin = self.edge_node2
        self.edge_node2.twin = self.edge_node1

    def test_edge_wrapper_creation(self):
        """Тест создания обертки ребра"""
        edge = EdgeWrapper(self.edge_node1, self.edge_node2)

        self.assertEqual(edge.from_vertex, self.vertex1)
        self.assertEqual(edge.to_vertex, self.vertex2)
        self.assertEqual(edge.weight, 2.5)

    def test_edge_wrapper_default_twin(self):
        """Тест создания обертки ребра с twin по умолчанию"""
        edge = EdgeWrapper(self.edge_node1)

        self.assertEqual(edge.from_vertex, self.vertex1)
        self.assertEqual(edge.to_vertex, self.vertex2)
        self.assertEqual(edge.weight, 2.5)
        self.assertIs(edge._twin, self.edge_node2)

    def test_edge_wrapper_properties(self):
        """Тест свойств обертки ребра"""
        edge = EdgeWrapper(self.edge_node1)

        # Проверяем свойства
        self.assertIsInstance(edge.from_vertex, VertexWrapper)
        self.assertIsInstance(edge.to_vertex, VertexWrapper)
        self.assertIsInstance(edge.weight, float)

        self.assertEqual(edge.from_vertex.value, "A")
        self.assertEqual(edge.to_vertex.value, "B")
        self.assertEqual(edge.weight, 2.5)

    def test_edge_wrapper_equality(self):
        """Тест сравнения оберток ребер"""
        # Создаем дополнительные вершины и ребра
        vertex3 = VertexWrapper("C", 2)
        edge_node3 = EdgeNode(self.vertex1, vertex3, 1.0)
        edge_node4 = EdgeNode(vertex3, self.vertex1, 1.0)
        edge_node3.twin = edge_node4
        edge_node4.twin = edge_node3

        edge1 = EdgeWrapper(self.edge_node1)  # A-B
        edge2 = EdgeWrapper(self.edge_node2)  # B-A (то же ребро, но в обратном направлении)
        edge3 = EdgeWrapper(edge_node3)  # A-C (другое ребро)

        # Для неориентированного графа A-B == B-A
        self.assertEqual(edge1, edge2)

        # Разные ребра не равны
        self.assertNotEqual(edge1, edge3)

        # Сравнение с неверным типом
        self.assertNotEqual(edge1, "not an edge")
        self.assertNotEqual(edge1, None)

    def test_edge_wrapper_hash(self):
        """Тест хэширования оберток ребер"""
        edge1 = EdgeWrapper(self.edge_node1)  # A-B
        edge2 = EdgeWrapper(self.edge_node2)  # B-A

        # Для неориентированного графа хэши должны совпадать
        self.assertEqual(hash(edge1), hash(edge2))

    def test_edge_wrapper_repr(self):
        """Тест строкового представления"""
        edge = EdgeWrapper(self.edge_node1)
        expected_repr = "Edge(A - B, w=2.5)"
        self.assertEqual(repr(edge), expected_repr)

    def test_edge_wrapper_with_different_weights(self):
        """Тест оберток ребер с разными весами"""
        weights = [0.1, 1.0, 5.5, 100.0]

        for weight in weights:
            edge_node = EdgeNode(self.vertex1, self.vertex2, weight)
            edge = EdgeWrapper(edge_node)
            self.assertEqual(edge.weight, weight)
            self.assertIn(f"w={weight}", repr(edge))


if __name__ == '__main__':
    unittest.main()