# Copyright 2018 Google Inc. All Rights Reserved.
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

from google.cloud import bigquery
from google.cloud import exceptions

import natality_tutorial


def dataset_exists(dataset, client):
    try:
        client.get_dataset(dataset)
        return True
    except exceptions.NotFound:
        return False


def test_natality_tutorial():
    client = bigquery.Client()
    dataset_ref = client.dataset('natality_regression')
    if dataset_exists(dataset_ref, client):
        raise AssertionError

    natality_tutorial.run_natality_tutorial()

    if not dataset_exists(dataset_ref, client):
        raise AssertionError

    table = client.get_table(
        bigquery.Table(dataset_ref.table('regression_input')))
    if table.num_rows <= 0:
        raise AssertionError

    client.delete_dataset(dataset_ref, delete_contents=True)
