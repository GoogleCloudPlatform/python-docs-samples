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

# [START functions_http_system_test]
import os
import uuid

import requests


def test_no_args():
    BASE_URL = os.getenv('BASE_URL')
    assert BASE_URL is not None

    res = requests.get(f'{BASE_URL}/hello_http')
    assert res.text == 'Hello, World!'


def test_args():
    BASE_URL = os.getenv('BASE_URL')
    assert BASE_URL is not None

    name = str(uuid.uuid4())
    res = requests.post(
      f'{BASE_URL}/hello_http',
      json={'name': name}
    )
    assert res.text == f'Hello, {name}!'
# [END functions_http_system_test]
