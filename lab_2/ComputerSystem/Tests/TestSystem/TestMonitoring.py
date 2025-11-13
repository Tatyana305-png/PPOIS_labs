import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from System.Monitoring import SystemMonitor, PerformanceCounter

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