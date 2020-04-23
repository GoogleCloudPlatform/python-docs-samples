# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock
from unittest.mock import MagicMock

from google.cloud import bigtable

bigtable.Client = MagicMock()


def test_main():
    import main

    bigtable_mock = main.table.read_rows.return_value = [{
      "row_key": "phone#1234",
      "stats_summary": {
        "os_build".encode("utf-8"): [
          {"value": "a"}
        ]
      }
    }]

    response = main.bigtable_read_data(None)

    assert 'SingerID' in response
    assert 'AlbumID' in response
    assert 'Album' in response
