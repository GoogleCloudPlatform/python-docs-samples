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

import base64
import os

from unittest.mock import MagicMock

import main


FUNCTIONS_TOPIC = os.getenv("FUNCTIONS_TOPIC")


def test_functions_pubsub_publish_should_fail_without_params():
    request = MagicMock()
    request.get_json.return_value = {}
    response = main.publish(request)

    assert 'Missing "topic" and/or "message" parameter.' in response


def test_functions_pubsub_publish_should_publish_message():
    request = MagicMock()
    request.get_json.return_value = {
        "topic": FUNCTIONS_TOPIC, "message": "my_message"
    }

    response = main.publish(request)

    assert response == "Message published."


def test_functions_pubsub_subscribe_should_print_message(capsys):
    pubsub_message = {"data": base64.b64encode(b"Hello, world!")}

    main.subscribe(pubsub_message, None)

    out, _ = capsys.readouterr()
    assert "Hello, world!" in out
