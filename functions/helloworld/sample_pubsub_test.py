# Copyright 2019 Google LLC
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

# [START functions_pubsub_unit_test]
import base64

from unittest import mock

import main


mock_context = mock.Mock()
mock_context.event_id = '617187464135194'
mock_context.timestamp = '2019-07-15T22:09:03.761Z'
mock_context.resource = {
    'name': 'projects/my-project/topics/my-topic',
    'service': 'pubsub.googleapis.com',
    'type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
}


def test_print_hello_world(capsys):
    data = {}

    # Call tested function
    main.hello_pubsub(data, mock_context)
    out, err = capsys.readouterr()
    assert 'Hello World!' in out


def test_print_name(capsys):
    name = 'test'
    data = {'data': base64.b64encode(name.encode())}

    # Call tested function
    main.hello_pubsub(data, mock_context)
    out, err = capsys.readouterr()
    assert f'Hello {name}!\n' in out
# [END functions_pubsub_unit_test]
