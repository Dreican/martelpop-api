import logging.config
from pathlib import Path

import logging
from app.core.config.settings import settings


def setup_logging():
    log_dir = Path(settings.log.dir)
    log_dir.mkdir(parents=True, exist_ok=True)

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
                    "level": settings.log.level
                },

                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": f"{log_dir}/{settings.log.file}",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf-8",
                    "level": settings.log.level
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
            },

            "loggers": {
                "uvicorn": {
                    "level": "INFO",
                    "propagate": False,
                },

                "uvicorn.error": {
                    "level": "INFO",
                    "propagate": False,
                },

                "http": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },

            "root": {
                "handlers": ["console", "file", "error_file"],
                "level": settings.log.level
            }
        }
    )
