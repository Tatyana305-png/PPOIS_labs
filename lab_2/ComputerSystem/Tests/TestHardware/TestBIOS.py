import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Motherboard.BIOS import BIOS

class TestBIOS:
    def test_bios_initialization(self):
        bios = BIOS("2.1.0")
        assert bios.version == "2.1.0"
        assert bios.settings == {}
        assert bios.boot_order == ["SSD", "HDD", "USB", "Network"]
        assert bios.secure_boot == True
        assert bios.fast_boot == False
        assert bios.overclocking_profiles == {}

    def test_bios_update_setting(self):
        bios = BIOS("2.1.0")
        bios.update_setting("virtualization", True)

        assert bios.settings["virtualization"] == True

    def test_bios_set_boot_order(self):
        bios = BIOS("2.1.0")
        new_order = ["USB", "SSD", "Network"]
        bios.set_boot_order(new_order)

        assert bios.boot_order == new_order

    def test_bios_perform_post(self):
        bios = BIOS("2.1.0")
        result = bios.perform_post()

        assert result == True

    def test_bios_secure_boot_toggle(self):
        bios = BIOS("2.1.0")

        bios.disable_secure_boot()
        assert bios.secure_boot == False

        bios.enable_secure_boot()
        assert bios.secure_boot == True

    def test_bios_fast_boot_toggle(self):
        bios = BIOS("2.1.0")

        bios.enable_fast_boot()
        assert bios.fast_boot == True

        bios.disable_fast_boot()
        assert bios.fast_boot == False

    def test_bios_add_overclocking_profile(self):
        bios = BIOS("2.1.0")
        settings = {"cpu_multiplier": 45, "voltage": 1.35}

        bios.add_overclocking_profile("Performance", settings)
        assert "Performance" in bios.overclocking_profiles
        assert bios.overclocking_profiles["Performance"] == settings

    def test_bios_get_bios_info(self):
        bios = BIOS("2.1.0")
        bios.update_setting("setting1", "value1")
        bios.add_overclocking_profile("profile1", {})

        info = bios.get_bios_info()
        assert info['version'] == "2.1.0"
        assert info['secure_boot'] == True
        assert info['fast_boot'] == False
        assert info['boot_order'] == ["SSD", "HDD", "USB", "Network"]
        assert info['settings_count'] == 1
        assert info['overclocking_profiles'] == ["profile1"]

    def test_bios_reset_to_defaults(self):
        bios = BIOS("2.1.0")
        bios.update_setting("custom_setting", "value")
        bios.set_boot_order(["USB"])
        bios.disable_secure_boot()
        bios.enable_fast_boot()
        bios.add_overclocking_profile("test", {})

        bios.reset_to_defaults()

        assert bios.settings == {}
        assert bios.boot_order == ["SSD", "HDD", "USB", "Network"]
        assert bios.secure_boot == True
        assert bios.fast_boot == False
        assert bios.overclocking_profiles == {}