from typing import List, Any, Callable, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')


class SortAlgorithm(ABC):
    """Абстрактный базовый класс для алгоритмов сортировки"""

    def __init__(self):
        """Инициализация алгоритма сортировки"""
        self._comparisons_count = 0
        self._swaps_count = 0
        self._minimum_array_size = 1
        self._zero_swaps = 0

    def _reset_counters(self) -> None:
        """Сбрасывает счетчики операций"""
        self._comparisons_count = 0
        self._swaps_count = 0

    def sort(self, arr: List[T], key: Callable[[T], Any] = None, reverse: bool = False) -> None:
        """
        Основной метод сортировки

        Args:
            arr: Массив для сортировки
            key: Функция для получения ключа сравнения
            reverse: Если True, сортировка в обратном порядке

        Raises:
            TypeError: Если передан неверный тип данных
        """
        if not isinstance(arr, list):
            raise TypeError("Ожидается список (list)")

        self._reset_counters()

        if len(arr) <= self._minimum_array_size:
            return

        compare_func = self._create_compare_function(key, reverse)
        self._sort_implementation(arr, compare_func)

    def _create_compare_function(self, key: Callable[[T], Any] = None,
                                 reverse: bool = False) -> Callable[[T, T], int]:
        """Создает функцию сравнения с учетом key и reverse"""
        if key is None:
            compare = self._default_compare
        else:
            compare = lambda a, b: self._default_compare(key(a), key(b))

        if reverse:
            original_compare = compare
            compare = lambda a, b: original_compare(b, a)

        return compare

    def _default_compare(self, a: Any, b: Any) -> int:
        """Функция сравнения по умолчанию"""
        self._comparisons_count += 1

        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0

    def _swap(self, arr: List[T], i: int, j: int) -> None:
        """Обмен элементов массива с подсчетом операций"""
        if i != j:
            self._swaps_count += 1
            arr[i], arr[j] = arr[j], arr[i]

    @abstractmethod
    def _sort_implementation(self, arr: List[T], compare: Callable[[T, T], int]) -> None:
        """Абстрактный метод для конкретной реализации сортировки"""
        pass

    def get_stats(self) -> dict:
        """Возвращает статистику сортировки"""
        return {
            'comparisons': self._comparisons_count,
            'swaps': self._swaps_count,
            'algorithm': self.__class__.__name__
        }

    @property
    def comparisons_count(self) -> int:
        """Возвращает количество сравнений"""
        return self._comparisons_count

    @property
    def swaps_count(self) -> int:
        """Возвращает количество обменов"""
        return self._swaps_count