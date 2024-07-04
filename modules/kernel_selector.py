import os
import configparser
import subprocess

CONFIG_DIR = "config"  # Папка с конфигами

def get_available_kernels(git_repo, git_branch="main"):
    """Получает список доступных версий ядер из Git репозитория."""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", git_repo],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result.check_return_code()  # Проверяем на ошибки Git

        tags = [
            tag.split("/")[-1].strip()
            for tag in result.stdout.splitlines()
            if "tags" in tag
        ]
        return tags
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении списка ядер: {e.stderr}")
        return []

def select_kernel_version(device=None):
    """Отображает список доступных ядер и позволяет пользователю выбрать нужную версию.
    Сохраняет выбранную версию в конфигурационный файл.
    """
    if device is None:
        print("Ошибка: Устройство не выбрано.")
        return None

    config_file = os.path.join(CONFIG_DIR, f"{device}.config")
    config = configparser.ConfigParser()
    config.read(config_file)

    git_repo = config.get('Kernel', 'git_repo')
    git_branch = config.get('Kernel', 'git_branch', fallback='main')

    available_kernels = get_available_kernels(git_repo, git_branch)

    if not available_kernels:
        print("Доступные версии ядер не найдены.")
        return None

    print("Доступные версии ядер:")
    for i, kernel in enumerate(available_kernels):
        print(f"{i+1}. {kernel}")

    while True:
        try:
            choice = int(input("Выберите номер версии ядра: "))
            if 1 <= choice <= len(available_kernels):
                selected_kernel = available_kernels[choice - 1]
                config['Kernel']['version'] = selected_kernel
                with open(config_file, 'w') as f:
                    config.write(f)
                print(f"Выбрана версия ядра: {selected_kernel}")
                return selected_kernel
            else:
                print("Неверный выбор. Пожалуйста, введите номер из списка.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер.")

def register():
    """Регистрирует модуль в главном скрипте."""
    return [{"name": "Выбрать версию ядра", "function": select_kernel_version}]
