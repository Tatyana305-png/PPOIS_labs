import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exceptions.hardware_exceptions import CPUOverheatException, MemoryAllocationException
from exceptions.security_exceptions import AuthenticationException, EncryptionException
from exceptions.software_exceptions import ApplicationCrashException

class TestExceptions:
    def test_cpu_overheat_exception(self):
        exception = CPUOverheatException(90.0)
        assert exception.temperature == 90.0
        assert "90.0" in str(exception)

    def test_memory_allocation_exception(self):
        exception = MemoryAllocationException("Custom message")
        assert "Custom message" in str(exception)

    def test_authentication_exception(self):
        exception = AuthenticationException("Auth failed")
        assert "Auth failed" in str(exception)

    def test_application_crash_exception(self):
        exception = ApplicationCrashException("App crashed")
        assert "App crashed" in str(exception)