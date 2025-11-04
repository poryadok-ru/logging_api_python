

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
        Initialize the Log class
        
        Args:
            token: API token for authentication
            timeout: Request timeout in seconds (default: 10)
            auto_host: Automatically detect hostname (default: True)
            silent_errors: Don't raise exceptions on network errors (default: False)
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
        """Set the headers for the Log class"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    
    def _safe_request(self, method: str, url: str, **kwargs):
        """
        Safe request wrapper with error handling
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            Response object or None if silent_errors=True
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
        """Log an info message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.INFO.value})

    def debug(self, msg: str):
        """Log a debug message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.DEBUG.value})

    def warning(self, msg: str):
        """Log a warning message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.WARNING.value})

    def error(self, msg: str):
        """Log an error message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.ERROR.value})

    def critical(self, msg: str):
        """Log a critical message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": LogStatus.CRITICAL.value})

    def log_start(self, msg: str, level: LogStatus):
        """Log a start message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        return self._safe_request("POST", url, json={"Msg": msg, "Status": level.value})

    def finish_success(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, **kwargs: Any):
        """Log a finish success message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": LogType.SUCCESS.value, 
            "Extra": kwargs
        })

    def finish_warning(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, **kwargs: Any):
        """Log a finish warning message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": LogType.WARNING.value, 
            "Extra": kwargs
        })

    def finish_error(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, **kwargs: Any):
        """Log a finish error message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": LogType.ERROR.value, 
            "Extra": kwargs
        })

    def finish_log(self, period_from: datetime, period_to: datetime, host: Optional[str] = None, status: LogType = None, **kwargs: Any):
        """Log a finish message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        return self._safe_request("POST", url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host or self.host, 
            "Status": status.value, 
            "Extra": kwargs
        })
    
    def __enter__(self):
        """Start timing for context manager"""
        self._start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically log finish based on exception"""
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