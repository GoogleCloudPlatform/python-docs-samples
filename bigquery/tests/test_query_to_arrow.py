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

import pyarrow

from .. import query_to_arrow


def test_query_to_arrow(capsys, client):

    arrow_table = query_to_arrow.query_to_arrow(client)
    out, err = capsys.readouterr()
    assert "Downloaded 8 rows, 2 columns." in out

    arrow_schema = arrow_table.schema
    assert arrow_schema.names == ["race", "participant"]
    assert pyarrow.types.is_string(arrow_schema.types[0])
    assert pyarrow.types.is_struct(arrow_schema.types[1])
