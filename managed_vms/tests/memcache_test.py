# Copyright 2015 Google Inc. All Rights Reserved.
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

import os

import requests

from .runserver import RunServerTestCase


class MemcacheTest(RunServerTestCase):
    application_path = os.path.join(
        os.path.dirname(__file__), '..', 'memcache')

    def test_index(self):
        r = requests.get(self.server_url)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Value is' in r.text)
