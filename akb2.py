import os
import importlib

def load_modules(modules_dir="modules"):
    """
    Динамически загружает модули из указанной директории.

    Args:
        modules_dir: Путь к директории с модулями.

    Returns:
        Список загруженных модулей.
    """

    loaded_modules = []
    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"{modules_dir}.{module_name}")
                loaded_modules.append(module)
            except ImportError as e:
                print(f"Ошибка при импорте модуля {module_name}: {e}")
    return loaded_modules

def main():
    """
    Основная функция скрипта.
    """

    modules = load_modules()
    menu_items = []

    for module in modules:
        try:
            # Предполагаем, что register() возвращает список элементов меню
            for item in module.register():
                menu_items.append({'module': module, 'item': item})
        except AttributeError as e:
            print(f"Ошибка при регистрации модуля {module.__name__}: {e}")

    while True:
        # Отображение меню
        print("\nМеню:")
        for i, item in enumerate(menu_items):
            print(f"{i+1}. {item['item']['name']}")

        choice = input("Выберите пункт меню (или введите 'q' для выхода): ")
        if choice.lower() == 'q':
            break

        try:
            choice = int(choice)
            selected_item = menu_items[choice - 1]

            # Вызов функции из модуля
            function = selected_item['item']['function']
            if "arguments" in selected_item['item']:
                args = selected_item['item']['arguments']
                function(*args)  # Распаковка аргументов
            else:
                function()

        except (ValueError, IndexError):
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()
