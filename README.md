# Poradock Logging Client

Python-клиент для работы с API логирования Poradock на https://api.automation.poryadok.ru/logging

## 📦 Установка

**Через SSH (рекомендуется для приватных репозиториев):**
```bash
pip install git+ssh://git@github.com/poryadok-ru/logging_api_python.git
```

**Через HTTPS:**
```bash
pip install git+https://github.com/poryadok-ru/logging_api_python.git
```

**Локальная установка:**
```bash
git clone git@github.com:poryadok-ru/logging_api_python.git
cd logging_python
pip install .
```

## 🚀 Быстрый старт

### 1️⃣ Простое логирование
```python
from log import Log

logger = Log(token="your-token-here")
logger.info("Приложение запущено")
logger.error("Произошла ошибка")
```

### 2️⃣ С контекстным менеджером (рекомендуется) ⭐
```python
from log import Log

# Автоматическое отслеживание времени выполнения
with Log(token="your-token-here") as logger:
    logger.info("Начинаем обработку данных")
    # ваш код здесь
    logger.info("Обработка завершена")
    
# После выхода из блока with автоматически отправится:
# - finish_success() если не было ошибок
# - finish_error() если произошло исключение
```

### 3️⃣ Тихий режим (не прерывает работу при сетевых ошибках)
```python
from log import Log

logger = Log(
    token="your-token-here",
    silent_errors=True,  # ошибки API не остановят программу
    timeout=5            # таймаут запроса в секундах
)

logger.info("Это сообщение попытается отправиться")
# Если API недоступен - программа продолжит работу
```

## 📚 API

### Класс `Log`

#### Инициализация

```python
logger = Log(
    token="your-token-here",    # API токен (обязательно)
    timeout=10,                  # таймаут запроса в секундах (по умолчанию: 10)
    auto_host=True,              # автоопределение имени хоста (по умолчанию: True)
    silent_errors=False          # не прерывать работу при ошибках API (по умолчанию: False)
)
```

**Параметры:**
- `token` (str) - API токен для аутентификации (обязательный)
- `timeout` (int) - таймаут HTTP запросов в секундах (по умолчанию: 10)
- `auto_host` (bool) - автоматически определять hostname через `socket.gethostname()` (по умолчанию: True)
- `silent_errors` (bool) - не выбрасывать исключения при ошибках сети (по умолчанию: False)

### Методы логирования

Все методы возвращают `Response` объект с информацией о результате запроса (или `None` если `silent_errors=True` и произошла ошибка).

| Метод | Описание | Уровень |
|-------|----------|---------|
| `logger.info(msg: str)` | Информационное сообщение | Info |
| `logger.debug(msg: str)` | Отладочное сообщение | Debug |
| `logger.warning(msg: str)` | Предупреждение | Warning |
| `logger.error(msg: str)` | Сообщение об ошибке | Error |
| `logger.critical(msg: str)` | Критическая ошибка | Critical |

**Примеры:**
```python
# Простая отправка лога
logger.info("Приложение запущено")

# Проверка результата
response = logger.error("Не удалось подключиться к БД")
if response and response.status_code == 201:
    print("Лог успешно отправлен")

# Логирование с переменными
records_count = 150
logger.info(f"Обработано записей: {records_count}")
```

### Методы записи о запусках

| Метод | Описание |
|-------|----------|
| `logger.finish_success(period_from, period_to, host, **kwargs)` | Успешное завершение |
| `logger.finish_warning(period_from, period_to, host, **kwargs)` | Завершение с предупреждениями |
| `logger.finish_error(period_from, period_to, host, **kwargs)` | Завершение с ошибкой |
| `logger.finish_log(period_from, period_to, host, status, **kwargs)` | Завершение с произвольным статусом |

