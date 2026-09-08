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

# [START bigquery_update_with_dml]
import pathlib
from typing import Dict, Optional

from google.cloud import bigquery
from google.cloud.bigquery import enums


def load_from_newline_delimited_json(
    client: bigquery.Client,
    filepath: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = enums.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = [
        bigquery.SchemaField("id", enums.SqlTypeNames.STRING),
        bigquery.SchemaField("user_id", enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("login_time", enums.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("logout_time", enums.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("ip_address", enums.SqlTypeNames.STRING),
    ]

    with open(filepath, "rb") as json_file:
        load_job = client.load_table_from_file(
            json_file, full_table_id, job_config=job_config
        )

    # Wait for load job to finish.
    load_job.result()


def update_with_dml(
    client: bigquery.Client, project_id: str, dataset_id: str, table_id: str
) -> int:
    query_text = f"""
    UPDATE `{project_id}.{dataset_id}.{table_id}`
    SET ip_address = REGEXP_REPLACE(ip_address, r"(\\.[0-9]+)$", ".0")
    WHERE TRUE
    """
    query_job = client.query(query_text)

    # Wait for query job to finish.
    query_job.result()

    assert query_job.num_dml_affected_rows is not None

    print(f"DML query modified {query_job.num_dml_affected_rows} rows.")
    return query_job.num_dml_affected_rows


def run_sample(override_values: Optional[Dict[str, str]] = None) -> int:
    if override_values is None:
        override_values = {}

    client = bigquery.Client()
    filepath = pathlib.Path(__file__).parent / "user_sessions_data.json"
    project_id = client.project
    dataset_id = "sample_db"
    table_id = "UserSessions"
    # [END bigquery_update_with_dml]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    dataset_id = override_values.get("dataset_id", dataset_id)
    table_id = override_values.get("table_id", table_id)
    # [START bigquery_update_with_dml]
    load_from_newline_delimited_json(client, filepath, project_id, dataset_id, table_id)
    return update_with_dml(client, project_id, dataset_id, table_id)


# [END bigquery_update_with_dml]
