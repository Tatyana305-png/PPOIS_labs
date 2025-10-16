from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import random
import hashlib
import base64


# ========== ПЕРСОНАЛЬНЫЕ ИСКЛЮЧЕНИЯ ==========

class ComputerError(Exception):
    """Базовое исключение для компьютерной системы"""
    pass


class HardwareError(ComputerError):
    """Ошибка оборудования"""
    pass


class SoftwareError(ComputerError):
    """Ошибка программного обеспечения"""
    pass


class MemoryAllocationError(HardwareError):
    """Ошибка выделения памяти"""
    pass


class CPUError(HardwareError):
    """Ошибка процессора"""
    pass


class DiskError(HardwareError):
    """Ошибка диска"""
    pass


class NetworkError(ComputerError):
    """Ошибка сети"""
    pass


class SecurityError(SoftwareError):
    """Ошибка безопасности"""
    pass


class AuthenticationError(SecurityError):
    """Ошибка аутентификации"""
    pass


class AuthorizationError(SecurityError):
    """Ошибка авторизации"""
    pass


class InsufficientResourcesError(SoftwareError):
    """Недостаточно ресурсов"""
    pass


class FileSystemError(SoftwareError):
    """Ошибка файловой системы"""
    pass


class InvalidOperationError(ComputerError):
    """Неверная операция"""
    pass


# ========== БАЗОВЫЕ КЛАССЫ ==========

class Component(ABC):
    """Абстрактный базовый класс для компонентов компьютера"""

    def __init__(self, name: str, manufacturer: str):
        self.name = name
        self.manufacturer = manufacturer
        self._is_working = True

    @abstractmethod
    def get_info(self) -> str:
        pass

    def diagnose(self) -> bool:
        return self._is_working


class ElectronicComponent(Component):
    """Базовый класс для электронных компонентов"""

    def __init__(self, name: str, manufacturer: str, voltage: float):
        super().__init__(name, manufacturer)
        self.voltage = voltage
        self.temperature = 25.0


class DataStorage(ABC):
    """Абстрактный класс для хранилищ данных"""

    @abstractmethod
    def read_data(self, address: int) -> bytes:
        pass

    @abstractmethod
    def write_data(self, address: int, data: bytes) -> bool:
        pass


# ========== КЛАССЫ ОБОРУДОВАНИЯ ==========

class CPU(ElectronicComponent):
    """Класс процессора"""

    def __init__(self, name: str, manufacturer: str, cores: int, speed: float):
        super().__init__(name, manufacturer, 1.2)
        self.cores = cores
        self.speed = speed
        self.cache_memory = CacheMemory("L3 Cache", manufacturer, 16)
        self.usage = 0.0

    def get_info(self) -> str:
        return f"CPU {self.name} ({self.cores} cores, {self.speed}GHz)"

    def execute_instruction(self, instruction: 'Instruction') -> bool:
        if self.usage > 95:
            raise CPUError("CPU overloaded!")
        self.usage += random.uniform(0.1, 1.0)
        return True


class RAM(ElectronicComponent, DataStorage):
    """Класс оперативной памяти"""

    def __init__(self, name: str, manufacturer: str, capacity: int):
        super().__init__(name, manufacturer, 1.5)
        self.capacity = capacity
        self.data: Dict[int, bytes] = {}
        self.memory_controller = MemoryController("Memory Controller", manufacturer)

    def get_info(self) -> str:
        return f"RAM {self.name} ({self.capacity}GB)"

    def read_data(self, address: int) -> bytes:
        if address not in self.data:
            raise MemoryAllocationError(f"Memory address {address} not found")
        return self.data[address]

    def write_data(self, address: int, data: bytes) -> bool:
        if len(data) > 1024:
            raise MemoryAllocationError("Data too large for single write")
        self.data[address] = data
        return True


class HardDrive(ElectronicComponent, DataStorage):
    """Класс жесткого диска"""

    def __init__(self, name: str, manufacturer: str, capacity: int, rpm: int):
        super().__init__(name, manufacturer, 5.0)
        self.capacity = capacity
        self.rpm = rpm
        self.file_system = FileSystem("NTFS")

    def get_info(self) -> str:
        return f"Hard Drive {self.name} ({self.capacity}GB, {self.rpm}RPM)"

    def read_data(self, address: int) -> bytes:
        if random.random() < 0.001:
            raise DiskError("Disk read error")
        return b"simulated_data"

    def write_data(self, address: int, data: bytes) -> bool:
        if self.capacity - len(self.file_system.files) < len(data):
            raise DiskError("Insufficient disk space")
        return True


