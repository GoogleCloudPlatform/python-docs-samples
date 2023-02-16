# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bigqueryconnection_create_connection]
from google.cloud import bigquery_connection_v1 as bq_connection

"""This sample shows how to create a BigQuery connection with a Cloud SQL for MySQL database"""


def main() -> None:
    # TODO(developer): Set all variables for your Cloud SQL for MySQL connection.
    project_id = "your-project-id"  # set project_id
    location = "US"  # set location
    # See: https://cloud.google.com/bigquery/docs/locations for a list of
    # available locations.
    database = "my-database"  # set database name
    username = "my-username"  # set database username
    password = "my-password"  # set database password
    cloud_sql_conn_name = ""  # set the name of your connection
    transport = "grpc"  # Set the transport to either "grpc" or "rest"

    cloud_sql_credential = bq_connection.CloudSqlCredential(
        {
            "username": username,
            "password": password,
        }
    )
    cloud_sql_properties = bq_connection.CloudSqlProperties(
        {
            "type_": bq_connection.CloudSqlProperties.DatabaseType.MYSQL,
            "database": database,
            "instance_id": cloud_sql_conn_name,
            "credential": cloud_sql_credential,
        }
    )
    create_mysql_connection(project_id, location, cloud_sql_properties, transport)


def create_mysql_connection(
    project_id: str,
    location: str,
    cloud_sql_properties: bq_connection.CloudSqlProperties,
    transport: str,
) -> None:
    connection = bq_connection.types.Connection({"cloud_sql": cloud_sql_properties})
    client = bq_connection.ConnectionServiceClient(transport=transport)
    parent = client.common_location_path(project_id, location)
    request = bq_connection.CreateConnectionRequest(
        {"parent": parent, "connection": connection}
    )
    response = client.create_connection(request)
    print(f"Created connection successfully: {response.name}")


# [END bigqueryconnection_create_connection]