**Параметры:**
- `period_from` (`datetime`) - время начала выполнения (обязательный)
- `period_to` (`datetime`) - время окончания выполнения (обязательный)
- `host` (`str`, optional) - имя хоста/сервера (по умолчанию используется auto_host)
- `status` (`LogType`, только для finish_log) - статус завершения
- `**kwargs` - любые дополнительные параметры (сохраняются в поле `Extra`)

**Примеры:**

```python
from datetime import datetime

start = datetime.now()
# ... ваш код ...
end = datetime.now()

# Успешное завершение с дополнительными данными
logger.finish_success(
    period_from=start,
    period_to=end,
    host="production-server",  # опционально
    duration_seconds=123.45,
    records_processed=5000,
    file_name="data.csv"
)

# Завершение с ошибкой
logger.finish_error(
    period_from=start,
    period_to=end,
    error="Connection timeout",
    error_type="TimeoutError",
    records_processed=2500
)

# Завершение с предупреждением
logger.finish_warning(
    period_from=start,
    period_to=end,
    warning="Some records skipped",
    records_skipped=10
)
```

## ⚡ Асинхронная функциональность

Библиотека поддерживает асинхронные методы для использования в `async/await` коде. Все асинхронные методы имеют префикс `a_` (async).

### Быстрый старт с asyncio

```python
import asyncio
from log import Log

async def main():
    async with Log(token="your-token") as logger:
        await logger.a_info("Асинхронное приложение запущено")
        await logger.a_debug("Отладочная информация")

        # ... ваш асинхронный код ...

        # Автоматическое логирование времени выполнения
    # при выходе из контекста

asyncio.run(main())
```

### Асинхронные методы логирования

Все асинхронные методы возвращают `aiohttp.ClientResponse` объект (или `None` если `silent_errors=True` и произошла ошибка).

| Метод | Описание | Уровень |
|-------|----------|---------|
| `await logger.a_info(msg: str)` | Асинхронное информационное сообщение | Info |
| `await logger.a_debug(msg: str)` | Асинхронное отладочное сообщение | Debug |
| `await logger.a_warning(msg: str)` | Асинхронное предупреждающее сообщение | Warning |
| `await logger.a_error(msg: str)` | Асинхронное сообщение об ошибке | Error |
| `await logger.a_critical(msg: str)` | Асинхронное критическое сообщение | Critical |

**Примеры:**
```python
async def async_task():
    logger = Log(token="your-token", silent_errors=True)

    # Простая отправка
    response = await logger.a_info("Асинхронное сообщение")
    if response and response.status == 201:
        print("✓ Лог отправлен")

    # С переменными
    user_count = 1250
    await logger.a_info(f"Обработано пользователей: {user_count}")

    # Закрытие сессии (рекомендуется)
    await logger.close()
```

### Асинхронные методы завершения запусков

| Метод | Описание |
|-------|----------|
| `await logger.a_finish_success(period_from, period_to, host, **kwargs)` | Асинхронное успешное завершение |
| `await logger.a_finish_warning(period_from, period_to, host, **kwargs)` | Асинхронное завершение с предупреждением |
| `await logger.a_finish_error(period_from, period_to, host, **kwargs)` | Асинхронное завершение с ошибкой |
| `await logger.a_finish_log(period_from, period_to, host, status, **kwargs)` | Асинхронное завершение с произвольным статусом |

**Примеры:**
```python
from datetime import datetime

async def process_data():
    async with Log(token="your-token") as logger:
        start_time = datetime.now()
        await logger.a_info("Начало обработки данных")

        try:
            # Ваш асинхронный код обработки данных
            await asyncio.sleep(2)  # Имитация работы

            end_time = datetime.now()
            await logger.a_finish_success(
                period_from=start_time,
                period_to=end_time,
                records_processed=5000,
                duration_seconds=(end_time - start_time).total_seconds()
            )

        except Exception as e:
            end_time = datetime.now()
            await logger.a_error(f"Ошибка обработки: {e}")
            await logger.a_finish_error(
                period_from=start_time,
                period_to=end_time,
                error=str(e),
                error_type=type(e).__name__
            )
```

