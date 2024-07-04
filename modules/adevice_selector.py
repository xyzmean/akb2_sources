import os
import glob
import json

CONFIG_DIR = "config"  # Папка с конфигами
DEV_FILE = ".dev"

def _save_selected_device(device_name):
    """Сохраняет выбранное устройство в файл .dev."""
    with open(DEV_FILE, "w") as f:
        json.dump({"selected_device": device_name}, f)

def get_available_devices():
    """Возвращает список доступных устройств, основываясь на наличии конфигурационных файлов."""
    config_files = glob.glob(os.path.join(CONFIG_DIR, "*.cfg"))
    return [os.path.basename(f)[:-4] for f in config_files]

def select_device():
    """Отображает список доступных устройств и позволяет пользователю выбрать одно."""
    available_devices = get_available_devices()

    if not available_devices:
        print("Устройства не найдены. Создайте конфигурационный файл для вашего устройства.")
        return

    print("Доступные устройства:")
    for i, device in enumerate(available_devices):
        print(f"{i+1}. {device}")

    while True:
        try:
            choice = int(input("Выберите номер устройства: "))
            if 1 <= choice <= len(available_devices):
                selected_device = available_devices[choice - 1]
                _save_selected_device(selected_device)
                print(f"Выбрано устройство: {selected_device}")
                return
            else:
                print("Неверный выбор. Пожалуйста, введите номер из списка.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер.")

def register():
    """Регистрирует модуль в главном скрипте."""
    return [{"name": "Выбрать устройство", "function": select_device}]
