import os
import glob

CONFIG_DIR = "config"  # Папка с конфигами

def get_available_devices():
    """Возвращает список доступных устройств, основываясь на наличии конфигурационных файлов."""
    config_files = glob.glob(os.path.join(CONFIG_DIR, "*.config"))
    return [os.path.basename(f)[:-7] for f in config_files]

def select_device():
    """Отображает список доступных устройств и позволяет пользователю выбрать одно."""
    available_devices = get_available_devices()

    if not available_devices:
        print("Устройства не найдены. Создайте конфигурационный файл для вашего устройства.")
        return None

    print("Доступные устройства:")
    for i, device in enumerate(available_devices):
        print(f"{i+1}. {device}")

    while True:
        try:
            choice = int(input("Выберите номер устройства: "))
            if 1 <= choice <= len(available_devices):
                selected_device = available_devices[choice - 1]
                print(f"Выбрано устройство: {selected_device}")
                return selected_device
            else:
                print("Неверный выбор. Пожалуйста, введите номер из списка.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер.")

def register():
    """Регистрирует модуль в главном скрипте."""
    return [{"name": "Выбрать устройство", "function": select_device}]
