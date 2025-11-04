

from enum import Enum
from typing import Any
import requests as req
from datetime import datetime

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

    def __init__(self, token: str) -> None:
        """Initialize the Log class"""
        self.token = token
        self.headers = self.set_headers(token=token)
        
        self.session = req.Session()
        self.session.headers.update(self.headers)

    def set_headers(self, token: str) -> dict[str, str]:
        """Set the headers for the Log class"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def info(self, msg: str):
        """Log an info message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        response = self.session.post(url=url, json={"Msg": msg, "Status": LogStatus.INFO.value})
        return response

    def debug(self, msg: str):
        """Log a debug message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        response = self.session.post(url=url, json={"Msg": msg, "Status": LogStatus.DEBUG.value})
        return response

    def warning(self, msg: str):
        """Log a warning message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        response = self.session.post(url=url, json={"Msg": msg, "Status": LogStatus.WARNING.value})
        return response

    def error(self, msg: str):
        """Log an error message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        response = self.session.post(url=url, json={"Msg": msg, "Status": LogStatus.ERROR.value})
        return response

    def critical(self, msg: str):
        """Log a critical message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        response = self.session.post(url=url, json={"Msg": msg, "Status": LogStatus.CRITICAL.value})
        return response

    def log_start(self, msg: str, level: LogStatus):
        """Log a start message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.LOGS.value}"
        response = self.session.post(url=url, json={"Msg": msg, "Status": level.value})
        return response

    
    
    def finish_success(self, period_from: datetime, period_to: datetime, host: str, **kwargs: Any):
        """Log a finish success message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        response = self.session.post(url=url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host, 
            "Status": LogType.SUCCESS.value, 
            "Extra": kwargs
        })
        return response

    def finish_warning(self, period_from: datetime, period_to: datetime, host: str, **kwargs: Any):
        """Log a finish warning message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        response = self.session.post(url=url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host, 
            "Status": LogType.WARNING.value, 
            "Extra": kwargs
        })
        return response

    def finish_error(self, period_from: datetime, period_to: datetime, host: str, **kwargs: Any):
        """Log a finish error message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        response = self.session.post(url=url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host, 
            "Status": LogType.ERROR.value, 
            "Extra": kwargs
        })
        return response

    def finish_log(self, period_from: datetime, period_to: datetime, host: str, status: LogType, **kwargs: Any):
        """Log a finish message"""
        url = f"{self.URL_BASE}/{self.API_GROUP}{Endpoint.EFF_RUNS.value}"
        response = self.session.post(url=url, json={
            "PeriodFrom": period_from.isoformat(), 
            "PeriodTo": period_to.isoformat(), 
            "Host": host, 
            "Status": status.value, 
            "Extra": kwargs
        })
        return response