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

# [START cloud_sql_mysql_cse_insert]
import datetime
import logging
import os

import sqlalchemy
import tink

from .cloud_kms_env_aead import init_tink_env_aead
from .cloud_sql_connection_pool import init_db


logger = logging.getLogger(__name__)


def main() -> None:
    db_user = os.environ["DB_USER"]  # e.g. "root", "mysql"
    db_pass = os.environ["DB_PASS"]  # e.g. "mysupersecretpassword"
    db_name = os.environ["DB_NAME"]  # e.g. "votes_db"

    # Set if connecting using TCP:
    db_host = os.environ["DB_HOST"]  # e.g. "127.0.0.1"

    # Set if connecting using Unix sockets:
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")

    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
    # e.g. "project-name:region:instance-name"

    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    key_uri = "gcp-kms://" + os.environ["GCP_KMS_URI"]
    # e.g. "gcp-kms://projects/...path/to/key
    # Tink uses the "gcp-kms://" prefix for paths to keys stored in Google
    # Cloud KMS. For more info on creating a KMS key and getting its path, see
    # https://cloud.google.com/kms/docs/quickstart

    table_name = "votes"
    team = "TABS"
    email = "hello@example.com"

    env_aead = init_tink_env_aead(key_uri, credentials)
    db = init_db(
        db_user,
        db_pass,
        db_name,
        table_name,
        cloud_sql_connection_name,
        db_socket_dir,
        db_host,
    )

    encrypt_and_insert_data(db, env_aead, table_name, team, email)


def encrypt_and_insert_data(
    db: sqlalchemy.engine.base.Engine,
    env_aead: tink.aead.KmsEnvelopeAead,
    table_name: str,
    team: str,
    email: str,
) -> None:
    time_cast = datetime.datetime.utcnow()
    # Use the envelope AEAD primitive to encrypt the email, using the team name as
    # associated data. Encryption with associated data ensures authenticity
    # (who the sender is) and integrity (the data has not been tampered with) of that
    # data, but not its secrecy. (see RFC 5116 for more info)
    encrypted_email = env_aead.encrypt(email.encode(), team.encode())
    # Verify that the team is one of the allowed options
    if team != "TABS" and team != "SPACES":
        logger.error(f"Invalid team specified: {team}")
        return

    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text(
        f"INSERT INTO {table_name} (time_cast, team, voter_email)"
        " VALUES (:time_cast, :team, :voter_email)"
    )

    # Using a with statement ensures that the connection is always released
    # back into the pool at the end of statement (even if an error occurs)
    with db.connect() as conn:
        conn.execute(
            stmt,
            time_cast=time_cast,
            team=team,
            voter_email=encrypted_email)
    print(f"Vote successfully cast for '{team}' at time {time_cast}!")


# [END cloud_sql_mysql_cse_insert]

if __name__ == "__main__":
    main()
