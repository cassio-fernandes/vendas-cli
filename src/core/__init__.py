import logging


def _setup_logger() -> logging.Logger:
    logger = logging.getLogger("vendas-cli")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt="> %(message)s")
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger

logger = _setup_logger()