### Асинхронный контекстный менеджер

Класс `Log` поддерживает асинхронный протокол контекстного менеджера:

```python
async def async_operation():
    async with Log(token="your-token") as logger:
        await logger.a_info("Начало работы")
        # ваш асинхронный код
        # автоматически логируется время выполнения и статус
```

### Закрытие соединений

Для корректного освобождения ресурсов рекомендуется использовать асинхронный контекстный менеджер или явно закрывать соединения:

```python
# Рекомендуемый способ
async with Log(token="your-token") as logger:
    await logger.a_info("Сообщение")

# Или явное закрытие
logger = Log(token="your-token")
await logger.a_info("Сообщение")
await logger.close()  # Важно!
```

### Примеры использования

#### Пример 1: Асинхронный ETL процесс

```python
import asyncio
from log import Log
from datetime import datetime

async def async_etl():
    async with Log(token="your-token", silent_errors=True) as logger:
        await logger.a_info("=== Запуск асинхронного ETL ===")

        # Extract
        await logger.a_info("Извлечение данных...")
        await asyncio.sleep(1)  # Имитация работы

        # Transform
        await logger.a_info("Трансформация данных...")
        await asyncio.sleep(1)

        # Load
        await logger.a_info("Загрузка данных...")
        await asyncio.sleep(1)

        await logger.a_info("=== ETL завершен успешно ===")

asyncio.run(async_etl())
```

#### Пример 2: Асинхронная обработка файлов

```python
import asyncio
import aiofiles
from log import Log

async def process_files_async(file_list):
    async with Log(token="your-token") as logger:
        await logger.a_info(f"Начало обработки {len(file_list)} файлов")

        processed = 0
        for file_path in file_list:
            try:
                await logger.a_debug(f"Обработка: {file_path}")

                # Асинхронная обработка файла
                async with aiofiles.open(file_path, 'r') as f:
                    content = await f.read()
                    # ... обработка content ...

                processed += 1

            except Exception as e:
                await logger.a_error(f"Ошибка {file_path}: {e}")

        await logger.a_info(f"Обработано файлов: {processed}")

# Использование
asyncio.run(process_files_async(["file1.txt", "file2.txt"]))
```

#### Пример 3: Асинхронная фоновая задача

```python
import asyncio
from log import Log

async def background_monitor():
    logger = Log(token="your-token", silent_errors=True)

    try:
        await logger.a_info("Мониторинг запущен")

        while True:
            await logger.a_debug("Проверка состояния")
            # ... проверки системы ...

            await asyncio.sleep(60)  # Каждую минуту

    except KeyboardInterrupt:
        await logger.a_info("Мониторинг остановлен")
    finally:
        await logger.close()  # Важно закрыть соединение

asyncio.run(background_monitor())
```

### Контекстный менеджер

Класс `Log` поддерживает протокол контекстного менеджера (`with` statement), который автоматически:
- Записывает время начала при входе в контекст
- Отправляет `finish_success()` при успешном выходе
- Отправляет `finish_error()` при возникновении исключения

**Пример:**
```python
with Log(token="your-token-here") as logger:
    logger.info("Начало работы")
    # ваш код
    # автоматически логируется время выполнения и статус
```

**Обработка исключений:**
```python
try:
    with Log(token="your-token-here") as logger:
        logger.info("Обработка файла")
        raise ValueError("Неверный формат данных")
except ValueError as e:
    print(f"Ошибка перехвачена: {e}")
    # finish_error() уже отправлен автоматически!
```

## 📋 Примеры использования

### Пример 1: Простой скрипт с логированием

```python
from log import Log

# Простейший вариант
logger = Log(token="your-token-here")

logger.info("Скрипт запущен")
logger.debug("Загрузка конфигурации")
logger.info("Обработка данных...")
logger.info("Скрипт завершен")
```

