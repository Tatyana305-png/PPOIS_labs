import sys
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional


class Tape:
    """Класс, реализующий ленту машины Тьюринга"""

    def __init__(self, initial_data: str = "", blank_symbol: str = " "):
        self.blank_symbol = blank_symbol
        self.tape = {}

        # Инициализация ленты начальными данными
        for i, symbol in enumerate(initial_data):
            self.tape[i] = symbol

        self.head_position = 0
        self.min_position = 0
        self.max_position = len(initial_data) - 1 if initial_data else 0

    def read(self) -> str:
        """Чтение символа под головкой"""
        return self.tape.get(self.head_position, self.blank_symbol)

    def write(self, symbol: str):
        """Запись символа под головкой"""
        if symbol != self.blank_symbol:
            self.tape[self.head_position] = symbol
        elif self.head_position in self.tape:
            del self.tape[self.head_position]

        # Обновление границ
        self.min_position = min(self.min_position, self.head_position)
        self.max_position = max(self.max_position, self.head_position)

    def move_left(self):
        """Движение головки влево"""
        self.head_position -= 1
        self.min_position = min(self.min_position, self.head_position)

    def move_right(self):
        """Движение головки вправо"""
        self.head_position += 1
        self.max_position = max(self.max_position, self.head_position)

    def get_visible_tape(self, padding: int = 5) -> str:
        """Получение видимой части ленты с padding символами вокруг головки"""
        start = min(self.min_position, self.head_position - padding)
        end = max(self.max_position, self.head_position + padding)

        result = []
        for i in range(start, end + 1):
            if i == self.head_position:
                result.append(f"[{self.tape.get(i, self.blank_symbol)}]")
            else:
                result.append(self.tape.get(i, self.blank_symbol))

        return "".join(result)

    def load_from_stream(self, stream):
        """Загрузка состояния ленты из потока"""
        data = stream.read().strip()
        self.tape.clear()

        for i, symbol in enumerate(data):
            self.tape[i] = symbol

        self.head_position = 0
        self.min_position = 0
        self.max_position = len(data) - 1 if data else 0


class Rule:
    """Класс, реализующий правило машины Тьюринга"""

    def __init__(self, current_state: str, read_symbol: str,
                 next_state: str, write_symbol: str, direction: str):
        self.current_state = current_state
        self.read_symbol = read_symbol
        self.next_state = next_state
        self.write_symbol = write_symbol
        self.direction = direction  # 'L', 'R', или 'S' (стой)

    def __str__(self):
        return f"{self.current_state} {self.read_symbol} -> {self.next_state} {self.write_symbol} {self.direction}"

    def matches(self, state: str, symbol: str) -> bool:
        """Проверяет, подходит ли правило для текущего состояния и символа"""
        return self.current_state == state and self.read_symbol == symbol


class Program:
    """Класс, реализующий программу машины Тьюринга"""

    def __init__(self):
        self.rules = []
        self.alphabet = set()
        self.states = set()
        self.initial_state = "q0"
        self.final_states = set()

    def add_rule(self, rule: Rule):
        """Добавление правила в программу"""
        self.rules.append(rule)
        self.alphabet.add(rule.read_symbol)
        self.alphabet.add(rule.write_symbol)
        self.states.add(rule.current_state)
        self.states.add(rule.next_state)

    def remove_rule(self, rule: Rule):
        """Удаление правила из программы"""
        if rule in self.rules:
            self.rules.remove(rule)
            # Обновление алфавита и состояний (упрощенная версия)
            self._update_sets()

    def get_rule(self, state: str, symbol: str) -> Optional[Rule]:
        """Поиск подходящего правила для данного состояния и символа"""
        for rule in self.rules:
            if rule.matches(state, symbol):
                return rule
        return None

    def _update_sets(self):
        """Обновление алфавита и состояний после изменений"""
        self.alphabet = set()
        self.states = set()

        for rule in self.rules:
            self.alphabet.add(rule.read_symbol)
            self.alphabet.add(rule.write_symbol)
            self.states.add(rule.current_state)
            self.states.add(rule.next_state)

    def load_from_stream(self, stream):
        """Загрузка программы из потока ввода"""
        self.rules.clear()
        self.alphabet.clear()
        self.states.clear()

        lines = stream.readlines() if hasattr(stream, 'readlines') else stream
        print(f"Загружаем программу из {len(lines)} строк")

        for line in lines:
            line = line.strip()
            print(f"Обрабатываем строку: '{line}'")

            if not line or line.startswith("#"):
                continue

            # Обрабатываем специальные команды
            if self._process_special_command(line):
                continue

            # Обрабатываем правила
            self._process_rule_line(line)

    def _process_special_command(self, line: str) -> bool:
        """Обработка специальных команд (initial, final)"""
        if line.startswith("initial"):
            parts = line.split()
            if len(parts) >= 2:
                self.initial_state = parts[1]
                print(f"Установлено начальное состояние: {self.initial_state}")
            return True

        elif line.startswith("final"):
            parts = line.split()
            if len(parts) >= 2:
                self.final_states = set(parts[1:])
                print(f"Установлены конечные состояния: {self.final_states}")
            return True

        return False

    def _process_rule_line(self, line: str):
        """Обработка строки с правилом"""
        parts = line.split()
        print(f"Части строки: {parts}")

        # Ищем позицию "->"
        if "->" in parts:
            self._parse_rule_with_arrow(parts)
        else:
            self._parse_rule_without_arrow(parts)

    def _parse_rule_with_arrow(self, parts: list):
        """Парсинг правила в формате с '->'"""
        arrow_index = parts.index("->")
        if arrow_index >= 1 and len(parts) >= arrow_index + 3:
            current_state = parts[0]
            read_symbol = parts[1]
            next_state = parts[arrow_index + 1]
            write_symbol = parts[arrow_index + 2]
            direction = parts[arrow_index + 3]

            # Для пробела используем специальное обозначение
            if read_symbol == "->":  # Если пробел пропущен
                read_symbol = " "
            if write_symbol == "->":  # Если пробел пропущен
                write_symbol = " "

            self._create_and_add_rule(current_state, read_symbol, next_state, write_symbol, direction)

    def _parse_rule_without_arrow(self, parts: list):
        """Парсинг правила в формате без '->'"""
        if len(parts) == 5:
            current_state, read_symbol, next_state, write_symbol, direction = parts
            self._create_and_add_rule(current_state, read_symbol, next_state, write_symbol, direction)

    def _create_and_add_rule(self, current_state: str, read_symbol: str,
                             next_state: str, write_symbol: str, direction: str):
        """Создание и добавление правила в программу"""
        rule = Rule(current_state, read_symbol, next_state, write_symbol, direction)
        self.add_rule(rule)
        print(f"Добавлено правило: {rule}")

    def view_rules(self):
        """Просмотр всех правил"""
        for i, rule in enumerate(self.rules):
            print(f"{i}: {rule}")


