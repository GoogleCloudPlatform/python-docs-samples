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

def remove_authz_views(client, dataset_ref):
    try:
        ds = client.get_dataset(dataset_ref)
        ds.access_entries = [entry for entry in ds.access_entries
                                if entry.entity_type != 'view']
        client.update_dataset(ds, ['access_entries'])
    except:
        pass

def test_authorized_view_tutorial(client):
    source_dataset_ref = client.dataset('github_source_data')
    shared_dataset_ref = client.dataset('shared_views')

    remove_authz_views(client, source_dataset_ref)
    authorized_view_tutorial.run_authorized_view_tutorial()

    source_dataset = client.get_dataset(source_dataset_ref)
    shared_dataset = client.get_dataset(shared_dataset_ref)
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

    # Remove the modification on exit
    remove_authz_views(client, source_dataset_ref)