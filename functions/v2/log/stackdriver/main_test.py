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

import base64
from collections import UserDict
import json

import main


def test_process_log_entry(capsys):
    inner_json = {
        "protoPayload": {
            "methodName": "method",
            "resourceName": "resource",
            "authenticationInfo": {"principalEmail": "me@example.com"},
        }
    }
    event = UserDict(data={})
    event.data = {
        "message": {"data": base64.b64encode(json.dumps(inner_json).encode())}
    }

    main.process_log_entry(event)

    out, _ = capsys.readouterr()
    assert "Method: method" in out
    assert "Resource: resource" in out
    assert "Initiator: me@example.com" in out
