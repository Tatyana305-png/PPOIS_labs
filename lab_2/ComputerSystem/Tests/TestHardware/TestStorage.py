import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Hardware.Storage import SSD, HardDrive, StorageDevice
from Exceptions.StorageFullException import StorageFullException

class TestStorage:
    @pytest.fixture
    def sample_ssd(self):
        return SSD(512000, "SATA")

    def test_ssd_initialization(self, sample_ssd):
        assert sample_ssd.capacity == 512000
        assert sample_ssd.type == "SSD"
        assert sample_ssd.interface == "SATA"
        assert sample_ssd.used_space == 0

    def test_store_file(self, sample_ssd):
        result = sample_ssd.store_file("test.txt", b"Hello World")
        assert result is True
        assert sample_ssd.used_space == 11
        assert "test.txt" in sample_ssd.files

    def test_store_file_full_exception(self, sample_ssd):
        large_data = b"x" * (sample_ssd.capacity + 100)

        with pytest.raises(StorageFullException):
            sample_ssd.store_file("large.txt", large_data)

    def test_storage_device_base_class(self):
        storage = StorageDevice(1000, "TestType")
        assert storage.capacity == 1000
        assert storage.type == "TestType"
        assert storage.used_space == 0

    def test_hard_drive_initialization(self):
        hdd = HardDrive(1000000, 7200)
        assert hdd.capacity == 1000000
        assert hdd.type == "HDD"
        assert hdd.rpm == 7200
        # Test defragment doesn't crash
        hdd.defragment()

    def test_ssd_health_calculation(self):
        ssd = SSD(500000, "NVMe")
        health = ssd.get_health_status()
        assert 0 <= health <= 100

        # Test after some usage - используем значительно больше места
        ssd.used_space = 400000  # 80% использовано
        health_after_usage = ssd.get_health_status()
        assert health_after_usage < health, f"Health should decrease after usage: {health_after_usage} < {health}"

    def test_storage_file_operations(self):
        ssd = SSD(1000, "SATA")

        # Store multiple files
        ssd.store_file("file1.txt", b"content1")
        ssd.store_file("file2.txt", b"content2")

        assert ssd.used_space == 16
        assert len(ssd.files) == 2

        # Read files
        content1 = ssd.read_file("file1.txt")
        content2 = ssd.read_file("file2.txt")
        assert content1 == b"content1"
        assert content2 == b"content2"

        # Calculate hashes
        hash1 = ssd.calculate_hash("file1.txt")
        hash2 = ssd.calculate_hash("file2.txt")
        assert len(hash1) == 64
        assert hash1 != hash2

    def test_storage_encryption_integration(self):
        ssd = SSD(1000, "SATA")

        class MockEncryption:
            def encrypt(self, data):
                return b"encrypted_" + data

            def decrypt(self, data):
                return data.replace(b"encrypted_", b"")

        encryption = MockEncryption()
        ssd.store_file("secret.txt", b"data", encryption)

        # File should be stored encrypted
        assert b"encrypted_data" in ssd.files["secret.txt"]

        # Read with decryption
        content = ssd.read_file("secret.txt", encryption)
        assert content == b"data"