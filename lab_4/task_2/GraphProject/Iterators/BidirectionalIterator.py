from typing import List, TypeVar, Generic
from .GraphIterator import GraphIterator

T = TypeVar('T')


class BidirectionalIterator(GraphIterator[T], Generic[T]):
    """
    Двунаправленный итератор с расширенной функциональностью.
    Поддерживает движение как вперед, так и назад.
    """

    def __init__(self, data: List[T]):
        super().__init__(data)

    def previous(self) -> T:
        """Возвращает предыдущий элемент и откатывается на одну позицию"""
        if self._index <= 1:
            raise IndexError("Нет предыдущего элемента")
        self._index -= 1
        return self._data[self._index - 1]

    def peek_next(self) -> T:
        """Заглядывает вперед на следующий элемент без перемещения"""
        if self._index >= len(self._data):
            raise IndexError("Нет следующего элемента")
        return self._data[self._index]

    def peek_previous(self) -> T:
        """Заглядывает назад на предыдущий элемент без перемещения"""
        if self._index <= 1:
            raise IndexError("Нет предыдущего элемента")
        return self._data[self._index - 2]