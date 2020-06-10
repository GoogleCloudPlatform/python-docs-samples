# Copyright 2020 Google LLC
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

# This script is a helper function to the Dataflow Template Operator Tutorial.
# It helps the user set up a BigQuery dataset and table that is needed
# for the tutorial.

import os
import uuid

from google.cloud import bigquery

from . import dataflowtemplateoperator_create_dataset_and_table_helper as helper

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

client = bigquery.Client()

dataset_UUID = str(uuid.uuid4()).split("-")[0]

expected_schema = [
    bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
    bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE"),
]


def test_creation():
    try:
        dataset, table = helper.create_dataset_and_table(PROJECT_ID, "US", dataset_UUID)

        assert table.table_id == "average_weather"
        assert dataset.dataset_id == dataset_UUID
        assert table.schema == expected_schema

    finally:

        client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)
        client.delete_table(table, not_found_ok=True)
