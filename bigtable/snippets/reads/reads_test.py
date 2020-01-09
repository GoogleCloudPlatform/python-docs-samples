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
import datetime
import os
import uuid
import pytest

from google.cloud import bigtable

PROJECT = os.environ['GCLOUD_PROJECT']
BIGTABLE_INSTANCE = os.environ['BIGTABLE_CLUSTER']
TABLE_ID_PREFIX = 'mobile-time-series-{}'


@pytest.fixture(scope="session", autouse=True)
def test_table():
    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)

    table_id = TABLE_ID_PREFIX.format(str(uuid.uuid4())[:16])
    table = instance.table(table_id)
    if table.exists():
        table.delete()

    table.create(column_families={'stats_summary': None})

    # table = instance.table(table_id)

    timestamp = datetime.datetime.utcnow()
    rows = [
        table.direct_row("phone#4c410523#20190501"),
        table.direct_row("phone#4c410523#20190502"),
        table.direct_row("phone#4c410523#20190505"),
        table.direct_row("phone#5c10102#20190501"),
        table.direct_row("phone#5c10102#20190502"),
    ]

    rows[0].set_cell("stats_summary", "connected_cell", 1, timestamp)
    rows[0].set_cell("stats_summary", "connected_wifi", 1, timestamp)
    rows[0].set_cell("stats_summary", "os_build", "PQ2A.190405.003", timestamp)
    rows[1].set_cell("stats_summary", "connected_cell", 1, timestamp)
    rows[1].set_cell("stats_summary", "connected_wifi", 1, timestamp)
    rows[1].set_cell("stats_summary", "os_build", "PQ2A.190405.004", timestamp)
    rows[2].set_cell("stats_summary", "connected_cell", 0, timestamp)
    rows[2].set_cell("stats_summary", "connected_wifi", 1, timestamp)
    rows[2].set_cell("stats_summary", "os_build", "PQ2A.190406.000", timestamp)
    rows[3].set_cell("stats_summary", "connected_cell", 1, timestamp)
    rows[3].set_cell("stats_summary", "connected_wifi", 1, timestamp)
    rows[3].set_cell("stats_summary", "os_build", "PQ2A.190401.002", timestamp)
    rows[4].set_cell("stats_summary", "connected_cell", 1, timestamp)
    rows[4].set_cell("stats_summary", "connected_wifi", 0, timestamp)
    rows[4].set_cell("stats_summary", "os_build", "PQ2A.190406.000", timestamp)

    response = table.mutate_rows(rows)
    # out, _ = capsys.readouterr()
    # assert 'Successfully wrote row' in out
    print("above")

    yield table_id

    print("below")
    # write_simple(PROJECT, BIGTABLE_INSTANCE, table_id)
    #
    # out, _ = capsys.readouterr()
    # assert 'Successfully wrote row' in out
    #
    # write_increment(PROJECT, BIGTABLE_INSTANCE, table_id)
    #
    # out, _ = capsys.readouterr()
    # assert 'Successfully updated row' in out
    #
    # write_conditional(PROJECT, BIGTABLE_INSTANCE, table_id)
    #
    # out, _ = capsys.readouterr()
    # assert 'Successfully updated row\'s os_name' in out
    #
    # write_batch(PROJECT, BIGTABLE_INSTANCE, table_id)
    #
    # out, _ = capsys.readouterr()
    # assert 'Successfully wrote 2 rows' in out

    # yield response

    # table.delete()


def test_read_simple(capsys, test_table):
    print("hi")
    assert "abc" in ""  # for demo purposes
