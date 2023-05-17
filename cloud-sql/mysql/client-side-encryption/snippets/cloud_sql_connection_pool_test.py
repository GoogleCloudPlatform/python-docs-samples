# Copyright 2021 Google LLC
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

# Copyright 2021 Google LLC
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

from __future__ import annotations

import os
import uuid

import pytest

from snippets.cloud_sql_connection_pool import (
    init_db,
    init_tcp_connection_engine,
    init_unix_connection_engine
)


@pytest.fixture(name="conn_vars")
def setup() -> dict[str, str]:
    try:
        conn_vars = {}
        conn_vars["db_user"] = os.environ["MYSQL_USER"]
        conn_vars["db_pass"] = os.environ["MYSQL_PASSWORD"]
        conn_vars["db_name"] = os.environ["MYSQL_DATABASE"]
        conn_vars["db_host"] = os.environ["MYSQL_HOST"]
        conn_vars["instance_conn_name"] = os.environ["MYSQL_INSTANCE"]
        conn_vars["db_socket_dir"] = os.getenv("DB_SOCKET_DIR", "/cloudsql")
    except KeyError:
        raise Exception(
            "The following env variables must be set to run these tests:"
            "MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST, "
            "MYSQL_INSTANCE"
        )
    else:
        yield conn_vars


def test_init_tcp_connection_engine(
        capsys: pytest.CaptureFixture,
        conn_vars: dict[str, str]) -> None:

    init_tcp_connection_engine(
        db_user=conn_vars["db_user"],
        db_name=conn_vars["db_name"],
        db_pass=conn_vars["db_pass"],
        db_host=conn_vars["db_host"],
    )

    captured = capsys.readouterr().out
    assert "Created TCP connection pool" in captured


def test_init_unix_connection_engine(
        capsys: pytest.CaptureFixture,
        conn_vars: dict[str, str]) -> None:

    init_unix_connection_engine(
        db_user=conn_vars["db_user"],
        db_name=conn_vars["db_name"],
        db_pass=conn_vars["db_pass"],
        instance_connection_name=conn_vars["instance_conn_name"],
        db_socket_dir=conn_vars["db_socket_dir"],
    )

    captured = capsys.readouterr().out
    assert "Created Unix socket connection pool" in captured


def test_init_db(
        capsys: pytest.CaptureFixture,
        conn_vars: dict[str, str]) -> None:

    table_name = f"votes_{uuid.uuid4().hex}"

    init_db(
        db_user=conn_vars["db_user"],
        db_name=conn_vars["db_name"],
        db_pass=conn_vars["db_pass"],
        table_name=table_name,
        db_host=conn_vars["db_host"],
    )

    captured = capsys.readouterr().out
    assert f"Created table {table_name} in db {conn_vars['db_name']}" in captured
