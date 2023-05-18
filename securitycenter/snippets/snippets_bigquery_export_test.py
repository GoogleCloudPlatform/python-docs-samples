#!/usr/bin/env python
#
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


# TODO(developer): Replace these variables before running the sample.
import os
import re
import uuid

from _pytest.capture import CaptureFixture
import backoff
from google.api_core.exceptions import ServiceUnavailable
import pytest

import snippets_bigquery_export

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
BIGQUERY_DATASET_ID = f"sampledataset{str(uuid.uuid4()).split('-')[0]}"


@pytest.fixture(scope="module")
def bigquery_export_id():
    bigquery_export_id = f"default-{str(uuid.uuid4()).split('-')[0]}"

    create_bigquery_dataset(BIGQUERY_DATASET_ID)
    export_filter = 'severity="LOW" OR severity="MEDIUM"'
    snippets_bigquery_export.create_bigquery_export(
        f"projects/{PROJECT_ID}", export_filter, BIGQUERY_DATASET_ID, bigquery_export_id
    )

    yield bigquery_export_id

    snippets_bigquery_export.delete_bigquery_export(
        f"projects/{PROJECT_ID}", bigquery_export_id
    )
    delete_bigquery_dataset(BIGQUERY_DATASET_ID)


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=3)
def create_bigquery_dataset(dataset_id: str):
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()

    dataset_id_full = f"{PROJECT_ID}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_id_full)

    dataset = bigquery_client.create_dataset(dataset)
    print(f"Dataset {dataset.dataset_id} created.")


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=3)
def delete_bigquery_dataset(dataset_id: str):
    from google.cloud import bigquery

    bigquery_client = bigquery.Client()
    bigquery_client.delete_dataset(dataset_id)
    print(f"Dataset {dataset_id} deleted.")


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=3)
def test_get_bigquery_export(capsys: CaptureFixture, bigquery_export_id: str):
    snippets_bigquery_export.get_bigquery_export(
        f"projects/{PROJECT_ID}", bigquery_export_id
    )
    out, _ = capsys.readouterr()
    assert re.search(
        "Retrieved the BigQuery export",
        out,
    )
    assert re.search(f"bigQueryExports/{bigquery_export_id}", out)


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=3)
def test_list_bigquery_exports(capsys: CaptureFixture, bigquery_export_id: str):
    snippets_bigquery_export.list_bigquery_exports(f"projects/{PROJECT_ID}")
    out, _ = capsys.readouterr()
    assert re.search("Listing BigQuery exports:", out)
    assert re.search(bigquery_export_id, out)


@backoff.on_exception(backoff.expo, ServiceUnavailable, max_tries=3)
def test_update_bigquery_exports(capsys: CaptureFixture, bigquery_export_id: str):
    export_filter = 'severity="MEDIUM"'
    snippets_bigquery_export.update_bigquery_export(
        f"projects/{PROJECT_ID}", export_filter, bigquery_export_id
    )
    out, _ = capsys.readouterr()
    assert re.search("BigQueryExport updated successfully!", out)
