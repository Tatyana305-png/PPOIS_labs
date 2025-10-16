from typing import Optional
from .rule import Rule


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
