from typing import List, Callable, Any
from SortAlgorithm import SortAlgorithm, T


class Smoothsort(SortAlgorithm):
    """Реализация алгоритма Smoothsort на основе рабочей версии"""

    def __init__(self):
        """Инициализация Smoothsort"""
        super().__init__()
        self._leonardo_numbers = []

    def _sort_implementation(self, arr: List[T], compare: Callable[[T, T], int]) -> None:
        """Основная реализация сортировки Smoothsort"""
        array_size = len(arr)
        if array_size < 2:
            return

        # Генерируем числа Леонардо
        self._build_leonardo_numbers(array_size)

        # Порядки куч в лесу
        heap_orders = []

        # Фаза построения леса
        for current_index in range(array_size):
            self._add_to_forest(heap_orders)
            self._heapify_up_down(arr, current_index, heap_orders, compare)

        # Фаза разборки леса
        for current_index in range(array_size - 1, -1, -1):
            if heap_orders[-1] < 2:
                heap_orders.pop()
            else:
                order = heap_orders.pop()
                right_root, right_order, left_root, left_order = self._split_tree(
                    current_index, order
                )

                heap_orders.append(left_order)
                self._heapify_up_down(arr, left_root, heap_orders, compare)

                heap_orders.append(right_order)
                self._heapify_up_down(arr, right_root, heap_orders, compare)

    def _build_leonardo_numbers(self, limit: int) -> None:
        """Строит список чисел Леонардо, не превышающих limit"""
        self._leonardo_numbers = []
        a, b = 1, 1
        while a <= limit:
            self._leonardo_numbers.append(a)
            a, b = b, a + b + 1

    def _split_tree(self, root_idx: int, order: int):
        """
        Для корня дерева Леонардо возвращает индексы корней двух поддеревьев.

        Returns:
            tuple: (right_root, right_order, left_root, left_order)
        """
        if order < 2:
            return None, None, None, None

        right_root = root_idx - 1
        right_order = order - 2

        if right_order < 0 or right_order >= len(self._leonardo_numbers):
            return None, None, None, None

        left_root = right_root - self._leonardo_numbers[right_order]
        left_order = order - 1

        return right_root, right_order, left_root, left_order

    def _add_to_forest(self, heap_orders: List[int]) -> None:
        """Добавляет новый элемент в лес куч"""
        if len(heap_orders) >= 2 and heap_orders[-2] == heap_orders[-1] + 1:
            heap_orders.pop()
            heap_orders[-1] += 1
        else:
            if heap_orders and heap_orders[-1] == 1:
                heap_orders.append(0)
            else:
                heap_orders.append(1)

    def _heapify_up_down(self, arr: List[T], current_idx: int,
                         heap_orders: List[int], compare: Callable[[T, T], int]) -> None:
        """
        Восстанавливает свойства леса деревьев Леонардо:
        сначала двигаем корень вверх между деревьями, затем просеиваем вниз.
        """
        position = len(heap_orders) - 1
        order = heap_orders[position]

        # Подъем корня вверх по деревьям
        while position > 0:
            parent_idx = current_idx - self._leonardo_numbers[order]

            if parent_idx < 0:
                break

            # Проверяем, нужно ли поднимать элемент
            if compare(arr[parent_idx], arr[current_idx]) > 0:
                # Для деревьев порядка 0 или 1 просто меняем
                if order < 2:
                    self._swap(arr, current_idx, parent_idx)
                    current_idx = parent_idx
                    position -= 1
                    if position >= 0:
                        order = heap_orders[position]
                    else:
                        break
                else:
                    # Проверяем детей родителя
                    left_child_idx = current_idx - 1
                    right_child_idx = current_idx - 2

                    if left_child_idx < 0 or right_child_idx < 0:
                        break

                    parent_is_largest = (
                            compare(arr[parent_idx], arr[left_child_idx]) > 0 and
                            compare(arr[parent_idx], arr[right_child_idx]) > 0
                    )

                    if parent_is_largest:
                        self._swap(arr, current_idx, parent_idx)
                        current_idx = parent_idx
                        position -= 1
                        if position >= 0:
                            order = heap_orders[position]
                        else:
                            break
                    else:
                        break
            else:
                break

        # Просеивание вниз внутри одного дерева
        while order >= 2:
            result = self._split_tree(current_idx, order)
            if result[0] is None:
                break

            right_root, right_order, left_root, left_order = result

            # Проверяем индексы
            if (right_root < 0 or right_root >= len(arr) or
                    left_root < 0 or left_root >= len(arr)):
                break

            # Выбираем большего ребенка
            if compare(arr[right_root], arr[left_root]) > 0:
                child_idx = right_root
                child_order = right_order
            else:
                child_idx = left_root
                child_order = left_order

            if compare(arr[current_idx], arr[child_idx]) < 0:
                self._swap(arr, current_idx, child_idx)
                current_idx = child_idx
                order = child_order
            else:
                break

    def __str__(self) -> str:
        return "Smoothsort (гладкая сортировка)"