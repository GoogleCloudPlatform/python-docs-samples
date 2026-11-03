# Copyright 2026 Google LLC
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

# [START bigquery_query_biglake_gcs_temp_table]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def query_biglake_gcs_temp_table(
    project_id: str,
    connection_id: str,
) -> None:
    """Configures and queries a temporary BigLake table backed by Cloud Storage.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        connection_id: Fully qualified BigQuery Cloud Resource connection ID
            (for example, 'projects/example-project/locations/us/connections/example-conn').
    """
    client = bigquery.Client(project=project_id)
    temp_table_name = "example_us_states_temp"
    source_uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    prefix_filter = "W%"

    # Bind the Cloud Resource connection and explicit schema to a temporary CSV ExternalConfig.
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [source_uri]
    external_config.connection_id = connection_id
    external_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    external_config.csv_options.skip_leading_rows = 1

    job_config = bigquery.QueryJobConfig(
        table_definitions={temp_table_name: external_config},
        query_parameters=[
            bigquery.ScalarQueryParameter("prefix_filter", "STRING", prefix_filter),
        ],
    )
    sql = f"""
        SELECT
          name,
          post_abbr
        FROM `{temp_table_name}`
        WHERE post_abbr LIKE @prefix_filter
        ORDER BY post_abbr ASC
        LIMIT 10;
    """

    try:
        print(f"Querying temporary BigLake table {temp_table_name} via {connection_id}")
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: BigLake connection '{connection_id}' or URI '{source_uri}' "
            f"not found in project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to query temporary BigLake table via connection "
            f"'{connection_id}' in project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {connection_id}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Rows Returned: {len(rows)}")
    print(f"Source URI: {source_uri}")


# [END bigquery_query_biglake_gcs_temp_table]
