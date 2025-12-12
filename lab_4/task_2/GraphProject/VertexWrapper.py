from typing import TypeVar, Generic, Any, Optional

T = TypeVar('T')


class VertexWrapper(Generic[T]):
    """Класс-обертка для вершины в структуре Вирта"""

    def __init__(self, value: T, index: int):
        self.value = value
        self.index = index
        self.first_edge: Optional['EdgeNode[T]'] = None  # Первое инцидентное ребро

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, VertexWrapper):
            return False
        return self.index == other.index and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.value, self.index))

    def __repr__(self) -> str:
        return f"Vertex({self.value})"