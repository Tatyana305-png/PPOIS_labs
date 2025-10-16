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
