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

# [START bigqueryconnection_quickstart]

from google.cloud import bigquery_connection_v1 as bq_connection


def main(
    project_id: str = "your-project-id", location: str = "US", transport: str = "grpc"
) -> None:
    """Prints details and summary information about connections for a given admin project and location"""
    client = bq_connection.ConnectionServiceClient(transport=transport)
    print(f"List of connections in project {project_id} in location {location}")
    req = bq_connection.ListConnectionsRequest(
        parent=client.common_location_path(project_id, location)
    )
    for connection in client.list_connections(request=req):
        print(f"\tConnection {connection.friendly_name} ({connection.name})")


# [END bigqueryconnection_quickstart]
