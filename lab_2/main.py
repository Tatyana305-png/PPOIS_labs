from computer_system import *

def main():
    """
    ДЕМОНСТРАЦИЯ РАБОТЫ КОМПЬЮТЕРНОЙ СИСТЕМЫ
    1. Включение компьютера и диагностику оборудования
    2. Аутентификацию пользователя
    3. Шифрование и дешифрование файлов разными алгоритмами
    4. Проверку надежности паролей
    5. Тестирование производительности системы
    6. Обработку исключений
    """

    print("ЗАПУСК КОМПЬЮТЕРНОЙ СИСТЕМЫ")
    print("=" * 50)

    # Создаем компьютер
    computer = Computer()

    # Демонстрация информации о системе
    print("\n ИНФОРМАЦИЯ О СИСТЕМЕ:")
    system_info = computer.get_system_info()
    for component, info in system_info.items():
        print(f"  {component}: {info}")

    # Включаем компьютер
    print("\n ВКЛЮЧЕНИЕ КОМПЬЮТЕРА...")
    if computer.power_on():
        # Логинимся
        print("\n АУТЕНТИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ...")
        session = computer.login("admin", "password123")

        if session:
            try:
                # Демонстрация шифрования файлов
                print("\n ДЕМОНСТРАЦИЯ ШИФРОВАНИЯ ФАЙЛОВ")
                print("-" * 40)

                # Создаем тестовый файл с секретными данными (используем ASCII)
                secret_content = b"This is very secret data: passwords, financial reports, personal correspondence!"

                # Шифруем разными алгоритмами
                algorithms = ['AES', 'XOR', 'CAESAR']
                encrypted_files = []

                for algo in algorithms:
                    print(f"\n Шифрование с помощью {algo}:")
                    encrypted_file = computer.encrypt_file(
                        f"secret_document_{algo}.txt",
                        secret_content,
                        algo,
                        "my_strong_password_123!",
                        session
                    )
                    encrypted_files.append(encrypted_file)
                    print(f"   Размер зашифрованного файла: {encrypted_file.size} байт")
                    print(f"   Дата шифрования: {encrypted_file.encryption_date}")

                # Дешифруем файлы
                print("\n ДЕШИФРОВАНИЕ ФАЙЛОВ:")
                print("-" * 30)
                for encrypted_file in encrypted_files:
                    try:
                        decrypted_file = computer.decrypt_file(
                            encrypted_file,
                            "my_strong_password_123!",
                            session
                        )
                        print(f" {encrypted_file.filename} успешно дешифрован")
                        original_text = decrypted_file.content.decode('utf-8', errors='ignore')
                        print(f"   Оригинальный текст: {original_text[:60]}...")
                    except SecurityError as e:
                        print(f" Ошибка дешифрования {encrypted_file.filename}: {e}")

                # Демонстрация проверки паролей
                print("\n ПРОВЕРКА НАДЕЖНОСТИ ПАРОЛЕЙ:")
                print("-" * 35)
                test_passwords = [
                    "123",
                    "password",
                    "Password123",
                    "VeryStrongPassword123!@#",
                    "MySuperSecurePass2024!"
                ]

                for pwd in test_passwords:
                    strength = computer.check_password_strength(pwd)
                    status = " НАДЕЖНЫЙ" if strength['is_strong'] else " СЛАБЫЙ"
                    print(f"   Пароль: '{pwd}'")
                    print(f"   Оценка: {strength['score']}/5 - {status}")
                    if not strength['is_strong']:
                        print("   Рекомендации: используйте заглавные буквы, цифры и спецсимволы!")
                    print()

                # Производительность шифрования
                print("\n ТЕСТИРОВАНИЕ СКОРОСТИ ШИФРОВАНИЯ:")
                print("-" * 40)
                print("Тестирование на данных объемом 100 КБ...")
                benchmark_results = computer.benchmark_encryption(1024 * 100, session)  # 100KB вместо 1MB для скорости

                print("\nРезультаты тестирования:")
                fastest_algo = None
                fastest_time = float('inf')

                for algo, time in benchmark_results.items():
                    status = " УСПЕХ" if time > 0 else " ОШИБКА"
                    print(f"   {algo:8}: {time:7.4f} секунд {status}")

                    if time > 0 and time < fastest_time:
                        fastest_time = time
                        fastest_algo = algo

                if fastest_algo:
                    print(f"\n Самый быстрый алгоритм: {fastest_algo} ({fastest_time:.4f} сек)")

                # Демонстрация работы с файловой системой
                print("\n РАБОТА С ФАЙЛОВОЙ СИСТЕМОЙ:")
                print("-" * 30)
                try:
                    file_system = computer.operating_system.file_system

                    # Создаем несколько файлов
                    files_to_create = [
                        ("report.docx", b"Annual financial company report"),
                        ("photo.jpg", b"fake_image_data_here"),
                        ("resume.pdf", b"My professional resume content")
                    ]

                    for filename, content in files_to_create:
                        new_file = file_system.create_file(filename)
                        new_file.write_content(content)
                        print(f" Создан файл: {new_file.filename}")
                        print(f"   Размер: {new_file.size} байт, создан: {new_file.created}")

                    print(f"\n Всего файлов в системе: {len(file_system.files)}")

                except FileSystemError as e:
                    print(f" Ошибка файловой системы: {e}")

                # Демонстрация обработки исключений
                print("\n  ДЕМОНСТРАЦИЯ ОБРАБОТКИ ИСКЛЮЧЕНИЙ:")
                print("-" * 40)

                # Искусственно вызываем различные исключения
                test_cases = [
                    ("Перегрузка CPU", lambda: (
                        setattr(computer.cpu, 'usage', 99),
                        computer.cpu.execute_instruction(Instruction("ADD", ["R1", "R2"]))
                    )),

                    ("Ошибка памяти", lambda: computer.ram.read_data(999999)),

                    ("Неверный ключ дешифрования", lambda: (
                        computer.operating_system.encryption_manager.decrypt_file(
                            encrypted_files[0], "wrong_key", session
                        ) if encrypted_files else None
                    )),

                    ("Создание существующего файла", lambda: (
                        file_system.create_file("report.docx")
                    )),
                ]

                for test_name, test_func in test_cases:
                    try:
                        print(f"\n Тест: {test_name}")
                        test_func()
                        print("    Исключение не сгенерировано (неожиданно)")
                    except ComputerError as e:
                        print(f"    Поймано ожидаемое исключение: {type(e).__name__}: {e}")
                    except Exception as e:
                        print(f"   ️  Другое исключение: {type(e).__name__}: {e}")

                print("\n ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
                print("=" * 50)

            except ComputerError as e:
                print(f"\n КРИТИЧЕСКАЯ ОШИБКА СИСТЕМЫ: {e}")
            except Exception as e:
                print(f"\n НЕИЗВЕСТНАЯ ОШИБКА: {e}")
        else:
            print("\n Не удалось войти в систему. Демонстрация прервана.")
    else:
        print("\n Не удалось включить компьютер. Проверьте оборудование.")

def demonstrate_system_capabilities():
    """Дополнительная демонстрация возможностей системы"""
    print("\n" + "="*60)
    print(" ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ СИСТЕМЫ")
    print("="*60)

    computer = Computer()

    if computer.power_on():
        session = computer.login("admin", "password123")

        if session:
            # Демонстрация разных типов контента
            print("\n ШИФРОВАНИЕ РАЗЛИЧНЫХ ТИПОВ ДАННЫХ:")

            test_cases = [
                ("Текстовый документ", b"Confidential business plan for 2024"),
                ("База данных", b"SQLite format 3...user_data...passwords..."),
                ("Изображение", b"PNG_HEADER" + b"x" * 1000),
                ("Архив", b"PK" + b"compressed_data" * 100)
            ]

            for data_type, content in test_cases:
                print(f"\n {data_type}:")
                try:
                    encrypted = computer.encrypt_file(
                        f"{data_type.replace(' ', '_')}.enc",
                        content,
                        "AES",
                        "secure_key_2024",
                        session
                    )
                    decrypted = computer.decrypt_file(encrypted, "secure_key_2024", session)

                    if content == decrypted.content:
                        print(f"    Целостность данных сохранена")
                        print(f"    Размер: {len(content)} → {encrypted.size} байт")
                    else:
                        print("    Ошибка целостности данных")

                except SecurityError as e:
                    print(f"    Ошибка безопасности: {e}")

if __name__ == "__main__":
    try:
        # Основная демонстрация
        main()

        # Дополнительная демонстрация (можно раскомментировать)
        # demonstrate_system_capabilities()

        print("\n" + "="*60)
        print(" ПРОГРАММА ЗАВЕРШИЛА РАБОТУ")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\n  Программа прервана пользователем")
    except Exception as e:
        print(f"\n ФАТАЛЬНАЯ ОШИБКА: {e}")
