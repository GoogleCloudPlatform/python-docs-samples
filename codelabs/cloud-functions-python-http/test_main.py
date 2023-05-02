# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import unittest.mock

import main


class TestHello(unittest.TestCase):
    def test_hello_world(self):
        request = unittest.mock.Mock()

        response = main.hello_world(request)
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "Hello World! 👋"

    def test_hello_name_no_name(self):
        request = unittest.mock.Mock(args={})

        response = main.hello_name(request)
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "Hello World! 🚀"

    def test_hello_name_with_name(self):
        name = "FirstName LastName"
        request = unittest.mock.Mock(args={"name": name})

        response = main.hello_name(request)
        assert response.status_code == 200
        assert response.get_data(as_text=True) == f"Hello {name}! 🚀"