class GPU(ElectronicComponent):
    """Класс графического процессора"""

    def __init__(self, name: str, manufacturer: str, vram: int):
        super().__init__(name, manufacturer, 1.8)
        self.vram = vram
        self.graphics_memory = GraphicsMemory("GDDR6", manufacturer, vram)

    def get_info(self) -> str:
        return f"GPU {self.name} ({self.vram}GB VRAM)"

    def render_frame(self, frame_buffer: 'FrameBuffer') -> bool:
        if self.vram < 1024:
            raise HardwareError("Insufficient VRAM")
        return True


class Motherboard(Component):
    """Класс материнской платы"""

    def __init__(self, name: str, manufacturer: str, chipset: str):
        super().__init__(name, manufacturer)
        self.chipset = chipset
        self.components: List[Component] = []
        self.bios = BIOS("UEFI BIOS", manufacturer)

    def get_info(self) -> str:
        return f"Motherboard {self.name} ({self.chipset})"

    def add_component(self, component: Component) -> None:
        self.components.append(component)


class PowerSupply(Component):
    """Класс блока питания"""

    def __init__(self, name: str, manufacturer: str, wattage: int):
        super().__init__(name, manufacturer)
        self.wattage = wattage
        self.voltage_regulator = VoltageRegulator("VRM", manufacturer)

    def get_info(self) -> str:
        return f"Power Supply {self.name} ({self.wattage}W)"

    def supply_power(self, component: ElectronicComponent) -> bool:
        required_power = component.voltage * 10
        if required_power > self.wattage * 0.8:
            raise HardwareError("Power supply overload")
        return True


# ========== СИСТЕМНЫЕ КЛАССЫ ==========

class OperatingSystem:
    """Класс операционной системы"""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager()
        self.file_system = FileSystem("EXT4")
        self.network_manager = NetworkManager()
        self.security_manager = SecurityManager()
        self.encryption_manager = EncryptionManager()


class ProcessManager:
    """Менеджер процессов"""

    def __init__(self):
        self.processes: List['Process'] = []
        self.scheduler = ProcessScheduler()

    def create_process(self, program: 'Program') -> 'Process':
        process = Process(program)
        self.processes.append(process)
        return process


class MemoryManager:
    """Менеджер памяти"""

    def __init__(self):
        self.allocated_memory: Dict[int, 'MemoryBlock'] = {}

    def allocate_memory(self, size: int) -> 'MemoryBlock':
        if size <= 0:
            raise MemoryAllocationError("Invalid memory size")
        block = MemoryBlock(size)
        self.allocated_memory[id(block)] = block
        return block


class FileSystem:
    """Файловая система"""

    def __init__(self, fs_type: str):
        self.fs_type = fs_type
        self.files: Dict[str, 'File'] = {}
        self.directories: Dict[str, 'Directory'] = {}

    def create_file(self, filename: str) -> 'File':
        if filename in self.files:
            raise FileSystemError(f"File {filename} already exists")
        file = File(filename)
        self.files[filename] = file
        return file


class NetworkManager:
    """Менеджер сети"""

    def __init__(self):
        self.connections: List['NetworkConnection'] = []
        self.network_adapter: Optional['NetworkAdapter'] = None

    def establish_connection(self, address: str) -> 'NetworkConnection':
        if not self.network_adapter:
            raise NetworkError("No network adapter available")
        connection = NetworkConnection(address)
        self.connections.append(connection)
        return connection


class SecurityManager:
    """Менеджер безопасности"""

    def __init__(self):
        self.users: Dict[str, 'User'] = {}
        self.firewall = Firewall()
        self.antivirus = Antivirus()

    def authenticate_user(self, username: str, password: str) -> 'UserSession':
        if username not in self.users:
            raise AuthenticationError("User not found")
        user = self.users[username]
        if not user.verify_password(password):
            raise AuthenticationError("Invalid password")
        return UserSession(user)


# ========== КЛАССЫ ШИФРОВАНИЯ ==========

