from typing import TypeVar, List, Tuple, Optional, Generic
from GraphError import GraphError
from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode
from EdgeWrapper import EdgeWrapper

T = TypeVar('T')


class WirthGraphOperations(Generic[T]):
    """Базовые операции графа в модифицированной структуре Вирта"""

    def __init__(self):
        self._vertices: List[VertexWrapper[T]] = []
        self._vertex_count = 0
        self._edge_count = 0
        self._edges_list: List[Tuple[EdgeNode[T], EdgeNode[T]]] = []

    # ============ ПРОВЕРКИ СУЩЕСТВОВАНИЯ ============

    def has_vertex(self, vertex_value: T) -> bool:
        """Проверка присутствия вершины в графе"""
        return any(v.value == vertex_value for v in self._vertices)

    def has_edge(self, from_value: T, to_value: T) -> bool:
        """Проверка присутствия ребра между вершинами в графе"""
        from_vertex = self._find_vertex(from_value)
        to_vertex = self._find_vertex(to_value)

        if from_vertex is None or to_vertex is None:
            return False

        # Ищем ребро в списке инцидентных ребер from_vertex
        current = from_vertex.first_edge
        while current:
            if current.other_vertex.value == to_value:
                return True
            current = current.next

        return False

    def _find_vertex(self, value: T) -> Optional[VertexWrapper[T]]:
        """Поиск вершины по значению"""
        for vertex in self._vertices:
            if vertex.value == value:
                return vertex
        return None

    def _find_edge_nodes(self, from_value: T, to_value: T) -> Optional[Tuple[EdgeNode[T], EdgeNode[T]]]:
        """Поиск пары EdgeNode для ребра"""
        from_vertex = self._find_vertex(from_value)
        to_vertex = self._find_vertex(to_value)

        if from_vertex is None or to_vertex is None:
            return None

        # Ищем ребро от from_vertex к to_vertex
        current = from_vertex.first_edge
        while current:
            if current.other_vertex.value == to_value:
                return (current, current.twin)
            current = current.next

        return None

    # ============ ПОЛУЧЕНИЕ КОЛИЧЕСТВА ============

    def vertex_count(self) -> int:
        """Получение количества вершин"""
        return self._vertex_count

    def edge_count(self) -> int:
        """Получение количества ребер"""
        return self._edge_count

    def degree(self, vertex_value: T) -> int:
        """Вычисление степени вершины"""
        vertex = self._find_vertex(vertex_value)
        if vertex is None:
            raise GraphError(f"Вершина {vertex_value} не найдена")

        degree = 0
        current = vertex.first_edge
        while current:
            degree += 1
            current = current.next

        return degree

    def edge_weight(self, from_value: T, to_value: T) -> float:
        """Получение веса ребра"""
        edge_nodes = self._find_edge_nodes(from_value, to_value)
        if edge_nodes is None:
            raise GraphError(f"Ребро между {from_value} и {to_value} не существует")

        return edge_nodes[0].weight

    # ============ ДОБАВЛЕНИЕ ЭЛЕМЕНТОВ ============

    def add_vertex(self, value: T) -> VertexWrapper[T]:
        """Добавление вершины"""
        if self.has_vertex(value):
            raise GraphError(f"Вершина {value} уже существует")

        # Добавляем новую вершину
        new_vertex = VertexWrapper(value, self._vertex_count)
        self._vertices.append(new_vertex)
        self._vertex_count += 1

        return new_vertex

    def add_edge(self, from_value: T, to_value: T, weight: float = 1.0) -> EdgeWrapper[T]:
        """Добавление ребра (неориентированного)"""
        from_vertex = self._find_vertex(from_value)
        to_vertex = self._find_vertex(to_value)

        if from_vertex is None:
            raise GraphError(f"Вершина {from_value} не найдена")
        if to_vertex is None:
            raise GraphError(f"Вершина {to_value} не найдена")

        if weight <= 0:
            raise GraphError("Вес ребра должен быть положительным")

        if from_value == to_value:
            raise GraphError("Петли не поддерживаются")

        # Проверяем, существует ли уже ребро
        if self.has_edge(from_value, to_value):
            raise GraphError(f"Ребро между {from_value} и {to_value} уже существует")

        # Создаем два EdgeNode для неориентированного ребра
        edge_node1 = EdgeNode(from_vertex, to_vertex, weight)
        edge_node2 = EdgeNode(to_vertex, from_vertex, weight)

        # Связываем их как близнецов
        edge_node1.twin = edge_node2
        edge_node2.twin = edge_node1

        # Добавляем edge_node1 в список инцидентных ребер from_vertex
        edge_node1.next = from_vertex.first_edge
        from_vertex.first_edge = edge_node1

        # Добавляем edge_node2 в список инцидентных ребер to_vertex
        edge_node2.next = to_vertex.first_edge
        to_vertex.first_edge = edge_node2

        # Сохраняем пару
        self._edges_list.append((edge_node1, edge_node2))
        self._edge_count += 1

        return EdgeWrapper(edge_node1, edge_node2)

    # ============ УДАЛЕНИЕ ЭЛЕМЕНТОВ ============

    def remove_vertex(self, vertex_value: T) -> None:
        """Удаление вершины"""
        vertex = self._find_vertex(vertex_value)
        if vertex is None:
            raise GraphError(f"Вершина {vertex_value} не найдена")

        # Собираем все ребра, которые нужно удалить
        edges_to_remove = []

        # Ищем все инцидентные ребра
        current = vertex.first_edge
        while current:
            edges_to_remove.append((current.vertex.value, current.other_vertex.value))
            current = current.next

        # Удаляем все инцидентные ребра
        for from_val, to_val in edges_to_remove:
            self.remove_edge(from_val, to_val)

        # Удаляем вершину из списка
        idx = self._vertices.index(vertex)
        self._vertices.pop(idx)

        # Обновляем индексы оставшихся вершин
        for i, v in enumerate(self._vertices):
            v.index = i

        self._vertex_count -= 1

    def remove_edge(self, from_value: T, to_value: T) -> None:
        """Удаление ребра"""
        edge_nodes = self._find_edge_nodes(from_value, to_value)
        if edge_nodes is None:
            raise GraphError(f"Ребро между {from_value} и {to_value} не существует")

        edge_node1, edge_node2 = edge_nodes

        # Удаляем edge_node1 из списка инцидентных ребер from_vertex
        from_vertex = self._find_vertex(from_value)
        if from_vertex.first_edge == edge_node1:
            from_vertex.first_edge = edge_node1.next
        else:
            current = from_vertex.first_edge
            while current and current.next != edge_node1:
                current = current.next
            if current:
                current.next = edge_node1.next

        # Удаляем edge_node2 из списка инцидентных ребер to_vertex
        to_vertex = self._find_vertex(to_value)
        if to_vertex.first_edge == edge_node2:
            to_vertex.first_edge = edge_node2.next
        else:
            current = to_vertex.first_edge
            while current and current.next != edge_node2:
                current = current.next
            if current:
                current.next = edge_node2.next

        # Удаляем пару из списка
        for i, (e1, e2) in enumerate(self._edges_list):
            if (e1 == edge_node1 and e2 == edge_node2) or (e1 == edge_node2 and e2 == edge_node1):
                self._edges_list.pop(i)
                break

        self._edge_count -= 1

    # ============ ОПЕРАТОР in ============

    def __contains__(self, vertex_value: T) -> bool:
        """Проверка присутствия вершины в графе (оператор in)"""
        return self.has_vertex(vertex_value)

    def clear(self) -> None:
        """Очистка графа"""
        self._vertices.clear()
        self._edges_list.clear()
        self._vertex_count = 0
        self._edge_count = 0