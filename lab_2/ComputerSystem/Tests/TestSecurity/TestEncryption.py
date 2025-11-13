import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Software.Security import EncryptionProvider
from Exceptions.EncryptionException import EncryptionException

class TestEncryption:
    @pytest.fixture
    def sample_encryption_provider(self):
        return EncryptionProvider("AES-256")

    @pytest.fixture
    def mock_key_manager(self):
        class MockKeyManager:
            def get_key(self):
                return b"test_key_1234567890123456"

        return MockKeyManager()

    def test_encryption_provider_initialization(self, sample_encryption_provider):
        assert sample_encryption_provider.algorithm == "AES-256"

    def test_encryption_decryption(self, sample_encryption_provider, mock_key_manager):
        original_data = b"Secret message for encryption"

        encrypted = sample_encryption_provider.encrypt(original_data, mock_key_manager)
        decrypted = sample_encryption_provider.decrypt(encrypted, mock_key_manager)

        assert encrypted != original_data
        assert decrypted == original_data

    def test_encryption_with_invalid_key_manager(self, sample_encryption_provider):
        class InvalidKeyManager:
            def get_key(self):
                raise Exception("Key error")

        with pytest.raises(EncryptionException):
            sample_encryption_provider.encrypt(b"data", InvalidKeyManager())