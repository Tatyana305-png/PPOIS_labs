import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Peripherals.Monitor import Monitor

class TestMonitor:
    def test_monitor_initialization(self):
        monitor = Monitor((1920, 1080), 60)
        assert monitor.resolution == (1920, 1080)
        assert monitor.refresh_rate == 60
        assert monitor.current_resolution == (1920, 1080)
        assert monitor.brightness == 50
        assert monitor.monitor_type == "IPS"
        assert monitor.screen_size == 27
        assert monitor.hdr_support == True

    def test_monitor_set_resolution(self):
        monitor = Monitor((1920, 1080), 60)
        monitor.set_resolution(2560, 1440)

        assert monitor.current_resolution == (2560, 1440)

    def test_monitor_adjust_brightness(self):
        monitor = Monitor((1920, 1080), 60)

        # Корректные значения
        monitor.adjust_brightness(75)
        assert monitor.brightness == 75

        monitor.adjust_brightness(200)
        assert monitor.brightness == 100

        monitor.adjust_brightness(-50)
        assert monitor.brightness == 0

    def test_monitor_set_refresh_rate(self):
        monitor = Monitor((1920, 1080), 60)
        monitor.set_refresh_rate(144)

        assert monitor.refresh_rate == 144

    def test_monitor_hdr_operations(self):
        monitor = Monitor((1920, 1080), 60)

        monitor.enable_hdr()

        monitor.disable_hdr()

    def test_monitor_hdr_without_support(self):
        monitor = Monitor((1920, 1080), 60)
        monitor.hdr_support = False

        monitor.enable_hdr()

    def test_monitor_get_monitor_info(self):
        monitor = Monitor((3840, 2160), 144)
        monitor.adjust_brightness(80)
        monitor.set_resolution(2560, 1440)

        info = monitor.get_monitor_info()
        assert info['resolution'] == (3840, 2160)
        assert info['current_resolution'] == (2560, 1440)
        assert info['refresh_rate'] == 144
        assert info['brightness'] == 80
        assert info['monitor_type'] == "IPS"
        assert info['screen_size'] == 27
        assert info['hdr_support'] == True

    def test_monitor_calibrate_colors(self):
        monitor = Monitor((1920, 1080), 60)
        monitor.calibrate_colors()

    def test_monitor_power_save_mode(self):
        monitor = Monitor((1920, 1080), 60)
        monitor.power_save_mode(True)
        monitor.power_save_mode(False)