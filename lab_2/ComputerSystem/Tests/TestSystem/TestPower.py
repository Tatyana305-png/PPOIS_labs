import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from System.Power import PowerSupply, Battery

class TestPower:
    @pytest.fixture
    def sample_power_supply(self):
        return PowerSupply(500, "80+ Bronze")

    @pytest.fixture
    def sample_battery(self):
        return Battery(50000, "Li-ion")

    def test_power_supply_initialization(self, sample_power_supply):
        assert sample_power_supply.wattage == 500
        assert not sample_power_supply.is_on

    def test_battery_discharge(self, sample_battery):
        result = sample_battery.discharge(10000)
        assert result is True
        assert sample_battery.current_charge == 40000