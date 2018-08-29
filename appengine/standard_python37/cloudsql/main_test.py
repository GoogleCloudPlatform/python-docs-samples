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

from unittest.mock import MagicMock

import mysql.connector.pooling
import psycopg2.pool


def test_main():
    import main
    main.mysql.connector = MagicMock()
    main.mysql.connector.connect().cursor().fetchall.return_value = [['0']]

    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '0' in r.data.decode('utf-8')


def test_main_pooling():
    mysql.connector.pooling.MySQLConnectionPool = MagicMock()

    import main_pooling

    mock_pool = main_pooling.mysql.connector.pooling.MySQLConnectionPool()
    mock_pool.get_connection().cursor().fetchall.return_value = [['0']]

    main_pooling.app.testing = True
    client = main_pooling.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '0' in r.data.decode('utf-8')


def test_main_postgressql():
    import main_postgressql
    main_postgressql.psycopg2.connect = MagicMock()
    mock_cursor = main_postgressql.psycopg2.connect().cursor()
    mock_cursor.__enter__().fetchall.return_value = [['0']]

    main_postgressql.app.testing = True
    client = main_postgressql.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '0' in r.data.decode('utf-8')


def test_main_postgressql_pooling():
    psycopg2.pool.ThreadedConnectionPool = MagicMock()

    import main_postgressql_pooling

    mock_pool = main_postgressql_pooling.psycopg2.pool.ThreadedConnectionPool()
    mock_pool.getconn().cursor().__enter__().fetchall.return_value = [['0']]

    main_postgressql_pooling.app.testing = True
    client = main_postgressql_pooling.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '0' in r.data.decode('utf-8')
