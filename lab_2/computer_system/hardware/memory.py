from typing import List, Optional
from exceptions.hardware_exceptions import MemoryAllocationException


class MemoryModule:
    def __init__(self, capacity: int, speed: int, type: str):
        self.capacity = capacity
        self.speed = speed
        self.type = type
        self.allocated_memory = 0
        self.memory_map = {}

    def allocate_memory(self, size: int, process_id: str) -> int:
        """Выделение памяти для процесса"""
        if self.allocated_memory + size > self.capacity:
            raise MemoryAllocationException("Недостаточно памяти")

        address = self.allocated_memory
        self.memory_map[process_id] = (address, size)
        self.allocated_memory += size
        return address

    def free_memory(self, process_id: str):
        """Освобождение памяти процесса"""
        if process_id in self.memory_map:
            address, size = self.memory_map[process_id]
            self.allocated_memory -= size
            del self.memory_map[process_id]


class RAM:
    def __init__(self, total_capacity: int):
        self.total_capacity = total_capacity
        self.modules: List[MemoryModule] = []  # Инициализируем пустой список
        self.memory_controller = None

    def add_module(self, module: MemoryModule):
        """Добавление модуля памяти"""
        self.modules.append(module)

    def get_total_allocated(self) -> int:
        """Получение общего объема выделенной памяти"""
        return sum(module.allocated_memory for module in self.modules)