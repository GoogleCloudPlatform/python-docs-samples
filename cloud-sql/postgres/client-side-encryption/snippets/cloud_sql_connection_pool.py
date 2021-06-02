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

# [START cloud_sql_postgres_cse_db]
import sqlalchemy


def init_tcp_connection_engine(
    db_user: str, db_pass: str, db_name: str, db_host: str
) -> sqlalchemy.engine.base.Engine:
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name,  # e.g. "my-database-name"
        ),
    )
    print("Created TCP connection pool")
    return pool


def init_unix_connection_engine(
    db_user: str,
    db_pass: str,
    db_name: str,
    cloud_sql_connection_name: str,
    db_socket_dir: str,
) -> sqlalchemy.engine.base.Engine:
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mpostgresql+pg8000://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
    )
    print("Created Unix socket connection pool")
    return pool


def init_db(
    db_user: str,
    db_pass: str,
    db_name: str,
    table_name: str,
    cloud_sql_connection_name: str = None,
    db_socket_dir: str = None,
    db_host: str = None,
) -> sqlalchemy.engine.base.Engine:

    if db_host:
        db = init_tcp_connection_engine(db_user, db_pass, db_name, db_host)
    else:
        db = init_unix_connection_engine(
            db_user, db_pass, db_name, cloud_sql_connection_name, db_socket_dir
        )

    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} "
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "team VARCHAR(6) NOT NULL, voter_email BYTEA, "
            "PRIMARY KEY (vote_id) );"
        )

    print(f"Created table {table_name} in db {db_name}")
    return db


# [END cloud_sql_postgres_cse_db]
