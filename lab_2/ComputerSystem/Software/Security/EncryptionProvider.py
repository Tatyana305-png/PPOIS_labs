from Exceptions.EncryptionException import EncryptionException

class EncryptionProvider:
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.key_storage = None

    def encrypt(self, data: bytes, key_manager) -> bytes:
        """Шифрование данных"""
        try:
            key = key_manager.get_key()
            # Простая имитация шифрования XOR
            encrypted = bytes(b ^ 0xAA for b in data)
            return encrypted
        except Exception as e:
            raise EncryptionException(f"Ошибка шифрования: {str(e)}")

    def decrypt(self, encrypted_data: bytes, key_manager) -> bytes:
        """Дешифрование данных"""
        try:
            key = key_manager.get_key()
            decrypted = bytes(b ^ 0xAA for b in encrypted_data)
            return decrypted
        except Exception as e:
            raise EncryptionException(f"Ошибка дешифрования: {str(e)}")