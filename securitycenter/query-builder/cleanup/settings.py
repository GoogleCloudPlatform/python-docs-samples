import os
import logging


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def configure_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(
        LOGGER_FORMAT))
    logger.addHandler(stream_handler)
    logger.info("LOGGER SET for %s", module_name)
    return logger
