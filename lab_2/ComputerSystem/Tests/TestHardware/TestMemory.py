import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Memory import RAM, MemoryModule
from Exceptions.MemoryAllocationException import MemoryAllocationException

class TestMemory:
    @pytest.fixture
    def sample_ram(self):
        ram = RAM(8192)
        module = MemoryModule(4096, 3200, "DDR4")
        ram.add_module(module)
        return ram

    def test_memory_module_initialization(self):
        module = MemoryModule(8192, 3200, "DDR4")
        assert module.capacity == 8192
        assert module.speed == 3200
        assert module.type == "DDR4"
        assert module.allocated_memory == 0

    def test_memory_allocation(self):
        module = MemoryModule(1024, 3200, "DDR4")
        address = module.allocate_memory(512, "process1")
        assert address == 0
        assert module.allocated_memory == 512
        assert "process1" in module.memory_map

    def test_memory_allocation_exception(self):
        module = MemoryModule(100, 3200, "DDR4")

        with pytest.raises(MemoryAllocationException):
            module.allocate_memory(200, "process1")

    def test_ram_initialization(self, sample_ram):
        assert sample_ram.total_capacity == 8192
        assert len(sample_ram.modules) == 1

    def test_ram_multiple_modules(self):
        ram = RAM(16384)
        module1 = MemoryModule(8192, 3200, "DDR4")
        module2 = MemoryModule(8192, 3200, "DDR4")

        ram.add_module(module1)
        ram.add_module(module2)

        assert len(ram.modules) == 2
        assert ram.get_total_allocated() == 0

    def test_memory_multiple_allocations(self):
        module = MemoryModule(2048, 3200, "DDR4")

        addr1 = module.allocate_memory(512, "process1")
        addr2 = module.allocate_memory(256, "process2")

        assert addr1 == 0
        assert addr2 == 512
        assert module.allocated_memory == 768

        module.free_memory("process1")
        assert module.allocated_memory == 256

    def test_memory_free_nonexistent(self):
        module = MemoryModule(1024, 3200, "DDR4")
        # Should not raise exception
        module.free_memory("nonexistent")

class TestMemoryModuleFixed:
    def test_memory_module_initialization(self):
        module = MemoryModule(8192, 3200, "DDR4")
        assert module.capacity == 8192
        assert module.speed == 3200
        assert module.type == "DDR4"
        assert module.allocated_memory == 0
        assert module.memory_map == {}
        assert module.manufacturer == "Unknown"
        assert module.cas_latency == 16

    def test_memory_module_allocate_memory(self):
        module = MemoryModule(8192, 3200, "DDR4")
        address = module.allocate_memory(1024, "test_process")

        assert address == 0
        assert module.allocated_memory == 1024
        assert "test_process" in module.memory_map
        assert module.memory_map["test_process"] == (0, 1024)

    def test_memory_module_allocate_memory_insufficient(self):
        module = MemoryModule(1024, 3200, "DDR4")

        with pytest.raises(MemoryAllocationException):
            module.allocate_memory(2048, "test_process")

    def test_memory_module_free_memory(self):
        module = MemoryModule(8192, 3200, "DDR4")
        module.allocate_memory(1024, "test_process")
        assert module.allocated_memory == 1024

        module.free_memory("test_process")
        assert module.allocated_memory == 0
        assert "test_process" not in module.memory_map

    def test_memory_module_free_nonexistent_process(self):
        module = MemoryModule(8192, 3200, "DDR4")
        # Не должно вызывать ошибку
        module.free_memory("nonexistent_process")

    def test_memory_module_get_memory_info(self):
        module = MemoryModule(8192, 3200, "DDR4")
        module.allocate_memory(2048, "test_process")

        info = module.get_memory_info()
        assert info['capacity'] == 8192
        assert info['allocated'] == 2048
        assert info['free'] == 6144
        assert info['speed'] == 3200
        assert info['type'] == "DDR4"
        assert info['utilization'] == 25.0

    def test_memory_module_defragment(self):
        module = MemoryModule(8192, 3200, "DDR4")
        module.allocate_memory(1024, "process1")
        module.allocate_memory(2048, "process2")

        # Просто проверяем что метод выполняется без ошибок
        module.defragment()
        assert module.allocated_memory == 3072

    def test_memory_module_get_processes(self):
        module = MemoryModule(8192, 3200, "DDR4")
        module.allocate_memory(1024, "process1")
        module.allocate_memory(2048, "process2")

        processes = module.get_processes()
        assert "process1" in processes
        assert "process2" in processes
        assert len(processes) == 2