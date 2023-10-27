# Copyright 2018 Google Inc.
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

from typing import Iterator, List
import uuid

from google.cloud import bigquery
import pytest

import authorized_view_tutorial  # type: ignore


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture
def datasets_to_delete(client: bigquery.Client) -> Iterator[List[str]]:
    doomed: List[str] = []
    yield doomed
    for item in doomed:
        client.delete_dataset(item, delete_contents=True, not_found_ok=True)


def test_authorized_view_tutorial(
    client: bigquery.Client, datasets_to_delete: List[str]
) -> None:
    override_values = {
        "source_dataset_id": "github_source_data_{}".format(
            str(uuid.uuid4()).replace("-", "_")
        ),
        "shared_dataset_id": "shared_views_{}".format(
            str(uuid.uuid4()).replace("-", "_")
        ),
    }
    source_dataset_ref = "{}.{}".format(
        client.project, override_values["source_dataset_id"]
    )
    shared_dataset_ref = "{}.{}".format(
        client.project, override_values["shared_dataset_id"]
    )
    datasets_to_delete.extend(
        [override_values["source_dataset_id"], override_values["shared_dataset_id"]]
    )

    authorized_view_tutorial.run_authorized_view_tutorial(override_values)

    source_dataset = client.get_dataset(source_dataset_ref)
    shared_dataset = client.get_dataset(shared_dataset_ref)
    analyst_email = "example-analyst-group@google.com"
    analyst_entries = [
        entry
        for entry in shared_dataset.access_entries
        if entry.entity_id == analyst_email
    ]
    assert len(analyst_entries) == 1
    assert analyst_entries[0].role == "READER"

    authorized_view_entries = [
        entry for entry in source_dataset.access_entries if entry.entity_type == "view"
    ]
    expected_view_ref = {
        "projectId": client.project,
        "datasetId": override_values["shared_dataset_id"],
        "tableId": "github_analyst_view",
    }
    assert len(authorized_view_entries) == 1
    assert authorized_view_entries[0].entity_id == expected_view_ref
