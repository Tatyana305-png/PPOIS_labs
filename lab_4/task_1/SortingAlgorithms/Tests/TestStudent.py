import unittest
from Student import Student
from StudentFactory import StudentFactory


class TestStudent(unittest.TestCase):
    """Тесты для класса Student"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.student1 = Student("Иван", 20, 4.5)
        self.student2 = Student("Мария", 21, 4.9)
        self.factory = StudentFactory()

    def test_initialization(self):
        """Тест инициализации студента"""
        self.assertEqual(self.student1.name, "Иван")
        self.assertEqual(self.student1.age, 20)
        self.assertEqual(self.student1.gpa, 4.5)

    def test_default_initialization(self):
        """Тест инициализации с значениями по умолчанию"""
        student = Student()
        self.assertEqual(student.name, "")
        self.assertEqual(student.age, 0)
        self.assertEqual(student.gpa, 0.0)

    def test_equality(self):
        """Тест сравнения студентов"""
        student1_copy = Student("Иван", 20, 4.5)
        self.assertEqual(self.student1, student1_copy)
        self.assertNotEqual(self.student1, self.student2)

    def test_less_than(self):
        """Тест оператора меньше"""
        self.assertTrue(self.student1 < self.student2)  # Иван < Мария
        self.assertFalse(self.student2 < self.student1)

    def test_string_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.student1), "Иван, 20 лет, средний балл: 4.50")
        self.assertEqual(repr(self.student1), "Student(name='Иван', age=20, gpa=4.5)")

    def test_properties(self):
        """Тест свойств только для чтения"""
        with self.assertRaises(AttributeError):
            self.student1.name = "Петр"
        with self.assertRaises(AttributeError):
            self.student1.age = 25
        with self.assertRaises(AttributeError):
            self.student1.gpa = 5.0


class TestStudentFactory(unittest.TestCase):
    """Тесты для класса StudentFactory"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.factory = StudentFactory()

    def test_create_student(self):
        """Тест создания студента"""
        student = self.factory.create_student("Петр", 22, 3.8)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.name, "Петр")
        self.assertEqual(student.age, 22)
        self.assertEqual(student.gpa, 3.8)

    def test_create_sample_students(self):
        """Тест создания тестовых студентов"""
        students = self.factory.create_sample_students()
        self.assertEqual(len(students), 8)
        self.assertIsInstance(students[0], Student)

    def test_create_sorted_students(self):
        """Тест создания отсортированных студентов"""
        by_name = self.factory.create_students_sorted_by_name()
        by_age = self.factory.create_students_sorted_by_age()
        by_gpa = self.factory.create_students_sorted_by_gpa()

        self.assertEqual(len(by_name), 8)
        self.assertEqual(len(by_age), 8)
        self.assertEqual(len(by_gpa), 8)

        # Проверяем сортировку по имени
        for i in range(len(by_name) - 1):
            self.assertLessEqual(by_name[i].name, by_name[i + 1].name)

        # Проверяем сортировку по возрасту
        for i in range(len(by_age) - 1):
            self.assertLessEqual(by_age[i].age, by_age[i + 1].age)

        # Проверяем сортировку по GPA (по убыванию)
        for i in range(len(by_gpa) - 1):
            self.assertGreaterEqual(by_gpa[i].gpa, by_gpa[i + 1].gpa)


if __name__ == "__main__":
    unittest.main()