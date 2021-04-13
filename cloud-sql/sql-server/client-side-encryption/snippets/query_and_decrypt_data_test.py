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

import os
import uuid

import pytest
import sqlalchemy
import tink

from snippets.cloud_kms_env_aead import init_tink_env_aead
from snippets.cloud_sql_connection_pool import init_db
from snippets.encrypt_and_insert_data import encrypt_and_insert_data
from snippets.query_and_decrypt_data import query_and_decrypt_data

table_name = f"votes_{uuid.uuid4().hex}"


@pytest.fixture(name="pool")
def setup_pool() -> sqlalchemy.engine.Engine:
    try:
        db_user = os.environ["SQLSERVER_USER"]
        db_pass = os.environ["SQLSERVER_PASSWORD"]
        db_name = os.environ["SQLSERVER_DATABASE"]
        db_host = os.environ["SQLSERVER_HOST"]
    except KeyError:
        raise Exception(
            "The following env variables must be set to run these tests:"
            "SQLSERVER_USER, SQLSERVER_PASSWORD, SQLSERVER_DATABASE, SQLSERVER_HOST")
    else:
        pool = init_db(
            db_user=db_user,
            db_pass=db_pass,
            db_name=db_name,
            table_name=table_name,
            db_host=db_host,
        )

        yield pool

        with pool.connect() as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")


@pytest.fixture(name="env_aead")
def setup_key() -> tink.aead.KmsEnvelopeAead:
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    key_uri = "gcp-kms://" + os.environ["CLOUD_KMS_KEY"]

    env_aead = init_tink_env_aead(key_uri, credentials)

    yield env_aead


def test_query_and_decrypt_data(
    capsys: pytest.CaptureFixture,
    pool: sqlalchemy.engine.Engine,
    env_aead: tink.aead.KmsEnvelopeAead
) -> None:

    # Insert data into table before testing
    encrypt_and_insert_data(
        pool,
        env_aead,
        table_name,
        "SPACES",
        "hello@example.com")

    query_and_decrypt_data(pool, env_aead, table_name)

    captured = capsys.readouterr()
    assert "Team\tEmail\tTime Cast" in captured.out
    assert "hello@example.com" in captured.out
