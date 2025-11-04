# Poradock Logging Client

Python-клиент для работы с API логирования Poradock на https://api.alexmayka.ru

## 📦 Установка

**Через SSH (рекомендуется для приватных репозиториев):**
```bash
pip install git+ssh://git@github.com/AlexMayka/logging_python.git
```

**Через HTTPS:**
```bash
pip install git+https://github.com/AlexMayka/logging_python.git
```

**Локальная установка:**
```bash
git clone git@github.com:AlexMayka/logging_python.git
cd logging_python
pip install .
```

## 🚀 Быстрый старт

```python
from log import Log
from datetime import datetime

# Инициализация с токеном
logger = Log(token="your-token-here")

# Отправка логов
logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")

# Запись о завершении выполнения
start_time = datetime.now()
# ... ваш код ...
end_time = datetime.now()

logger.finish_success(
    period_from=start_time,
    period_to=end_time,
    host="my-server",
    records_processed=100
)
```

## 📚 API

### Класс `Log`

**Инициализация:**
```python
logger = Log(token="your-token-here")
```

### Методы логирования

Все методы возвращают `Response` объект с информацией о результате запроса.

| Метод | Описание |
|-------|----------|
| `logger.info(msg: str)` | Информационное сообщение |
| `logger.debug(msg: str)` | Отладочное сообщение |
| `logger.warning(msg: str)` | Предупреждение |
| `logger.error(msg: str)` | Сообщение об ошибке |
| `logger.critical(msg: str)` | Критическая ошибка |

**Пример:**
```python
response = logger.info("Приложение запущено")
if response.status_code == 201:
    print("Лог успешно отправлен")
```

### Методы записи о запусках

| Метод | Описание |
|-------|----------|
| `logger.finish_success(period_from, period_to, host, **kwargs)` | Успешное завершение |
| `logger.finish_warning(period_from, period_to, host, **kwargs)` | Завершение с предупреждениями |
| `logger.finish_error(period_from, period_to, host, **kwargs)` | Завершение с ошибкой |

**Параметры:**
- `period_from` (`datetime`) - время начала выполнения
- `period_to` (`datetime`) - время окончания выполнения
- `host` (`str`) - имя хоста/сервера
- `**kwargs` - дополнительные параметры (сохраняются в поле `Extra`)

**Пример:**
```python
logger.finish_success(
    period_from=start_time,
    period_to=end_time,
    host="production-server",
    duration_seconds=123.45,
    records_processed=5000
)
```

## 📋 Полный пример использования

```python
from log import Log
from datetime import datetime

# Инициализация
logger = Log(token="f95e9305-107e-4967-ad3f-c65c70e8930a")

def process_data():
    """Пример обработки данных с логированием"""
    logger.info("Начало обработки данных")
    start_time = datetime.now()
    
    try:
        # Основная логика
        logger.debug("Загрузка данных из БД")
        data = load_data()
        
        logger.debug("Обработка данных")
        result = process(data)
        
        logger.info(f"Обработано {len(result)} записей")
        
        # Успешное завершение
        end_time = datetime.now()
        logger.finish_success(
            period_from=start_time,
            period_to=end_time,
            host="app-server-01",
            records_processed=len(result),
            duration_seconds=(end_time - start_time).total_seconds()
        )
        
    except Exception as e:
        # Обработка ошибок
        end_time = datetime.now()
        logger.error(f"Ошибка обработки: {e}")
        logger.finish_error(
            period_from=start_time,
            period_to=end_time,
            host="app-server-01",
            error=str(e),
            error_type=type(e).__name__
        )
        raise

if __name__ == "__main__":
    process_data()
```

## 🔑 Токен доступа

Для работы требуется **активный токен**, привязанный к боту. 

Токен передается при инициализации логгера:
```python
logger = Log(token="ваш-токен-здесь")
```

## 📡 API Эндпоинты

Библиотека работает со следующими эндпоинтами:

- **POST** `/api/v1/logs` - создание лога
- **POST** `/api/v1/eff-runs` - создание записи о запуске

### HTTP статус коды

| Код | Описание |
|-----|----------|
| `201` | Успешно создано |
| `400` | Неверный формат данных |
| `401` | Токен деактивирован или невалиден |
| `403` | Недостаточно прав |
| `500` | Ошибка сервера |

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
git clone git@github.com:AlexMayka/logging_python.git
cd logging_python

# Установка в режиме разработки (изменения сразу доступны)
pip install -e .
```

### Зависимости

- `requests >= 2.31.0` - для HTTP запросов

### Типы и Enum

Доступные enum классы:

**`LogStatus`** - уровни логирования:
- `LogStatus.INFO` → "Info"
- `LogStatus.DEBUG` → "Debug"
- `LogStatus.WARNING` → "Warning"
- `LogStatus.ERROR` → "Error"
- `LogStatus.CRITICAL` → "Critical"

**`LogType`** - типы завершения:
- `LogType.SUCCESS` → "success"
- `LogType.WARNING` → "warning"
- `LogType.ERROR` → "error"

## ⚙️ Требования

- Python >= 3.7
- requests >= 2.31.0

## 📝 Лицензия

MIT License

---

**Разработано для Poradock**
