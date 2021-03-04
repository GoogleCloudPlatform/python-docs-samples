# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
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

import pytest
import sqlalchemy

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
    "MYSQL_USER": "DB_USER",
    "MYSQL_PASSWORD": "DB_PASS",
    "MYSQL_DATABASE": "DB_NAME",
    "MYSQL_INSTANCE": "CLOUD_SQL_CONNECTION_NAME",
}


@pytest.fixture(scope="module")
def tcp_db_connection():
    tcp_env_map = {key: value for key, value in env_map.items()}
    tcp_env_map["MYSQL_HOST"] = "DB_HOST"

    with mapped_env_variables(tcp_env_map):
        yield from _common_setup()


@pytest.fixture(scope="module")
def unix_db_connection():
    with mapped_env_variables(env_map):
        yield from _common_setup()


def _common_setup():
    pool = main.init_connection_engine()

    table_name: str = uuid.uuid4().hex

    try:
        with pool.connect() as conn:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS `{table_name}`"
                "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
                "candidate CHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
            )
    except sqlalchemy.exc.OperationalError as e:
        logger.warning(
            "Could not connect to the production database. "
            "If running tests locally, is the cloud_sql_proxy currently running?"
        )
        # If there is cloud sql proxy log, dump the contents.
        home_dir = os.environ.get("HOME", "")
        log_file = f"{home_dir}/cloud_sql_proxy.log"
        if home_dir and os.path.isfile(log_file):
            print(f"Dumping the contents of {log_file}")
            with open(log_file, "r") as f:
                print(f.read())
        raise e

    yield pool

    with pool.connect() as conn:
        conn.execute(f"DROP TABLE IF EXISTS `{table_name}`")


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
