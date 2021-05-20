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

# [START cloud_sql_postgres_cse_query]
import os

import sqlalchemy
import tink

from .cloud_kms_env_aead import init_tink_env_aead
from .cloud_sql_connection_pool import init_db
from .encrypt_and_insert_data import encrypt_and_insert_data


def main() -> None:
    db_user = os.environ["DB_USER"]  # e.g. "root", "postgres"
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
    query_and_decrypt_data(db, env_aead, table_name)


def query_and_decrypt_data(
    db: sqlalchemy.engine.base.Engine,
    env_aead: tink.aead.KmsEnvelopeAead,
    table_name: str,
) -> None:
    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_votes = conn.execute(
            f"SELECT team, time_cast, voter_email FROM {table_name} "
            "ORDER BY time_cast DESC LIMIT 5"
        ).fetchall()

        print("Team\tEmail\tTime Cast")

        for row in recent_votes:
            team = row[0]

            # Postgres pads CHAR fields with spaces. These will need to be removed before
            # decrypting.
            aad = team.rstrip()

            # Use the envelope AEAD primitive to decrypt the email, using the team name as
            # associated data. Encryption with associated data ensures authenticity
            # (who the sender is) and integrity (the data has not been tampered with) of that
            # data, but not its secrecy. (see RFC 5116 for more info)
            email = env_aead.decrypt(row[2], aad.encode()).decode()
            time_cast = row[1]

            # Print recent votes
            print(f"{team}\t{email}\t{time_cast}")


# [END cloud_sql_postgres_cse_query]

if __name__ == "__main__":
    main()
