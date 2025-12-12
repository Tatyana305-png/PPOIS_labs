from typing import List, TypeVar, Generic
from collections.abc import Iterator as ABCIterator

T = TypeVar('T')


class BaseIterator(ABCIterator[T], Generic[T]):
    """Базовый абстрактный класс для итераторов"""

    def __init__(self, data: List[T]):
        self._data = data
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> T:
        raise NotImplementedError("Метод должен быть переопределен в подклассе")

    def current(self) -> T:
        """Возвращает текущий элемент"""
        raise NotImplementedError("Метод должен быть переопределен в подклассе")

    def has_next(self) -> bool:
        """Проверяет, есть ли следующий элемент"""
        raise NotImplementedError("Метод должен быть переопределен в подклассе")

    def reset(self) -> None:
        """Сбрасывает итератор в начальное состояние"""
        raise NotImplementedError("Метод должен быть переопределен в подклассе")

    def size(self) -> int:
        """Возвращает количество элементов"""
        return len(self._data)

    def get_data(self) -> List[T]:
        """Возвращает копию данных"""
        return self._data.copy()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(index={self._index}, size={len(self._data)})"