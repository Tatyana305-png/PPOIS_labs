class Student:
    """Класс для представления студента"""

    def __init__(self, name: str = "", age: int = 0, gpa: float = 0.0):
        """
        Инициализация объекта студента

        Args:
            name: Имя студента
            age: Возраст студента
            gpa: Средний балл успеваемости
        """
        self._name = name
        self._age = age
        self._gpa = gpa

    @property
    def name(self) -> str:
        """Возвращает имя студента"""
        return self._name

    @property
    def age(self) -> int:
        """Возвращает возраст студента"""
        return self._age

    @property
    def gpa(self) -> float:
        """Возвращает средний балл студента"""
        return self._gpa

    def __eq__(self, other: object) -> bool:
        """Проверка на равенство двух студентов"""
        if not isinstance(other, Student):
            return False
        return (self._name == other._name and
                self._age == other._age and
                self._gpa == other._gpa)

    def __lt__(self, other: 'Student') -> bool:
        """Сравнение для сортировки по умолчанию (по имени)"""
        if not isinstance(other, Student):
            return NotImplemented
        return self._name < other._name

    def __repr__(self) -> str:
        """Строковое представление для отладки"""
        return f"Student(name='{self._name}', age={self._age}, gpa={self._gpa})"

    def __str__(self) -> str:
        """Человекочитаемое строковое представление"""
        return f"{self._name}, {self._age} лет, средний балл: {self._gpa:.2f}"
