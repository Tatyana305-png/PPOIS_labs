import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from System.Cooling import CoolingSystem, Fan

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