class TuringMachine:
    """Класс, реализующий абстрактную машину Тьюринга"""

    def __init__(self, tape: Tape = None, program: Program = None):
        self.tape = tape if tape else Tape()
        self.program = program if program else Program()
        self.current_state = self.program.initial_state if self.program else "q0"
        self.step_count = 0
        self.is_halted = False

    def load_program_from_stream(self, stream):
        """Загрузка программы из потока"""
        self.program.load_from_stream(stream)
        self.current_state = self.program.initial_state

    def load_tape_from_stream(self, stream):
        """Загрузка ленты из потока"""
        self.tape.load_from_stream(stream)

    def step(self) -> bool:
        """Выполнение одного шага машины"""
        if self.is_halted:
            return False

        current_symbol = self.tape.read()
        rule = self.program.get_rule(self.current_state, current_symbol)

        if rule is None:
            self.is_halted = True
            return False

        # Применение правила
        self.tape.write(rule.write_symbol)

        # Движение головки
        if rule.direction == 'L':
            self.tape.move_left()
        elif rule.direction == 'R':
            self.tape.move_right()
        # Для 'S' ничего не делаем - головка остается на месте

        self.current_state = rule.next_state
        self.step_count += 1

        # Проверка на конечное состояние
        if self.current_state in self.program.final_states:
            self.is_halted = True

        return True

    def run(self, max_steps: int = 1000, log: bool = False):
        """Выполнение программы до завершения или достижения максимального числа шагов"""
        if log:
            self.print_state()

        while self.step_count < max_steps and not self.is_halted:
            if not self.step():  # Выполняем шаг и проверяем результат
                break
            if log:
                self.print_state()

        if self.step_count >= max_steps:
            print(f"Достигнуто максимальное число шагов: {max_steps}")

    def print_state(self):
        """Вывод текущего состояния машины"""
        print(f"Шаг {self.step_count}: Состояние={self.current_state}, Лента={self.tape.get_visible_tape()}")

    def set_tape_value(self, position: int, value: str):
        """Установка значения на ленте в указанной позиции"""
        old_pos = self.tape.head_position
        self.tape.head_position = position
        self.tape.write(value)
        self.tape.head_position = old_pos

    def get_tape_value(self, position: int) -> str:
        """Получение значения с ленты в указанной позиции"""
        old_pos = self.tape.head_position
        self.tape.head_position = position
        value = self.tape.read()
        self.tape.head_position = old_pos
        return value


def main():
    """Основная функция программы"""
    if len(sys.argv) < 2:
        print("Использование: python turing_machine.py <файл> [-log]")
        print("  <файл> - файл с программой и начальным состоянием ленты")
        print("  -log   - вывод состояния после каждого шага")
        return

    filename = sys.argv[1]
    log_enabled = "-log" in sys.argv

    try:
        # Создание машины Тьюринга
        tm = TuringMachine()

        # Чтение файла
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Разделение на программу и начальную ленту
        program_lines = []
        tape_line = ""

        in_tape_section = False
        for line in lines:
            if line.strip() == "===TAPE===":
                in_tape_section = True
            elif in_tape_section:
                tape_line = line.strip()
                break
            else:
                program_lines.append(line)

        # Загрузка программы
        import io
        program_stream = io.StringIO("".join(program_lines))
        tm.load_program_from_stream(program_stream)

        # Загрузка ленты
        if tape_line:
            tape_stream = io.StringIO(tape_line)
            tm.load_tape_from_stream(tape_stream)

        print("Начальное состояние:")
        tm.print_state()
        print()

        # Запуск интерпретации
        tm.run(log=log_enabled)

        print("\nФинальное состояние:")
        tm.print_state()
        print(f"Всего шагов: {tm.step_count}")
        print(f"Результат: {tm.tape.get_visible_tape(padding=10)}")

    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
