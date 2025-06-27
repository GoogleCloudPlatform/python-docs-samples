# Copyright 2025 Google LLC
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

import os
from pathlib import Path

from google.cloud.alloydb.connector import IPTypes

from pg8000 import dbapi

import pytest

from vector_search import execute_sql_request, get_db_connection, perform_vector_search


GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
ALLOYDB_REGION = os.environ["ALLOYDB_REGION"]
ALLOYDB_CLUSTER = os.environ["ALLOYDB_CLUSTER"]
ALLOYDB_INSTANCE = os.environ["ALLOYDB_INSTANCE"]

ALLOYDB_DATABASE_NAME = os.environ["ALLOYDB_DATABASE_NAME"]
ALLOYDB_PASSWORD = os.environ["ALLOYDB_PASSWORD"]
ALLOYDB_USERNAME = "postgres"


@pytest.fixture(scope="module")
def db_connection() -> dbapi.Connection:
    return get_db_connection(
        project_id=GOOGLE_CLOUD_PROJECT,
        region=ALLOYDB_REGION,
        cluster_id=ALLOYDB_CLUSTER,
        instance_id=ALLOYDB_INSTANCE,
        db_user=ALLOYDB_USERNAME,
        db_pass=ALLOYDB_PASSWORD,
        db_name=ALLOYDB_DATABASE_NAME,
        ip_type=IPTypes.PUBLIC,
    )


def test_basic_vector_search(db_connection: dbapi.Connection) -> None:
    # Install required extensions
    sql_statement = """
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE EXTENSION IF NOT EXISTS alloydb_scann;
    """
    execute_sql_request(db_connection, sql_statement)

    # Insert product and product inventory data
    with open(
        Path(__file__).parent / "resources/example_data.sql", encoding="utf-8"
    ) as f:
        sql_statement = f.read()
        execute_sql_request(db_connection, sql_statement)

    # Perform a Vector search in the DB
    result = perform_vector_search(db_connection, word_to_find="music", limit=3)
    assert len(result) == 3
