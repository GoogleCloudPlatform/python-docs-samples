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

from unittest.case import SkipTest

from testing import CloudTest

from . import main


class MemcacheTest(CloudTest):

    def test_index(self):
        main.memcache_client.set('counter', 0)

        if main.memcache_client.get('counter') is None:
            raise SkipTest('Memcache is unavailable.')

        main.app.testing = True
        client = main.app.test_client()

        r = client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('1' in r.data.decode('utf-8'))

        r = client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('2' in r.data.decode('utf-8'))
