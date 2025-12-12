from typing import TypeVar, Generic, Any, Optional
from VertexWrapper import VertexWrapper
from EdgeNode import EdgeNode

T = TypeVar('T')


class EdgeWrapper(Generic[T]):
    """Класс-обертка для ребра (представление для пользователя)"""

    def __init__(self, edge_node: EdgeNode[T], twin: Optional[EdgeNode[T]] = None):
        self._edge_node = edge_node
        self._twin = twin or edge_node.twin

    @property
    def from_vertex(self) -> VertexWrapper[T]:
        return self._edge_node.vertex

    @property
    def to_vertex(self) -> VertexWrapper[T]:
        return self._edge_node.other_vertex

    @property
    def weight(self) -> float:
        return self._edge_node.weight

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EdgeWrapper):
            return False

        # Для неориентированного графа порядок вершин не важен
        return (self.from_vertex == other.from_vertex and self.to_vertex == other.to_vertex) or \
            (self.from_vertex == other.to_vertex and self.to_vertex == other.from_vertex)

    def __hash__(self) -> int:
        vertices = tuple(sorted((hash(self.from_vertex), hash(self.to_vertex))))
        return hash((vertices, self.weight))

    def __repr__(self) -> str:
        return f"Edge({self.from_vertex.value} - {self.to_vertex.value}, w={self.weight})"