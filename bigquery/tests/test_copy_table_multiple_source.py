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

import io
import typing

from google.cloud import bigquery

from .. import copy_table_multiple_source

if typing.TYPE_CHECKING:
    import pytest


def test_copy_table_multiple_source(
    capsys: "pytest.CaptureFixture[str]",
    random_table_id: str,
    random_dataset_id: str,
    client: bigquery.Client,
) -> None:
    dataset = bigquery.Dataset(random_dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    table_data = {"table1": b"Washington,WA", "table2": b"California,CA"}
    for table_id, data in table_data.items():
        table_ref = dataset.table(table_id)
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("post_abbr", "STRING"),
            ]
        )
        body = io.BytesIO(data)
        client.load_table_from_file(
            body, table_ref, location="US", job_config=job_config
        ).result()

    table_ids = [
        "{}.table1".format(random_dataset_id),
        "{}.table2".format(random_dataset_id),
    ]

    copy_table_multiple_source.copy_table_multiple_source(random_table_id, table_ids)
    dest_table = client.get_table(random_table_id)
    out, err = capsys.readouterr()
    assert (
        "The tables {} have been appended to {}".format(table_ids, random_table_id)
        in out
    )
    assert dest_table.num_rows > 0
