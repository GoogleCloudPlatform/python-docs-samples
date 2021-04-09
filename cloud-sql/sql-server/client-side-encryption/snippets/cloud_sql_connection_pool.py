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

# [START cloud_sql_sqlserver_cse_db]
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy import Table


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
        # mssql+pytds://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="mssql+pytds",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 1433
            database=db_name,  # e.g. "my-database-name"
        ),
    )
    print("Created TCP connection pool")
    return pool


def init_db(
    db_user: str,
    db_pass: str,
    db_name: str,
    db_host: str,
    table_name: str,
) -> sqlalchemy.engine.base.Engine:

    db = init_tcp_connection_engine(db_user, db_pass, db_name, db_host)

    # Create tables (if they don't already exist)
    if not db.has_table("votes"):
        metadata = sqlalchemy.MetaData(db)
        Table(
            table_name,
            metadata,
            Column("vote_id", Integer, primary_key=True, nullable=False),
            Column("voter_email", LargeBinary, nullable=False),
            Column("time_cast", DateTime, nullable=False),
            Column("candidate", String(6), nullable=False),
        )
        metadata.create_all()

    print(f"Created table {table_name} in db {db_name}")
    return db


# [END cloud_sql_sqlserver_cse_db]
