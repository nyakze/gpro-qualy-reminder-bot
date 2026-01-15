import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

_SCRIPT_DIR = None
_LOG_FILE = None


def init_logging_paths(script_dir: str) -> None:
    global _SCRIPT_DIR, _LOG_FILE
    _SCRIPT_DIR = script_dir
    _LOG_FILE = _SCRIPT_DIR + "/gpro_bot.log"


class StructuredLogFormatter(logging.Formatter):
    """Log formatter that outputs structured JSON format"""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra") and record.extra:
            for key, value in record.extra.items():
                if not key.startswith("_"):
                    try:
                        log_data[key] = json.dumps(value)
                    except (TypeError, ValueError):
                        log_data[key] = str(value)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    """Configure structured JSON logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    json_formatter = StructuredLogFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        _LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

    return logger


def log_structured(level: int, message: str, **extra) -> None:
    """Log with structured extra data"""
    logger = logging.getLogger()
    logger.log(level, message, extra=extra)
