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

# [START functions_storage_unit_test]
from unittest import mock

import main


def test_print(capsys):
    name = 'test'
    event = {
        'bucket': 'some-bucket',
        'name': name,
        'metageneration': 'some-metageneration',
        'timeCreated': '0',
        'updated': '0'
    }

    context = mock.MagicMock()
    context.event_id = 'some-id'
    context.event_type = 'gcs-event'

    # Call tested function
    main.hello_gcs(event, context)
    out, err = capsys.readouterr()
    assert f'File: {name}\n' in out
# [END functions_storage_unit_test]
