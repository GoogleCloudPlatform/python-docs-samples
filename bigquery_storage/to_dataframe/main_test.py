# Copyright 2019 Google LLC
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

import uuid

from google.cloud import bigquery
import pytest

from . import main


@pytest.fixture
def temporary_dataset():
    client = bigquery.Client()
    dataset_id = "bqstorage_to_dataset_{}".format(uuid.uuid4().hex)
    dataset_ref = client.dataset(dataset_id)
    client.create_dataset(dataset_ref)
    yield dataset_id
    client.delete_dataset(dataset_id, delete_contents=True)


def test_main(capsys, temporary_dataset):
    main.main(dataset_id=temporary_dataset)
    out, _ = capsys.readouterr()
    assert "country_name" in out
    assert "stackoverflow" in out
    assert "species_common_name" in out
