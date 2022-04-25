"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
db_config = {
    # Pool size is the maximum number of permanent connections to keep.
    "pool_size": 5,
    # Temporarily exceeds the set pool_size if no connections are available.
    "max_overflow": 2,
    # The total number of concurrent connections for your application will be
    # a total of pool_size and max_overflow.
    # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
    # new connection from the pool. After the specified amount of time, an
    # exception will be thrown.
    "pool_timeout": 30,  # 30 seconds
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    # Connections that live longer than the specified amount of time will be
    # reestablished
    "pool_recycle": 1800,  # 30 minutes
}

# [START cloud_sql_postgres_sqlalchemy_connect_connector]
import os
import sqlalchemy
import pg8000
from google.cloud.sql.connector import Connector, IPTypes

# create_connector_pool initializes a connection pool for a
# Cloud SQL instance of Postgres using the Cloud SQL Python Connector.
def create_connector_pool():
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets safe.

    # Either a DB_USER or a DB_IAM_USER should be defined. If both are
    # defined, DB_IAM_USER takes precedence.
    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'
    db_user = os.environ.get("DB_USER", "")  # e.g. 'my-db-user'
    db_iam_user = os.environ.get("DB_IAM_USER", "")  # e.g. 'sa-name@project-id.iam'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    private_ip = os.environ.get("PRIVATE_IP", False)

    if db_iam_user:
        enable_iam_auth = True
    else:
        enable_iam_auth = False

    if private_ip:
        ip_type = IPTypes.PRIVATE
    else:
        ip_type = IPTypes.PUBLIC

    connector = Connector(ip_type, enable_iam_auth)

    def getconn() -> pg8000.dbapi.Connection:
        if db_iam_user:
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_iam_user,
                db=db_name,
            )
        else:
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
            )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # [START_EXCLUDE]
        **db_config
        # [END_EXCLUDE]
    )
    return pool


# [END cloud_sql_postgres_sqlalchemy_connect_connector]
