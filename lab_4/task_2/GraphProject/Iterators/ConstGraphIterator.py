from typing import List, TypeVar, Generic
from .BaseIterator import BaseIterator

T = TypeVar('T')


class ConstGraphIterator(BaseIterator[T], Generic[T]):
    """
    Константный итератор (только для чтения).
    """

    def __init__(self, data: List[T]):
        super().__init__(data)

    def __next__(self) -> T:
        if self._index >= len(self._data):
            raise StopIteration
        result = self._data[self._index]
        self._index += 1
        return result

    def current(self) -> T:
        if self._index == 0 or self._index > len(self._data):
            raise IndexError("Итератор не инициализирован")
        return self._data[self._index - 1]

    def has_next(self) -> bool:
        return self._index < len(self._data)

    def reset(self) -> None:
        self._index = 0