### Пример 2: С контекстным менеджером (рекомендуется)

```python
from log import Log

# Автоматическое отслеживание времени и статуса
with Log(token="your-token-here") as logger:
    logger.info("Начало обработки")
    
    # Ваш код здесь
    for i in range(100):
        # обработка данных
        pass
    
    logger.info("Обработка завершена")

# Автоматически отправится finish_success с временем выполнения
```

### Пример 3: Обработка файлов с логированием

```python
from log import Log

def process_files(file_list):
    """Обработка списка файлов с логированием"""
    
    with Log(token="your-token-here", silent_errors=True) as logger:
        logger.info(f"Начало обработки {len(file_list)} файлов")
        
        processed = 0
        errors = 0
        
        for file_path in file_list:
            try:
                logger.debug(f"Обработка файла: {file_path}")
                
                # Ваша логика обработки файла
                # result = process_single_file(file_path)
                
                processed += 1
                
            except Exception as e:
                logger.error(f"Ошибка при обработке {file_path}: {e}")
                errors += 1
        
        # Итоговый статус
        if errors == 0:
            logger.info(f"✓ Все файлы обработаны успешно ({processed}/{len(file_list)})")
        else:
            logger.warning(f"⚠ Обработка завершена с ошибками: {processed} успешно, {errors} ошибок")

# Использование
process_files(["file1.txt", "file2.txt", "file3.txt"])
```

### Пример 4: Ручное управление временем

```python
from log import Log
from datetime import datetime
import time

logger = Log(token="your-token-here")

start_time = datetime.now()
logger.info("Запуск длительной операции")

try:
    # Ваша работа
    time.sleep(5)
    logger.info("Операция выполняется...")
    
    # Успешное завершение
    end_time = datetime.now()
    logger.finish_success(
        period_from=start_time,
        period_to=end_time,
        duration_seconds=(end_time - start_time).total_seconds(),
        records_processed=1500,
        status="completed"
    )
    
except Exception as e:
    # Ошибка
    end_time = datetime.now()
    logger.error(f"Ошибка выполнения: {e}")
    logger.finish_error(
        period_from=start_time,
        period_to=end_time,
        error=str(e),
        error_type=type(e).__name__
    )
    raise
```

### Пример 5: ETL процесс с подробным логированием

```python
from log import Log
from datetime import datetime

def etl_pipeline():
    """ETL процесс с полным логированием"""
    
    with Log(token="your-token-here", silent_errors=True) as logger:
        logger.info("=== Запуск ETL Pipeline ===")
        
        # Extract
        logger.info("Этап 1: Извлечение данных")
        try:
            # data = extract_from_database()
            logger.info("✓ Данные извлечены успешно")
        except Exception as e:
            logger.error(f"✗ Ошибка извлечения: {e}")
            raise
        
        # Transform
        logger.info("Этап 2: Трансформация данных")
        try:
            # transformed_data = transform(data)
            logger.info("✓ Данные трансформированы успешно")
        except Exception as e:
            logger.error(f"✗ Ошибка трансформации: {e}")
            raise
        
        # Load
        logger.info("Этап 3: Загрузка данных")
        try:
            # load_to_warehouse(transformed_data)
            logger.info("✓ Данные загружены успешно")
        except Exception as e:
            logger.error(f"✗ Ошибка загрузки: {e}")
            raise
        
        logger.info("=== ETL Pipeline завершен успешно ===")

# Запуск
etl_pipeline()
```

### Пример 6: Фоновая задача с тихим режимом

