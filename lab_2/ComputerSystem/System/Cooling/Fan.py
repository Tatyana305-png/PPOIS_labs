class Fan:
    def __init__(self, size: int, max_rpm: int):
        self.size = size
        self.max_rpm = max_rpm
        self.current_rpm = 0
        self.location = "unknown"

    def set_speed(self, rpm: int):
        self.current_rpm = min(rpm, self.max_rpm)

    def adjust_speed(self, target_temp: float):
        """Автоматическая регулировка скорости на основе температуры"""
        if target_temp > 80:
            self.set_speed(self.max_rpm)
        elif target_temp > 60:
            self.set_speed(self.max_rpm * 0.7)
        else:
            self.set_speed(self.max_rpm * 0.4)