import os
import configparser
import subprocess
import json

CONFIG_DIR = "config"  # Папка с конфигами
DEV_FILE = ".dev"

def _load_device_config():
    """Загружает конфигурацию устройства из файла .dev."""
    try:
        with open(DEV_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_available_kernels(git_repo, git_branch="main"):
    """Возвращает список доступных версий ядра из указанного репозитория."""
    try:
        process = subprocess.run(
            ["git", "ls-remote", "--tags", f"{git_repo}", f"refs/tags/v*"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        process.check_returncode()
        tags = [
            tag.split("/")[-1]
            for tag in process.stdout.splitlines()
            if tag.startswith("refs/tags/v")
        ]
        return tags
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении тегов из репозитория: {e}")
        return []

def select_kernel_version():
    """Отображает список доступных ядер и позволяет пользователю выбрать нужную версию.
    Сохраняет выбранную версию в конфигурационный файл.
    """
    config = _load_device_config()
    selected_device = config.get("selected_device")

    if selected_device is None:
        print("Ошибка: Устройство не выбрано.")
        return None

    config_file = os.path.join(CONFIG_DIR, f"{selected_device}.cfg")
    config = configparser.ConfigParser()
    config.read(config_file)

    # Проверяем наличие секции 'Kernel' в конфиге
    if not config.has_section('Kernel'):
        print(f"Ошибка: Секция 'Kernel' не найдена в конфигурационном файле {config_file}.")
        return None

    # Безопасное получение значений из конфига
    try:
        git_repo = config.get('Kernel', 'git_repo')
        git_branch = config.get('Kernel', 'git_branch', fallback='master')
    except configparser.NoOptionError as e:
        print(f"Ошибка в конфигурационном файле: {e}")
        return None

    available_kernels = get_available_kernels(git_repo, git_branch)

    if not available_kernels:
        print("Доступные версии ядра не найдены.")
        return None

    print("Доступные версии ядра:")
    for i, kernel in enumerate(available_kernels):
        print(f"{i+1}. {kernel}")

    while True:
        try:
            choice = int(input("Выберите номер версии ядра: "))
            if 1 <= choice <= len(available_kernels):
                selected_kernel = available_kernels[choice - 1]
                config.set('Kernel', 'version', selected_kernel)
                with open(config_file, 'w') as f:
                    config.write(f)
                print(f"Выбрана версия ядра: {selected_kernel}")
                return selected_kernel
            else:
                print("Неверный выбор. Пожалуйста, введите номер из списка.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер.")

def register():
    return [{"name": "Выбрать версию ядра", "function": select_kernel_version}]
