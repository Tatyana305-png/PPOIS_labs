from .tape import Tape
from .program import Program
from .rule import Rule


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
