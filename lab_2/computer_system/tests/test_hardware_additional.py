import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.cpu import CPU, CPUCore
from hardware.memory import RAM, MemoryModule
from hardware.storage import StorageDevice, HardDrive, SSD
from hardware.motherboard import Motherboard, BIOS
from hardware.peripherals import Peripheral, Keyboard, Mouse, Monitor
from exceptions.hardware_exceptions import HardwareIncompatibilityException


class TestCPUAdditional:
    def test_cpu_multiple_instructions(self):
        cpu = CPU("AMD", "Ryzen 5", 6, 3.6)
        for i in range(5):
            result = cpu.execute_instruction(f"MOV R{i}, #{i}")
            assert "Выполнена инструкция" in result
        assert cpu.temperature > 35.0
        assert cpu.usage > 0

    def test_cpu_core_task_management(self):
        core = CPUCore(0, 4.2)
        test_task = "calculation_task"

        core.assign_task(test_task)
        assert core.current_task == test_task
        assert core.is_active

        core.release_task()
        assert core.current_task is None
        assert not core.is_active


class TestMemoryAdditional:
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


class TestStorageAdditional:
    def test_storage_device_base_class(self):
        storage = StorageDevice(1000, "TestType")
        assert storage.capacity == 1000
        assert storage.type == "TestType"
        assert storage.used_space == 0

    def test_hard_drive_initialization(self):
        hdd = HardDrive(1000000, 7200)
        assert hdd.capacity == 1000000
        assert hdd.type == "HDD"
        assert hdd.rpm == 7200
        # Test defragment doesn't crash
        hdd.defragment()

    def test_ssd_health_calculation(self):
        ssd = SSD(500000, "NVMe")
        health = ssd.get_health_status()
        assert 0 <= health <= 100

        # Test after some usage
        ssd.used_space = 100000
        health_after_usage = ssd.get_health_status()
        assert health_after_usage < health

    def test_storage_file_operations(self):
        ssd = SSD(1000, "SATA")

        # Store multiple files
        ssd.store_file("file1.txt", b"content1")
        ssd.store_file("file2.txt", b"content2")

        assert ssd.used_space == 16
        assert len(ssd.files) == 2

        # Read files
        content1 = ssd.read_file("file1.txt")
        content2 = ssd.read_file("file2.txt")
        assert content1 == b"content1"
        assert content2 == b"content2"

        # Calculate hashes
        hash1 = ssd.calculate_hash("file1.txt")
        hash2 = ssd.calculate_hash("file2.txt")
        assert len(hash1) == 64
        assert hash1 != hash2

    def test_storage_encryption_integration(self):
        ssd = SSD(1000, "SATA")

        class MockEncryption:
            def encrypt(self, data):
                return b"encrypted_" + data

            def decrypt(self, data):
                return data.replace(b"encrypted_", b"")

        encryption = MockEncryption()
        ssd.store_file("secret.txt", b"data", encryption)

        # File should be stored encrypted
        assert b"encrypted_data" in ssd.files["secret.txt"]

        # Read with decryption
        content = ssd.read_file("secret.txt", encryption)
        assert content == b"data"


class TestMotherboardAdditional:
    def test_motherboard_comprehensive(self):
        mb = Motherboard("Gigabyte", "X570")
        cpu = CPU("AMD", "Ryzen 7", 8, 3.8)
        ram = RAM(32768)

        mb.install_cpu(cpu)
        mb.install_ram(ram, 0)

        assert mb.cpu_socket == cpu
        assert mb.ram_slots[0] == ram
        assert mb.get_total_ram() == 32768

    def test_motherboard_device_connections(self):
        mb = Motherboard("MSI", "B550")
        keyboard = Keyboard("QWERTY", True)

        mb.connect_device(keyboard, "USB1")
        assert mb.connected_devices["USB1"] == keyboard

    def test_bios_comprehensive(self):
        bios = BIOS("2.1")

        bios.update_setting("boot_order", ["SSD", "USB", "Network"])
        bios.update_setting("secure_boot", True)

        assert bios.settings["boot_order"] == ["SSD", "USB", "Network"]
        assert bios.settings["secure_boot"] is True

        bios.set_boot_order(["USB", "SSD"])
        assert bios.boot_order == ["USB", "SSD"]

        # POST should return True
        assert bios.perform_post() is True


class TestPeripheralsAdditional:
    def test_peripheral_base_class(self):
        peripheral = Peripheral("Scanner", "USB")
        assert peripheral.name == "Scanner"
        assert peripheral.connection_type == "USB"
        assert not peripheral.is_connected

        peripheral.connect()
        assert peripheral.is_connected

        peripheral.disconnect()
        assert not peripheral.is_connected

    def test_keyboard_comprehensive(self):
        keyboard = Keyboard("AZERTY", True)

        # Test multiple key presses
        keys = ["A", "B", "Ctrl", "S"]
        for key in keys:
            keyboard.key_press(key)

        assert len(keyboard.pressed_keys) == 4
        assert keyboard.get_key_combination() == keys

        # Test backlight
        assert keyboard.backlight is True

    def test_mouse_comprehensive(self):
        mouse = Mouse(3200, 6)

        # Test multiple movements
        positions = [(100, 200), (150, 250), (200, 300)]
        for pos in positions:
            mouse.move(pos[0], pos[1])

        assert mouse.position == (200, 300)

        # Test all buttons
        for button in range(1, mouse.buttons + 1):
            result = mouse.click(button)
            assert f"кнопка мыши: {button}" in result

    def test_monitor_comprehensive(self):
        monitor = Monitor((2560, 1440), 144)

        # Test resolution changes
        resolutions = [(1920, 1080), (1280, 720), (3840, 2160)]
        for res in resolutions:
            monitor.set_resolution(res[0], res[1])
            assert monitor.current_resolution == res

        # Test brightness adjustments
        for brightness in [0, 25, 50, 75, 100, 150, -10]:
            monitor.adjust_brightness(brightness)
            assert 0 <= monitor.brightness <= 100