import sys
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    """Configure centralized logging for the INSIGHT-X platform."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "insightx.log")

    logger = logging.getLogger("insightx")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Prevent duplicate handlers if setup is called multiple times
    if not logger.handlers:
        # Console Handler (Stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # Rotating File Handler (Max 10MB per file, up to 5 backups)
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

logger = setup_logging()