```python
from log import Log
import time

def background_task():
    """Фоновая задача, которая не должна прерываться при ошибках логирования"""
    
    # silent_errors=True - если API недоступен, задача продолжит работу
    logger = Log(
        token="your-token-here",
        silent_errors=True,
        timeout=3
    )
    
    logger.info("Фоновая задача запущена")
    
    while True:
        try:
            # Ваша периодическая работа
            logger.debug("Проверка состояния системы")
            
            # check_system_health()
            
            time.sleep(60)  # Каждую минуту
            
        except KeyboardInterrupt:
            logger.info("Фоновая задача остановлена пользователем")
            break
        except Exception as e:
            logger.error(f"Ошибка в фоновой задаче: {e}")
            time.sleep(60)
```

## 💡 Лучшие практики

### 1. Используйте контекстный менеджер для автоматического отслеживания

✅ **Рекомендуется:**
```python
with Log(token="your-token") as logger:
    logger.info("Работа...")
    # автоматическое логирование времени и статуса
```

❌ **Не рекомендуется:**
```python
logger = Log(token="your-token")
start = datetime.now()
# ... код ...
end = datetime.now()
logger.finish_success(start, end)  # легко забыть
```

### 2. Включайте silent_errors для критичных приложений

Для production систем, где недоступность API логирования не должна прерывать работу:

```python
logger = Log(token="your-token", silent_errors=True)
```

### 3. Добавляйте контекстную информацию в логи

```python
# Плохо
logger.error("Ошибка")

# Хорошо
logger.error(f"Ошибка обработки файла {filename}: {error_message}")
```

### 4. Используйте правильные уровни логирования

- `debug()` - детальная отладочная информация
- `info()` - общие информационные сообщения
- `warning()` - предупреждения, не критичные проблемы
- `error()` - ошибки, требующие внимания
- `critical()` - критические ошибки, требующие немедленного вмешательства

### 5. Передавайте дополнительные метрики в finish_*

```python
logger.finish_success(
    period_from=start,
    period_to=end,
    records_processed=1000,
    duration_seconds=123.45,
    memory_used_mb=256,
    file_size_mb=10.5
)
```

## 🔑 Токен доступа

Для работы требуется **активный токен**, привязанный к боту. 

Токен передается при инициализации логгера:
```python
logger = Log(token="your-token-here")
```

**Рекомендации по безопасности:**
- Не храните токен в коде - используйте переменные окружения
- Не коммитьте токен в Git

```python
import os
from log import Log

# Получение токена из переменной окружения
token = os.getenv("PORADOCK_LOG_TOKEN")
logger = Log(token=token)
```

## 🚨 Обработка ошибок

### Режим по умолчанию (с исключениями)

```python
logger = Log(token="your-token")  # silent_errors=False по умолчанию

try:
    logger.info("Сообщение")
except requests.exceptions.RequestException as e:
    print(f"Ошибка отправки лога: {e}")
    # Обработка ошибки
```

### Тихий режим (без исключений)

```python
logger = Log(token="your-token", silent_errors=True)

# Если API недоступен, будет выведено сообщение в консоль
# и метод вернет None, но программа продолжит работу
response = logger.info("Сообщение")

if response is None:
    print("Лог не был отправлен")
elif response.status_code == 201:
    print("Лог отправлен успешно")
```

### Проверка результата отправки

```python
logger = Log(token="your-token", silent_errors=True)

response = logger.error("Критическая ошибка")

if response:
    if response.status_code == 201:
        print("✓ Лог отправлен")
    elif response.status_code == 401:
        print("✗ Невалидный токен")
    elif response.status_code == 500:
        print("✗ Ошибка сервера")
else:
    print("✗ Не удалось связаться с API")
```

### Таймауты

```python
# Установка кастомного таймаута (по умолчанию 10 секунд)
logger = Log(token="your-token", timeout=5)

try:
    logger.info("Сообщение")
except requests.exceptions.Timeout:
    print("Превышено время ожидания ответа от сервера")
```

## 📡 API Эндпоинты

Библиотека работает со следующими эндпоинтами API `https://api.automation.poryadok.ru/logging`:

