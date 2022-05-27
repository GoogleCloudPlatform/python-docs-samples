# Copyright 2022 Google LLC
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

# [START cloud_sql_server_sqlalchemy_connect_tcp]
# [START cloud_sql_server_sqlalchemy_sslcerts]
import os

import sqlalchemy


# connect_tcp_socket initializes a TCP connection pool
# for a Cloud SQL instance of MySQL.
def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_host = os.environ["INSTANCE_HOST"]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    db_port = os.environ["DB_PORT"]  # e.g. 1433

    connect_args = {}
    # [END cloud_sql_server_sqlalchemy_connect_tcp]
    # For deployments that connect directly to a Cloud SQL instance without
    # using the Cloud SQL Proxy, configuring SSL certificates will ensure the
    # connection is encrypted.
    query_string = {}
    if os.environ.get("DB_ROOT_CERT"):
        query_string["driver"] = "ODBC Driver 17 for SQL Server"
    if os.environ.get("CLOUD_SQL_AUTH_PROXY_IP_ADDRESS_TYPE") == "PRIVATE":
        query_string = {
            "driver": "ODBC Driver 17 for SQL Server",
            "Encrypt": "yes",
            "Trusted_Connection": "no"
        }


    # [START cloud_sql_server_sqlalchemy_connect_tcp]
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mssql+pyodbc://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mssql+pyodbc",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
            query=query_string,
        ),
        # [START_EXCLUDE]
        # [START cloud_sql_server_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=5,
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_server_sqlalchemy_limit]

        # [START cloud_sql_server_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_server_sqlalchemy_backoff]

        # [START cloud_sql_server_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # [END cloud_sql_server_sqlalchemy_timeout]

        # [START cloud_sql_server_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # re-established
        pool_recycle=1800,  # 30 minutes
        # [END cloud_sql_server_sqlalchemy_lifetime]
        # [END_EXCLUDE]
    )

    return pool
    # [END cloud_sql_sqlserver_sqlalchemy_create_tcp]
    # [END cloud_sql_server_sqlalchemy_create_tcp]


# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None



# [END cloud_sql_server_sqlalchemy_sslcerts]
# [END cloud_sql_server_sqlalchemy_connect_tcp]
