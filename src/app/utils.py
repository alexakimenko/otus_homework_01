import logging
from dataclasses import dataclass
from datetime import datetime

import structlog


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        handlers=[logging.StreamHandler()],  # Log to terminal only
    )

    # Configure structlog to use the standard logging system
    structlog.configure(
        processors=[structlog.processors.JSONRenderer()],  # Log in JSON format
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


@dataclass
class LogFile:
    path: str
    date: datetime
