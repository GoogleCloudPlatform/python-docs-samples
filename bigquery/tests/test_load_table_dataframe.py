# Copyright 2019 Google LLC
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

import pytest

from .. import load_table_dataframe


pytest.importorskip("pandas")
pytest.importorskip("pyarrow")


def test_load_table_dataframe(capsys, client, random_table_id):
    table = load_table_dataframe.load_table_dataframe(client, random_table_id)
    out, _ = capsys.readouterr()
    assert "Loaded 4 rows and 3 columns" in out

    column_names = [field.name for field in table.schema]
    assert column_names == ["wikidata_id", "title", "release_year"]
