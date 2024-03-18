import logging
import sys

import structlog

LOGGING_LEVEL = 10


def setup_logger() -> structlog.typing.FilteringBoundLogger:
    logging.basicConfig(
        level=LOGGING_LEVEL,
        stream=sys.stdout,
    )
    logger: structlog.typing.FilteringBoundLogger = structlog.get_logger(
        structlog.stdlib.BoundLogger
    )
    shared_processors: list[structlog.typing.Processor] = [
        structlog.processors.add_log_level
    ]
    if sys.stderr.isatty():
        processors = shared_processors + [
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.processors.TimeStamper(fmt=None, utc=True),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(LOGGING_LEVEL),
    )
    return logger
