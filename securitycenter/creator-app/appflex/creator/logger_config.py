import logging
import os

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGER_LEVEL = logging.getLevelName(os.getenv('LOGGER_LEVEL', 'INFO'))


def configure_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(LOGGER_LEVEL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOGGER_LEVEL)
    stream_handler.setFormatter(logging.Formatter(
        LOGGER_FORMAT))
    logger.addHandler(stream_handler)
    logger.info("LOGGER SET for %s", module_name)
    return logger
