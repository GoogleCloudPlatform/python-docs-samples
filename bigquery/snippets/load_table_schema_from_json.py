# Copyright 2022 Google LLC
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

import pathlib


def load_table(table_id: str) -> None:
    orig_uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    orig_table_id = table_id
    current_directory = pathlib.Path(__file__).parent
    orig_schema_path = str(current_directory / "schema_us_states.json")
    # [START bigquery_schema_file_load]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change uri variable to the path of your data file.
    uri = "gs://your-bucket/path/to/your-file.csv"
    # TODO(dev): Change table_id to the full name of the table you want to create.
    table_id = "your-project.your_dataset.your_table"
    # TODO(dev): Change schema_path variable to the path of your schema file.
    schema_path = "path/to/schema.json"
    # [END bigquery_schema_file_load]
    uri = orig_uri
    table_id = orig_table_id
    schema_path = orig_schema_path
    # [START bigquery_schema_file_load]
    # To load a schema file use the schema_from_json method.
    schema = client.schema_from_json(schema_path)

    job_config = bigquery.LoadJobConfig(
        # To use the schema you loaded pass it into the
        # LoadJobConfig constructor.
        schema=schema,
        skip_leading_rows=1,
    )

    # Pass the job_config object to the load_table_from_file,
    # load_table_from_json, or load_table_from_uri method
    # to use the schema on a new table.
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print(f"Loaded {destination_table.num_rows} rows to {table_id}.")
    # [END bigquery_schema_file_load]
