 ## Скрипт сборки кастомного ядра Android(AKB2)

Этот скрипт автоматизирует процесс сборки кастомного ядра Android. Он предоставляет удобный интерфейс командной строки для выбора устройства, версии ядра и запуска процесса сборки.

### Структура проекта

```
├── modules
│   ├── device_selector.py
│   ├── kernel_selector.py
│   └── build_kernel.py
└── main.py
```

### Модули

- **[main.py](main.py):** Основной скрипт, который загружает модули и обрабатывает взаимодействие с пользователем.
- **[modules/device_selector.py](modules/device_selector.py):** Модуль для выбора устройства из доступных конфигураций.
- **[modules/kernel_selector.py](modules/kernel_selector.py):** Модуль для выбора версии ядра из указанного Git-репозитория.
- **[modules/build_kernel.py](modules/build_kernel.py):** Модуль для запуска процесса сборки ядра.

### Конфигурация

- **[config/](config/):** Папка для хранения конфигурационных файлов устройств (`.cfg`).
- **[.dev](.dev):** Файл для хранения выбранного устройства.

### Использование

1. **Настройка:**
   - **Создайте конфигурационные файлы устройств:**
     - Создайте файл `.cfg` для каждого поддерживаемого устройства в папке `config`.
     - В каждом файле определите секции `Kernel` и `Build` с необходимыми параметрами:
       ```ini
       [Kernel]
       git_repo = <URL-адрес Git-репозитория с ядрами>
       git_branch = <название ветки Git (необязательно, по умолчанию "main")>
       version = <версия ядра>
       architecture = <архитектура ядра>

       [Build]
       compiler = <путь к кросс-компилятору>
       compiler_flags = <флаги компилятора>
       make_flags = <флаги make>
       ```
   - **Клонируйте репозиторий с ядрами:** Клонируйте репозиторий, указанный в параметре `git_repo` конфигурационного файла устройства.

2. **Запуск скрипта:**
   - Запустите скрипт `main.py`.
   - Следуйте инструкциям в меню, чтобы выбрать устройство, версию ядра и запустить сборку.

### Пример конфигурационного файла устройства ([config/example_device.cfg](config/example_device.cfg))

```ini
[Kernel]
git_repo = https://github.com/example/example_kernel.git
git_branch = main
version = 5.10
architecture = arm64

[Build]
compiler = /path/to/aarch64-linux-android-gcc
compiler_flags = -O2 -march=armv8-a
make_flags = -j8
```

### Зависимости

- Python 3.6+
- Git

### Лицензия

[MIT License](LICENSE)

### Автор

[xyzmean]

