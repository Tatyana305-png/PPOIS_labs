import unittest
import io
import sys
from core.tape import Tape
from core.rule import Rule
from core.program import Program
from core.machine import TuringMachine


class TestTape(unittest.TestCase):
    """Тесты для класса Tape"""

    def test_tape_initialization(self):
        """Тест инициализации ленты"""
        tape = Tape("101")
        self.assertEqual(tape.read(), '1')
        self.assertEqual(tape.head_position, 0)

    def test_tape_read_write(self):
        """Тест чтения и записи на ленту"""
        tape = Tape("101")
        self.assertEqual(tape.read(), '1')

        tape.write('0')
        self.assertEqual(tape.read(), '0')

    def test_tape_movement(self):
        """Тест движения головки"""
        tape = Tape("101")
        tape.move_right()
        self.assertEqual(tape.head_position, 1)
        self.assertEqual(tape.read(), '0')

        tape.move_left()
        self.assertEqual(tape.head_position, 0)

    def test_tape_blank_symbol(self):
        """Тест работы с пустыми символами"""
        tape = Tape("")
        self.assertEqual(tape.read(), ' ')  # Пустой символ по умолчанию

        tape.write('A')
        self.assertEqual(tape.read(), 'A')

        tape.write(' ')  # Записываем пустой символ
        self.assertEqual(tape.read(), ' ')

    def test_tape_load_from_stream(self):
        """Тест загрузки ленты из потока"""
        tape = Tape()
        stream = io.StringIO("Hello")
        tape.load_from_stream(stream)

        self.assertEqual(tape.read(), 'H')
        tape.move_right()
        self.assertEqual(tape.read(), 'e')


class TestRule(unittest.TestCase):
    """Тесты для класса Rule"""

    def test_rule_creation(self):
        """Тест создания правила"""
        rule = Rule("q0", "0", "q1", "1", "R")
        self.assertEqual(rule.current_state, "q0")
        self.assertEqual(rule.read_symbol, "0")
        self.assertEqual(rule.next_state, "q1")
        self.assertEqual(rule.write_symbol, "1")
        self.assertEqual(rule.direction, "R")

    def test_rule_matching(self):
        """Тест проверки соответствия правила"""
        rule = Rule("q0", "0", "q1", "1", "R")

        self.assertTrue(rule.matches("q0", "0"))
        self.assertFalse(rule.matches("q0", "1"))
        self.assertFalse(rule.matches("q1", "0"))

    def test_rule_string_representation(self):
        """Тест строкового представления правила"""
        rule = Rule("q0", "0", "q1", "1", "R")
        expected = "q0 0 -> q1 1 R"
        self.assertEqual(str(rule), expected)


class TestProgram(unittest.TestCase):
    """Тесты для класса Program"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.program = Program()

    def test_add_rule(self):
        """Тест добавления правила"""
        rule = Rule("q0", "0", "q1", "1", "R")
        self.program.add_rule(rule)

        self.assertEqual(len(self.program.rules), 1)
        self.assertIn("0", self.program.alphabet)
        self.assertIn("1", self.program.alphabet)
        self.assertIn("q0", self.program.states)
        self.assertIn("q1", self.program.states)

    def test_get_rule(self):
        """Тест поиска правила"""
        rule1 = Rule("q0", "0", "q1", "1", "R")
        rule2 = Rule("q0", "1", "q1", "0", "R")
        self.program.add_rule(rule1)
        self.program.add_rule(rule2)

        found_rule = self.program.get_rule("q0", "0")
        self.assertEqual(found_rule, rule1)

        found_rule = self.program.get_rule("q0", "1")
        self.assertEqual(found_rule, rule2)

        # Правило не найдено
        found_rule = self.program.get_rule("q0", "A")
        self.assertIsNone(found_rule)

    def test_load_from_stream(self):
        """Тест загрузки программы из потока"""
        program_text = """# Тестовая программа
initial q0
final q_final

