# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from contextlib import contextmanager
import logging
import os
from typing import Dict
import uuid

import pg8000
import pytest

import main


logger = logging.getLogger()


@pytest.mark.usefixtures("tcp_db_connection")
def test_tcp_connection(tcp_db_connection):
    assert tcp_db_connection is not None


@pytest.mark.usefixtures("unix_db_connection")
def test_unix_connection(unix_db_connection):
    assert unix_db_connection is not None


@pytest.mark.usefixtures("tcp_db_connection")
def test_get(tcp_db_connection):
    main.create_tables()
    context = main.get_index_context()
    assert isinstance(context, dict)
    assert len(context.get("recent_votes")) >= 0
    assert context.get("tab_count") >= 0
    assert context.get("space_count") >= 0


env_map = {
    "POSTGRES_USER": "DB_USER",
    "POSTGRES_PASSWORD": "DB_PASS",
    "POSTGRES_DATABASE": "DB_NAME",
    "POSTGRES_INSTANCE": "CLOUD_SQL_CONNECTION_NAME",
}


@pytest.fixture(scope="module")
def tcp_db_connection():
    tcp_env_map = {key: value for key, value in env_map.items()}
    tcp_env_map["POSTGRES_HOST"] = "DB_HOST"

    with mapped_env_variables(tcp_env_map):
        yield from _common_setup()


@pytest.fixture(scope="module")
def unix_db_connection():
    with mapped_env_variables(env_map):
        yield from _common_setup()


def _common_setup():
    try:
        pool = main.init_connection_engine()
    except pg8000.exceptions.InterfaceError as e:
        logger.warning(
            "Could not connect to the production database. "
            "If running tests locally, is the cloud_sql_proxy currently running?"
        )
        raise e

    table_name: str = uuid.uuid4().hex

    with pool.connect() as conn:
        conn.execute(
            f'CREATE TABLE IF NOT EXISTS "{table_name}"'
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "candidate VARCHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
        )

    yield pool

    with pool.connect() as conn:
        conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')


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
