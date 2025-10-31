import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from system.power import PowerSupply, Battery
from system.cooling import CoolingSystem, Fan, TemperatureSensor
from system.monitoring import SystemMonitor, PerformanceCounter

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

class TestCooling:
    @pytest.fixture
    def sample_cooling_system(self):
        return CoolingSystem()

    @pytest.fixture
    def sample_fan(self):
        return Fan(120, 1500)

    def test_cooling_system_initialization(self, sample_cooling_system):
        assert sample_cooling_system.fans == []

    def test_fan_initialization(self, sample_fan):
        assert sample_fan.size == 120
        assert sample_fan.max_rpm == 1500

class TestMonitoring:
    @pytest.fixture
    def sample_system_monitor(self):
        return SystemMonitor()

    @pytest.fixture
    def sample_performance_counter(self):
        return PerformanceCounter("test_metric")

    def test_system_monitor_initialization(self, sample_system_monitor):
        assert sample_system_monitor.metrics == {}

    def test_performance_counter_add_sample(self, sample_performance_counter):
        sample_performance_counter.add_sample(50.0)
        assert len(sample_performance_counter.values) == 1