| Endpoint | Метод | Описание | Используется в |
|----------|-------|----------|----------------|
| `/api/v1/logs` | POST | Создание лога | `info()`, `debug()`, `warning()`, `error()`, `critical()`, `log_start()` |
| `/api/v1/eff-runs` | POST | Создание записи о запуске | `finish_success()`, `finish_warning()`, `finish_error()`, `finish_log()` |

### HTTP статус коды

| Код | Описание |
|-----|----------|
| `201` | Успешно создано |
| `400` | Неверный формат данных |
| `401` | Токен деактивирован или невалиден |
| `403` | Недостаточно прав |
| `500` | Ошибка сервера |

### Формат запроса

**Для логов (`/api/v1/logs`):**
```json
{
  "Msg": "Текст сообщения",
  "Status": "Info"
}
```

**Для запусков (`/api/v1/eff-runs`):**
```json
{
  "PeriodFrom": "2025-11-04T10:00:00",
  "PeriodTo": "2025-11-04T10:05:00",
  "Host": "production-server",
  "Status": "success",
  "Extra": {
    "records_processed": 1500,
    "duration_seconds": 300.5
  }
}
```

## 🛠️ Структура проекта

```
logging_python/
├── log/
│   ├── __init__.py    # Экспорт классов
│   └── log.py         # Основная реализация
├── requirements.txt   # Зависимости
├── setup.py          # Конфигурация пакета
└── README.md         # Документация
```

## 🔧 Для разработчиков

### Установка для разработки

```bash
# Клонирование репозитория
git clone git@github.com:poryadok-ru/logging_api_python.git
cd logging_python

# Установка в режиме разработки (изменения сразу доступны)
pip install -e .
```

### Зависимости

- `requests >= 2.31.0` - для синхронных HTTP запросов
- `aiohttp >= 3.9.0` - для асинхронных HTTP запросов

### Типы и Enum

Библиотека предоставляет следующие enum классы для типизации:

#### `LogStatus` - уровни логирования

```python
from log import LogStatus

# Доступные значения:
LogStatus.INFO       # → "Info"
LogStatus.DEBUG      # → "Debug"
LogStatus.WARNING    # → "Warning"
LogStatus.ERROR      # → "Error"
LogStatus.CRITICAL   # → "Critical"
```

**Использование:**
```python
from log import Log, LogStatus

logger = Log(token="your-token")
logger.log_start("Запуск процесса", LogStatus.INFO)
```

#### `LogType` - типы завершения запуска

```python
from log import LogType

# Доступные значения:
LogType.SUCCESS   # → "success"
LogType.WARNING   # → "warning"
LogType.ERROR     # → "error"
```

**Использование:**
```python
from log import Log, LogType
from datetime import datetime

logger = Log(token="your-token")

start = datetime.now()
# ... ваш код ...
end = datetime.now()

logger.finish_log(
    period_from=start,
    period_to=end,
    status=LogType.SUCCESS  # используем enum
)
```

#### `Endpoint` - эндпоинты API (внутренний)

```python
# Используется внутри библиотеки
Endpoint.LOGS      # → "logs"
Endpoint.EFF_RUNS  # → "eff-runs"
```

## ⚙️ Требования

- Python >= 3.7
- requests >= 2.31.0

## ❓ Частые вопросы (FAQ)

### Что делать, если API недоступен?

Используйте параметр `silent_errors=True` при инициализации. Это позволит вашему приложению продолжать работу даже если сервис логирования недоступен:

```python
logger = Log(token="your-token", silent_errors=True)
```

### Как логировать в нескольких местах одновременно?

Создайте экземпляр логгера один раз и используйте его во всех модулях:

```python
# config.py
from log import Log
import os

logger = Log(
    token=os.getenv("PORADOCK_LOG_TOKEN"),
    silent_errors=True
)
```

```python
# main.py
from config import logger

def main():
    logger.info("Приложение запущено")
```

