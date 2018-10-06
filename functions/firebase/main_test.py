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

from mock import MagicMock, patch

import main


class Context(object):
    pass


def test_rtdb(capsys):
    data_id = str(uuid.uuid4())
    resource_id = str(uuid.uuid4())

    data = {
        'admin': True,
        'delta': {'id': data_id}
    }

    context = Context()
    context.resource = resource_id

    main.hello_rtdb(data, context)

    out, _ = capsys.readouterr()

    assert ('Function triggered by change to: %s' % resource_id) in out
    assert 'Admin?: True' in out
    assert data_id in out


def test_firestore(capsys):
    resource_id = str(uuid.uuid4())

    context = Context()
    context.resource = resource_id

    data = {
        'oldValue': {'uuid': str(uuid.uuid4())},
        'value': {'uuid': str(uuid.uuid4())}
    }

    main.hello_firestore(data, context)

    out, _ = capsys.readouterr()

    assert ('Function triggered by change to: %s' % resource_id) in out
    assert json.dumps(data['oldValue']) in out
    assert json.dumps(data['value']) in out


def test_auth(capsys):
    user_id = str(uuid.uuid4())
    date_string = datetime.now().isoformat()
    email_string = '%s@%s.com' % (uuid.uuid4(), uuid.uuid4())

    data = {
        'uid': user_id,
        'metadata': {'createdAt': date_string},
        'email': email_string
    }

    main.hello_auth(data, None)

    out, _ = capsys.readouterr()

    assert user_id in out
    assert date_string in out
    assert email_string in out


@patch('main.client')
def test_make_upper_case(firestore_mock, capsys):

    firestore_mock.collection = MagicMock(return_value=firestore_mock)
    firestore_mock.document = MagicMock(return_value=firestore_mock)
    firestore_mock.set = MagicMock(return_value=firestore_mock)

    user_id = str(uuid.uuid4())
    date_string = datetime.now().isoformat()
    email_string = '%s@%s.com' % (uuid.uuid4(), uuid.uuid4())

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
