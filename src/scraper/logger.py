import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import LOG_FILE, LOG_LEVEL


def get_logger(name: str = "scraper") -> logging.Logger:
    """Create and return a configured application logger."""

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    log_file = Path(LOG_FILE)

    # Make sure the log directory exists
    log_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Convert the configured log level into a logging constant
    level = getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO
    )

    logger.setLevel(level)

    # ==========================================
    # LOG FORMAT
    # ==========================================

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    # ==========================================
    # FILE HANDLER
    # ==========================================

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # ==========================================
    # CONSOLE HANDLER
    # ==========================================

    console_handler = logging.StreamHandler()

    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # ==========================================
    # ADD HANDLERS
    # ==========================================

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger