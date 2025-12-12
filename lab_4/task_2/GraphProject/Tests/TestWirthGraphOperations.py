import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GraphError import GraphError
from WirthGraphOperations import WirthGraphOperations


class TestWirthGraphOperations(unittest.TestCase):
    """Тесты для класса WirthGraphOperations"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.graph = WirthGraphOperations[int]()

    def test_empty_graph(self):
        """Тест пустого графа"""
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)
        # Вместо empty() проверяем vertex_count()
        self.assertEqual(self.graph.vertex_count(), 0)

    def test_add_vertex(self):
        """Тест добавления вершин"""
        # Добавляем вершины
        for i in range(5):
            vertex = self.graph.add_vertex(i)
            self.assertEqual(vertex.value, i)
            self.assertEqual(vertex.index, i)

        self.assertEqual(self.graph.vertex_count(), 5)
        # Вместо empty() проверяем vertex_count()
        self.assertNotEqual(self.graph.vertex_count(), 0)

    def test_add_duplicate_vertex(self):
        """Тест добавления дубликата вершины"""
        self.graph.add_vertex(1)

        with self.assertRaises(GraphError) as context:
            self.graph.add_vertex(1)

        self.assertIn("уже существует", str(context.exception))

    def test_has_vertex(self):
        """Тест проверки наличия вершины"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)

        self.assertTrue(self.graph.has_vertex(1))
        self.assertTrue(self.graph.has_vertex(2))
        self.assertFalse(self.graph.has_vertex(3))
        self.assertFalse(self.graph.has_vertex(0))

    def test_add_edge(self):
        """Тест добавления ребер"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)

        # Добавляем ребра
        edge1 = self.graph.add_edge(1, 2, 1.5)
        self.assertEqual(self.graph.edge_count(), 1)
        self.assertEqual(edge1.weight, 1.5)

        edge2 = self.graph.add_edge(2, 3, 2.0)
        self.assertEqual(self.graph.edge_count(), 2)
        self.assertEqual(edge2.weight, 2.0)

        # Проверяем, что ребра неориентированные
        self.assertTrue(self.graph.has_edge(1, 2))
        self.assertTrue(self.graph.has_edge(2, 1))
        self.assertTrue(self.graph.has_edge(2, 3))
        self.assertTrue(self.graph.has_edge(3, 2))

    def test_add_edge_with_nonexistent_vertices(self):
        """Тест добавления ребра с несуществующими вершинами"""
        self.graph.add_vertex(1)

        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(1, 2)
        self.assertIn("не найдена", str(context.exception))

        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(2, 1)
        self.assertIn("не найдена", str(context.exception))

    def test_add_duplicate_edge(self):
        """Тест добавления дубликата ребра"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2)

        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(1, 2)
        self.assertIn("уже существует", str(context.exception))

        # Также нельзя добавить в обратном направлении
        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(2, 1)
        self.assertIn("уже существует", str(context.exception))

    def test_add_edge_with_invalid_weight(self):
        """Тест добавления ребра с невалидным весом"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)

        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(1, 2, 0)
        self.assertIn("должен быть положительным", str(context.exception))

        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(1, 2, -1.5)
        self.assertIn("должен быть положительным", str(context.exception))

    def test_add_loop(self):
        """Тест добавления петли"""
        self.graph.add_vertex(1)

        with self.assertRaises(GraphError) as context:
            self.graph.add_edge(1, 1)
        self.assertIn("Петли не поддерживаются", str(context.exception))

    def test_degree(self):
        """Тест вычисления степени вершины"""
        # Создаем граф-звезду
        self.graph.add_vertex(0)  # Центральная вершина
        for i in range(1, 6):
            self.graph.add_vertex(i)
            self.graph.add_edge(0, i)

        self.assertEqual(self.graph.degree(0), 5)

        for i in range(1, 6):
            self.assertEqual(self.graph.degree(i), 1)

    def test_degree_nonexistent_vertex(self):
        """Тест степени несуществующей вершина"""
        with self.assertRaises(GraphError) as context:
            self.graph.degree(1)
        self.assertIn("не найдена", str(context.exception))

    def test_edge_weight(self):
        """Тест получения веса ребра"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2, 3.5)

        weight = self.graph.edge_weight(1, 2)
        self.assertEqual(weight, 3.5)

        # Проверяем в обратном направлении
        weight_reverse = self.graph.edge_weight(2, 1)
        self.assertEqual(weight_reverse, 3.5)

    def test_edge_weight_nonexistent_edge(self):
        """Тест веса несуществующего ребра"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)
        self.graph.add_edge(1, 2)

        with self.assertRaises(GraphError) as context:
            self.graph.edge_weight(1, 3)
        self.assertIn("не существует", str(context.exception))

        with self.assertRaises(GraphError) as context:
            self.graph.edge_weight(3, 1)
        self.assertIn("не существует", str(context.exception))

    def test_remove_edge(self):
        """Тест удаления ребра"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)

        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)

        self.assertEqual(self.graph.edge_count(), 2)
        self.assertTrue(self.graph.has_edge(1, 2))

        # Удаляем ребро
        self.graph.remove_edge(1, 2)

        self.assertEqual(self.graph.edge_count(), 1)
        self.assertFalse(self.graph.has_edge(1, 2))
        self.assertFalse(self.graph.has_edge(2, 1))
        self.assertTrue(self.graph.has_edge(2, 3))

    def test_remove_nonexistent_edge(self):
        """Тест удаления несуществующего ребра"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)

        with self.assertRaises(GraphError) as context:
            self.graph.remove_edge(1, 2)
        self.assertIn("не существует", str(context.exception))

    def test_remove_vertex(self):
        """Тест удаления вершины"""
        # Создаем граф: 1-2-3
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)

        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)

        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertEqual(self.graph.edge_count(), 2)

        # Удаляем вершину 2
        self.graph.remove_vertex(2)

        self.assertEqual(self.graph.vertex_count(), 2)
        self.assertEqual(self.graph.edge_count(), 0)
        self.assertFalse(self.graph.has_vertex(2))
        self.assertFalse(self.graph.has_edge(1, 2))
        self.assertFalse(self.graph.has_edge(2, 3))

    def test_remove_vertex_with_multiple_edges(self):
        """Тест удаления вершины с несколькими ребрами"""
        # Создаем граф-звезду
        self.graph.add_vertex(0)
        for i in range(1, 6):
            self.graph.add_vertex(i)
            self.graph.add_edge(0, i)

        self.assertEqual(self.graph.vertex_count(), 6)
        self.assertEqual(self.graph.edge_count(), 5)
        self.assertEqual(self.graph.degree(0), 5)

        # Удаляем центральную вершину
        self.graph.remove_vertex(0)

        self.assertEqual(self.graph.vertex_count(), 5)
        self.assertEqual(self.graph.edge_count(), 0)

        # Проверяем, что все ребра удалены
        for i in range(1, 6):
            self.assertFalse(self.graph.has_edge(0, i))
            self.assertEqual(self.graph.degree(i), 0)

    def test_remove_nonexistent_vertex(self):
        """Тест удаления несуществующей вершины"""
        with self.assertRaises(GraphError) as context:
            self.graph.remove_vertex(1)
        self.assertIn("не найдена", str(context.exception))

    def test_clear(self):
        """Тест очистки графа"""
        # Добавляем вершины и ребра
        for i in range(5):
            self.graph.add_vertex(i)

        for i in range(4):
            self.graph.add_edge(i, i + 1)

        self.assertEqual(self.graph.vertex_count(), 5)
        self.assertEqual(self.graph.edge_count(), 4)

        # Очищаем
        self.graph.clear()

        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)
        # Вместо empty() проверяем vertex_count()
        self.assertEqual(self.graph.vertex_count(), 0)

    def test_contains_operator(self):
        """Тест оператора in"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)

        self.assertTrue(1 in self.graph)
        self.assertTrue(2 in self.graph)
        self.assertFalse(3 in self.graph)
        self.assertFalse(0 in self.graph)


if __name__ == '__main__':
    unittest.main()