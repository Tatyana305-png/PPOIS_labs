import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.CPU import CPU
from Hardware.Memory import RAM
from Hardware.Motherboard import Motherboard, BIOS
from Hardware.Peripherals import Keyboard

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

    def test_motherboard_comprehensive(self):
        mb = Motherboard("Gigabyte", "X570")
        cpu = CPU("AMD", "Ryzen 7", 8, 3.8)
        ram = RAM(32768)

        mb.install_cpu(cpu)
        mb.install_ram(ram, 0)

        assert mb.cpu_socket == cpu
        assert mb.ram_slots[0] == ram
        assert mb.get_total_ram() == 32768, f"Expected 32768, got {mb.get_total_ram()}"

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

class TestMotherboardFixed:
    def test_motherboard_initialization(self):
        mb = Motherboard("ASUS ROG", "Z790")
        assert mb.model == "ASUS ROG"
        assert mb.chipset == "Z790"
        assert mb.cpu_socket is None
        assert mb.ram_slots == []
        assert mb.connected_devices == {}
        assert mb.bios_version == "1.0"

    def test_motherboard_install_cpu(self):
        mb = Motherboard("ASUS ROG", "Z790")
        cpu = CPU("Intel", "Core i9", 8, 5.0)

        mb.install_cpu(cpu)
        assert mb.cpu_socket == cpu

    def test_motherboard_install_cpu_twice(self):
        mb = Motherboard("ASUS ROG", "Z790")
        cpu1 = CPU("Intel", "Core i9", 8, 5.0)
        cpu2 = CPU("AMD", "Ryzen 7", 8, 4.5)

        mb.install_cpu(cpu1)
        mb.install_cpu(cpu2)
        assert mb.cpu_socket == cpu1

    def test_motherboard_install_ram(self):
        mb = Motherboard("ASUS ROG", "Z790")
        ram = RAM(16384)

        mb.install_ram(ram, 0)
        assert len(mb.ram_slots) >= 1
        assert mb.ram_slots[0] == ram

    def test_motherboard_connect_disconnect_device(self):
        mb = Motherboard("ASUS ROG", "Z790")
        device = "GPU"  # Простой объект для теста

        mb.connect_device(device, "PCIe_x16")
        assert "PCIe_x16" in mb.connected_devices
        assert mb.connected_devices["PCIe_x16"] == device

        mb.disconnect_device("PCIe_x16")
        assert "PCIe_x16" not in mb.connected_devices

    def test_motherboard_get_total_ram(self):
        mb = Motherboard("ASUS ROG", "Z790")
        ram1 = RAM(8192)
        ram2 = RAM(8192)

        mb.install_ram(ram1, 0)
        mb.install_ram(ram2, 1)

        total_ram = mb.get_total_ram()
        assert total_ram == 16384

    def test_motherboard_get_motherboard_info(self):
        mb = Motherboard("ASUS ROG", "Z790")
        cpu = CPU("Intel", "Core i9", 8, 5.0)
        ram = RAM(16384)

        mb.install_cpu(cpu)
        mb.install_ram(ram, 0)

        info = mb.get_motherboard_info()
        assert info['model'] == "ASUS ROG"
        assert info['chipset'] == "Z790"
        assert info['cpu_installed'] == True
        assert info['ram_slots_used'] == 1
        assert info['total_ram'] == 16384

    def test_motherboard_add_ports(self):
        mb = Motherboard("ASUS ROG", "Z790")

        mb.add_pci_slot("PCIe_x16")
        mb.add_sata_port()
        mb.add_usb_port("USB 3.2")

        assert len(mb.pci_slots) == 1
        assert len(mb.sata_ports) == 1
        assert len(mb.usb_ports) == 1

    def test_motherboard_power_on_off(self):
        mb = Motherboard("ASUS ROG", "Z790")

        # Просто проверяем что методы выполняются без ошибок
        mb.power_on()
        mb.power_off()