class CPUCore:
    def __init__(self, core_id: int, speed: float):
        self.core_id = core_id
        self.speed = speed
        self.current_task = None
        self.is_active = False
        self.temperature = 35.0
        self.utilization = 0.0

    def assign_task(self, task):
        """Назначение задачи ядру"""
        self.current_task = task
        self.is_active = True
        self.utilization = 75.0
        self.temperature += 5.0
        print(f"Ядро {self.core_id}: назначена задача '{task}'")

    def release_task(self):
        """Освобождение ядра от задачи"""
        self.current_task = None
        self.is_active = False
        self.utilization = 5.0
        self.temperature = max(35.0, self.temperature - 2.0)
        print(f"Ядро {self.core_id}: задача завершена")

    def get_status(self) -> dict:
        """Получение статуса ядра"""
        return {
            'core_id': self.core_id,
            'speed': self.speed,
            'is_active': self.is_active,
            'current_task': self.current_task,
            'temperature': self.temperature,
            'utilization': self.utilization
        }

    def overclock(self, new_speed: float):
        """Разгон ядра"""
        self.speed = new_speed
        print(f"Ядро {self.core_id} разогнано до {new_speed} GHz")