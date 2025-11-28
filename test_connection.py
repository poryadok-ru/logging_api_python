#!/usr/bin/env python3
"""
Простой тест для проверки подключения к API логирования
Использование: python test_connection.py <TOKEN>
"""

import sys
from log import Log

def test_connection(token: str):
    """Тестирует подключение к API"""
    print("=" * 60)
    print("Тест подключения к API логирования")
    print("=" * 60)
    print(f"URL: https://api.automation.poryadok.ru/logging")
    print(f"Token: {token[:10]}...{token[-4:] if len(token) > 14 else '***'}")
    print()
    
    logger = Log(token=token, timeout=10, silent_errors=False)
    
    try:
        print("1. Тест health endpoint...")
        import requests
        health_url = "https://api.automation.poryadok.ru/logging/health"
        health_response = requests.get(health_url, timeout=5)
        print(f"   ✓ Health check: {health_response.status_code} - {health_response.json()}")
        print()
        
        print("2. Тест отправки info лога...")
        response = logger.info("Test connection message from test_connection.py")
        if response and response.status_code == 201:
            print(f"   ✓ Лог успешно отправлен (Status: {response.status_code})")
        else:
            print(f"   ✗ Ошибка отправки лога (Status: {response.status_code if response else 'None'})")
            if response:
                print(f"   Response: {response.text}")
        print()
        
        print("3. Тест отправки debug лога...")
        response = logger.debug("Debug test message")
        if response and response.status_code == 201:
            print(f"   ✓ Debug лог успешно отправлен (Status: {response.status_code})")
        else:
            print(f"   ✗ Ошибка отправки debug лога (Status: {response.status_code if response else 'None'})")
        print()
        
        print("=" * 60)
        print("✓ Все тесты пройдены успешно!")
        print("=" * 60)
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Ошибка сети: {e}")
        print()
        print("=" * 60)
        print("✗ Тесты не пройдены из-за сетевой ошибки")
        print("=" * 60)
        return False
    except Exception as e:
        print(f"   ✗ Неожиданная ошибка: {e}")
        print()
        print("=" * 60)
        print("✗ Тесты не пройдены")
        print("=" * 60)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python test_connection.py <TOKEN>")
        print()
        print("Пример:")
        print("  python test_connection.py your-token-here")
        sys.exit(1)
    
    token = sys.argv[1]
    success = test_connection(token)
    sys.exit(0 if success else 1)