### Можно ли использовать без контекстного менеджера?

Да, можно использовать все методы напрямую:

```python
logger = Log(token="your-token")
logger.info("Сообщение")
logger.error("Ошибка")

# Ручное управление временем
start = datetime.now()
# ... код ...
logger.finish_success(start, datetime.now())
```

### Как проверить, что лог успешно отправлен?

Проверьте код ответа:

```python
response = logger.info("Тестовое сообщение")
if response and response.status_code == 201:
    print("✓ Лог успешно отправлен")
```

### Что означает ошибка 401?

Ошибка 401 означает, что токен невалидный или деактивирован. Проверьте:
1. Правильность токена
2. Что токен активен в системе Poradock

### Можно ли изменить таймаут запросов?

Да, используйте параметр `timeout` (в секундах):

```python
logger = Log(token="your-token", timeout=30)  # 30 секунд
```

### Как логировать из Docker контейнера?

Передайте токен через переменную окружения:

```dockerfile
# Dockerfile
ENV PORADOCK_LOG_TOKEN="your-token"
```

```python
# app.py
import os
from log import Log

logger = Log(token=os.getenv("PORADOCK_LOG_TOKEN"))
```

### Поддерживается ли асинхронный режим?

Да! Начиная с версии 2.1, библиотека поддерживает полный асинхронный режим с использованием `aiohttp`. Все асинхронные методы имеют префикс `a_`.

```python
import asyncio
from log import Log

async def main():
    async with Log(token="your-token") as logger:
        await logger.a_info("Асинхронное сообщение")
        await logger.a_debug("Отладочная информация")

asyncio.run(main())
```

Для минимизации задержек в асинхронном режиме также рекомендуется использовать `silent_errors=True` и небольшой `timeout`.

## 🔍 Устранение проблем

### Проблема: `ConnectionError` при отправке логов

**Решение:** Проверьте доступность API и используйте `silent_errors=True`:

```python
logger = Log(token="your-token", silent_errors=True, timeout=5)
```

### Проблема: Логи не отображаются в системе

**Возможные причины:**
1. Неверный токен - проверьте токен
2. Токен деактивирован - активируйте токен в системе
3. Ошибка сети - проверьте доступность `api.automation.poryadok.ru/logging`

**Проверка:**
```python
response = logger.info("Тест")
print(f"Статус: {response.status_code if response else 'Нет ответа'}")
```

### Проблема: `TypeError: Object of type datetime is not JSON serializable`

**Решение:** Библиотека автоматически сериализует datetime. Если видите эту ошибку, убедитесь что используете объекты `datetime`:

```python
from datetime import datetime

start = datetime.now()  # правильно
# start = "2025-11-04"  # неправильно
```

## 📊 Краткая справка

| Задача | Код |
|--------|-----|
| Простой лог | `logger.info("Сообщение")` |
| Лог с контекстом | `with Log(token="...") as logger:` |
| Тихий режим | `Log(token="...", silent_errors=True)` |
| Увеличить таймаут | `Log(token="...", timeout=30)` |
| Завершение успешное | `logger.finish_success(start, end)` |
| Завершение с ошибкой | `logger.finish_error(start, end, error="...")` |
| Токен из переменной | `Log(token=os.getenv("TOKEN"))` |
| Проверка отправки | `if response.status_code == 201:` |

## 🔗 Полезные ссылки

- **API документация:** https://api.automation.poryadok.ru/logging/swagger/index.html
- **Репозиторий API (Backend):** https://github.com/AlexMayka/logs - серверная часть для приёма и обработки логов
- **Репозиторий клиента (Python):** https://github.com/poryadok-ru/logging_api_python
- **Установка:** `pip install git+ssh://git@github.com/poryadok-ru/logging_api_python.git`

## 📝 Лицензия

MIT License

---

**Разработано для Poradock** 🚀

*Версия документации: 2.1*
