from typing import List, Tuple, Generic, TypeVar
from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode
from EdgeWrapper import EdgeWrapper
from GraphError import GraphError
from Iterators import GraphIterator, ReverseGraphIterator, ConstGraphIterator

T = TypeVar('T')


class WirthIteratorsProvider(Generic[T]):
    """Поставщик итераторов для структуры Вирта"""

    def __init__(self, vertices: List[VertexWrapper[T]],
                 edges_list: List[Tuple[EdgeNode[T], EdgeNode[T]]]):
        self._vertices = vertices
        self._edges_list = edges_list

    def vertices_iterator(self) -> GraphIterator[VertexWrapper[T]]:
        return GraphIterator(self._vertices.copy())

    def edges_iterator(self) -> GraphIterator[EdgeWrapper[T]]:
        """Двунаправленный итератор для перебора ребер"""
        edges_list = []
        visited_pairs = set()  # Для отслеживания уже добавленных ребер

        for edge_node1, edge_node2 in self._edges_list:
            # Создаем уникальный ключ для пары вершин (независимо от порядка)
            key = tuple(sorted((edge_node1.vertex.value, edge_node1.other_vertex.value)))

            if key not in visited_pairs:
                edges_list.append(EdgeWrapper(edge_node1, edge_node2))
                visited_pairs.add(key)

        return GraphIterator(edges_list)

    def incident_edges_iterator(self, vertex_value: T) -> GraphIterator[EdgeWrapper[T]]:
        vertex = self._find_vertex(vertex_value)
        if vertex is None:
            raise GraphError(f"Вершина {vertex_value} не найдена")

        edges_list = []
        current = vertex.first_edge
        while current:
            edges_list.append(EdgeWrapper(current, current.twin))
            current = current.next

        return GraphIterator(edges_list)

    def adjacent_vertices_iterator(self, vertex_value: T) -> GraphIterator[VertexWrapper[T]]:
        vertex = self._find_vertex(vertex_value)
        if vertex is None:
            raise GraphError(f"Вершина {vertex_value} не найдена")

        vertices_list = []
        current = vertex.first_edge
        while current:
            vertices_list.append(current.other_vertex)
            current = current.next

        return GraphIterator(vertices_list)

    def reverse_vertices_iterator(self) -> ReverseGraphIterator[VertexWrapper[T]]:
        return ReverseGraphIterator(self._vertices.copy())

    def reverse_edges_iterator(self) -> ReverseGraphIterator[EdgeWrapper[T]]:
        edges_list = []
        for edge_node1, edge_node2 in self._edges_list:
            if not any(e._edge_node == edge_node1 or e._edge_node == edge_node2
                       for e in edges_list):
                edges_list.append(EdgeWrapper(edge_node1, edge_node2))
        return ReverseGraphIterator(edges_list)

    def const_vertices_iterator(self) -> ConstGraphIterator[VertexWrapper[T]]:
        return ConstGraphIterator(self._vertices.copy())

    def const_edges_iterator(self) -> ConstGraphIterator[EdgeWrapper[T]]:
        edges_list = []
        for edge_node1, edge_node2 in self._edges_list:
            if not any(e._edge_node == edge_node1 or e._edge_node == edge_node2
                       for e in edges_list):
                edges_list.append(EdgeWrapper(edge_node1, edge_node2))
        return ConstGraphIterator(edges_list)

    def _find_vertex(self, value: T) -> VertexWrapper[T]:
        for vertex in self._vertices:
            if vertex.value == value:
                return vertex
        return None