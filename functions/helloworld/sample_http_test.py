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

# [START functions_http_unit_test]
from unittest.mock import Mock

import main


def test_print_name():
    name = 'test'
    data = {'name': name}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    assert main.hello_http(req) == f'Hello {name}!'


def test_print_hello_world():
    data = {}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    assert main.hello_http(req) == 'Hello World!'
# [END functions_http_unit_test]