q0 0 -> q0 1 R
q0 1 -> q0 0 R
q0 _ -> q_final _ S
"""
        stream = io.StringIO(program_text)
        self.program.load_from_stream(stream)

        self.assertEqual(len(self.program.rules), 3)
        self.assertEqual(self.program.initial_state, "q0")
        self.assertIn("q_final", self.program.final_states)

    def test_remove_rule(self):
        """Тест удаления правила"""
        rule = Rule("q0", "0", "q1", "1", "R")
        self.program.add_rule(rule)
        self.assertEqual(len(self.program.rules), 1)

        self.program.remove_rule(rule)
        self.assertEqual(len(self.program.rules), 0)


class TestTuringMachine(unittest.TestCase):
    """Тесты для класса TuringMachine"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.tape = Tape("101")
        self.program = Program()

        # Создаем программу для инвертирования битов
        self.program.add_rule(Rule("q0", "0", "q0", "1", "R"))
        self.program.add_rule(Rule("q0", "1", "q0", "0", "R"))
        self.program.add_rule(Rule("q0", " ", "q_final", " ", "S"))

        self.program.initial_state = "q0"
        self.program.final_states = {"q_final"}

        self.tm = TuringMachine(self.tape, self.program)

    def test_machine_initialization(self):
        """Тест инициализации машины"""
        self.assertEqual(self.tm.current_state, "q0")
        self.assertEqual(self.tm.step_count, 0)
        self.assertFalse(self.tm.is_halted)

    def test_single_step(self):
        """Тест выполнения одного шага"""
        # Первый шаг: 1 -> 0
        result = self.tm.step()
        self.assertTrue(result)
        self.assertEqual(self.tm.step_count, 1)
        self.assertEqual(self.tm.current_state, "q0")
        self.assertEqual(self.tm.tape.read(), '0')  # 1 инвертировалось в 0

    def test_multiple_steps(self):
        """Тест выполнения нескольких шагов"""
        # Выполняем 3 шага для строки "101"
        for _ in range(3):
            self.tm.step()

        self.assertEqual(self.tm.step_count, 3)

        # После трех шагов должно быть "010", но головка будет после последнего символа
        # Поэтому проверяем содержимое ленты, игнорируя позицию головки
        tape_content = self.tm.tape.get_visible_tape(padding=2)
        # Убираем скобки и пробелы для проверки содержимого
        tape_clean = tape_content.replace('[', '').replace(']', '').replace(' ', '')
        self.assertEqual(tape_clean, "010")

        # Дополнительно проверяем, что головка на правильной позиции
        self.assertEqual(self.tm.tape.head_position, 3)

    def test_full_execution(self):
        """Тест полного выполнения программы"""
        self.tm.run(max_steps=10, log=False)

        # После выполнения строка "101" должна инвертироваться в "010"
        self.assertTrue(self.tm.is_halted)
        self.assertEqual(self.tm.current_state, "q_final")

        # Проверяем результат
        tape_content = self.tm.tape.get_visible_tape(padding=5)
        self.assertIn("010", tape_content)

    def test_machine_halt(self):
        """Тест остановки машины"""
        # Создаем машину без правил для текущего состояния
        empty_program = Program()
        empty_program.initial_state = "q0"
        tm = TuringMachine(Tape("1"), empty_program)

        # Машина должна остановиться сразу
        result = tm.step()
        self.assertFalse(result)
        self.assertTrue(tm.is_halted)

    def test_tape_manipulation(self):
        """Тест методов управления лентой"""
        self.tm.set_tape_value(5, "X")
        value = self.tm.get_tape_value(5)
        self.assertEqual(value, "X")

        # Головка должна вернуться на исходную позицию
        self.assertEqual(self.tm.tape.head_position, 0)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def test_inverter_program(self):
        """Интеграционный тест программы инвертирования"""
        # Создаем полную программу инвертирования
        program = Program()
        program.add_rule(Rule("q0", "0", "q0", "1", "R"))
        program.add_rule(Rule("q0", "1", "q0", "0", "R"))
        program.add_rule(Rule("q0", " ", "halt", " ", "S"))
        program.initial_state = "q0"
        program.final_states = {"halt"}

        # Тестируем на различных входных данных
        test_cases = [
            ("101", "010"),
            ("000", "111"),
            ("111", "000"),
            ("0101", "1010"),
            ("1", "0"),
            ("0", "1"),
        ]

        for input_data, expected_output in test_cases:
            with self.subTest(input=input_data, expected=expected_output):
                tape = Tape(input_data)
                tm = TuringMachine(tape, program)
                tm.run(max_steps=100, log=False)

                # Получаем результат (игнорируя пробелы и скобки)
                result = tm.tape.get_visible_tape(padding=10)
                result_clean = result.replace('[', '').replace(']', '').replace(' ', '')
                result_clean = result_clean.strip()

                self.assertEqual(result_clean, expected_output)

    def test_specific_uncovered_lines(self):
        """Тесты для конкретных непокрытых строк"""

        # Тест для Tape.load_from_stream с пустыми данными
        tape = Tape("original")
        stream = io.StringIO("")  # Пустой поток
        tape.load_from_stream(stream)
        self.assertEqual(tape.read(), ' ')

        # Тест для Program.load_from_stream с различными форматами
        program = Program()

        # Тест с неправильным форматом строк
        stream = io.StringIO("invalid line without arrow\nanother invalid line")
        program.load_from_stream(stream)  # Не должно упасть

        # Тест с пустой строкой после ->
        stream = io.StringIO("q0 A ->\nq1 B -> C D R")
        program.load_from_stream(stream)

        # Тест для TuringMachine.step с конечным состоянием
        tape = Tape("A")
        program = Program()
        program.add_rule(Rule("q0", "A", "q_final", "B", "S"))
        program.final_states = {"q_final"}
        tm = TuringMachine(tape, program)

        result = tm.step()
        self.assertTrue(result)
        self.assertTrue(tm.is_halted)

        # Повторный вызов step на остановленной машине
        result = tm.step()
        self.assertFalse(result)

    def test_file_loading(self):
        """Тест загрузки из файла"""
        # Создаем временный файл с программой
        import tempfile
        import os

        program_content = """initial q0
final halt
q0 0 -> q0 1 R
q0 1 -> q0 0 R
q0 _ -> halt _ S
===TAPE===
101"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tm') as f:
            f.write(program_content)
            temp_filename = f.name

        try:
            # Тестируем загрузку (упрощенная версия)
            tape = Tape()
            program = Program()

            with open(temp_filename, 'r') as f:
                lines = f.readlines()

            # Разделяем программу и ленту
            program_lines = []
            tape_line = ""
            in_tape_section = False

            for line in lines:
                if line.strip() == "===TAPE===":
                    in_tape_section = True
                elif in_tape_section:
                    tape_line = line.strip()
                else:
                    program_lines.append(line)

            # Загружаем программу
            program_stream = io.StringIO("".join(program_lines))
            program.load_from_stream(program_stream)

            # Загружаем ленту
            tape_stream = io.StringIO(tape_line)
            tape.load_from_stream(tape_stream)

            # Проверяем загрузку
            self.assertEqual(len(program.rules), 3)
            self.assertEqual(tape.read(), '1')

        finally:
            os.unlink(temp_filename)


class TestEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев и непокрытого кода"""

    def test_tape_special_cases(self):
        """Тест специальных случаев ленты"""
        # Тест get_visible_tape с разными значениями padding
        tape = Tape("ABC")
        result1 = tape.get_visible_tape(padding=0)
        result2 = tape.get_visible_tape(padding=1)
        result3 = tape.get_visible_tape(padding=10)

        self.assertIn("[A]", result1)
        self.assertIn("[A]", result2)
        self.assertIn("[A]", result3)

        # Тест движения за пределы и обновление min/max позиций
        tape = Tape("X")
        tape.move_left()
        tape.move_left()  # Два раза влево
        self.assertEqual(tape.head_position, -2)
        self.assertEqual(tape.min_position, -2)

        tape.move_right()
        tape.move_right()
        tape.move_right()  # Три раза вправо
        self.assertEqual(tape.head_position, 1)
        self.assertEqual(tape.max_position, 1)

    def test_tape_write_blank_cleanup(self):
        """Тест очистки ячеек при записи пустого символа"""
        tape = Tape("ABC")

        # Записываем в позицию 1 пустой символ
        tape.head_position = 1
        tape.write(' ')  # Должен удалить ячейку из tape dict

        # Проверяем что ячейка удалена
        self.assertNotIn(1, tape.tape)
        self.assertEqual(tape.read(), ' ')

        # Проверяем что границы обновились
        self.assertEqual(tape.min_position, 0)
        self.assertEqual(tape.max_position, 2)

    def test_program_update_sets(self):
        """Тест обновления множеств после удаления правил"""
        program = Program()

        # Тест _update_sets метода через remove_rule
        rule1 = Rule("q0", "A", "q1", "B", "R")
        rule2 = Rule("q1", "B", "q2", "C", "L")
        program.add_rule(rule1)
        program.add_rule(rule2)

        # Вызываем remove_rule чтобы активировать _update_sets
        program.remove_rule(rule1)

        # Проверяем что множества обновились
        self.assertIn("B", program.alphabet)
        self.assertIn("C", program.alphabet)
        self.assertIn("q1", program.states)
        self.assertIn("q2", program.states)

    def test_rule_direction_stay(self):
        """Тест правила с направлением 'S' (стой)"""
        tape = Tape("A")
        program = Program()
        program.add_rule(Rule("q0", "A", "q1", "B", "S"))  # Стойка
        program.initial_state = "q0"

        tm = TuringMachine(tape, program)
        tm.step()

        # Головка должна остаться на месте
        self.assertEqual(tm.tape.head_position, 0)
        self.assertEqual(tm.tape.read(), 'B')  # Символ должен быть записан
        self.assertEqual(tm.current_state, "q1")

    def test_turing_machine_empty_initialization(self):
        """Тест инициализации машины без параметров"""
        # Тест машины без программы и без ленты
        tm = TuringMachine()
        self.assertEqual(tm.current_state, "q0")
        self.assertEqual(tm.tape.read(), ' ')

        # Тест с программой но без ленты
        program = Program()
        program.add_rule(Rule("q0", " ", "q1", "X", "R"))
        tm = TuringMachine(program=program)
        self.assertEqual(tm.current_state, "q0")
        self.assertEqual(tm.tape.read(), ' ')

    def test_turing_machine_run_with_logging(self):
        """Тест выполнения с логированием"""
        tape = Tape("TEST")
        program = Program()
        program.add_rule(Rule("q0", "T", "q1", "X", "R"))
        program.add_rule(Rule("q1", "E", "halt", "Y", "S"))
        program.final_states = {"halt"}

        tm = TuringMachine(tape, program)

        # Перехватываем вывод для проверки логирования
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            tm.run(max_steps=10, log=True)

        output = f.getvalue()
        self.assertIn("Шаг", output)
        self.assertIn("Лента", output)

    def test_turing_machine_max_steps(self):
        """Тест достижения максимального количества шагов"""
        tape = Tape("AAAA")
        program = Program()
        program.add_rule(Rule("q0", "A", "q0", "A", "R"))  # Бесконечный цикл
        program.initial_state = "q0"

        tm = TuringMachine(tape, program)
        tm.run(max_steps=3, log=False)

        self.assertEqual(tm.step_count, 3)
        self.assertFalse(tm.is_halted)  # Не должна была остановиться

    def test_program_complex_parsing(self):
        """Тест сложных случаев парсинга программы"""
        program = Program()

        # Тест строк с разным количеством пробелов
        test_cases = [
            "q0  A  ->  q1  B  R",  # Много пробелов
            "  q0   A -> q1  B  R  ",  # Пробелы в начале и конце
        ]

        for test_case in test_cases:
            with self.subTest(case=test_case):
                stream = io.StringIO(test_case)
                program.load_from_stream(stream)
                self.assertEqual(len(program.rules), 1)

    def test_program_view_rules_output(self):
        """Тест вывода метода просмотра правил"""
        program = Program()
        program.add_rule(Rule("q0", "A", "q1", "B", "R"))
        program.add_rule(Rule("q1", "B", "q2", "C", "L"))

        # Перехватываем вывод
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            program.view_rules()

        output = f.getvalue()
        self.assertIn("q0 A -> q1 B R", output)
        self.assertIn("q1 B -> q2 C L", output)
        self.assertIn("0:", output)  # Нумерация правил
        self.assertIn("1:", output)

    def test_load_methods_separately(self):
        """Тест раздельной загрузки программы и ленты"""
        tm = TuringMachine()

        # Загрузка программы
        program_stream = io.StringIO("initial q0\nq0 A -> q1 B R")
        tm.load_program_from_stream(program_stream)
        self.assertEqual(tm.current_state, "q0")
        self.assertEqual(len(tm.program.rules), 1)

        # Загрузка ленты
        tape_stream = io.StringIO("NEWDATA")
        tm.load_tape_from_stream(tape_stream)
        self.assertEqual(tm.tape.read(), 'N')


