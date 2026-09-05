import logging.config
from pathlib import Path

import seqlog

from app.core.config.configuration import get_config


_STANDARD_LOG_RECORD_ATTRIBUTES = frozenset(
    logging.makeLogRecord({}).__dict__
) | {"message", "asctime"}


class SeqExtraPropertiesFilter(logging.Filter):
    """Expose standard logging ``extra`` values as Seq properties."""

    def filter(self, record: logging.LogRecord) -> bool:
        properties = dict(getattr(record, "log_props", {}))

        properties.update(
            (name, value)
            for name, value in vars(record).items()
            if name not in _STANDARD_LOG_RECORD_ATTRIBUTES
            and name != "log_props"
        )

        record.log_props = properties
        return True


def setup_logging():
    config = get_config()
    log_dir = Path(config.log.dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,

            "formatters": {
                "default": {
                    "format": config.log.format
                }
            },
            "filters": {
                "seq_extra_properties": {
                    "()": SeqExtraPropertiesFilter,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": config.log.level
                },

                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": str(log_dir / config.log.file),
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf-8",
                    "level": config.log.level
                },

                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": str(log_dir / config.log.error_file),
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf-8",
                    "level": "ERROR"
                },

                "seq": {
                    "class": "seqlog.SeqLogHandler",
                    "server_url": config.log.seq_url,
                    "auto_flush_timeout": 1,
                    "filters": ["seq_extra_properties"],
                    "level": config.log.level
                }
            },

            "loggers": {
                "uvicorn": {
                    "handlers": ["console", "file", "seq"],
                    "level": "INFO",
                    "propagate": False,
                },

                "uvicorn.error": {
                    "handlers": ["console", "file", "seq"],
                    "level": "INFO",
                    "propagate": False,
                },

                "uvicorn.access": {
                    "handlers": ["console", "file", "seq"],
                    "level": "INFO",
                    "propagate": False,
                },

                "http": {
                    "handlers": ["console", "file", "seq"],
                    "level": "INFO",
                    "propagate": False,
                },
            },

            "root": {
                "handlers": ["console", "file", "error_file", "seq"],
                "level": config.log.level
            }
        }
    )