class EncryptionManager:
    """Менеджер шифрования"""

    def __init__(self):
        self.encryption_algorithms: Dict[str, 'EncryptionAlgorithm'] = {
            'AES': AESEncryption(),
            'XOR': XOREncryption(),
            'CAESAR': CaesarCipher()
        }
        self.key_storage = EncryptionKeyStorage()

    def encrypt_file(self, file: 'File', algorithm: str, key: str, session: 'UserSession') -> 'EncryptedFile':
        if not session.is_active:
            raise AuthorizationError("Session expired")

        if algorithm not in self.encryption_algorithms:
            raise SecurityError(f"Unknown encryption algorithm: {algorithm}")

        encryption_algorithm = self.encryption_algorithms[algorithm]
        encrypted_data = encryption_algorithm.encrypt(file.content, key)

        encrypted_file = EncryptedFile(file.filename, encrypted_data, algorithm)
        self.key_storage.store_key(encrypted_file.id, key, session.user)

        return encrypted_file

    def decrypt_file(self, encrypted_file: 'EncryptedFile', key: str, session: 'UserSession') -> 'File':
        if not session.is_active:
            raise AuthorizationError("Session expired")

        if encrypted_file.algorithm not in self.encryption_algorithms:
            raise SecurityError(f"Unknown encryption algorithm: {encrypted_file.algorithm}")

        if not self.key_storage.verify_key(encrypted_file.id, key, session.user):
            raise SecurityError("Invalid decryption key")

        encryption_algorithm = self.encryption_algorithms[encrypted_file.algorithm]
        decrypted_data = encryption_algorithm.decrypt(encrypted_file.encrypted_data, key)

        return File(encrypted_file.filename, decrypted_data)


class EncryptionAlgorithm(ABC):
    """Абстрактный класс алгоритма шифрования"""

    @abstractmethod
    def encrypt(self, data: bytes, key: str) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, encrypted_data: bytes, key: str) -> bytes:
        pass


class AESEncryption(EncryptionAlgorithm):
    """AES шифрование (упрощенная версия без внешних библиотек)"""

    def encrypt(self, data: bytes, key: str) -> bytes:
        # Упрощенная реализация AES для демонстрации
        key_hash = hashlib.sha256(key.encode()).digest()[:16]
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key_hash[i % len(key_hash)])
        return bytes(result)

    def decrypt(self, encrypted_data: bytes, key: str) -> bytes:
        # AES симметричный, поэтому дешифрование такое же
        return self.encrypt(encrypted_data, key)


class XOREncryption(EncryptionAlgorithm):
    """XOR шифрование"""

    def encrypt(self, data: bytes, key: str) -> bytes:
        key_bytes = key.encode()
        key_length = len(key_bytes)
        return bytes([data[i] ^ key_bytes[i % key_length] for i in range(len(data))])

    def decrypt(self, encrypted_data: bytes, key: str) -> bytes:
        return self.encrypt(encrypted_data, key)


class CaesarCipher(EncryptionAlgorithm):
    """Шифр Цезаря"""

    def encrypt(self, data: bytes, key: str) -> bytes:
        try:
            shift = int(key) % 256
        except ValueError:
            shift = sum(ord(c) for c in key) % 256

        return bytes([(b + shift) % 256 for b in data])

    def decrypt(self, encrypted_data: bytes, key: str) -> bytes:
        try:
            shift = int(key) % 256
        except ValueError:
            shift = sum(ord(c) for c in key) % 256

        return bytes([(b - shift) % 256 for b in encrypted_data])


class EncryptionKeyStorage:
    """Хранилище ключей шифрования"""

    def __init__(self):
        self.keys: Dict[str, Dict] = {}

    def store_key(self, file_id: str, key: str, user: 'User') -> None:
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        self.keys[file_id] = {
            'key_hash': key_hash,
            'user': user,
            'timestamp': datetime.now()
        }

    def verify_key(self, file_id: str, key: str, user: 'User') -> bool:
        if file_id not in self.keys:
            return False

        stored_key = self.keys[file_id]
        key_hash = hashlib.sha256(key.encode()).hexdigest()

        return (stored_key['key_hash'] == key_hash and
                stored_key['user'].username == user.username)


class EncryptedFile:
    """Зашифрованный файл"""

    def __init__(self, filename: str, encrypted_data: bytes, algorithm: str):
        self.id = hashlib.md5(f"{filename}{datetime.now()}".encode()).hexdigest()
        self.filename = filename
        self.encrypted_data = encrypted_data
        self.algorithm = algorithm
        self.encryption_date = datetime.now()
        self.size = len(encrypted_data)


# ========== ПРОГРАММНЫЕ КЛАССЫ ==========

class Program:
    """Класс программы"""

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.instructions: List['Instruction'] = []


