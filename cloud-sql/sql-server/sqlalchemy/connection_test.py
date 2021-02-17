from contextlib import contextmanager
import logging
import os
from typing import Dict

import pyodbc
import pytest

import main


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("tcp_db_connection")
def test_tcp_connection(tcp_db_connection):
    assert tcp_db_connection is not None


@pytest.mark.usefixtures('tcp_db_connection')
def test_get(tcp_db_connection):
    main.create_tables()
    context = main.get_index_context()
    assert isinstance(context, dict)
    assert len(context.get('recent_votes')) >= 0
    assert context.get('tab_count') >= 0
    assert context.get('space_count') >= 0


env_map = {
    'SQLSERVER_USER': 'DB_USER',
    'SQLSERVER_PASSWORD': 'DB_PASS',
    'SQLSERVER_DATABASE': 'DB_NAME',
    'SQLSERVER_HOST': 'DB_HOST',
    'SQLSERVER_INSTANCE': 'CLOUD_SQL_CONNECTION_NAME',
}


@pytest.fixture(scope='module')
def tcp_db_connection():
    with mapped_env_variables(env_map):
        yield from _common_setup()


def _common_setup():
    try:
        pool = main.init_connection_engine()
    except pyodbc.OperationalError as e:
        logger.warning(
            'Could not connect to the production database. '
            'If running tests locally, is the cloud_sql_proxy currently running?'
        )
        raise e

    with pool.connect() as conn:
        conn.execute("SELECT GETDATE()")

    yield pool


@contextmanager
def mapped_env_variables(env_map: Dict):
    """Copies values in the environment to other values, also in
    the environment.

    In `env_map`, keys are source environment variables and values
    are destination environment variables.
    """
    for key, value in env_map.items():
        os.environ[value] = os.environ[key]

    try:
        yield
    finally:
        for variable_name in env_map.values():
            if os.environ.get(variable_name):
                del os.environ[variable_name]
