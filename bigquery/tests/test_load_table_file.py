# Copyright 2020 Google LLC
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

import os

from google.cloud import bigquery

from .. import load_table_file


def test_load_table_file(capsys, random_table_id, client):

    samples_test_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(
        samples_test_dir, "..", "..", "tests", "data", "people.csv"
    )
    table = load_table_file.load_table_file(file_path, random_table_id)

    out, _ = capsys.readouterr()
    assert "Loaded 2 rows and 2 columns" in out

    rows = list(client.list_rows(table))  # Make an API request.
    assert len(rows) == 2
    # Order is not preserved, so compare individually
    row1 = bigquery.Row(("Wylma Phlyntstone", 29), {"full_name": 0, "age": 1})
    assert row1 in rows
    row2 = bigquery.Row(("Phred Phlyntstone", 32), {"full_name": 0, "age": 1})
    assert row2 in rows
