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

# [START functions_pubsub_unit_test]
import base64

import main


def test_print_hello_world(capsys):
    data = {}

    # Call tested function
    main.hello_pubsub(data, None)
    out, err = capsys.readouterr()
    assert out == 'Hello World!\n'


def test_print_name(capsys):
    name = 'test'
    data = {'data': base64.b64encode(name.encode())}

    # Call tested function
    main.hello_pubsub(data, None)
    out, err = capsys.readouterr()
    assert out == 'Hello {}!\n'.format(name)
# [END functions_pubsub_unit_test]
