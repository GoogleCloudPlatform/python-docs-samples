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

from collections import UserDict
from datetime import datetime
import json
import uuid

from unittest.mock import MagicMock, patch

import main


class Context:
    pass


def test_rtdb(capsys):
    data = {
        'admin': True,
        'delta': {'id': 'my-data'}
    }

    context = Context()
    context.resource = 'my-resource'

    main.hello_rtdb(data, context)

    out, _ = capsys.readouterr()

    assert 'Function triggered by change to: my-resource' in out
    assert 'Admin?: True' in out
    assert 'my-data' in out


def test_firestore(capsys):
    context = Context()
    context.resource = 'my-resource'

    data = {
        'oldValue': {'a': 1},
        'value': {'b': 2}
    }

    main.hello_firestore(data, context)

    out, _ = capsys.readouterr()

    assert 'Function triggered by change to: my-resource' in out
    assert json.dumps(data['oldValue']) in out
    assert json.dumps(data['value']) in out


def test_auth(capsys):
    date_string = datetime.now().isoformat()

    data = {
        'uid': 'my-user',
        'metadata': {'createdAt': date_string},
        'email': 'me@example.com'
    }

    main.hello_auth(data, None)

    out, _ = capsys.readouterr()

    assert 'Function triggered by creation/deletion of user: my-user' in out
    assert date_string in out
    assert 'Email: me@example.com' in out


@patch('main.client')
def test_make_upper_case(firestore_mock, capsys):

    firestore_mock.collection = MagicMock(return_value=firestore_mock)
    firestore_mock.document = MagicMock(return_value=firestore_mock)
    firestore_mock.set = MagicMock(return_value=firestore_mock)

    user_id = str(uuid.uuid4())
    date_string = datetime.now().isoformat()
    email_string = '{}@{}.com'.format(uuid.uuid4(), uuid.uuid4())

    data = {
        'uid': user_id,
        'metadata': {'createdAt': date_string},
        'email': email_string,
        'value': {
            'fields': {
                'original': {
                    'stringValue': 'foobar'
                }
            }
        }
    }

    context = UserDict()
    context.resource = '/documents/some_collection/path/some/path'

    main.make_upper_case(data, context)

    out, _ = capsys.readouterr()

    assert 'Replacing value: foobar --> FOOBAR' in out
    firestore_mock.collection.assert_called_with('some_collection')
    firestore_mock.document.assert_called_with('path/some/path')
    firestore_mock.set.assert_called_with({'original': 'FOOBAR'})


@patch('main.client')
def test_make_upper_case_ignores_already_uppercased(firestore_mock, capsys):

    firestore_mock.collection = MagicMock(return_value=firestore_mock)
    firestore_mock.document = MagicMock(return_value=firestore_mock)
    firestore_mock.set = MagicMock(return_value=firestore_mock)

    user_id = str(uuid.uuid4())
    date_string = datetime.now().isoformat()
    email_string = '{}@{}.com'.format(uuid.uuid4(), uuid.uuid4())

    data = {
        'uid': user_id,
        'metadata': {'createdAt': date_string},
        'email': email_string,
        'value': {
            'fields': {
                'original': {
                    'stringValue': 'FOOBAR'
                }
            }
        }
    }

    context = UserDict()
    context.resource = '/documents/some_collection/path/some/path'

    main.make_upper_case(data, context)

    out, _ = capsys.readouterr()

    assert 'Value is already upper-case.' in out
    firestore_mock.set.assert_not_called()


def test_analytics(capsys):
    timestamp = int(datetime.utcnow().timestamp())

    data = {
        'eventDim': [{
            'name': 'my-event',
            'timestampMicros': f'{str(timestamp)}000000'
        }],
        'userDim': {
            'deviceInfo': {
                'deviceModel': 'Pixel'
            },
            'geoInfo': {
                'city': 'London',
                'country': 'UK'
            }
        }
    }

    context = Context()
    context.resource = 'my-resource'

    main.hello_analytics(data, context)

    out, _ = capsys.readouterr()

    assert 'Function triggered by the following event: my-resource' in out
    assert f'Timestamp: {datetime.utcfromtimestamp(timestamp)}' in out
    assert 'Name: my-event' in out
    assert 'Device Model: Pixel' in out
    assert 'Location: London, UK' in out


def test_remote_config(capsys):
    data = {
        'updateOrigin': 'CONSOLE',
        'updateType': 'INCREMENTAL_UPDATE',
        'versionNumber': '1'
    }
    context = Context()

    main.hello_remote_config(data, context)

    out, _ = capsys.readouterr()

    assert 'Update type: INCREMENTAL_UPDATE' in out
    assert 'Origin: CONSOLE' in out
    assert 'Version: 1' in out
