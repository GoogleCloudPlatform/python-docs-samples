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

from nose.plugins.skip import SkipTest
from testing import CloudTest

from . import main


class ExtendingRuntimeTest(CloudTest):

    def test_index(self):
        if not os.path.exists('/usr/games/fortune'):
            raise SkipTest(
                'Extending runtime test will only execute if fortune is'
                'installed')

        main.app.testing = True
        client = main.app.test_client()

        r = client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.data))
