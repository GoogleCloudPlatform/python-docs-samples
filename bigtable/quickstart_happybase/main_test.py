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

import os

import random

import pytest
from google.cloud import bigtable
from main import main

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_INSTANCE = os.environ['BIGTABLE_INSTANCE']
TABLE_ID_FORMAT = 'quickstart-hb-test-{}'
TABLE_ID_RANGE = 10000


@pytest.fixture()
def table():
    table_id = TABLE_ID_FORMAT.format(
        random.randrange(TABLE_ID_RANGE))
    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)
    table = instance.table(table_id)
    column_family_id = 'cf1'
    column_families = {column_family_id: None}
    table.create(column_families=column_families)

    row = table.direct_row("r1")
    row.set_cell(column_family_id, "c1", "test-value")
    row.commit()

    yield table_id

    table.delete()


def test_main(capsys, table):
    table_id = table
    main(PROJECT, BIGTABLE_INSTANCE, table_id)

    out, _ = capsys.readouterr()
    assert 'Row key: r1\nData: test-value\n' in out
