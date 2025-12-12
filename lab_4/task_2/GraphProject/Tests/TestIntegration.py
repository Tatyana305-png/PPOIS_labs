
import unittest
import sys
import os
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ДОБАВЛЯЕМ ИМПОРТ GraphError
from GraphError import GraphError
from WirthAdjacencyListGraph import WirthAdjacencyListGraph


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты для всей системы графа"""

    def test_complete_graph_operations(self):
        """Тест полного набора операций с графом"""
        graph = WirthAdjacencyListGraph[int]()

        # 1. Создание графа
        for i in range(1, 6):
            graph.add_vertex(i)

        self.assertEqual(graph.vertex_count(), 5)

        # 2. Добавление ребра
        edges_to_add = [
            (1, 2, 1.0),
            (2, 3, 2.0),
            (3, 4, 3.0),
            (4, 5, 4.0),
            (5, 1, 5.0),
            (1, 3, 1.5),
            (2, 4, 2.5)
        ]

        for from_v, to_v, weight in edges_to_add:
            graph.add_edge(from_v, to_v, weight)

        self.assertEqual(graph.edge_count(), 7)

        # 3. Проверка степеней вершин
        expected_degrees = {1: 3, 2: 3, 3: 3, 4: 3, 5: 2}
        for vertex, expected_degree in expected_degrees.items():
            self.assertEqual(graph.degree(vertex), expected_degree)

        # 4. Проверка наличия ребер
        for from_v, to_v, _ in edges_to_add:
            self.assertTrue(graph.has_edge(from_v, to_v))
            self.assertTrue(graph.has_edge(to_v, from_v))  # Неориентированный

        # 5. Проверка весов
        for from_v, to_v, weight in edges_to_add:
            self.assertEqual(graph.edge_weight(from_v, to_v), weight)
            self.assertEqual(graph.edge_weight(to_v, from_v), weight)

        # 6. Итераторы
        vertices = list(graph.vertices())
        self.assertEqual(len(vertices), 5)

        edges = list(graph.edges())
        self.assertEqual(len(edges), 7)

        # 7. Смежные вершины
        adjacent_to_1 = list(graph.adjacent_vertices(1))
        self.assertEqual(len(adjacent_to_1), 3)

        # 8. Инцидентные ребра
        incident_to_1 = list(graph.incident_edges(1))
        self.assertEqual(len(incident_to_1), 3)

        # 9. Копирование
        graph_copy = copy.deepcopy(graph)
        self.assertEqual(graph, graph_copy)

        # 10. Модификация копии
        graph_copy.add_vertex(6)
        graph_copy.add_edge(6, 1, 6.0)
        self.assertNotEqual(graph, graph_copy)

        # 11. Обратные итераторы
        reverse_vertices = list(graph.rvertices())
        self.assertEqual(len(reverse_vertices), 5)

        reverse_edges = list(graph.redges())
        self.assertEqual(len(reverse_edges), 7)

        # 12. Константные итераторы
        const_vertices = list(graph.cvertices())
        self.assertEqual(len(const_vertices), 5)

        const_edges = list(graph.cedges())
        self.assertEqual(len(const_edges), 7)

        # 13. Удаление ребра
        graph.remove_edge(1, 2)
        self.assertEqual(graph.edge_count(), 6)
        self.assertFalse(graph.has_edge(1, 2))
        self.assertFalse(graph.has_edge(2, 1))

        # 14. Удаление вершины
        graph.remove_vertex(3)
        self.assertEqual(graph.vertex_count(), 4)
        self.assertFalse(graph.has_vertex(3))

        # Все ребра, инцидентные вершине 3, должны быть удалены
        for from_v, to_v, _ in edges_to_add:
            if from_v == 3 or to_v == 3:
                self.assertFalse(graph.has_edge(from_v, to_v))

        # 15. Очистка
        graph.clear()
        self.assertTrue(graph.empty())
        self.assertEqual(graph.vertex_count(), 0)
        self.assertEqual(graph.edge_count(), 0)

    def test_complex_graph_structure(self):
        """Тест сложной структуры графа"""
        graph = WirthAdjacencyListGraph[str]()

        # Добавляем вершины (города)
        cities = ["Москва", "СПб", "Казань", "Новосибирск", "Екатеринбург"]
        for city in cities:
            graph.add_vertex(city)

        # Добавляем ребра (расстояния между городами)
        distances = [
            ("Москва", "СПб", 700.0),
            ("Москва", "Казань", 800.0),
            ("Москва", "Екатеринбург", 1800.0),
            ("СПб", "Казань", 1500.0),
            ("Казань", "Екатеринбург", 1000.0),
            ("Екатеринбург", "Новосибирск", 1500.0),
            ("Новосибирск", "Казань", 2000.0)
        ]

        for city1, city2, distance in distances:
            graph.add_edge(city1, city2, distance)

        # Проверяем структуру
        self.assertEqual(graph.vertex_count(), 5)
        self.assertEqual(graph.edge_count(), 7)

        # Проверяем степени вершин
        self.assertEqual(graph.degree("Москва"), 3)
        self.assertEqual(graph.degree("СПб"), 2)
        self.assertEqual(graph.degree("Казань"), 4)
        self.assertEqual(graph.degree("Екатеринбург"), 3)
        self.assertEqual(graph.degree("Новосибирск"), 2)

        # Проверяем расстояния
        self.assertEqual(graph.edge_weight("Москва", "СПб"), 700.0)
        self.assertEqual(graph.edge_weight("Казань", "Екатеринбург"), 1000.0)

        # Итераторы
        all_cities = [v.value for v in graph.vertices()]
        self.assertEqual(len(all_cities), 5)

        all_distances = [e.weight for e in graph.edges()]
        self.assertEqual(len(all_distances), 7)

        # Смежные города для Казани
        adjacent_to_kazan = [v.value for v in graph.adjacent_vertices("Казань")]
        self.assertEqual(len(adjacent_to_kazan), 4)
        self.assertIn("Москва", adjacent_to_kazan)
        self.assertIn("СПб", adjacent_to_kazan)
        self.assertIn("Екатеринбург", adjacent_to_kazan)
        self.assertIn("Новосибирск", adjacent_to_kazan)

    def test_graph_with_different_data_types(self):
        """Тест графа с разными типами данных"""
        # Тест с целыми числами
        graph_int = WirthAdjacencyListGraph[int]()
        graph_int.add_vertex(1)
        graph_int.add_vertex(2)
        graph_int.add_edge(1, 2, 10)

        # Тест со строками
        graph_str = WirthAdjacencyListGraph[str]()
        graph_str.add_vertex("A")
        graph_str.add_vertex("B")
        graph_str.add_edge("A", "B", 5.5)

        # Тест с кортежами
        graph_tuple = WirthAdjacencyListGraph[tuple]()
        graph_tuple.add_vertex((1, "A"))
        graph_tuple.add_vertex((2, "B"))
        graph_tuple.add_edge((1, "A"), (2, "B"), 3.0)

        # Тест с пользовательскими объектами
        class City:
            def __init__(self, name, population):
                self.name = name
                self.population = population

            def __eq__(self, other):
                if not isinstance(other, City):
                    return False
                return self.name == other.name and self.population == other.population

        graph_obj = WirthAdjacencyListGraph[City]()
        moscow = City("Moscow", 12000000)
        spb = City("SPb", 5000000)

        graph_obj.add_vertex(moscow)
        graph_obj.add_vertex(spb)
        graph_obj.add_edge(moscow, spb, 700.0)

        self.assertEqual(graph_obj.vertex_count(), 2)
        self.assertEqual(graph_obj.edge_count(), 1)
        self.assertTrue(graph_obj.has_edge(moscow, spb))

    def test_error_handling_integration(self):
        """Тест обработки ошибок в интеграционном сценарии"""
        graph = WirthAdjacencyListGraph[int]()

        # Добавляем нормальные вершины и ребра
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)

        # Пытаемся добавить дубликат вершины
        with self.assertRaises(GraphError):
            graph.add_vertex(1)

        # Пытаемся добавить дубликат ребра
        with self.assertRaises(GraphError):
            graph.add_edge(1, 2)

        # Пытаемся добавить ребро с несуществующей вершиной
        with self.assertRaises(GraphError):
            graph.add_edge(1, 3)

        # Пытаемся удалить несуществующую вершину
        with self.assertRaises(GraphError):
            graph.remove_vertex(3)

        # Пытаемся удалить несуществующее ребро
        with self.assertRaises(GraphError):
            graph.remove_edge(2, 3)

        # Пытаемся получить степень несуществующей вершины
        with self.assertRaises(GraphError):
            graph.degree(3)

        # Пытаемся получить вес несуществующего ребра
        with self.assertRaises(GraphError):
            graph.edge_weight(1, 3)

        # После всех ошибок граф должен остаться в целости
        self.assertEqual(graph.vertex_count(), 2)
        self.assertEqual(graph.edge_count(), 1)
        self.assertTrue(graph.has_edge(1, 2))


if __name__ == '__main__':
    unittest.main()