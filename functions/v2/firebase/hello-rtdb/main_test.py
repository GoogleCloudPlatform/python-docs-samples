# Copyright 2023 Google LLC
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

import json

from cloudevents.http import CloudEvent

import main


def test_hello_rtdb(capsys):
    attributes = {
        "id": "5e9f24a",
        "type": "google.firebase.database.ref.v1.written",
        "source": "this is a test source",
    }

    data = {"data": {"original": "hello"}, "delta": {"original": "HELLO"}}
    cloud_event = CloudEvent(attributes, data)

    # Calling the function with the mocked cloud event
    main.hello_rtdb(cloud_event)

    out, _ = capsys.readouterr()

    assert "Function triggered by change to: " in out
    assert attributes["source"] in out
    assert "\nData:" in out
    assert json.dumps(data["data"]) in out
    assert "\nDelta:" in out
    assert json.dumps(data["delta"]) in out
