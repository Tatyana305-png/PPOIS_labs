from typing import List
from Student import Student

class StudentFactory:
    """Фабрика для создания студентов и тестовых данных"""

    def __init__(self):
        """Инициализация фабрики"""
        self._default_students = [
            ("Анна", 20, 4.5),
            ("Иван", 22, 3.8),
            ("Мария", 21, 4.9),
            ("Петр", 19, 3.5),
            ("Ольга", 23, 4.2),
            ("Алексей", 20, 3.9),
            ("Екатерина", 22, 4.7),
            ("Дмитрий", 21, 3.2)
        ]

    def create_student(self, name: str, age: int, gpa: float) -> Student:
        """Создает объект студента"""
        return Student(name, age, gpa)

    def create_sample_students(self) -> List[Student]:
        """Создает список тестовых студентов"""
        return [self.create_student(name, age, gpa)
                for name, age, gpa in self._default_students]

    def create_students_sorted_by_name(self) -> List[Student]:
        """Создает список студентов, отсортированных по имени"""
        students = self.create_sample_students()
        return sorted(students, key=lambda s: s.name)

    def create_students_sorted_by_age(self) -> List[Student]:
        """Создает список студентов, отсортированных по возрасту"""
        students = self.create_sample_students()
        return sorted(students, key=lambda s: s.age)

    def create_students_sorted_by_gpa(self) -> List[Student]:
        """Создает список студентов, отсортированных по среднему баллу"""
        students = self.create_sample_students()
        return sorted(students, key=lambda s: s.gpa, reverse=True)