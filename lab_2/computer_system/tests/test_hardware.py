import pytest
import sys
import os

# Добавляем путь к корневой директории
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.cpu import CPU, CPUCore
from hardware.memory import RAM, MemoryModule
from hardware.storage import SSD, HardDrive
from hardware.motherboard import Motherboard, BIOS
from hardware.peripherals import Keyboard, Mouse, Monitor
from exceptions.hardware_exceptions import CPUOverheatException, MemoryAllocationException, StorageFullException


class TestCPU:
    @pytest.fixture
    def sample_cpu(self):
        return CPU("Intel", "Core i7", 4, 3.2)

    def test_cpu_initialization(self, sample_cpu):
        assert sample_cpu.brand == "Intel"
        assert sample_cpu.model == "Core i7"
        assert sample_cpu.cores == 4
        assert sample_cpu.speed == 3.2
        assert sample_cpu.temperature == 35.0
        assert sample_cpu.usage == 0.0

    def test_execute_instruction(self, sample_cpu):
        result = sample_cpu.execute_instruction("ADD R1, R2")
        assert "Выполнена инструкция: ADD R1, R2" in result
        assert sample_cpu.usage > 0
        assert sample_cpu.temperature > 35.0

    def test_cpu_overheat_exception(self, sample_cpu):
        sample_cpu.thermal_threshold = 40.0
        sample_cpu.temperature = 39.0

        with pytest.raises(CPUOverheatException):
            for _ in range(10):
                sample_cpu.execute_instruction("TEST")

    def test_cpu_cool_down(self, sample_cpu):
        sample_cpu.temperature = 80.0
        sample_cpu.cool_down()
        assert sample_cpu.temperature == 70.0

    def test_cpu_core_initialization(self):
        core = CPUCore(1, 3.2)
        assert core.core_id == 1
        assert core.speed == 3.2
        assert core.current_task is None
        assert not core.is_active


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


class TestStorage:
    @pytest.fixture
    def sample_ssd(self):
        return SSD(512000, "SATA")

    def test_ssd_initialization(self, sample_ssd):
        assert sample_ssd.capacity == 512000
        assert sample_ssd.type == "SSD"
        assert sample_ssd.interface == "SATA"
        assert sample_ssd.used_space == 0

    def test_store_file(self, sample_ssd):
        result = sample_ssd.store_file("test.txt", b"Hello World")
        assert result is True
        assert sample_ssd.used_space == 11
        assert "test.txt" in sample_ssd.files

    def test_store_file_full_exception(self, sample_ssd):
        large_data = b"x" * (sample_ssd.capacity + 100)

        with pytest.raises(StorageFullException):
            sample_ssd.store_file("large.txt", large_data)


class TestMotherboard:
    @pytest.fixture
    def sample_motherboard(self):
        return Motherboard("ASUS Prime", "B460")

    @pytest.fixture
    def sample_bios(self):
        return BIOS("1.0")

    def test_motherboard_initialization(self, sample_motherboard):
        assert sample_motherboard.model == "ASUS Prime"
        assert sample_motherboard.chipset == "B460"
        assert sample_motherboard.cpu_socket is None

    def test_install_cpu(self, sample_motherboard):
        cpu = CPU("Intel", "Core i5", 4, 2.8)
        sample_motherboard.install_cpu(cpu)
        assert sample_motherboard.cpu_socket == cpu

    def test_bios_initialization(self, sample_bios):
        assert sample_bios.version == "1.0"
        assert sample_bios.settings == {}


class TestPeripherals:
    @pytest.fixture
    def sample_keyboard(self):
        return Keyboard("QWERTY", False)

    @pytest.fixture
    def sample_mouse(self):
        return Mouse(1600, 3)

    def test_keyboard_initialization(self, sample_keyboard):
        assert sample_keyboard.name == "Keyboard"
        assert sample_keyboard.connection_type == "USB"
        assert sample_keyboard.layout == "QWERTY"

    def test_keyboard_key_press(self, sample_keyboard):
        result = sample_keyboard.key_press("A")
        assert "Нажата клавиша: A" in result
        assert "A" in sample_keyboard.pressed_keys

    def test_mouse_move(self, sample_mouse):
        position = sample_mouse.move(100, 200)
        assert position == (100, 200)
        assert sample_mouse.position == (100, 200)