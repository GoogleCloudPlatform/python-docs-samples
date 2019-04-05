# coding: utf-8
import os
import logging


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
QUERIES_RUN_TOPIC = os.getenv('QUERIES_RUN_TOPIC', None)
MARK_CLEAN_UP_TOPIC = os.getenv('MARK_CLEAN_UP_TOPIC', None)
SCC_SEARCH_TIMEOUT_SECONDS = os.getenv('SCC_SEARCH_TIMEOUT_SECONDS', None)
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
