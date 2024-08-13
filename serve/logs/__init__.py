import logging
import os
import sys
from logging import handlers

# Global variable to store the logger instance
_logger = None


def get_logger():
    global _logger
    if _logger is None:
        # Create the logger instance if it doesn't exist
        _logger = logging.getLogger("life-bookshelf-ai")
        _logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
        format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        _logger.addHandler(ch)

        fh = handlers.RotatingFileHandler(
            os.path.join(os.path.dirname(__file__), "life-bookshelf-ai.log"),
            maxBytes=(1048576 * 5),
            backupCount=7,
        )
        fh.setFormatter(format)
        _logger.addHandler(fh)

    return _logger
