class BIOS:
    def __init__(self, version: str):
        self.version = version
        self.settings = {}
        self.boot_order = ["SSD", "HDD", "USB", "Network"]
        self.secure_boot = True
        self.fast_boot = False
        self.overclocking_profiles = {}

    def update_setting(self, key: str, value):
        """Обновление настройки BIOS"""
        self.settings[key] = value
        print(f"Настройка BIOS '{key}' установлена в '{value}'")

    def set_boot_order(self, order: list):
        """Установка порядка загрузки"""
        self.boot_order = order
        print(f"Порядок загрузки установлен: {order}")

    def perform_post(self) -> bool:
        """Power-On Self-Test"""
        print("Выполняется POST (Power-On Self-Test)...")
        # Проверка основных компонентов
        checks = [
            "Проверка процессора... OK",
            "Проверка памяти... OK",
            "Проверка видеокарты... OK",
            "Проверка накопителей... OK"
        ]

        for check in checks:
            print(f"  {check}")

        print("POST завершен успешно")
        return True

    def enable_secure_boot(self):
        """Включение Secure Boot"""
        self.secure_boot = True
        print("Secure Boot включен")

    def disable_secure_boot(self):
        """Выключение Secure Boot"""
        self.secure_boot = False
        print("Secure Boot выключен")

    def enable_fast_boot(self):
        """Включение Fast Boot"""
        self.fast_boot = True
        print("Fast Boot включен")

    def disable_fast_boot(self):
        """Выключение Fast Boot"""
        self.fast_boot = False
        print("Fast Boot выключен")

    def add_overclocking_profile(self, name: str, settings: dict):
        """Добавление профиля разгона"""
        self.overclocking_profiles[name] = settings
        print(f"Профиль разгона '{name}' добавлен")

    def get_bios_info(self) -> dict:
        """Получение информации о BIOS"""
        return {
            'version': self.version,
            'secure_boot': self.secure_boot,
            'fast_boot': self.fast_boot,
            'boot_order': self.boot_order,
            'settings_count': len(self.settings),
            'overclocking_profiles': list(self.overclocking_profiles.keys())
        }

    def reset_to_defaults(self):
        """Сброс настроек BIOS к заводским"""
        self.settings.clear()
        self.boot_order = ["SSD", "HDD", "USB", "Network"]
        self.secure_boot = True
        self.fast_boot = False
        self.overclocking_profiles.clear()
        print("Настройки BIOS сброшены к заводским")