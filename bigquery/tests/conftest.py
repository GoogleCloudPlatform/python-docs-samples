# Copyright 2019 Google LLC
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

import datetime
import uuid

import pytest

from google.cloud import bigquery


@pytest.fixture(scope="module")
def client():
    return bigquery.Client()


@pytest.fixture
def dataset_id(client):
    now = datetime.datetime.now()
    dataset_id = "python_samples_{}_{}".format(
        now.strftime("%Y%m%d%H%M%S"), uuid.uuid4().hex[:8]
    )
    dataset = client.create_dataset(dataset_id)
    yield "{}.{}".format(dataset.project, dataset.dataset_id)
    client.delete_dataset(dataset, delete_contents=True)


@pytest.fixture
def model_id(client, dataset_id):
    model_id = "{}.{}".format(dataset_id, uuid.uuid4().hex)

    # The only way to create a model resource is via SQL.
    # Use a very small dataset (2 points), to train a model quickly.
    sql = """
    CREATE MODEL `{}`
    OPTIONS (
        model_type='linear_reg',
        max_iteration=1,
        learn_rate=0.4,
        learn_rate_strategy='constant'
    ) AS (
        SELECT 'a' AS f1, 2.0 AS label
        UNION ALL
        SELECT 'b' AS f1, 3.8 AS label
    )
    """.format(
        model_id
    )

    client.query(sql).result()
    return model_id
