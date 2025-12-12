from typing import List, TypeVar, Generic
from .BaseIterator import BaseIterator

T = TypeVar('T')


class ReverseGraphIterator(BaseIterator[T], Generic[T]):
    """
    Обратный итератор для перебора элементов в обратном порядке.
    """

    def __init__(self, data: List[T]):
        super().__init__(data)
        self._index = len(data) - 1

    def __next__(self) -> T:
        if self._index < 0:
            raise StopIteration
        result = self._data[self._index]
        self._index -= 1
        return result

    def current(self) -> T:
        if self._index < -1 or self._index >= len(self._data) - 1:
            raise IndexError("Итератор не инициализирован")
        return self._data[self._index + 1]

    def has_next(self) -> bool:
        return self._index >= 0

    def has_previous(self) -> bool:
        return self._index < len(self._data) - 2

    def reset(self) -> None:
        self._index = len(self._data) - 1