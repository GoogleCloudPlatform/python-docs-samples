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

from datetime import datetime
import json

import main


class Context(object):
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
