import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.OS import OperatingSystem, Kernel
from Software.Applications import TextEditor


class TestOperatingSystem:
    @pytest.fixture
    def sample_os(self):
        return OperatingSystem("Linux", "5.0")

    def test_os_initialization(self, sample_os):
        assert sample_os.name == "Linux"
        assert sample_os.version == "5.0"
        assert sample_os.running_processes == {}

    def test_install_application(self, sample_os):
        editor = TextEditor()
        sample_os.install_application(editor)
        assert len(sample_os.installed_applications) == 1

    def test_kernel_comprehensive(self):
        kernel = Kernel()

        # Test driver registration
        drivers = ["network_driver", "storage_driver", "usb_driver"]
        for driver in drivers:
            kernel.register_driver(driver)

        assert len(kernel.drivers) == 3

        # Test interrupt handlers
        def mock_handler(data):
            return f"handled: {data}"

        kernel.interrupt_handlers[1] = mock_handler
        result = kernel.handle_interrupt(1, "test_data")
        assert result == "handled: test_data"

        # Test unknown interrupt
        result = kernel.handle_interrupt(999, "data")
        assert result is None

    def test_os_process_management(self):
        os = OperatingSystem("TestOS", "1.0")
        editor = TextEditor()

        os.install_application(editor)
        process_id = os.run_application("TextEditor")

        assert process_id in os.running_processes
        assert os.running_processes[process_id] == editor

        os.shutdown()