class Process:
    """Класс процесса"""

    def __init__(self, program: Program):
        self.program = program
        self.pid = random.randint(1, 65535)
        self.state = "running"
        self.memory_blocks: List[MemoryBlock] = []


class Instruction:
    """Класс инструкции процессора"""

    def __init__(self, opcode: str, operands: List[str]):
        self.opcode = opcode
        self.operands = operands


class MemoryBlock:
    """Блок памяти"""

    def __init__(self, size: int):
        self.size = size
        self.data = bytearray(size)


class File:
    """Класс файла"""

    def __init__(self, filename: str, content: bytes = b""):
        self.filename = filename
        self.content = content
        self.size = len(content)
        self.created = datetime.now()
        self.modified = datetime.now()

    def read_content(self) -> bytes:
        return self.content

    def write_content(self, content: bytes) -> None:
        self.content = content
        self.size = len(content)
        self.modified = datetime.now()


class Directory:
    """Класс директории"""

    def __init__(self, name: str):
        self.name = name
        self.files: List[File] = []
        self.subdirectories: List[Directory] = []


class User:
    """Класс пользователя"""

    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password_hash = password_hash
        self.permissions: List[str] = []

    def verify_password(self, password: str) -> bool:
        return hash(password) == int(self.password_hash)


class UserSession:
    """Сессия пользователя"""

    def __init__(self, user: User):
        self.user = user
        self.start_time = datetime.now()
        self.is_active = True


# ========== СПЕЦИАЛИЗИРОВАННЫЕ КЛАССЫ ==========

class CacheMemory(RAM):
    """Кэш-память"""

    def __init__(self, name: str, manufacturer: str, size: int):
        super().__init__(name, manufacturer, size)
        self.access_time = 0.1


class GraphicsMemory(RAM):
    """Видеопамять"""

    def __init__(self, name: str, manufacturer: str, size: int):
        super().__init__(name, manufacturer, size)
        self.bandwidth = 448


class MemoryController(Component):
    """Контроллер памяти"""

    def __init__(self, name: str, manufacturer: str):
        super().__init__(name, manufacturer)
        self.clock_speed = 3200

    def get_info(self) -> str:
        return f"Memory Controller {self.name} ({self.clock_speed}MHz)"


class BIOS(Component):
    """BIOS системы"""

    def __init__(self, name: str, manufacturer: str):
        super().__init__(name, manufacturer)
        self.version = "2.1"

    def get_info(self) -> str:
        return f"BIOS {self.name} v{self.version}"


class VoltageRegulator(Component):
    """Регулятор напряжения"""

    def __init__(self, name: str, manufacturer: str):
        super().__init__(name, manufacturer)
        self.efficiency = 0.95

    def get_info(self) -> str:
        return f"Voltage Regulator {self.name}"


class ProcessScheduler:
    """Планировщик процессов"""

    def __init__(self):
        self.quantum = 100
        self.algorithm = "Round Robin"


class NetworkConnection:
    """Сетевое соединение"""

    def __init__(self, address: str):
        self.address = address
        self.is_connected = True
        self.bandwidth = 1000


class NetworkAdapter(Component):
    """Сетевой адаптер"""

    def __init__(self, name: str, manufacturer: str, speed: int):
        super().__init__(name, manufacturer)
        self.speed = speed
        self.mac_address = self._generate_mac()

    def get_info(self) -> str:
        return f"Network Adapter {self.name} ({self.speed}Mbps)"

    def _generate_mac(self) -> str:
        return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])


class Firewall:
    """Фаервол"""

    def __init__(self):
        self.rules: List[str] = []
        self.is_enabled = True

    def check_packet(self, packet: 'NetworkPacket') -> bool:
        return self.is_enabled and random.random() > 0.1


class Antivirus:
    """Антивирус"""

    def __init__(self):
        self.signatures: List[str] = []
        self.last_update = datetime.now()

    def scan_file(self, file: File) -> bool:
        return random.random() > 0.05


