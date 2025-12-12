from typing import TypeVar, Generic, Any
from GraphError import GraphError
from WirthGraphOperations import WirthGraphOperations
from WirthIteratorsProvider import WirthIteratorsProvider
from WirthGraphComparator import WirthGraphComparator
from Iterators import GraphIterator
from EdgeWrapper import EdgeWrapper
from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode

T = TypeVar('T')


class WirthAdjacencyListGraph(Generic[T], WirthGraphOperations[T]):
    """
    Шаблонный класс неориентированного графа
    с использованием модифицированной структуры Вирта
    """

    def __init__(self):
        super().__init__()
        self._update_dependencies()

    def __copy__(self) -> 'WirthAdjacencyListGraph[T]':
        new_graph = WirthAdjacencyListGraph[T]()
        new_graph._vertices = self._vertices.copy()
        new_graph._edges_list = self._edges_list.copy()
        new_graph._vertex_count = self._vertex_count
        new_graph._edge_count = self._edge_count
        new_graph._update_dependencies()
        return new_graph

    def __deepcopy__(self, memo=None) -> 'WirthAdjacencyListGraph[T]':
        if memo is None:
            memo = {}

        if id(self) in memo:
            return memo[id(self)]

        new_graph = WirthAdjacencyListGraph[T]()
        memo[id(self)] = new_graph

        # Глубокое копирование вершин
        vertex_map = {}
        for vertex in self._vertices:
            new_vertex = VertexWrapper(vertex.value, vertex.index)
            new_vertex.first_edge = None
            new_graph._vertices.append(new_vertex)
            vertex_map[vertex] = new_vertex

        # Глубокое копирование ребер
        edge_map = {}
        for edge_node1, edge_node2 in self._edges_list:
            # Создаем новые узлы ребер
            new_edge_node1 = EdgeNode(
                vertex_map[edge_node1.vertex],
                vertex_map[edge_node1.other_vertex],
                edge_node1.weight
            )
            new_edge_node2 = EdgeNode(
                vertex_map[edge_node2.vertex],
                vertex_map[edge_node2.other_vertex],
                edge_node2.weight
            )

            # Сохраняем связь между новыми узлами
            edge_map[edge_node1] = new_edge_node1
            edge_map[edge_node2] = new_edge_node2

        # Восстанавливаем связи между узлами
        for edge_node1, edge_node2 in self._edges_list:
            new_edge_node1 = edge_map[edge_node1]
            new_edge_node2 = edge_map[edge_node2]

            # Восстанавливаем twin связи
            new_edge_node1.twin = new_edge_node2
            new_edge_node2.twin = new_edge_node1

            # Восстанавливаем next связи (если они есть)
            if edge_node1.next:
                new_edge_node1.next = edge_map.get(edge_node1.next)
            if edge_node2.next:
                new_edge_node2.next = edge_map.get(edge_node2.next)

        # Восстанавливаем first_edge для вершин
        for vertex in self._vertices:
            if vertex.first_edge:
                new_vertex = vertex_map[vertex]
                new_vertex.first_edge = edge_map.get(vertex.first_edge)

        # Восстанавливаем список ребер
        for edge_node1, edge_node2 in self._edges_list:
            new_graph._edges_list.append((edge_map[edge_node1], edge_map[edge_node2]))

        new_graph._vertex_count = self._vertex_count
        new_graph._edge_count = self._edge_count
        new_graph._update_dependencies()

        return new_graph

    def _update_dependencies(self) -> None:
        """Обновление зависимых объектов после изменения состояния"""
        self._iterators_provider = WirthIteratorsProvider[T](
            self._vertices, self._edges_list
        )
        self._comparator = WirthGraphComparator[T](
            self._vertices, self._edges_list, self._vertex_count, self._edge_count
        )

    # ============ БАЗОВЫЕ МЕТОДЫ КОНТЕЙНЕРА ============

    def empty(self) -> bool:
        """Проверка на пустой контейнер"""
        return self._vertex_count == 0

    def clear(self) -> None:
        """Очистка контейнера"""
        # Очищаем базовые структуры
        self._vertices.clear()
        self._edges_list.clear()
        self._vertex_count = 0
        self._edge_count = 0
        # Обновляем зависимости
        self._update_dependencies()

    def size(self) -> int:
        """Получение размера контейнера (количество вершин)"""
        return self._vertex_count

    # ============ ОПЕРАТОРЫ СРАВНЕНИЯ ============

    def __eq__(self, other: Any) -> bool:
        """Оператор сравнения =="""
        return self._comparator.equals(other)

    def __ne__(self, other: Any) -> bool:
        """Оператор сравнения !="""
        return self._comparator.not_equals(other)

    def __lt__(self, other: Any) -> bool:
        """Оператор сравнения <"""
        return self._comparator.less_than(other)

    def __le__(self, other: Any) -> bool:
        """Оператор сравнения <="""
        return self._comparator.less_or_equal(other)

    def __gt__(self, other: Any) -> bool:
        """Оператор сравнения >"""
        return self._comparator.greater_than(other)

    def __ge__(self, other: Any) -> bool:
        """Оператор сравнения >="""
        return self._comparator.greater_or_equal(other)

    # ============ МЕТОДЫ ДОБАВЛЕНИЯ/УДАЛЕНИЯ ============

    def add_vertex(self, value: T):
        """Добавление вершины с обновлением зависимостей"""
        result = super().add_vertex(value)
        self._update_dependencies()
        return result

    def add_edge(self, from_value: T, to_value: T, weight: float = 1.0):
        """Добавление ребра с обновлением зависимостей"""
        result = super().add_edge(from_value, to_value, weight)
        self._update_dependencies()
        return result

    def remove_vertex(self, vertex_value: T) -> None:
        """Удаление вершины с обновлением зависимостей"""
        super().remove_vertex(vertex_value)
        self._update_dependencies()

    def remove_edge(self, from_value: T, to_value: T) -> None:
        """Удаление ребра с обновлением зависимостей"""
        super().remove_edge(from_value, to_value)
        self._update_dependencies()

    # ============ ИТЕРАТОРЫ ============

    def vertices(self):
        """Двунаправленный итератор для перебора вершин"""
        return self._iterators_provider.vertices_iterator()

    def edges(self):
        """Двунаправленный итератор для перебора ребер"""
        return self._iterators_provider.edges_iterator()

    def incident_edges(self, vertex_value: T):
        """Двунаправленный итератор для перебора ребер, инцидентных вершине"""
        return self._iterators_provider.incident_edges_iterator(vertex_value)

    def adjacent_vertices(self, vertex_value: T):
        """Двунаправленный итератор для перебора вершин, смежных вершине"""
        return self._iterators_provider.adjacent_vertices_iterator(vertex_value)

    def rvertices(self):
        """Обратный итератор для вершин"""
        return self._iterators_provider.reverse_vertices_iterator()

    def redges(self):
        """Обратный итератор для ребер"""
        return self._iterators_provider.reverse_edges_iterator()

    def cvertices(self):
        """Константный итератор для вершин"""
        return self._iterators_provider.const_vertices_iterator()

    def cedges(self):
        """Константный итератор для ребер"""
        return self._iterators_provider.const_edges_iterator()

    # ============ УДАЛЕНИЕ ПО ИТЕРАТОРУ ============

    def remove_vertex_by_iterator(self, vertex_iterator: GraphIterator) -> None:
        """Удаление вершины по итератору на вершину"""
        if not isinstance(vertex_iterator, GraphIterator):
            raise GraphError("Некорректный итератор")

        try:
            current_vertex = vertex_iterator.current()
            self.remove_vertex(current_vertex.value)
        except (IndexError, AttributeError):
            raise GraphError("Некорректный итератор или итератор не инициализирован")

    def remove_edge_by_iterator(self, edge_iterator: GraphIterator) -> None:
        """Удаление ребра по итератору на ребро"""
        if not isinstance(edge_iterator, GraphIterator):
            raise GraphError("Некорректный итератор")

        try:
            current_edge = edge_iterator.current()
            if isinstance(current_edge, EdgeWrapper):
                self.remove_edge(current_edge.from_vertex.value, current_edge.to_vertex.value)
            else:
                raise GraphError("Итератор не указывает на ребро")
        except (IndexError, AttributeError):
            raise GraphError("Некорректный итератор или итератор не инициализирован")

    # ============ ОПЕРАТОР ВЫВОДА ============

    def __str__(self) -> str:
        """Перегруженный оператор вывода"""
        result = []
        result.append(f"Граф (структура Вирта): вершин={self._vertex_count}, ребер={self._edge_count}")

        if self._vertex_count == 0:
            result.append("  Граф пуст")
            return "\n".join(result)

        result.append("\nСтруктура графа:")
        for vertex in self.cvertices():
            result.append(f"\nВершина {vertex.value}:")
            edges = list(self.incident_edges(vertex.value))
            if edges:
                for edge in edges:
                    result.append(f"  -> {edge.to_vertex.value} (вес: {edge.weight})")
            else:
                result.append("  (нет смежных вершин)")

        return "\n".join(result)

    def __repr__(self) -> str:
        return f"WirthAdjacencyListGraph(vertices={self._vertex_count}, edges={self._edge_count})"

    # ============ ОПЕРАТОР ПРИСВАИВАНИЯ ============

    def assign(self, other: 'WirthAdjacencyListGraph[T]') -> None:
        """Оператор присваивания"""
        if not isinstance(other, WirthAdjacencyListGraph):
            raise GraphError("Некорректный тип для присваивания")

        self.clear()

        for vertex in other._vertices:
            self.add_vertex(vertex.value)

        for edge_node1, edge_node2 in other._edges_list:
            v1 = edge_node1.vertex.value
            v2 = edge_node1.other_vertex.value
            if not self.has_edge(v1, v2):
                self.add_edge(v1, v2, edge_node1.weight)

    # ============ ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ============

    def get_vertex_structure(self, vertex_value: T) -> str:
        """Получить структуру вершины в формате Вирта"""
        vertex = self._find_vertex(vertex_value)
        if vertex is None:
            raise GraphError(f"Вершина {vertex_value} не найдена")

        result = []
        result.append(f"Вершина: {vertex.value}")
        result.append(f"Индекс: {vertex.index}")
        result.append("Инцидентные ребра:")

        current = vertex.first_edge
        edge_num = 1
        while current:
            result.append(f"  Ребро {edge_num}:")
            result.append(f"    Вершина: {current.vertex.value}")
            result.append(f"    Смежная вершина: {current.other_vertex.value}")
            result.append(f"    Вес: {current.weight}")
            result.append(f"    Следующее ребро: {current.next}")
            result.append(f"    Близнец: {current.twin}")
            current = current.next
            edge_num += 1

        return "\n".join(result)