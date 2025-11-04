# Poradock Logging Client

Python-клиент для работы с API логирования на https://api.alexmayka.ru

## 📦 Установка

### Способ 1: Из Git репозитория (рекомендуется)

```bash
pip install git+https://github.com/AlexMayka/logging_python.git
```

### Способ 2: Локальная установка

```bash
# Клонируйте репозиторий или скопируйте папку
git clone https://github.com/AlexMayka/logging_python.git
cd logging_python

# Установите в режиме разработки
pip install -e .

# Или просто установите
pip install .
```

### Способ 3: Прямая установка из папки

```bash
pip install /путь/к/папке/logging_python
```

## 🚀 Быстрый старт

```python
from log import Log
from datetime import datetime

# Инициализация с токеном
logger = Log(token="your-token-here")

# Отправка логов
logger.info("Информационное сообщение")
logger.debug("Отладочное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")
logger.critical("Критическая ошибка")

# Запись о завершении выполнения
start_time = datetime.now()
# ... ваш код ...
end_time = datetime.now()

logger.finish_success(
    period_from=start_time,
    period_to=end_time,
    host="server-name",
    duration=10.5
)
```

## 📚 API

### Методы логирования

- `logger.info(msg: str)` - информационное сообщение
- `logger.debug(msg: str)` - отладочное сообщение  
- `logger.warning(msg: str)` - предупреждение
- `logger.error(msg: str)` - ошибка
- `logger.critical(msg: str)` - критическая ошибка

### Методы записи о запусках

- `logger.finish_success(period_from, period_to, host, **kwargs)` - успешное завершение
- `logger.finish_warning(period_from, period_to, host, **kwargs)` - завершение с предупреждениями
- `logger.finish_error(period_from, period_to, host, **kwargs)` - завершение с ошибкой

**Параметры:**
- `period_from: datetime` - время начала
- `period_to: datetime` - время окончания
- `host: str` - имя хоста
- `**kwargs` - дополнительные параметры (будут сохранены в поле `Extra`)

## 📋 Полный пример

```python
from log import Log
from datetime import datetime

logger = Log(token="f95e9305-107e-4967-ad3f-c65c70e8930a")

def process_data():
    logger.info("Начало обработки данных")
    start_time = datetime.now()
    
    try:
        # Ваша логика
        logger.debug("Выполнение шага 1")
        # ...
        
        end_time = datetime.now()
        logger.finish_success(
            period_from=start_time,
            period_to=end_time,
            host="my-server",
            records_processed=1000
        )
        
    except Exception as e:
        end_time = datetime.now()
        logger.error(f"Ошибка: {e}")
        logger.finish_error(
            period_from=start_time,
            period_to=end_time,
            host="my-server",
            error=str(e)
        )

if __name__ == "__main__":
    process_data()
```

## 🔑 Получение токена

Для работы требуется активный токен, привязанный к боту. Получить токен можно в панели управления API.

## 📡 Эндпоинты

- `POST /api/v1/logs` - создание лога
- `POST /api/v1/eff-runs` - создание записи о запуске

## ✅ HTTP статус коды

- `201` - успешно создано
- `400` - неверный формат данных
- `401` - токен деактивирован или невалиден
- `403` - недостаточно прав
- `500` - ошибка сервера

## 🤝 Для разработчиков

### Структура проекта

```
logging_python/
├── log/
│   ├── __init__.py       # Экспорт классов
│   └── log.py            # Основная библиотека
├── main.py               # Пример использования
├── requirements.txt      # Зависимости
├── setup.py              # Конфигурация пакета
└── README.md             # Документация
```

### Разработка

```bash
# Клонирование
git clone https://github.com/AlexMayka/logging_python.git
cd logging_python

# Установка в режиме разработки
pip install -e .

# Запуск примера
python main.py
```

## 📄 Лицензия

MIT License

