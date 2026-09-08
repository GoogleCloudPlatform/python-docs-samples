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

import typing

from google.cloud import bigquery

from .. import update_table_require_partition_filter

if typing.TYPE_CHECKING:
    import pytest


def test_update_table_require_partition_filter(
    capsys: "pytest.CaptureFixture[str]",
    random_table_id: str,
    client: bigquery.Client,
) -> None:
    # Make a partitioned table.
    schema = [bigquery.SchemaField("transaction_timestamp", "TIMESTAMP")]
    table = bigquery.Table(random_table_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(field="transaction_timestamp")
    table = client.create_table(table)

    update_table_require_partition_filter.update_table_require_partition_filter(
        random_table_id
    )
    out, _ = capsys.readouterr()
    assert (
        "Updated table '{}' with require_partition_filter=True".format(random_table_id)
        in out
    )
