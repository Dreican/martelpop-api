import logging
import logging.config
from pathlib import Path

from app.core.config import settings


def setup_logging():
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": settings.LOG_LEVEL
                },

                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": f"{log_dir}/app.log",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf-8",
                    "level": settings.LOG_LEVEL
                },

                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": f"{log_dir}/error.log",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf-8",
                    "level": "ERROR"
                },

                "root": {
                    "handlers": ["console", "file", "error_file"],
                    "level": settings.LOG_LEVEL
                }
            }
        }
    )