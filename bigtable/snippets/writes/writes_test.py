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
import uuid
import pytest

from google.cloud import bigtable

from .write_batch import write_batch
from .write_conditionally import write_conditional
from .write_increment import write_increment
from .write_simple import write_simple

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_INSTANCE = os.environ['BIGTABLE_CLUSTER']
TABLE_ID_PREFIX = 'mobile-time-series-{}'


@pytest.fixture
def bigtable_client():
    return bigtable.Client(project=PROJECT, admin=True)


@pytest.fixture
def bigtable_instance(bigtable_client):
    return bigtable_client.instance(BIGTABLE_INSTANCE)


@pytest.fixture
def table_id(bigtable_instance):
    table_id = TABLE_ID_PREFIX.format(str(uuid.uuid4())[:16])
    table = bigtable_instance.table(table_id)
    if table.exists():
        table.delete()

    column_family_id = 'stats_summary'
    column_families = {column_family_id: None}
    table.create(column_families=column_families)

    yield table_id

    table.delete()


def test_writes(capsys, table_id):
    write_simple(PROJECT, BIGTABLE_INSTANCE, table_id)

    out, _ = capsys.readouterr()
    assert 'Successfully wrote row' in out

    write_increment(PROJECT, BIGTABLE_INSTANCE, table_id)

    out, _ = capsys.readouterr()
    assert 'Successfully updated row' in out

    write_conditional(PROJECT, BIGTABLE_INSTANCE, table_id)

    out, _ = capsys.readouterr()
    assert 'Successfully updated row\'s os_name' in out

    write_batch(PROJECT, BIGTABLE_INSTANCE, table_id)

    out, _ = capsys.readouterr()
    assert 'Successfully wrote 2 rows' in out
