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


def load_table_uri_firestore(table_id: str) -> None:
    orig_table_id = table_id
    # [START bigquery_load_table_gcs_firestore]
    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = "your-project.your_dataset.your_table_name"

    # TODO(developer): Set uri to the path of the kind export metadata
    uri = (
        "gs://cloud-samples-data/bigquery/us-states"
        "/2021-07-02T16:04:48_70344/all_namespaces/kind_us-states"
        "/all_namespaces_kind_us-states.export_metadata"
    )

    # TODO(developer): Set projection_fields to a list of document properties
    #                  to import. Leave unset or set to `None` for all fields.
    projection_fields = ["name", "post_abbr"]

    # [END bigquery_load_table_gcs_firestore]
    table_id = orig_table_id

    # [START bigquery_load_table_gcs_firestore]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.DATASTORE_BACKUP,
        projection_fields=projection_fields,
    )

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_firestore]
