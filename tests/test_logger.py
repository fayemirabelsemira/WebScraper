from pathlib import Path

from src.scraper.logger import get_logger


def test_logger_creation():
    logger = get_logger("test_logger")

    assert logger is not None
    assert logger.name == "test_logger"


def test_logger_writes_message():
    logger = get_logger("test_logger_write")

    logger.info("Test log message")

    log_file = Path("logs/scraper.log")

    assert log_file.exists()

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert "Test log message" in content