import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Memory.RAM import RAM
from Hardware.Memory.MemoryModule import MemoryModule

class TestRAM:
    def test_ram_initialization(self):
        ram = RAM(16384)
        assert ram.total_capacity == 16384
        assert ram.modules == []
        assert ram.dual_channel_enabled == False
        assert ram.xmp_profile == False

    def test_ram_add_module(self):
        ram = RAM(32768)
        module = MemoryModule(8192, 3200, "DDR4")
        ram.add_module(module)
        assert len(ram.modules) == 1
        assert ram.modules[0] == module

    def test_ram_remove_module(self):
        ram = RAM(16384)
        module = MemoryModule(8192, 3200, "DDR4")
        ram.add_module(module)
        assert len(ram.modules) == 1

        ram.remove_module(0)
        assert len(ram.modules) == 0

    def test_ram_get_total_allocated(self):
        ram = RAM(16384)
        module1 = MemoryModule(8192, 3200, "DDR4")
        module2 = MemoryModule(8192, 3200, "DDR4")
        ram.add_module(module1)
        ram.add_module(module2)

        # Выделяем память в модулях
        module1.allocate_memory(1024, "process1")
        module2.allocate_memory(2048, "process2")

        total_allocated = ram.get_total_allocated()
        assert total_allocated == 3072

    def test_ram_get_total_capacity(self):
        ram = RAM(16384)
        module1 = MemoryModule(8192, 3200, "DDR4")
        module2 = MemoryModule(8192, 3200, "DDR4")
        ram.add_module(module1)
        ram.add_module(module2)

        total_capacity = ram.get_total_capacity()
        assert total_capacity == 16384

    def test_ram_enable_dual_channel(self):
        ram = RAM(16384)
        ram.enable_dual_channel()
        assert ram.dual_channel_enabled == True

    def test_ram_enable_xmp(self):
        ram = RAM(16384)
        ram.enable_xmp()
        assert ram.xmp_profile == True

    def test_ram_get_ram_info(self):
        ram = RAM(16384)
        module = MemoryModule(8192, 3200, "DDR4")
        ram.add_module(module)

        info = ram.get_ram_info()
        assert info['total_capacity'] == 8192
        assert info['total_allocated'] == 0
        assert info['free_memory'] == 8192
        assert info['modules_count'] == 1
        assert info['dual_channel'] == False
        assert info['xmp_enabled'] == False
        assert info['utilization'] == 0.0

    def test_ram_clear_memory(self):
        ram = RAM(16384)
        module = MemoryModule(8192, 3200, "DDR4")
        ram.add_module(module)

        module.allocate_memory(1024, "process1")
        assert module.allocated_memory == 1024

        ram.clear_memory()
        assert module.allocated_memory == 0
        assert len(module.memory_map) == 0