from typing import TypeVar, Generic, Optional
from VertexWrapper import VertexWrapper

T = TypeVar('T')


class EdgeNode(Generic[T]):
    """Узел ребра в модифицированной структуре Вирта"""

    def __init__(self, vertex: VertexWrapper[T],
                 other_vertex: VertexWrapper[T],
                 weight: float = 1.0):
        self.vertex = vertex  # Вершина, для которой это ребро
        self.other_vertex = other_vertex  # Смежная вершина
        self.weight = weight
        self.next: Optional['EdgeNode[T]'] = None  # Следующее ребро для этой вершины
        self.twin: Optional['EdgeNode[T]'] = None  # "Близнец" для неориентированного графа

    def __repr__(self) -> str:
        return f"EdgeNode({self.vertex.value}-{self.other_vertex.value}, w={self.weight})"