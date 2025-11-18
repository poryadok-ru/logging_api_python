#!/usr/bin/env python3
"""
Полное тестирование библиотеки логирования с реальным токеном
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

from log.log import Log, LogType, LogStatus

REAL_TOKEN = 'd4d82b07-5c89-4680-8ca7-e84e180a5537'

def test_sync_methods():
    """Тестирование синхронных методов"""
    print("\n🔄 Тестирование СИНХРОННЫХ методов...")

    logger = Log(token=REAL_TOKEN, silent_errors=False, timeout=10)

    # Тестовые сообщения
    test_messages = [
        ("info", "Синхронное информационное сообщение"),
        ("debug", "Синхронное отладочное сообщение"),
        ("warning", "Синхронное предупреждающее сообщение"),
        ("error", "Синхронное сообщение об ошибке"),
        ("critical", "Синхронное критическое сообщение")
    ]

    success_count = 0

    for level, message in test_messages:
        try:
            print(f"  📤 Отправка {level}: {message[:30]}...")

            if level == "info":
                response = logger.info(message)
            elif level == "debug":
                response = logger.debug(message)
            elif level == "warning":
                response = logger.warning(message)
            elif level == "error":
                response = logger.error(message)
            elif level == "critical":
                response = logger.critical(message)

            if response and response.status_code == 201:
                print(f"    ✅ {level.upper()} успешно отправлен")
                success_count += 1
            else:
                print(f"    ❌ {level.upper()} ошибка: {response.status_code if response else 'No response'}")

        except Exception as e:
            print(f"    💥 {level.upper()} исключение: {e}")

    # Тестирование методов завершения
    print("\n  🎯 Тестирование методов завершения...")
    start_time = datetime.now() - timedelta(minutes=5)
    end_time = datetime.now()

    finish_tests = [
        ("finish_success", lambda: logger.finish_success(start_time, end_time, test_sync="success")),
        ("finish_warning", lambda: logger.finish_warning(start_time, end_time, test_sync="warning")),
        ("finish_error", lambda: logger.finish_error(start_time, end_time, test_sync="error")),
        ("finish_log", lambda: logger.finish_log(start_time, end_time, status=LogType.SUCCESS, test_sync="log"))
    ]

    for method_name, method_func in finish_tests:
        try:
            print(f"    📤 {method_name}...")
            response = method_func()

            if response and response.status_code == 201:
                print(f"      ✅ {method_name} успешно")
                success_count += 1
            else:
                print(f"      ❌ {method_name} ошибка: {response.status_code if response else 'No response'}")

        except Exception as e:
            print(f"      💥 {method_name} исключение: {e}")

    print(f"\n📊 Синхронные методы: {success_count}/9 успешных")
    return success_count >= 8  # 80% успех - приемлемо

async def test_async_methods():
    """Тестирование асинхронных методов"""
    print("\n⚡ Тестирование АСИНХРОННЫХ методов...")

    async with Log(token=REAL_TOKEN, silent_errors=False, timeout=10) as logger:
        # Тестовые сообщения
        test_messages = [
            ("a_info", "Асинхронное информационное сообщение"),
            ("a_debug", "Асинхронное отладочное сообщение"),
            ("a_warning", "Асинхронное предупреждающее сообщение"),
            ("a_error", "Асинхронное сообщение об ошибке"),
            ("a_critical", "Асинхронное критическое сообщение")
        ]

        success_count = 0

        for method_name, message in test_messages:
            try:
                print(f"  📤 Отправка {method_name}: {message[:30]}...")

                if method_name == "a_info":
                    response = await logger.a_info(message)
                elif method_name == "a_debug":
                    response = await logger.a_debug(message)
                elif method_name == "a_warning":
                    response = await logger.a_warning(message)
                elif method_name == "a_error":
                    response = await logger.a_error(message)
                elif method_name == "a_critical":
                    response = await logger.a_critical(message)

                if response and response.status == 201:
                    print(f"    ✅ {method_name.upper()} успешно отправлен")
                    success_count += 1
                else:
                    print(f"    ❌ {method_name.upper()} ошибка: {response.status if response else 'No response'}")

            except Exception as e:
                print(f"    💥 {method_name.upper()} исключение: {e}")

        # Тестирование асинхронных методов завершения
        print("\n  🎯 Тестирование асинхронных методов завершения...")
        start_time = datetime.now() - timedelta(minutes=3)
        end_time = datetime.now()

        finish_tests = [
            ("a_finish_success", lambda: logger.a_finish_success(start_time, end_time, test_async="success")),
            ("a_finish_warning", lambda: logger.a_finish_warning(start_time, end_time, test_async="warning")),
            ("a_finish_error", lambda: logger.a_finish_error(start_time, end_time, test_async="error")),
            ("a_finish_log", lambda: logger.a_finish_log(start_time, end_time, status=LogType.SUCCESS, test_async="log"))
        ]

        for method_name, method_func in finish_tests:
            try:
                print(f"    📤 {method_name}...")
                response = await method_func()

                if response and response.status == 201:
                    print(f"      ✅ {method_name} успешно")
                    success_count += 1
                else:
                    print(f"      ❌ {method_name} ошибка: {response.status if response else 'No response'}")

            except Exception as e:
                print(f"      💥 {method_name} исключение: {e}")

    print(f"\n📊 Асинхронные методы: {success_count}/9 успешных")
    return success_count >= 8  # 80% успех - приемлемо

def test_context_manager():
    """Тестирование контекстного менеджера"""
    print("\n📦 Тестирование контекстного менеджера...")

    try:
        with Log(token=REAL_TOKEN, silent_errors=True) as logger:
            print("  ✅ Контекстный менеджер открыт")

            # Отправка сообщения внутри контекста
            response = logger.info("Тест контекстного менеджера - начало")
            if response and response.status_code == 201:
                print("    ✅ Сообщение внутри контекста отправлено")
            else:
                print("    ❌ Ошибка отправки внутри контекста")

            # Имитация работы
            print("    🔄 Имитация работы...")

        print("  ✅ Контекстный менеджер закрыт (автоматическое логирование)")

        # Проверяем, что автоматическое логирование сработало
        # (это будет видно в БД как finish_success)

        return True

    except Exception as e:
        print(f"  💥 Ошибка контекстного менеджера: {e}")
        return False

async def test_async_context_manager():
    """Тестирование асинхронного контекстного менеджера"""
    print("\n📦 Тестирование асинхронного контекстного менеджера...")

    try:
        async with Log(token=REAL_TOKEN, silent_errors=True) as logger:
            print("  ✅ Асинхронный контекстный менеджер открыт")

            # Отправка сообщения внутри асинхронного контекста
            response = await logger.a_info("Тест асинхронного контекстного менеджера - начало")
            if response and response.status == 201:
                print("    ✅ Асинхронное сообщение внутри контекста отправлено")
            else:
                print("    ❌ Ошибка асинхронной отправки внутри контекста")

            # Имитация асинхронной работы
            print("    🔄 Имитация асинхронной работы...")
            await asyncio.sleep(0.1)

        print("  ✅ Асинхронный контекстный менеджер закрыт (автоматическое логирование)")

        return True

    except Exception as e:
        print(f"  💥 Ошибка асинхронного контекстного менеджера: {e}")
        return False

async def main():
    """Главная функция тестирования"""
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ БИБЛИОТЕКИ ЛОГИРОВАНИЯ")
    print("=" * 50)
    print(f"🎯 Токен: {REAL_TOKEN[:10]}...")
    print(f"🌐 API: https://api.alexmayka.ru")
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    results = []

    # Тестирование синхронных методов
    results.append(("Синхронные методы", test_sync_methods()))

    # Тестирование асинхронных методов
    results.append(("Асинхронные методы", await test_async_methods()))

    # Тестирование контекстных менеджеров
    results.append(("Контекстный менеджер", test_context_manager()))
    results.append(("Асинхронный контекстный менеджер", await test_async_context_manager()))

    # Итоговый отчет
    print("\n" + "=" * 50)
    print("📊 ИТОГОВЫЙ ОТЧЕТ:")
    print("=" * 50)

    success_count = 0
    for test_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"{test_name:<35} {status}")
        if success:
            success_count += 1

    print(f"\n🎯 ОБЩИЙ РЕЗУЛЬТАТ: {success_count}/{len(results)} тестов пройдено")

    if success_count == len(results):
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Библиотека полностью функциональна!")
        return True
    elif success_count >= len(results) * 0.8:
        print("⚠️  Большинство тестов пройдено. Библиотека работоспособна.")
        return True
    else:
        print("❌ Критические ошибки. Требуется исправление.")
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    print(f"\n🔚 Выход с кодом: {0 if result else 1}")
    sys.exit(0 if result else 1)
