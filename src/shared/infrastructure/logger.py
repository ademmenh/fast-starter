import gzip
import json
import logging
import os
import shutil
from datetime import UTC, datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

__all__ = ["JsonFormatter", "GZipTimedRotatingFileHandler", "Logger"]


class JsonFormatter(logging.Formatter):
    """Formats every log record as a single-line JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        self.formatException  # ensure exc_info is populated if present
        payload: dict = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)
        extra_keys = set(record.__dict__) - {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
            "taskName",
        }
        for key in extra_keys:
            payload[key] = getattr(record, key)
        return json.dumps(payload, default=str)


class GZipTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Daily-rotating file handler that gzip-compresses each rolled-over file,
    matching the behaviour of winston-daily-rotate-file.

    Active file : logs/app.log
    Rotated file: logs/app.log.YYYY-MM-DD.gz
    """

    def namer(self, default_name: str) -> str:
        return default_name + ".gz"

    def rotator(self, source: str, dest: str) -> None:
        with open(source, "rb") as f_in, gzip.open(dest, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(source)


class Logger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(f"restaurant_api.{name}")

    def info(self, message: str, **kwargs) -> None:
        self._logger.info(message, extra=kwargs)

    def warn(self, message: str, **kwargs) -> None:
        self._logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._logger.error(message, extra=kwargs, exc_info=True)
