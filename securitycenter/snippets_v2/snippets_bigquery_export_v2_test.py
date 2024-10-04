#!/usr/bin/env python
#
# Copyright 2024 Google LLC
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


# TODO(developer): Replace these variables before running the sample.
import os
import uuid

import backoff
from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable
import pytest

import snippets_bigquery_export_v2

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
BIGQUERY_DATASET_ID = f"sampledataset{str(uuid.uuid4()).split('-')[0]}"
LOCATION_ID = os.getenv("GCLOUD_LOCATION", "global")


@pytest.fixture(scope="module")
def bigquery_export_id():
    bigquery_export_id = f"default-{str(uuid.uuid4()).split('-')[0]}"

    create_bigquery_dataset(BIGQUERY_DATASET_ID)
    export_filter = 'severity="LOW" OR severity="MEDIUM"'
    snippets_bigquery_export_v2.create_bigquery_export(
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}",
        export_filter,
        f"projects/{PROJECT_ID}/datasets/{BIGQUERY_DATASET_ID}",
        bigquery_export_id,
    )

    yield bigquery_export_id

    snippets_bigquery_export_v2.delete_bigquery_export(
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}", bigquery_export_id
    )
    delete_bigquery_dataset(BIGQUERY_DATASET_ID)


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def create_bigquery_dataset(dataset_id: str):
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()

    dataset_id_full = f"{PROJECT_ID}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_id_full)

    dataset = bigquery_client.create_dataset(dataset)
    print(f"Dataset {dataset.dataset_id} created.")


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def delete_bigquery_dataset(dataset_id: str):
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()
    bigquery_client.delete_dataset(dataset_id)
    print(f"Dataset {dataset_id} deleted.")


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_bigquery_export(bigquery_export_id: str):
    response = snippets_bigquery_export_v2.get_bigquery_export(
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}", bigquery_export_id
    )
    assert bigquery_export_id.split("/")[-1] == response.name.split("/")[-1]


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_bigquery_exports(bigquery_export_id: str):
    response = snippets_bigquery_export_v2.list_bigquery_exports(
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
    )
    names = []
    for bigquery_export in response:
        names.append(bigquery_export.name.split("/")[-1])
    assert bigquery_export_id in names


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_bigquery_exports(bigquery_export_id: str):
    export_filter = 'severity="MEDIUM"'
    response = snippets_bigquery_export_v2.update_bigquery_export(
        f"projects/{PROJECT_ID}/locations/{LOCATION_ID}",
        export_filter,
        bigquery_export_id,
    )
    assert bigquery_export_id.split("/")[-1] == response.name.split("/")[-1]
