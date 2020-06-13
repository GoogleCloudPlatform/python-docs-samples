# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import uuid

from google.cloud import bigtable
import pytest
from requests import Request

import main

PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
BIGTABLE_INSTANCE = os.environ['BIGTABLE_INSTANCE']
TABLE_ID_PREFIX = 'mobile-time-series-{}'


@pytest.fixture(scope="module", autouse=True)
def table_id():
    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)

    table_id = TABLE_ID_PREFIX.format(str(uuid.uuid4())[:16])
    table = instance.table(table_id)
    if table.exists():
        table.delete()

    table.create(column_families={'stats_summary': None})

    timestamp = datetime.datetime(2019, 5, 1)
    rows = [
        table.direct_row("phone#4c410523#20190501"),
        table.direct_row("phone#4c410523#20190502")
    ]

    rows[0].set_cell("stats_summary", "os_build", "PQ2A.190405.003", timestamp)
    rows[1].set_cell("stats_summary", "os_build", "PQ2A.190405.004", timestamp)

    table.mutate_rows(rows)

    yield table_id

    table.delete()


def test_main(table_id):
    request = Request('GET', headers={
      'instance_id': BIGTABLE_INSTANCE,
      'table_id': table_id
    })

    response = main.bigtable_read_data(request)

    assert """Rowkey: phone#4c410523#20190501, os_build: PQ2A.190405.003
Rowkey: phone#4c410523#20190502, os_build: PQ2A.190405.004""" in response
