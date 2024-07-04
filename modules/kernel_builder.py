import os
import subprocess
import configparser

CONFIG_DIR = "config"

def build_kernel(device=None):
    """
    Собирает ядро Android, используя настройки из файла конфигурации.
    """

    if device is None:
        # Выбор конфигурационного файла
        config_files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".cfg")]
        print("Доступные конфигурации устройств:")
        for i, file in enumerate(config_files):
            print(f"{i+1}. {file}")
        try:
            choice = int(input("Выберите номер конфигурации: ")) - 1
            config_file = os.path.join(CONFIG_DIR, config_files[choice])
        except (ValueError, IndexError):
            print("Неверный выбор конфигурации.")
            return
    else:
        config_file = os.path.join(CONFIG_DIR, f"{device}.config")

    # Чтение настроек из файла
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        kernel_version = config.get("Kernel", "version")
        architecture = config.get("Kernel", "architecture")
        compiler = config.get("Build", "compiler")
        compiler_flags = config.get("Build", "compiler_flags")
        make_flags = config.get("Build", "make_flags")
    except configparser.NoOptionError as e:
        print(f"Ошибка в конфигурационном файле: {e}")
        return

    # Формирование команды сборки
    build_command = [
        "make",
        f"ARCH={architecture}",
        f"CROSS_COMPILE={compiler}",
        f"{compiler_flags}",
        f"{make_flags}",
    ]

    # Вывод информации о сборке
    print("----------------------------------------")
    print("Параметры сборки:")
    print(f"Конфигурация: {config_file}")
    print(f"Версия ядра: {kernel_version}")
    print(f"Архитектура: {architecture}")
    print(f"Компилятор: {compiler}")
    print("----------------------------------------")

    # Запуск процесса сборки
    try:
        subprocess.run(build_command, check=True)
        print("Сборка ядра завершена успешно!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка сборки ядра: {e}")

def register():
    """
    Регистрирует функцию build_kernel в главном скрипте.
    """
    return [{"name": "Собрать ядро", "function": build_kernel}]
