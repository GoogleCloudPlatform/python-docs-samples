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

import logging
import os
import uuid

import pytest

from snippets.cloud_kms_env_aead import init_tink_env_aead
from snippets.cloud_sql_connection_pool import init_db
from snippets.encrypt_and_insert_data import encrypt_and_insert_data
from snippets.query_and_decrypt_data import query_and_decrypt_data

REQUIRED_ENV_VARS = [
    "MYSQL_USER", "MYSQL_PASS", "MYSQL_DB", "MYSQL_HOST", "GCP_KMS_URI"]

table_name = f"votes_{uuid.uuid4().hex}"


@pytest.fixture
def check_env_vars():
    for var in REQUIRED_ENV_VARS:
        if not os.environ.get(var):
            raise Exception(
                f"Environment variable {var} must be set to perform tests.")
    yield


@pytest.fixture(name="pool")
def setup_pool():
    pool = init_db(
        db_user=os.environ["MYSQL_USER"],
        db_pass=os.environ["MYSQL_PASS"],
        db_name=os.environ["MYSQL_DB"],
        table_name=table_name,
        db_host=os.environ["MYSQL_HOST"],

    )

    yield pool

    with pool.connect() as conn:
        conn.execute(f"DROP TABLE IF EXISTS `{table_name}`")


@pytest.fixture(name="env_aead")
def setup_key():
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    key_uri = "gcp-kms://" + os.environ["GCP_KMS_URI"]

    env_aead = init_tink_env_aead(key_uri, credentials)

    yield env_aead


def test_query_and_decrypt_data(check_env_vars, pool, env_aead, caplog):
    # Insert data into table before testing
    encrypt_and_insert_data(
        pool, env_aead, table_name, "SPACES", "hello@example.com")

    with caplog.at_level(logging.INFO):
        query_and_decrypt_data(
            pool, env_aead, table_name)
        assert "Team\tEmail\tTime Cast" in caplog.text
        assert "hello@example.com" in caplog.text
