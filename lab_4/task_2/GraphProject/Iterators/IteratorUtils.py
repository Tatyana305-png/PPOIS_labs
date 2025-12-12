from typing import List, TypeVar, Callable, Any
from collections.abc import Iterator as ABCIterator
from .GraphIterator import GraphIterator
from .ConstGraphIterator import ConstGraphIterator
from .ReverseGraphIterator import ReverseGraphIterator
from .BidirectionalIterator import BidirectionalIterator

T = TypeVar('T')


class IteratorUtils:
    """Утилиты для работы с итераторами"""

    def __init__(self):
        pass

    def to_list(self, iterator: ABCIterator[T]) -> List[T]:
        """Преобразует итератор в список"""
        return list(iterator)

    def count(self, iterator: ABCIterator[T]) -> int:
        """Подсчитывает количество элементов в итераторе"""
        count = 0
        for _ in iterator:
            count += 1
        return count

    def find(self, iterator: ABCIterator[T], value: T) -> bool:
        """Ищет значение в итераторе"""
        for item in iterator:
            if item == value:
                return True
        return False

    def apply(self, iterator: ABCIterator[T], func: Callable[[T], Any]) -> None:
        """Применяет функцию к каждому элементу итератора"""
        for item in iterator:
            func(item)

    def make_iterator(self, data: List[T]) -> GraphIterator[T]:
        """Создает стандартный итератор для данных"""
        return GraphIterator(data)

    def make_const_iterator(self, data: List[T]) -> ConstGraphIterator[T]:
        """Создает константный итератор для данных"""
        return ConstGraphIterator(data)

    def make_reverse_iterator(self, data: List[T]) -> ReverseGraphIterator[T]:
        """Создает обратный итератор для данных"""
        return ReverseGraphIterator(data)

    def make_bidirectional_iterator(self, data: List[T]) -> BidirectionalIterator[T]:
        """Создает двунаправленный итератор для данных"""
        return BidirectionalIterator(data)

    def filter(self, iterator: ABCIterator[T], predicate: Callable[[T], bool]) -> List[T]:
        """Фильтрует элементы итератора по условию"""
        return [item for item in iterator if predicate(item)]

    def map(self, iterator: ABCIterator[T], func: Callable[[T], Any]) -> List[Any]:
        """Применяет функцию к каждому элементу и возвращает список результатов"""
        return [func(item) for item in iterator]