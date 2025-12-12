from typing import List, Callable
from SortAlgorithm import SortAlgorithm, T


class PancakeSort(SortAlgorithm):
    """Реализация алгоритма Pancake Sort"""

    def __init__(self):
        """Инициализация Pancake Sort"""
        super().__init__()

    def _sort_implementation(self, arr: List[T], compare: Callable[[T, T], int]) -> None:
        """Внутренняя реализация Pancake Sort"""
        n = len(arr)

        for size in range(n, 1, -1):
            # Находим индекс максимального элемента
            max_index = self._find_max_index(arr[:size], compare)

            if max_index != size - 1:
                # Переворачиваем так, чтобы максимальный элемент оказался наверху
                if max_index != 0:
                    self._flip(arr, max_index)

                # Переворачиваем всю текущую часть
                self._flip(arr, size - 1)

    def _find_max_index(self, arr: List[T], compare: Callable[[T, T], int]) -> int:
        """Находит индекс максимального элемента в массиве"""
        max_index = 0
        for i in range(1, len(arr)):
            if compare(arr[i], arr[max_index]) > 0:
                max_index = i
        return max_index

    def _flip(self, arr: List[T], end_index: int) -> None:
        """Переворачивает часть массива от начала до end_index включительно"""
        start_index = 0
        while start_index < end_index:
            self._swap(arr, start_index, end_index)
            start_index += 1
            end_index -= 1

    def __str__(self) -> str:
        return "Pancake Sort (сортировка переворотами)"