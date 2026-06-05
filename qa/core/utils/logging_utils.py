import logging
from pathlib import Path


def get_logger(name):
    log_dir = Path("qa/logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logging.getLogger("faker").setLevel(logging.WARNING)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # file handler
        file_handler = logging.FileHandler("qa/logs/test_run.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
