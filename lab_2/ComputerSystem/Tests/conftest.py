import pytest
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Общие фикстуры для всех тестов
@pytest.fixture
def sample_cpu():
    from Hardware.CPU.CPU import CPU
    return CPU("Intel", "Core i5", 4, 3.5)

@pytest.fixture
def sample_ram():
    from Hardware.Memory.RAM import RAM
    return RAM(8192)

@pytest.fixture
def sample_motherboard():
    from Hardware.Motherboard.Motherboard import Motherboard
    return Motherboard("ASUS", "B550")

@pytest.fixture
def sample_ssd():
    from Hardware.Storage.SSD import SSD
    return SSD(512000, "SATA")

@pytest.fixture
def sample_keyboard():
    from Hardware.Peripherals.Keyboard import Keyboard
    return Keyboard("QWERTY", True)

@pytest.fixture
def sample_mouse():
    from Hardware.Peripherals.Mouse import Mouse
    return Mouse(1600, 3)

@pytest.fixture
def sample_monitor():
    from Hardware.Peripherals.Monitor import Monitor
    return Monitor((1920, 1080), 60)

# Маркеры для категоризации тестов
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "hardware: тесты аппаратного обеспечения"
    )
    config.addinivalue_line(
        "markers", "software: тесты программного обеспечения"
    )
    config.addinivalue_line(
        "markers", "network: тесты сетевого взаимодействия"
    )
    config.addinivalue_line(
        "markers", "security: тесты безопасности"
    )
    config.addinivalue_line(
        "markers", "system: тесты системных компонентов"
    )
    config.addinivalue_line(
        "markers", "slow: медленные тесты"
    )
    config.addinivalue_line(
        "markers", "fast: быстрые тесты"
    )