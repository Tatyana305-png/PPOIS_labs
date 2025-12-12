import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from WirthAdjacencyListGraph import WirthAdjacencyListGraph


class TestWirthAdjacencyListGraph(unittest.TestCase):
    """Тесты для основного класса WirthAdjacencyListGraph"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.graph = WirthAdjacencyListGraph[int]()

    def test_empty_graph(self):
        """Тест пустого графа"""
        self.assertTrue(self.graph.empty())
        self.assertEqual(self.graph.size(), 0)
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_add_and_remove_vertices(self):
        """Тест добавления и удаления вершин"""
        # Добавляем вершины
        for i in range(1, 6):
            vertex = self.graph.add_vertex(i)
            self.assertEqual(vertex.value, i)
            self.assertEqual(self.graph.vertex_count(), i)

        self.assertEqual(self.graph.size(), 5)
        self.assertFalse(self.graph.empty())

        # Проверяем наличие вершин
        for i in range(1, 6):
            self.assertTrue(self.graph.has_vertex(i))
            self.assertTrue(i in self.graph)

        # Удаляем вершину
        self.graph.remove_vertex(3)
        self.assertEqual(self.graph.vertex_count(), 4)
        self.assertFalse(self.graph.has_vertex(3))

        # Удаляем еще вершину
        self.graph.remove_vertex(1)
        self.assertEqual(self.graph.vertex_count(), 3)

        # Проверяем оставшиеся вершины
        self.assertTrue(self.graph.has_vertex(2))
        self.assertTrue(self.graph.has_vertex(4))
        self.assertTrue(self.graph.has_vertex(5))

    def test_add_and_remove_edges(self):
        """Тест добавления и удаления ребер"""
        # Создаем граф: 1-2-3
        for i in range(1, 4):
            self.graph.add_vertex(i)

        # Добавляем ребра
        edge1 = self.graph.add_edge(1, 2, 1.5)
        self.assertEqual(self.graph.edge_count(), 1)
        self.assertEqual(edge1.weight, 1.5)

        edge2 = self.graph.add_edge(2, 3, 2.0)
        self.assertEqual(self.graph.edge_count(), 2)
        self.assertEqual(edge2.weight, 2.0)

        # Проверяем наличие ребер (неориентированные)
        self.assertTrue(self.graph.has_edge(1, 2))
        self.assertTrue(self.graph.has_edge(2, 1))
        self.assertTrue(self.graph.has_edge(2, 3))
        self.assertTrue(self.graph.has_edge(3, 2))
        self.assertFalse(self.graph.has_edge(1, 3))

        # Проверяем веса
        self.assertEqual(self.graph.edge_weight(1, 2), 1.5)
        self.assertEqual(self.graph.edge_weight(2, 1), 1.5)
        self.assertEqual(self.graph.edge_weight(2, 3), 2.0)

        # Удаляем ребро
        self.graph.remove_edge(1, 2)
        self.assertEqual(self.graph.edge_count(), 1)
        self.assertFalse(self.graph.has_edge(1, 2))
        self.assertFalse(self.graph.has_edge(2, 1))
        self.assertTrue(self.graph.has_edge(2, 3))

    def test_degree(self):
        """Тест вычисления степени вершины"""
        # Создаем граф-звезду: 0 соединен с 1-5
        self.graph.add_vertex(0)
        for i in range(1, 6):
            self.graph.add_vertex(i)
            self.graph.add_edge(0, i)

        self.assertEqual(self.graph.degree(0), 5)

        for i in range(1, 6):
            self.assertEqual(self.graph.degree(i), 1)

    def test_iterators(self):
        """Тест итераторов"""
        # Создаем граф: 1-2-3
        for i in range(1, 4):
            self.graph.add_vertex(i)

        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)

        # Итератор вершин
        vertices = list(self.graph.vertices())
        self.assertEqual(len(vertices), 3)
        vertex_values = [v.value for v in vertices]
        self.assertEqual(sorted(vertex_values), [1, 2, 3])

        # Итератор ребер
        edges = list(self.graph.edges())
        self.assertEqual(len(edges), 2)

        # Итератор смежных вершин
        adjacent = list(self.graph.adjacent_vertices(2))
        self.assertEqual(len(adjacent), 2)
        adj_values = [v.value for v in adjacent]
        self.assertIn(1, adj_values)
        self.assertIn(3, adj_values)

        # Итератор инцидентных ребер
        incident = list(self.graph.incident_edges(2))
        self.assertEqual(len(incident), 2)

    def test_reverse_iterators(self):
        """Тест обратных итераторов"""
        for i in range(1, 4):
            self.graph.add_vertex(i)

        # Обратный итератор вершин
        reverse_vertices = list(self.graph.rvertices())
        vertex_values = [v.value for v in reverse_vertices]
        self.assertEqual(vertex_values, [3, 2, 1])

        # Добавляем ребра для теста обратного итератора ребер
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)

        reverse_edges = list(self.graph.redges())
        self.assertEqual(len(reverse_edges), 2)

    def test_const_iterators(self):
        """Тест константных итераторов"""
        for i in range(1, 4):
            self.graph.add_vertex(i)

        self.graph.add_edge(1, 2)

        # Константный итератор вершин
        const_vertices = list(self.graph.cvertices())
        self.assertEqual(len(const_vertices), 3)

        # Константный итератор ребер
        const_edges = list(self.graph.cedges())
        self.assertEqual(len(const_edges), 1)

    def test_copy_and_deepcopy(self):
        """Тест копирования графа"""
        import copy

        # Создаем граф
        for i in range(1, 4):
            self.graph.add_vertex(i)

        self.graph.add_edge(1, 2, 1.5)
        self.graph.add_edge(2, 3, 2.0)

        # Поверхностное копирование
        shallow_copy = copy.copy(self.graph)
        self.assertEqual(self.graph, shallow_copy)

        # Глубокое копирование
        deep_copy = copy.deepcopy(self.graph)
        self.assertEqual(self.graph, deep_copy)

        # Модифицируем копию
        deep_copy.add_vertex(4)
        self.assertNotEqual(self.graph, deep_copy)
        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertEqual(deep_copy.vertex_count(), 4)

    def test_comparison_operators(self):
        """Тест операторов сравнения"""
        graph1 = WirthAdjacencyListGraph[int]()
        graph2 = WirthAdjacencyListGraph[int]()

        # Пустые графы равны
        self.assertEqual(graph1, graph2)
        self.assertFalse(graph1 != graph2)
        self.assertFalse(graph1 < graph2)
        self.assertTrue(graph1 <= graph2)
        self.assertFalse(graph1 > graph2)
        self.assertTrue(graph1 >= graph2)

        # Добавляем вершины в graph1
        graph1.add_vertex(1)
        graph1.add_vertex(2)
        graph1.add_edge(1, 2)

        # graph1 > graph2 (больше вершин)
        self.assertNotEqual(graph1, graph2)
        self.assertTrue(graph1 != graph2)
        self.assertFalse(graph1 < graph2)
        self.assertFalse(graph1 <= graph2)
        self.assertTrue(graph1 > graph2)
        self.assertTrue(graph1 >= graph2)

        # Создаем graph3 такой же как graph1
        graph3 = WirthAdjacencyListGraph[int]()
        graph3.add_vertex(1)
        graph3.add_vertex(2)
        graph3.add_edge(1, 2)

        self.assertEqual(graph1, graph3)
        self.assertFalse(graph1 != graph3)
        self.assertFalse(graph1 < graph3)
        self.assertTrue(graph1 <= graph3)
        self.assertFalse(graph1 > graph3)
        self.assertTrue(graph1 >= graph3)

    def test_remove_by_iterator(self):
        """Тест удаления по итератору"""
        # Создаем граф: 1-2-3
        for i in range(1, 4):
            self.graph.add_vertex(i)

        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)

        # Удаляем вершину по итератору
        vertex_iterator = self.graph.vertices()

        # Пропускаем все вершины и сбрасываем
        list(vertex_iterator)  # Проходим по всем вершинам
        vertex_iterator.reset()  # Сбрасываем итератор

        # Теперь берем первую вершину
        next(vertex_iterator)  # Берем вершину 1
        current_vertex = vertex_iterator.current()
        print(f"Удаляем вершину: {current_vertex.value}")  # Для отладки

        self.graph.remove_vertex_by_iterator(vertex_iterator)

        self.assertEqual(self.graph.vertex_count(), 2)
        self.assertFalse(self.graph.has_vertex(1))  # Удалили вершину 1

        # Удаляем ребро по итератору
        edge_iterator = self.graph.edges()

        # Пропускаем все ребра и сбрасываем
        list(edge_iterator)  # Проходим по всем ребрам
        edge_iterator.reset()  # Сбрасываем итератор

        # Берем первое ребро
        next(edge_iterator)
        current_edge = edge_iterator.current()
        print(f"Удаляем ребро: {current_edge.from_vertex.value}-{current_edge.to_vertex.value}")  # Для отладки

        self.graph.remove_edge_by_iterator(edge_iterator)

        self.assertEqual(self.graph.edge_count(), 0)

    def test_clear(self):
        """Тест очистки графа"""
        # Заполняем граф
        for i in range(1, 6):
            self.graph.add_vertex(i)

        for i in range(1, 5):
            self.graph.add_edge(i, i + 1)

        self.assertEqual(self.graph.vertex_count(), 5)
        self.assertEqual(self.graph.edge_count(), 4)

        # Очищаем
        self.graph.clear()

        self.assertTrue(self.graph.empty())
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_assign(self):
        """Тест оператора присваивания"""
        # Создаем исходный граф
        source = WirthAdjacencyListGraph[int]()
        for i in range(1, 4):
            source.add_vertex(i)

        source.add_edge(1, 2, 1.5)
        source.add_edge(2, 3, 2.0)

        # Присваиваем
        self.graph.assign(source)

        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertEqual(self.graph.edge_count(), 2)
        self.assertTrue(self.graph.has_edge(1, 2))
        self.assertTrue(self.graph.has_edge(2, 3))
        self.assertEqual(self.graph.edge_weight(1, 2), 1.5)

        # Проверяем, что это копия, а не ссылка
        source.add_vertex(4)
        self.assertEqual(source.vertex_count(), 4)
        self.assertEqual(self.graph.vertex_count(), 3)  # Не изменился

    def test_str_and_repr(self):
        """Тест строкового представления"""
        # Пустой граф
        empty_str = str(self.graph)
        self.assertIn("Граф пуст", empty_str)

        # Граф с вершинами и ребрами
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2, 3.0)

        graph_str = str(self.graph)
        self.assertIn("вершин=2", graph_str)
        self.assertIn("ребер=1", graph_str)
        self.assertIn("Вершина 1", graph_str)
        self.assertIn("Вершина 2", graph_str)

        # repr
        graph_repr = repr(self.graph)
        self.assertIn("WirthAdjacencyListGraph", graph_repr)
        self.assertIn("vertices=2", graph_repr)
        self.assertIn("edges=1", graph_repr)

    def test_get_vertex_structure(self):
        """Тест получения структуры вершины"""
        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_edge(1, 2, 2.5)

        structure = self.graph.get_vertex_structure(1)
        self.assertIn("Вершина: 1", structure)
        self.assertIn("Индекс: 0", structure)
        self.assertIn("Инцидентные ребра", structure)
        self.assertIn("Смежная вершина: 2", structure)
        self.assertIn("Вес: 2.5", structure)


if __name__ == '__main__':
    unittest.main()