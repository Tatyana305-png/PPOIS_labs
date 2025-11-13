from .MemoryModule import MemoryModule


class RAM:
    def __init__(self, total_capacity: int):
        self.total_capacity = total_capacity
        self.modules = []
        self.memory_controller = None
        self.dual_channel_enabled = False
        self.xmp_profile = False

    def add_module(self, module: MemoryModule):
        """Добавление модуля памяти"""
        self.modules.append(module)
        print(f"Добавлен модуль памяти: {module.capacity}MB {module.type}")

    def remove_module(self, index: int):
        """Удаление модуля памяти"""
        if 0 <= index < len(self.modules):
            module = self.modules.pop(index)
            print(f"Удален модуль памяти: {module.capacity}MB")
        else:
            print("Неверный индекс модуля")

    def get_total_allocated(self) -> int:
        """Получение общего объема выделенной памяти"""
        return sum(module.allocated_memory for module in self.modules)

    def get_total_capacity(self) -> int:
        """Получение общей емкости памяти"""
        return sum(module.capacity for module in self.modules)

    def enable_dual_channel(self):
        """Включение двухканального режима"""
        self.dual_channel_enabled = True
        print("Двухканальный режим включен")

    def enable_xmp(self):
        """Включение XMP профиля"""
        self.xmp_profile = True
        print("XMP профиль активирован")

    def get_ram_info(self) -> dict:
        """Получение информации о RAM"""
        total_allocated = self.get_total_allocated()
        total_capacity = self.get_total_capacity()

        return {
            'total_capacity': total_capacity,
            'total_allocated': total_allocated,
            'free_memory': total_capacity - total_allocated,
            'modules_count': len(self.modules),
            'dual_channel': self.dual_channel_enabled,
            'xmp_enabled': self.xmp_profile,
            'utilization': (total_allocated / total_capacity) * 100 if total_capacity > 0 else 0
        }

    def clear_memory(self):
        """Очистка всей памяти"""
        for module in self.modules:
            module.memory_map.clear()
            module.allocated_memory = 0
        print("Вся память очищена")