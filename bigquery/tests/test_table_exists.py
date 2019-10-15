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


from google.cloud import bigquery

from .. import table_exists


def test_table_exists(capsys, client, random_table_id):

    table_exists.table_exists(client, random_table_id)
    out, err = capsys.readouterr()
    assert "Table {} is not found.".format(random_table_id) in out
    table = bigquery.Table(random_table_id)
    table = client.create_table(table)
    table_exists.table_exists(client, random_table_id)
    out, err = capsys.readouterr()
    assert "Table {} already exists.".format(random_table_id) in out
