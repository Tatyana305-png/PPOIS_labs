from Exceptions.MemoryAllocationException import MemoryAllocationException


class MemoryModule:
    def __init__(self, capacity: int, speed: int, type: str):
        self.capacity = capacity
        self.speed = speed
        self.type = type
        self.allocated_memory = 0
        self.memory_map = {}
        self.manufacturer = "Unknown"
        self.cas_latency = 16

    def allocate_memory(self, size: int, process_id: str) -> int:
        """Выделение памяти для процесса"""
        if self.allocated_memory + size > self.capacity:
            raise MemoryAllocationException("Недостаточно памяти")

        address = self.allocated_memory
        self.memory_map[process_id] = (address, size)
        self.allocated_memory += size
        print(f"Выделено {size} байт памяти для процесса {process_id}")
        return address

    def free_memory(self, process_id: str):
        """Освобождение памяти процесса"""
        if process_id in self.memory_map:
            address, size = self.memory_map[process_id]
            self.allocated_memory -= size
            del self.memory_map[process_id]
            print(f"Освобождено {size} байт памяти от процесса {process_id}")
        else:
            print(f"Процесс {process_id} не найден в памяти")

    def get_memory_info(self) -> dict:
        """Получение информации о памяти"""
        return {
            'capacity': self.capacity,
            'allocated': self.allocated_memory,
            'free': self.capacity - self.allocated_memory,
            'speed': self.speed,
            'type': self.type,
            'utilization': (self.allocated_memory / self.capacity) * 100
        }

    def defragment(self):
        """Дефрагментация памяти"""
        print(f"Дефрагментация модуля памяти {self.type}...")
        # Логика дефрагментации
        self.allocated_memory = sum(size for _, size in self.memory_map.values())

    def get_processes(self) -> list:
        """Получение списка процессов в памяти"""
        return list(self.memory_map.keys())