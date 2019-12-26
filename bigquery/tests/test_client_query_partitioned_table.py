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

from .. import client_load_partitioned_table
from .. import client_query_partitioned_table


def test_client_query_partitioned_table(capsys, client, random_table_id):

    client_load_partitioned_table.client_load_partitioned_table(client, random_table_id)
    client_query_partitioned_table.client_query_partitioned_table(
        client, random_table_id
    )
    out, err = capsys.readouterr()
    assert "29 states were admitted to the US in the 1800s" in out
