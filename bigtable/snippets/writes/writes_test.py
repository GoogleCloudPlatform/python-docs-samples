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

import backoff
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import bigtable

from .write_batch import write_batch
from .write_conditionally import write_conditional
from .write_increment import write_increment
from .write_simple import write_simple

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_INSTANCE = os.environ['BIGTABLE_INSTANCE']
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

    # `row.commit()` sometimes ends up with DeadlineExceeded, so now
    # we put retries with a hard deadline.
    @backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=60)
    def _write_simple():
        write_simple(PROJECT, BIGTABLE_INSTANCE, table_id)

    _write_simple()
    out, _ = capsys.readouterr()
    assert 'Successfully wrote row' in out

    @backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=60)
    def _write_increment():
        write_increment(PROJECT, BIGTABLE_INSTANCE, table_id)

    _write_increment()
    out, _ = capsys.readouterr()
    assert 'Successfully updated row' in out

    @backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=60)
    def _write_conditional():
        write_conditional(PROJECT, BIGTABLE_INSTANCE, table_id)

    _write_conditional()
    out, _ = capsys.readouterr()
    assert 'Successfully updated row\'s os_name' in out

    @backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=60)
    def _write_batch():
        write_batch(PROJECT, BIGTABLE_INSTANCE, table_id)

    _write_batch()
    out, _ = capsys.readouterr()
    assert 'Successfully wrote 2 rows' in out
