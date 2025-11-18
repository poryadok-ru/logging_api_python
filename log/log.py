

from enum import Enum
from typing import Any, Optional
import requests as req
from datetime import datetime
import socket
from functools import wraps

class LogStatus(Enum):
    INFO = "Info"
    DEBUG = "Debug"
    WARNING = "Warning"
    ERROR = "Error"
    CRITICAL = "Critical"

class LogType(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

class Endpoint(Enum):
    LOGS = "logs"
    EFF_RUNS = "eff-runs"

class Log:
    URL_BASE = "https://api.alexmayka.ru"
    API_GROUP = "api/v1/"

    def __init__(self, token: str = None, timeout: int = 10, auto_host: bool = True, silent_errors: bool = False) -> None:
        """
        Инициализация класса Log

        Args:
            token: API токен для аутентификации
            timeout: Таймаут запроса в секундах (по умолчанию: 10)
            auto_host: Автоматически определять имя хоста (по умолчанию: True)
            silent_errors: Не выбрасывать исключения при сетевых ошибках (по умолчанию: False)
        """
        self.token = token
        self.timeout = timeout
        self.silent_errors = silent_errors
        self.host = socket.gethostname() if auto_host else None
        self.headers = self.set_headers(token=token)
        
        self.session = req.Session()
        self.session.headers.update(self.headers)
        
        self._start_time: Optional[datetime] = None

    def set_headers(self, token: str) -> dict[str, str]:
        """Установить заголовки для класса Log"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    
    def _safe_request(self, method: str, url: str, **kwargs):
        """
        Безопасная оболочка запроса с обработкой ошибок

        Args:
            method: HTTP метод
            url: URL запроса
            **kwargs: Дополнительные параметры запроса

        Returns:
            Объект ответа или None если silent_errors=True
        """
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            return response
        except req.exceptions.RequestException as e:
            if self.silent_errors:
                print(f"[Logging Error] Failed to send log: {e}")
                return None
            else:
                raise

    def info(self, msg: str):
        """Записать информационное сообщение"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.INFO.value})

    def debug(self, msg: str):
        """Записать отладочное сообщение"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.DEBUG.value})

    def warning(self, msg: str):
        """Записать предупреждающее сообщение"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.WARNING.value})

    def error(self, msg: str):
        """Записать сообщение об ошибке"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.ERROR.value})

    def critical(self, msg: str):
        """Записать критическое сообщение"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.CRITICAL.value})

    def log_start(self, msg: str, level: LogStatus):
        """Записать сообщение о начале"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": level.value})

    def finish_success(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, **kwargs: Any):
        """Записать сообщение об успешном завершении"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": LogType.SUCCESS.value, 
            "Extra": kwargs
        })

    def finish_warning(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, **kwargs: Any):
        """Записать сообщение о завершении с предупреждением"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": LogType.WARNING.value, 
            "Extra": kwargs
        })

    def finish_error(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, **kwargs: Any):
        """Записать сообщение о завершении с ошибкой"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": LogType.ERROR.value, 
            "Extra": kwargs
        })

    def finish_log(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, status: LogType = None, **kwargs: Any):
        """Записать сообщение о завершении"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": status.value, 
            "Extra": kwargs
        })
    
    def __enter__(self):
        """Начать отсчет времени для контекстного менеджера"""
        self._start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматически логировать завершение на основе исключения"""
        end_time = datetime.now()
        
        if exc_type is None:
            self.finish_success(
                period_from=self._start_time,
                period_to=end_time,
                duration_seconds=(end_time - self._start_time).total_seconds()
            )
        else:
            self.finish_error(
                period_from=self._start_time,
                period_to=end_time,
                error=str(exc_val),
                error_type=exc_type.__name__,
                duration_seconds=(end_time - self._start_time).total_seconds()
            )
        
        return False