from typing import TypeVar, Generic, Any

T = TypeVar('T')


class WirthGraphComparator(Generic[T]):
    """Класс для операций сравнения графов в структуре Вирта"""

    def __init__(self, vertices, edges_list, vertex_count, edge_count):
        self._vertices = vertices
        self._edges_list = edges_list
        self._vertex_count = vertex_count
        self._edge_count = edge_count

    def equals(self, other: Any) -> bool:
        if not hasattr(other, '_vertices') or not hasattr(other, '_edges_list'):
            return False

        if self._vertex_count != other._vertex_count or self._edge_count != other._edge_count:
            return False

        if len(self._vertices) != len(other._vertices):
            return False

        for v1, v2 in zip(self._vertices, other._vertices):
            if v1.value != v2.value:
                return False

        if len(self._edges_list) != len(other._edges_list):
            return False

        for edge_pair in self._edges_list:
            edge_node1, edge_node2 = edge_pair
            found = False
            for other_pair in other._edges_list:
                other_node1, other_node2 = other_pair
                if ((edge_node1.vertex.value == other_node1.vertex.value and
                     edge_node1.other_vertex.value == other_node1.other_vertex.value) or
                        (edge_node1.vertex.value == other_node2.vertex.value and
                         edge_node1.other_vertex.value == other_node2.other_vertex.value)):
                    if edge_node1.weight == other_node1.weight:
                        found = True
                        break
            if not found:
                return False

        return True

    def not_equals(self, other: Any) -> bool:
        return not self.equals(other)

    def less_than(self, other: Any) -> bool:
        if not hasattr(other, '_vertex_count') or not hasattr(other, '_edge_count'):
            return NotImplemented

        if self._vertex_count != other._vertex_count:
            return self._vertex_count < other._vertex_count

        return self._edge_count < other._edge_count

    def less_or_equal(self, other: Any) -> bool:
        if not hasattr(other, '_vertex_count') or not hasattr(other, '_edge_count'):
            return NotImplemented

        if self._vertex_count != other._vertex_count:
            return self._vertex_count <= other._vertex_count

        return self._edge_count <= other._edge_count

    def greater_than(self, other: Any) -> bool:
        if not hasattr(other, '_vertex_count') or not hasattr(other, '_edge_count'):
            return NotImplemented

        if self._vertex_count != other._vertex_count:
            return self._vertex_count > other._vertex_count

        return self._edge_count > other._edge_count

    def greater_or_equal(self, other: Any) -> bool:
        if not hasattr(other, '_vertex_count') or not hasattr(other, '_edge_count'):
            return NotImplemented

        if self._vertex_count != other._vertex_count:
            return self._vertex_count >= other._vertex_count

        return self._edge_count >= other._edge_count