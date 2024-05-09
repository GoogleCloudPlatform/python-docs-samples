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

# [START functions_http_integration_test]
import os
import uuid

from functions_framework import create_app


def test_args():
    name = str(uuid.uuid4())
    target = "hello_http"
    source = os.path.join(os.path.dirname(__file__), "main.py")
    client = create_app(target, source).test_client()
    resp = client.post("/my_path", json={"name": name})
    assert resp.status_code == 200
    expected_response = f"Hello {name}!"
    assert resp.data.decode("utf-8") == expected_response

# [END functions_http_integration_test]
