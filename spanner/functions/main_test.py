# Copyright 2018 Google LLC
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

from unittest.mock import MagicMock

from google.cloud import spanner

spanner.Client = MagicMock()


def test_main():
    import main
    snapshot_mock = main.client.instance().database().snapshot().__enter__()
    snapshot_mock.execute_sql.return_value = [('SingerID', 'AlbumID', 'Album')]

    response = main.spanner_read_data(None)

    assert 'SingerID' in response
    assert 'AlbumID' in response
    assert 'Album' in response
