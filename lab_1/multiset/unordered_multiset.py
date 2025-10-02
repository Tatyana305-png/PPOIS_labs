import re
from collections import defaultdict
from typing import Union, List, Dict, Any
import itertools


class UnorderedMultiset:
    def __init__(self, data: Union[str, List[Any]] = None):
        """
        Инициализация мультимножества из строки или списка
        """
        self.elements = defaultdict(int)

        if data is not None:
            if isinstance(data, str):
                self._parse_string(data)
            elif isinstance(data, list):
                self._parse_list(data)

    def _parse_string(self, s: str):
        """Парсинг строки вида {a, a, c, {a, b, b}, {}, {a, {c, c}}}"""
        s = s.strip()
        if s.startswith('{') and s.endswith('}'):
            s = s[1:-1].strip()

        if not s:
            return

        elements = self._split_elements(s)

        for elem in elements:
            elem = elem.strip()
            if elem.startswith('{') and elem.endswith('}'):
                nested = UnorderedMultiset(elem)
                self.add(nested)
            elif elem:
                self.add(elem)

    def _split_elements(self, s: str) -> List[str]:
        """Разбивает строку на элементы, учитывая вложенные множества"""
        elements = []
        current = ""
        brace_count = 0

        for char in s:
            if char == '{':
                brace_count += 1
                current += char
            elif char == '}':
                brace_count -= 1
                current += char
            elif char == ',' and brace_count == 0:
                elements.append(current.strip())
                current = ""
            else:
                current += char

        if current.strip():
            elements.append(current.strip())

        return elements

    def _parse_list(self, lst: List[Any]):
        """Парсинг из списка"""
        for item in lst:
            if isinstance(item, (list, UnorderedMultiset)):
                self.add(UnorderedMultiset(item))
            else:
                self.add(str(item))

    def add(self, element: Any):
        """Добавление элемента в мультимножество"""
        if isinstance(element, UnorderedMultiset):
            key = element._get_hash_key()
        else:
            key = str(element)

        self.elements[key] += 1

    def remove(self, element: Any):
        """Удаление одного вхождения элемента"""
        if isinstance(element, UnorderedMultiset):
            key = element._get_hash_key()
        else:
            key = str(element)

        if key in self.elements and self.elements[key] > 0:
            self.elements[key] -= 1
            if self.elements[key] == 0:
                del self.elements[key]

    def count(self, element: Any) -> int:
        """Подсчет количества вхождений элемента"""
        if isinstance(element, UnorderedMultiset):
            key = element._get_hash_key()
        else:
            key = str(element)

        return self.elements.get(key, 0)

    def _get_hash_key(self) -> str:
        """Генерация ключа для хеширования множества"""
        items = []
        for elem, count in sorted(self.elements.items()):
            items.append(f"{elem}:{count}")
        return "{" + ",".join(items) + "}"

    def __contains__(self, element: Any) -> bool:
        """Проверка наличия элемента"""
        return self.count(element) > 0

    def __eq__(self, other: 'UnorderedMultiset') -> bool:
        """Проверка равенства множеств"""
        if not isinstance(other, UnorderedMultiset):
            return False

        return dict(self.elements) == dict(other.elements)

    def __add__(self, other: 'UnorderedMultiset') -> 'UnorderedMultiset':
        """Объединение множеств"""
        result = UnorderedMultiset()

        for elem, count in self.elements.items():
            result.elements[elem] = count

        for elem, count in other.elements.items():
            result.elements[elem] = result.elements.get(elem, 0) + count

        return result

    def __sub__(self, other: 'UnorderedMultiset') -> 'UnorderedMultiset':
        """Разность множеств"""
        result = UnorderedMultiset()

        for elem, count in self.elements.items():
            other_count = other.elements.get(elem, 0)
            new_count = max(0, count - other_count)
            if new_count > 0:
                result.elements[elem] = new_count

        return result

    def __len__(self) -> int:
        """Общее количество элементов (с учетом кратности)"""
        return sum(self.elements.values())

    def unique_count(self) -> int:
        """Количество уникальных элементов"""
        return len(self.elements)

    # НОВЫЕ МЕТОДЫ:

    def is_empty(self) -> bool:
        """Проверка на пустое множество"""
        return len(self.elements) == 0

    def __iadd__(self, other: 'UnorderedMultiset') -> 'UnorderedMultiset':
        """Оператор += для объединения"""
        for elem, count in other.elements.items():
            self.elements[elem] += count
        return self

    def __isub__(self, other: 'UnorderedMultiset') -> 'UnorderedMultiset':
        """Оператор -= для разности"""
        for elem, count in other.elements.items():
            if elem in self.elements:
                self.elements[elem] = max(0, self.elements[elem] - count)
                if self.elements[elem] == 0:
                    del self.elements[elem]
        return self

    def __mul__(self, other: 'UnorderedMultiset') -> 'UnorderedMultiset':
        """Пересечение двух множеств (оператор *)"""
        result = UnorderedMultiset()
        for elem in self.elements:
            if elem in other.elements:
                result.elements[elem] = min(self.elements[elem], other.elements[elem])
        return result

    def __imul__(self, other: 'UnorderedMultiset') -> 'UnorderedMultiset':
        """Оператор *= для пересечения"""
        elements_to_remove = []
        for elem in self.elements:
            if elem in other.elements:
                self.elements[elem] = min(self.elements[elem], other.elements[elem])
            else:
                elements_to_remove.append(elem)

        for elem in elements_to_remove:
            del self.elements[elem]
        return self

    def power_set(self) -> List['UnorderedMultiset']:
        """Построение булеана - множества всех подмножеств"""
        # Создаем список всех элементов с учетом кратности
        all_elements = []
        for elem, count in self.elements.items():
            for i in range(count):
                if elem.startswith('{') and elem.endswith('}'):
                    # Для вложенных множеств создаем новый объект
                    nested_ms = UnorderedMultiset(elem)
                    all_elements.append(nested_ms)
                else:
                    all_elements.append(elem)

        # Генерируем все возможные подмножества
        result = []
        n = len(all_elements)

        # Проходим по всем возможным размерам подмножеств
        for size in range(n + 1):
            # Генерируем все комбинации данного размера
            for indices in itertools.combinations(range(n), size):
                subset = UnorderedMultiset()
                for idx in indices:
                    subset.add(all_elements[idx])
                result.append(subset)

        return result

    def __str__(self) -> str:
        """Строковое представление"""
        items = []
        for elem, count in self.elements.items():
            for _ in range(count):
                if elem.startswith('{') and elem.endswith('}'):
                    items.append(elem)
                else:
                    items.append(elem)
        return "{" + ", ".join(str(item) for item in items) + "}"

    def __repr__(self) -> str:
        return f"UnorderedMultiset('{str(self)}')"