class FrameBuffer:
    """Буфер кадра"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = bytearray(width * height * 4)


class NetworkPacket:
    """Сетевой пакет"""

    def __init__(self, source: str, destination: str, data: bytes):
        self.source = source
        self.destination = destination
        self.data = data


# ========== КОМПЬЮТЕР И СИСТЕМА ==========

class Computer:
    """Основной класс компьютера"""

    def __init__(self):
        self.motherboard = Motherboard("Z790", "ASUS", "Intel Z790")
        self.cpu = CPU("Core i9-13900K", "Intel", 24, 5.8)
        self.ram = RAM("DDR5", "Corsair", 64)
        self.hard_drive = HardDrive("WD Black", "Western Digital", 2000, 7200)
        self.gpu = GPU("RTX 4090", "NVIDIA", 24)
        self.power_supply = PowerSupply("RM1000x", "Corsair", 1000)
        self.operating_system = OperatingSystem("Windows", "11")

        self.motherboard.add_component(self.cpu)
        self.motherboard.add_component(self.ram)
        self.motherboard.add_component(self.gpu)

        self.network_adapter = NetworkAdapter("Gigabit Ethernet", "Intel", 1000)
        self.operating_system.network_manager.network_adapter = self.network_adapter

        test_user = User("admin", str(hash("password123")))
        self.operating_system.security_manager.users["admin"] = test_user

        self.is_running = False

    def power_on(self) -> bool:
        """Включение компьютера"""
        try:
            components = [self.cpu, self.ram, self.hard_drive, self.gpu, self.power_supply]
            for component in components:
                if not component.diagnose():
                    raise HardwareError(f"Component {component.name} failed diagnostics")

            for component in [self.cpu, self.ram, self.gpu]:
                self.power_supply.supply_power(component)

            if not self.motherboard.bios.diagnose():
                raise HardwareError("BIOS failed to load")

            self.is_running = True
            print("Computer powered on successfully")
            return True

        except HardwareError as e:
            print(f"Hardware error during power on: {e}")
            return False

    def login(self, username: str, password: str) -> Optional[UserSession]:
        """Аутентификация пользователя"""
        try:
            session = self.operating_system.security_manager.authenticate_user(username, password)
            print(f"User {username} logged in successfully")
            return session
        except AuthenticationError as e:
            print(f"Authentication failed: {e}")
            return None

    def encrypt_file(self, filename: str, content: bytes, algorithm: str, key: str,
                     session: UserSession) -> EncryptedFile:
        """Шифрование файла"""
        if not session.is_active:
            raise AuthorizationError("Session expired")

        file = File(filename, content)
        encrypted_file = self.operating_system.encryption_manager.encrypt_file(
            file, algorithm, key, session
        )

        print(f"File '{filename}' encrypted successfully using {algorithm}")
        return encrypted_file

    def decrypt_file(self, encrypted_file: EncryptedFile, key: str, session: UserSession) -> File:
        """Дешифрование файла"""
        if not session.is_active:
            raise AuthorizationError("Session expired")

        decrypted_file = self.operating_system.encryption_manager.decrypt_file(
            encrypted_file, key, session
        )

        print(f"File '{encrypted_file.filename}' decrypted successfully")
        return decrypted_file

    def check_password_strength(self, password: str) -> dict:
        """Проверка надежности пароля"""
        result = {
            "length_ok": len(password) >= 8,
            "has_upper": any(c.isupper() for c in password),
            "has_lower": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(not c.isalnum() for c in password)
        }

        result["score"] = sum(result.values())
        result["is_strong"] = result["score"] >= 4

        return result

    def benchmark_encryption(self, data_size: int, session: UserSession) -> Dict[str, float]:
        """Тестирование скорости шифрования разными алгоритмами"""
        if not session.is_active:
            raise AuthorizationError("Session expired")

        test_data = b"X" * data_size
        results = {}

        for algo_name in self.operating_system.encryption_manager.encryption_algorithms.keys():
            start_time = datetime.now()

            try:
                test_file = File(f"test_{algo_name}", test_data)
                encrypted_file = self.encrypt_file(
                    f"test_{algo_name}", test_data, algo_name, "test_key", session
                )

                decrypted_file = self.decrypt_file(encrypted_file, "test_key", session)

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                results[algo_name] = duration

                if test_data != decrypted_file.content:
                    raise SecurityError(f"Data integrity check failed for {algo_name}")

            except SecurityError as e:
                print(f"Error in {algo_name} benchmark: {e}")
                results[algo_name] = -1.0

        return results

    def get_system_info(self) -> Dict[str, str]:
        """Получение информации о системе"""
        return {
            "CPU": self.cpu.get_info(),
            "RAM": self.ram.get_info(),
            "GPU": self.gpu.get_info(),
            "Hard Drive": self.hard_drive.get_info(),
            "Motherboard": self.motherboard.get_info(),
            "Power Supply": self.power_supply.get_info(),
            "OS": f"{self.operating_system.name} {self.operating_system.version}"
        }
