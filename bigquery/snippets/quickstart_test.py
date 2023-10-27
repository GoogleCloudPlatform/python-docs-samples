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

from typing import Iterator, List
import uuid

from google.cloud import bigquery
import pytest

import quickstart  # type: ignore

# Must match the dataset listed in quickstart.py (there's no easy way to
# extract this).
DATASET_ID = "my_new_dataset"


@pytest.fixture(scope="module")
def client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture
def datasets_to_delete(client: bigquery.Client) -> Iterator[List[str]]:
    doomed: List[str] = []
    yield doomed
    for item in doomed:
        client.delete_dataset(item, delete_contents=True)


def test_quickstart(
    capsys: "pytest.CaptureFixture[str]",
    client: bigquery.Client,
    datasets_to_delete: List[str],
) -> None:
    override_values = {
        "dataset_id": "my_new_dataset_{}".format(str(uuid.uuid4()).replace("-", "_")),
    }
    datasets_to_delete.append(override_values["dataset_id"])

    quickstart.run_quickstart(override_values)
    out, _ = capsys.readouterr()
    assert override_values["dataset_id"] in out
