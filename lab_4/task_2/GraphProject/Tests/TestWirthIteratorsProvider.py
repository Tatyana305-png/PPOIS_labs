import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode
from EdgeWrapper import EdgeWrapper
from GraphError import GraphError
from WirthIteratorsProvider import WirthIteratorsProvider


class TestWirthIteratorsProvider(unittest.TestCase):
    """Тесты для класса WirthIteratorsProvider"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем простой граф: 1-2-3
        self.vertices = [
            VertexWrapper(1, 0),
            VertexWrapper(2, 1),
            VertexWrapper(3, 2)
        ]

        # Создаем ребра
        edge1_a = EdgeNode(self.vertices[0], self.vertices[1], 1.0)
        edge1_b = EdgeNode(self.vertices[1], self.vertices[0], 1.0)
        edge1_a.twin = edge1_b
        edge1_b.twin = edge1_a

        edge2_a = EdgeNode(self.vertices[1], self.vertices[2], 2.0)
        edge2_b = EdgeNode(self.vertices[2], self.vertices[1], 2.0)
        edge2_a.twin = edge2_b
        edge2_b.twin = edge2_a

        # Настраиваем списки инцидентных ребер
        self.vertices[0].first_edge = edge1_a
        self.vertices[1].first_edge = edge2_a
        edge2_a.next = edge1_b  # Для вершины 2: edge2_a -> edge1_b
        self.vertices[2].first_edge = edge2_b

        self.edges_list = [(edge1_a, edge1_b), (edge2_a, edge2_b)]

        self.provider = WirthIteratorsProvider(self.vertices, self.edges_list)

    def test_vertices_iterator(self):
        """Тест итератора вершин"""
        iterator = self.provider.vertices_iterator()

        vertices = list(iterator)
        self.assertEqual(len(vertices), 3)

        # Проверяем значения вершин
        values = [v.value for v in vertices]
        self.assertEqual(values, [1, 2, 3])

    def test_edges_iterator(self):
        """Тест итератора ребер"""
        iterator = self.provider.edges_iterator()

        edges = list(iterator)
        self.assertEqual(len(edges), 2)

        # Проверяем, что все элементы - EdgeWrapper
        for edge in edges:
            self.assertIsInstance(edge, EdgeWrapper)

        # Проверяем веса ребер
        weights = [edge.weight for edge in edges]
        self.assertIn(1.0, weights)
        self.assertIn(2.0, weights)

    def test_incident_edges_iterator(self):
        """Тест итератора инцидентных ребер"""
        # Для вершины 1
        iterator = self.provider.incident_edges_iterator(1)
        edges = list(iterator)

        self.assertEqual(len(edges), 1)  # Одно ребро: 1-2
        self.assertIsInstance(edges[0], EdgeWrapper)
        self.assertEqual(edges[0].weight, 1.0)

        # Для вершины 2
        iterator = self.provider.incident_edges_iterator(2)
        edges = list(iterator)

        self.assertEqual(len(edges), 2)  # Два ребра: 2-1 и 2-3

        # Проверяем веса
        weights = [edge.weight for edge in edges]
        self.assertIn(1.0, weights)
        self.assertIn(2.0, weights)

    def test_incident_edges_nonexistent_vertex(self):
        """Тест инцидентных ребер для несуществующей вершины"""
        with self.assertRaises(GraphError) as context:
            self.provider.incident_edges_iterator(99)
        self.assertIn("не найдена", str(context.exception))

    def test_adjacent_vertices_iterator(self):
        """Тест итератора смежных вершин"""
        # Для вершины 1
        iterator = self.provider.adjacent_vertices_iterator(1)
        vertices = list(iterator)

        self.assertEqual(len(vertices), 1)
        self.assertEqual(vertices[0].value, 2)

        # Для вершины 2
        iterator = self.provider.adjacent_vertices_iterator(2)
        vertices = list(iterator)

        self.assertEqual(len(vertices), 2)
        values = [v.value for v in vertices]
        self.assertIn(1, values)
        self.assertIn(3, values)

        # Для вершины 3
        iterator = self.provider.adjacent_vertices_iterator(3)
        vertices = list(iterator)

        self.assertEqual(len(vertices), 1)
        self.assertEqual(vertices[0].value, 2)

    def test_adjacent_vertices_nonexistent_vertex(self):
        """Тест смежных вершин для несуществующей вершины"""
        with self.assertRaises(GraphError) as context:
            self.provider.adjacent_vertices_iterator(99)
        self.assertIn("не найдена", str(context.exception))

    def test_reverse_vertices_iterator(self):
        """Тест обратного итератора вершин"""
        iterator = self.provider.reverse_vertices_iterator()

        vertices = list(iterator)
        values = [v.value for v in vertices]
        self.assertEqual(values, [3, 2, 1])  # В обратном порядке

    def test_reverse_edges_iterator(self):
        """Тест обратного итератора ребер"""
        iterator = self.provider.reverse_edges_iterator()

        edges = list(iterator)
        self.assertEqual(len(edges), 2)

        # Проверяем, что итерация в обратном порядке
        # (порядок может быть любым, но должно быть 2 ребра)
        for edge in edges:
            self.assertIsInstance(edge, EdgeWrapper)

    def test_const_vertices_iterator(self):
        """Тест константного итератора вершин"""
        iterator = self.provider.const_vertices_iterator()

        vertices = list(iterator)
        self.assertEqual(len(vertices), 3)

        # Проверяем, что это действительно вершины
        for vertex in vertices:
            self.assertIsInstance(vertex, VertexWrapper)

    def test_const_edges_iterator(self):
        """Тест константного итератора ребер"""
        iterator = self.provider.const_edges_iterator()

        edges = list(iterator)
        self.assertEqual(len(edges), 2)

        # Проверяем, что это действительно обертки ребер
        for edge in edges:
            self.assertIsInstance(edge, EdgeWrapper)

    def test_provider_with_empty_graph(self):
        """Тест поставщика с пустым графом"""
        empty_provider = WirthIteratorsProvider([], [])

        # Итераторы должны возвращать пустые последовательности
        vertices = list(empty_provider.vertices_iterator())
        self.assertEqual(vertices, [])

        edges = list(empty_provider.edges_iterator())
        self.assertEqual(edges, [])

    def test_provider_with_single_vertex(self):
        """Тест поставщика с одной вершиной"""
        vertex = VertexWrapper(1, 0)
        provider = WirthIteratorsProvider([vertex], [])

        vertices = list(provider.vertices_iterator())
        self.assertEqual(len(vertices), 1)
        self.assertEqual(vertices[0].value, 1)

        edges = list(provider.edges_iterator())
        self.assertEqual(edges, [])

        # Инцидентные ребра для изолированной вершины
        iterator = provider.incident_edges_iterator(1)
        incident_edges = list(iterator)
        self.assertEqual(incident_edges, [])

        # Смежные вершины для изолированной вершины
        iterator = provider.adjacent_vertices_iterator(1)
        adjacent_vertices = list(iterator)
        self.assertEqual(adjacent_vertices, [])


if __name__ == '__main__':
    unittest.main()