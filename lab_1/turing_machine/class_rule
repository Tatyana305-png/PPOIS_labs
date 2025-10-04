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
