from turing_machine import Tape, Program, Rule, TuringMachine


def create_inverter_program():
    """Создание программы для инвертирования битов"""
    prog = Program()  # Измененное имя переменной

    # Правила для инвертирования битов
    prog.add_rule(Rule("q0", "0", "q0", "1", "R"))
    prog.add_rule(Rule("q0", "1", "q0", "0", "R"))
    prog.add_rule(Rule("q0", " ", "q_final", " ", "S"))

    prog.initial_state = "q0"
    prog.final_states = {"q_final"}

    return prog


def create_copier_program():
    """Альтернативная программа для копирования строки"""
    copier = Program()

    # Правила для копирования строки
    copier.add_rule(Rule("q0", "0", "q0", "0", "R"))
    copier.add_rule(Rule("q0", "1", "q0", "1", "R"))
    copier.add_rule(Rule("q0", " ", "q_final", " ", "S"))

    copier.initial_state = "q0"
    copier.final_states = {"q_final"}

    return copier


# Демонстрация
if __name__ == "__main__":
    # Создание ленты с начальными данными
    tape = Tape("1011001")

    # Создание программы
    program = create_inverter_program()

    # Создание и запуск машины Тьюринга
    tm = TuringMachine(tape, program)

    print("Демонстрация машины Тьюринга:")
    print("Начальная лента:", tape.get_visible_tape())
    print("Правила программы:")
    program.view_rules()
    print()

    # Пошаговое выполнение с логированием
    print("Пошаговое выполнение:")
    tm.print_state()
    while tm.step():
        tm.print_state()

    print("\nФинальный результат:", tm.tape.get_visible_tape())
