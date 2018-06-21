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

from google.cloud import bigquery
import pytest

import authorized_view_tutorial


@pytest.fixture(scope='module')
def client():
    return bigquery.Client()


@pytest.fixture
def to_delete(client):
    doomed = []
    yield doomed
    for item in doomed:
        if isinstance(item, (bigquery.Dataset, bigquery.DatasetReference)):
            client.delete_dataset(item, delete_contents=True)
        elif isinstance(item, (bigquery.Table, bigquery.TableReference)):
            client.delete_table(item)
        else:
            item.delete()


def test_authorized_view_tutorial(client, to_delete):
    source_dataset, shared_dataset = (
        authorized_view_tutorial.run_authorized_view_tutorial())
    to_delete.extend([source_dataset, shared_dataset])

    analyst_email = 'example-analyst-group@google.com'
    analyst_entries = [entry for entry in shared_dataset.access_entries
                       if entry.entity_id == analyst_email]
    assert len(analyst_entries) == 1
    assert analyst_entries[0].role == 'READER'

    authorized_view_entries = [entry for entry in source_dataset.access_entries
                               if entry.entity_type == 'view']
    expected_view_ref = {
        'projectId': client.project,
        'datasetId': 'shared_views',
        'tableId': 'github_analyst_view',
    }
    assert len(authorized_view_entries) == 1
    assert authorized_view_entries[0].entity_id == expected_view_ref
