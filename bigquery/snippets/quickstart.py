#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

from typing import Dict, Optional


def run_quickstart(override_values: Optional[Dict[str, str]] = None) -> None:
    if override_values is None:
        override_values = {}

    # [START bigquery_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import bigquery

    # Instantiates a client
    bigquery_client = bigquery.Client()

    # The name for the new dataset
    dataset_id = "my_new_dataset"

    # [END bigquery_quickstart]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    dataset_id = override_values.get("dataset_id", dataset_id)
    # [START bigquery_quickstart]

    # Prepares a reference to the new dataset
    dataset_id_full = "{}.{}".format(bigquery_client.project, dataset_id)
    dataset = bigquery.Dataset(dataset_id_full)

    # Creates the new dataset
    dataset = bigquery_client.create_dataset(dataset)

    print("Dataset {} created.".format(dataset.dataset_id))
    # [END bigquery_quickstart]


if __name__ == "__main__":
    run_quickstart()
