# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud.firestore_v1.bulk_writer import BulkWriter
from google.cloud.firestore_v1.client import Client

import pytest

from query_filter_or import query_or_composite_filter

os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['FIRESTORE_PROJECT']
PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']


@pytest.fixture
def setup(scope="function", autouse=True):
    client = Client(project=PROJECT_ID)
    cr = client.collection('users')
    bw = client.bulk_writer()
    td = [
        {u'shortName': 'aturing', u'birthYear': 1912},
        {u'shortName': 'cbabbage', u'birthYear': 1791},
        {u'shortName': 'ghopper', u'birthYear': 1906},
        {u'shortName': 'alovelace', u'birthYear': 1815},
    ]

    for d in td:
        bw.create(cr.document(d['shortName']), {u'birthYear': d['birthYear']})

    bw.close()
 
    yield

    # Need new BulkWriter instance for deletes
    bw = client.bulk_writer()
    for d in td:
        bw.delete(cr.documents(d['shortName']))
    
    bw.close()

def test_query_or_composite_filter(capsys):
    query_or_composite_filter(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert 'aturing' in out