class TestAdditionalCoverage(unittest.TestCase):
    """Дополнительные тесты для покрытия оставшегося кода"""

    def test_tape_special_blank_cases(self):
        """Тест специальных случаев с пустыми символами"""
        # Тест когда лента полностью пустая и мы двигаемся
        tape = Tape("")
        tape.move_right()
        tape.move_left()
        tape.move_left()  # Двигаемся в отрицательные позиции
        self.assertEqual(tape.read(), ' ')

        # Запись и чтение в отрицательных позициях
        tape.write('X')
        self.assertEqual(tape.read(), 'X')
        tape.move_right()
        self.assertEqual(tape.read(), ' ')

    def test_program_special_commands_parsing(self):
        """Тест парсинга специальных команд с разными форматами"""
        program = Program()

        # Тест команд initial и final в разных регистрах и форматах
        test_cases = [
            "INITIAL start_state",
            "FINAL end1 end2",
            "Initial q0",
            "Final halt",
        ]

        for test_case in test_cases:
            with self.subTest(case=test_case):
                stream = io.StringIO(test_case)
                program.load_from_stream(stream)
                # Главное, что не выдает с ошибкой

    def test_turing_machine_special_step_cases(self):
        """Тест специальных случаев выполнения шагов"""
        # Тест когда нет подходящего правила (должен остановиться)
        tape = Tape("X")
        program = Program()
        program.add_rule(Rule("q0", "A", "q1", "B", "R"))  # Правило для A, но у нас X
        program.initial_state = "q0"

        tm = TuringMachine(tape, program)
        result = tm.step()
        self.assertFalse(result)
        self.assertTrue(tm.is_halted)

    def test_tape_boundary_updates(self):
        """Тест обновления границ ленты при различных операциях"""
        tape = Tape("")

        # Движение в отрицательную область и запись
        tape.move_left()
        tape.write('A')
        self.assertEqual(tape.min_position, -1)

        # Движение в положительную область и запись
        tape.head_position = 5
        tape.write('B')
        self.assertEqual(tape.max_position, 5)

        # Запись пустого символа должна обновить границы
        tape.head_position = 10
        tape.write(' ')
        self.assertEqual(tape.max_position, 10)  # Все равно обновляет max_position

    def test_program_rule_management(self):
        """Тест управления правилами программы"""
        program = Program()

        # Добавление и удаление нескольких правил
        rules = [
            Rule("q0", "0", "q1", "1", "R"),
            Rule("q1", "1", "q2", "0", "L"),
            Rule("q2", "0", "q0", "1", "S")
        ]

        for rule in rules:
            program.add_rule(rule)

        self.assertEqual(len(program.rules), 3)

        # Удаление несуществующего правила не должно вызывать ошибку
        non_existent_rule = Rule("x", "y", "z", "w", "R")
        program.remove_rule(non_existent_rule)
        self.assertEqual(len(program.rules), 3)

    def test_turing_machine_initial_state_handling(self):
        """Тест обработки начального состояния"""
        # Машина с программой где initial_state не установлен
        program = Program()
        program.add_rule(Rule("q0", "A", "q1", "B", "R"))
        # Не устанавливаем program.initial_state явно

        tm = TuringMachine(program=program)
        self.assertEqual(tm.current_state, "q0")  # Должен использовать значение по умолчанию

    def test_visible_tape_edge_cases(self):
        """Тест граничных случаев отображения ленты"""
        # Лента с данными только в отрицательных позициях
        tape = Tape("")
        tape.head_position = -3
        tape.write('X')
        tape.head_position = -1
        tape.write('Y')
        tape.head_position = 0

        result = tape.get_visible_tape(padding=2)
        self.assertIn("X", result)
        self.assertIn("Y", result)

    def test_rule_comparison_and_management(self):
        """Тест сравнения и управления правилами"""
        # Создаем идентичные правила
        rule1 = Rule("q0", "A", "q1", "B", "R")
        rule2 = Rule("q0", "A", "q1", "B", "R")

        program = Program()
        program.add_rule(rule1)

        # Попытка удалить "такое же" правило (но другой объект)
        program.remove_rule(rule2)
        # Правило должно остаться, т.к. это разные объекты
        self.assertEqual(len(program.rules), 1)

def run_tests():
    """Функция для запуска тестов с красивым выводом"""
    # Создаем TestLoader для более детального вывода
    loader = unittest.TestLoader()

    # Загружаем все тесты
    suite = loader.loadTestsFromModule(sys.modules[__name__])

    # Запускаем тесты с детальным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим итоговую статистику
    print(f"\n{'=' * 50}")
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Тестов пройдено: {result.testsRun}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Провалов: {len(result.failures)}")
    print(f"Успешно: {result.testsRun - len(result.errors) - len(result.failures)}")

    if result.wasSuccessful():
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("ЕСТЬ ПРОБЛЕМЫ В ТЕСТАХ")

    return result.wasSuccessful()


if __name__ == '__main__':
    # Запуск тестов
    run_tests()
