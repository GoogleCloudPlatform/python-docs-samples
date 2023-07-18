# Copyright 2020 Google LLC
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

import datetime
import uuid

import pytest

from . import copy_dataset


def temp_suffix():
    now = datetime.datetime.now()
    return f"{now.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="module")
def destination_dataset_id(bigquery_client, project_id):
    dataset_id = f"bqdts_dest_{temp_suffix()}"
    bigquery_client.create_dataset(f"{project_id}.{dataset_id}")
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="module")
def source_dataset_id(bigquery_client, project_id):
    dataset_id = f"bqdts_src_{temp_suffix()}"
    bigquery_client.create_dataset(f"{project_id}.{dataset_id}")
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


def test_copy_dataset(
    capsys,
    transfer_client,
    project_id,
    destination_dataset_id,
    source_dataset_id,
    to_delete_configs,
):
    # Use the transfer_client fixture so we know quota is attributed to the
    # correct project.
    assert transfer_client is not None

    transfer_config = copy_dataset.copy_dataset(
        {
            "destination_project_id": project_id,
            "destination_dataset_id": destination_dataset_id,
            "source_project_id": project_id,
            "source_dataset_id": source_dataset_id,
        }
    )
    to_delete_configs.append(transfer_config.name)
    out, _ = capsys.readouterr()
    assert transfer_config.name in out
