import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode
from WirthGraphComparator import WirthGraphComparator


class TestWirthGraphComparator(unittest.TestCase):
    """Тесты для класса WirthGraphComparator"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Граф 1: 1-2-3
        self.vertices1 = [
            VertexWrapper(1, 0),
            VertexWrapper(2, 1),
            VertexWrapper(3, 2)
        ]

        edge1_a = EdgeNode(self.vertices1[0], self.vertices1[1], 1.0)
        edge1_b = EdgeNode(self.vertices1[1], self.vertices1[0], 1.0)
        edge1_a.twin = edge1_b
        edge1_b.twin = edge1_a

        edge2_a = EdgeNode(self.vertices1[1], self.vertices1[2], 2.0)
        edge2_b = EdgeNode(self.vertices1[2], self.vertices1[1], 2.0)
        edge2_a.twin = edge2_b
        edge2_b.twin = edge2_a

        self.edges_list1 = [(edge1_a, edge1_b), (edge2_a, edge2_b)]

        self.comparator1 = WirthGraphComparator(
            self.vertices1, self.edges_list1, 3, 2
        )

        # Граф 2: такой же как граф 1
        self.vertices2 = [
            VertexWrapper(1, 0),
            VertexWrapper(2, 1),
            VertexWrapper(3, 2)
        ]

        edge1_a_2 = EdgeNode(self.vertices2[0], self.vertices2[1], 1.0)
        edge1_b_2 = EdgeNode(self.vertices2[1], self.vertices2[0], 1.0)
        edge1_a_2.twin = edge1_b_2
        edge1_b_2.twin = edge1_a_2

        edge2_a_2 = EdgeNode(self.vertices2[1], self.vertices2[2], 2.0)
        edge2_b_2 = EdgeNode(self.vertices2[2], self.vertices2[1], 2.0)
        edge2_a_2.twin = edge2_b_2
        edge2_b_2.twin = edge2_a_2

        self.edges_list2 = [(edge1_a_2, edge1_b_2), (edge2_a_2, edge2_b_2)]

        self.comparator2 = WirthGraphComparator(
            self.vertices2, self.edges_list2, 3, 2
        )

        # Граф 3: отличается весом ребра
        self.vertices3 = [
            VertexWrapper(1, 0),
            VertexWrapper(2, 1),
            VertexWrapper(3, 2)
        ]

        edge1_a_3 = EdgeNode(self.vertices3[0], self.vertices3[1], 5.0)  # Другой вес
        edge1_b_3 = EdgeNode(self.vertices3[1], self.vertices3[0], 5.0)
        edge1_a_3.twin = edge1_b_3
        edge1_b_3.twin = edge1_a_3

        edge2_a_3 = EdgeNode(self.vertices3[1], self.vertices3[2], 2.0)
        edge2_b_3 = EdgeNode(self.vertices3[2], self.vertices3[1], 2.0)
        edge2_a_3.twin = edge2_b_3
        edge2_b_3.twin = edge2_a_3

        self.edges_list3 = [(edge1_a_3, edge1_b_3), (edge2_a_3, edge2_b_3)]

        self.comparator3 = WirthGraphComparator(
            self.vertices3, self.edges_list3, 3, 2
        )

        # Граф 4: меньше вершин
        self.vertices4 = [
            VertexWrapper(1, 0),
            VertexWrapper(2, 1)
        ]

        self.comparator4 = WirthGraphComparator(
            self.vertices4, [], 2, 0
        )

        # Граф 5: больше вершин
        self.vertices5 = [
            VertexWrapper(1, 0),
            VertexWrapper(2, 1),
            VertexWrapper(3, 2),
            VertexWrapper(4, 3)
        ]

        self.comparator5 = WirthGraphComparator(
            self.vertices5, [], 4, 0
        )

    def test_equals_same_graph(self):
        """Тест сравнения одинаковых графов"""
        self.assertTrue(self.comparator1.equals(self.comparator2))
        self.assertTrue(self.comparator2.equals(self.comparator1))

    def test_equals_different_weights(self):
        """Тест сравнения графов с разными весами"""
        self.assertFalse(self.comparator1.equals(self.comparator3))
        self.assertFalse(self.comparator3.equals(self.comparator1))

    def test_equals_different_vertex_count(self):
        """Тест сравнения графов с разным количеством вершин"""
        self.assertFalse(self.comparator1.equals(self.comparator4))
        self.assertFalse(self.comparator4.equals(self.comparator1))

    def test_equals_with_non_graph_object(self):
        """Тест сравнения с объектом не-графом"""
        self.assertFalse(self.comparator1.equals("not a graph"))
        self.assertFalse(self.comparator1.equals(None))
        self.assertFalse(self.comparator1.equals(123))
        self.assertFalse(self.comparator1.equals([]))

    def test_not_equals(self):
        """Тест оператора not equals"""
        self.assertFalse(self.comparator1.not_equals(self.comparator2))
        self.assertTrue(self.comparator1.not_equals(self.comparator3))
        self.assertTrue(self.comparator1.not_equals(self.comparator4))

    def test_less_than(self):
        """Тест оператора less than"""
        # Граф с 2 вершинами < графа с 3 вершинами
        self.assertTrue(self.comparator4.less_than(self.comparator1))
        self.assertFalse(self.comparator1.less_than(self.comparator4))

        # Графы с одинаковым количеством вершин сравниваются по ребрам
        # comparator1 и comparator3 имеют по 3 вершины и 2 ребра, но веса разные
        # less_than сравнивает только количество вершин и ребер
        self.assertFalse(self.comparator1.less_than(self.comparator3))
        self.assertFalse(self.comparator3.less_than(self.comparator1))

    def test_less_or_equal(self):
        """Тест оператора less or equal"""
        # Граф с 2 вершинами <= графа с 3 вершинами
        self.assertTrue(self.comparator4.less_or_equal(self.comparator1))

        # Граф с 3 вершинами <= графа с 3 вершинами
        self.assertTrue(self.comparator1.less_or_equal(self.comparator2))

        # Граф с 4 вершинами не <= графа с 3 вершинами
        self.assertFalse(self.comparator5.less_or_equal(self.comparator1))

    def test_greater_than(self):
        """Тест оператора greater than"""
        # Граф с 4 вершинами > графа с 3 вершинами
        self.assertTrue(self.comparator5.greater_than(self.comparator1))
        self.assertFalse(self.comparator1.greater_than(self.comparator5))

        # Граф с 3 вершинами > графа с 2 вершинами
        self.assertTrue(self.comparator1.greater_than(self.comparator4))

    def test_greater_or_equal(self):
        """Тест оператора greater or equal"""
        # Граф с 4 вершиннами >= графа с 3 вершинами
        self.assertTrue(self.comparator5.greater_or_equal(self.comparator1))

        # Граф с 3 вершинами >= графа с 3 вершинами
        self.assertTrue(self.comparator1.greater_or_equal(self.comparator2))

        # Граф с 2 вершинами не >= графа с 3 вершинами
        self.assertFalse(self.comparator4.greater_or_equal(self.comparator1))

    def test_comparison_with_invalid_object(self):
        """Тест сравнения с некорректным объектом"""
        # less_than с объектом без атрибутов графа
        result = self.comparator1.less_than("invalid")
        self.assertEqual(result, NotImplemented)

        # less_or_equal с объектом без атрибутов графа
        result = self.comparator1.less_or_equal("invalid")
        self.assertEqual(result, NotImplemented)

        # greater_than с объектом без атрибутов графа
        result = self.comparator1.greater_than("invalid")
        self.assertEqual(result, NotImplemented)

        # greater_or_equal с объектом без атрибутов графа
        result = self.comparator1.greater_or_equal("invalid")
        self.assertEqual(result, NotImplemented)

    def test_empty_graph_comparison(self):
        """Тест сравнения пустых графов"""
        empty1 = WirthGraphComparator([], [], 0, 0)
        empty2 = WirthGraphComparator([], [], 0, 0)

        self.assertTrue(empty1.equals(empty2))
        self.assertFalse(empty1.not_equals(empty2))
        self.assertFalse(empty1.less_than(empty2))
        self.assertTrue(empty1.less_or_equal(empty2))
        self.assertFalse(empty1.greater_than(empty2))
        self.assertTrue(empty1.greater_or_equal(empty2))

    def test_single_vertex_graph_comparison(self):
        """Тест сравнения графов с одной вершиной"""
        vertex = VertexWrapper(1, 0)
        single1 = WirthGraphComparator([vertex], [], 1, 0)
        single2 = WirthGraphComparator([vertex], [], 1, 0)

        self.assertTrue(single1.equals(single2))
        self.assertFalse(single1.less_than(single2))
        self.assertTrue(single1.less_or_equal(single2))
        self.assertFalse(single1.greater_than(single2))
        self.assertTrue(single1.greater_or_equal(single2))


if __name__ == '__main__':
    unittest.main()