import logging
from logging import Logger

def info(message: str) -> Logger:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger()
    return logger.info(message)