# ТЕСТИРОВАНИЕ НОВЫХ ФУНКЦИЙ
if __name__ == "__main__":
    # Тест проверки на пустое множество
    print("1. Проверка на пустое множество:")
    empty_ms = UnorderedMultiset()
    print(f"   Пустое множество: {empty_ms.is_empty()}")  # True

    non_empty_ms = UnorderedMultiset("{a, b}")
    print(f"   Непустое множество: {non_empty_ms.is_empty()}")  # False
    print()

    # Тест операторов += и -=
    print("2. Операторы += и -=:")
    ms1 = UnorderedMultiset("{x, y}")
    ms2 = UnorderedMultiset("{y, z}")
    ms1 += ms2
    print(f"   После +=: {ms1}")  # {x, y, y, z}

    ms1 -= UnorderedMultiset("{y}")
    print(f"   После -=: {ms1}")  # {x, y, z}
    print()

    # Тест пересечения множеств
    print("3. Пересечение множеств:")
    ms3 = UnorderedMultiset("{a, a, b, c}")
    ms4 = UnorderedMultiset("{a, b, b, d}")
    intersection = ms3 * ms4
    print(f"   {ms3} ∩ {ms4} = {intersection}")  # {a, b}

    ms3 *= ms4
    print(f"   После *=: {ms3}")  # {a, b}
    print()

    # Тест булеана
    print("4. Булеан множества:")
    simple_ms = UnorderedMultiset("{a, b}")
    boolean = simple_ms.power_set()
    print(f"   Булеан множества {simple_ms}:")
    for i, subset in enumerate(boolean):
        print(f"   {i + 1}. {subset}")

    print(f"   Всего подмножеств: {len(boolean)}")  # Должно быть 2^n = 4
