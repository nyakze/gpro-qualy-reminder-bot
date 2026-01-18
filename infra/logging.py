import json
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, cast

_SCRIPT_DIR = None
_LOG_FILE = None
_VERBOSE = False
_STARTUP_DATA = {}


def init_logging_paths(script_dir: str) -> None:
    global _SCRIPT_DIR, _LOG_FILE
    _SCRIPT_DIR = script_dir
    _LOG_FILE = _SCRIPT_DIR + "/gpro_bot.log"


def set_startup_data(**kwargs) -> None:
    global _STARTUP_DATA
    _STARTUP_DATA.update(kwargs)


def _format_timestamp() -> str:
    return datetime.utcnow().strftime("%H:%M:%S")


_LEVEL_ABBREV = {
    "DEBUG": "DBG",
    "INFO": "INF",
    "WARNING": "WRN",
    "ERROR": "ERR",
    "CRITICAL": "CRT",
}

_LevelColors = {
    "DEBUG": "gray",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


class StructuredLogFormatter(logging.Formatter):
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

        extra = getattr(record, "extra", None)  # type: ignore
        if extra:
            for key, value in extra.items():
                if not key.startswith("_"):
                    try:
                        log_data[key] = json.dumps(value)
                    except (TypeError, ValueError):
                        log_data[key] = str(value)

        return json.dumps(log_data, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.use_colors = kwargs.pop("use_colors", True)
        super().__init__(*args, **kwargs)
        self._level_width = 5

    def _get_color(self, levelname: str) -> str:
        if not self.use_colors:
            return ""
        color = _LevelColors.get(levelname, "white")
        return color

    def format(self, record: logging.LogRecord) -> str:
        level_abbrev = _LEVEL_ABBREV.get(record.levelname, record.levelname[:5].upper())
        timestamp = _format_timestamp()

        module = record.module
        if len(module) > 15:
            module = module[:12] + "..."

        base = f"[{timestamp}] [{level_abbrev:<5}] {record.getMessage()}"

        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            base += f"\n{exc_text}"

        extra = getattr(record, "extra", None)  # type: ignore
        if extra:
            extra_parts = []
            for key, value in extra.items():
                if not key.startswith("_") and key not in ("reason", "error", "signal", "version", "count", "races", "users_count", "admins_count", "tz_count", "i18n_langs"):
                    try:
                        extra_parts.append(f"{key}={json.dumps(value)}")
                    except (TypeError, ValueError):
                        extra_parts.append(f"{key}={value}")
            if extra_parts:
                base += f" | {' | '.join(extra_parts)}"

        return base


def print_banner() -> None:
    if not _STARTUP_DATA:
        return

    version = _STARTUP_DATA.get("version", "?.?")
    users = _STARTUP_DATA.get("users_count", "?")
    races = _STARTUP_DATA.get("races", "?")
    admins = _STARTUP_DATA.get("admins_count", "?")
    tz_count = _STARTUP_DATA.get("tz_count", "?")
    i18n_langs = _STARTUP_DATA.get("i18n_langs", "?")

    banner = f"""
╔════════════════════════════════════════════════════════╗
║              GPRO Bot v{version} - Starting...               ║
╠════════════════════════════════════════════════════════╣
║  Users: {str(users):<6} │ Races: {str(races):<3} │ Admins: {str(admins):<2}             ║
║  Timezones: {str(tz_count):<4} │ i18n: {str(i18n_langs):<2} languages               ║
╚════════════════════════════════════════════════════════╝"""
    print(banner)


def print_log_rotation_summary() -> None:
    if not _LOG_FILE or not os.path.exists(_LOG_FILE):
        return

    size_bytes = os.path.getsize(_LOG_FILE)
    size_mb = size_bytes / (1024 * 1024)

    print(f"\n📊 Log file: {_LOG_FILE} ({size_mb:.1f} MB)")
    print("📊 Log rotation: 10 MB per file, 5 backups\n")


def setup_logging(verbose: bool = False) -> logging.Logger:
    global _VERBOSE
    _VERBOSE = verbose

    if _LOG_FILE is None:
        raise RuntimeError("Log file path not initialized. Call init_logging_paths() first.")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()

    json_formatter = StructuredLogFormatter()

    file_handler = RotatingFileHandler(
        cast(str, _LOG_FILE), maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ConsoleFormatter(use_colors=sys.stdout.isatty())

    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(console_handler)

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

    return logger


def log_structured(level: int, message: str, **extra) -> None:
    logger = logging.getLogger()
    logger.log(level, message, extra=extra)


class ProgressLogger:
    def __init__(self, name: str, total: int, description: str = ""):
        self.name = name
        self.total = total
        self.current = 0
        self.description = description
        self._last_pct = -1
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self._spinner = iter(lambda: (c for c in chars), None)

    def update(self, n: int = 1, message: str = "") -> None:
        self.current += n
        pct = (self.current / self.total) * 100 if self.total > 0 else 100

        if pct >= self._last_pct + 10:
            self._last_pct = int(pct // 10) * 10

            try:
                spin = next(self._spinner)
            except StopIteration:
                self._spinner = iter(lambda: (c for c in ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]), None)
                spin = "⠋"

            spin_str = f"{spin} " if sys.stdout.isatty() else ""
            logger = logging.getLogger()
            logger.info(f"{spin_str}{self.description}: {self.current}/{self.total} ({pct:.0f}%)")

    def complete(self, final_message: str = "") -> None:
        logger = logging.getLogger()
        complete_msg = final_message or f"{self.description} complete: {self.current}/{self.total}"
        logger.info(f"✅ {complete_msg}")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
