# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import sys
import unittest

from monitoring.samples import auth


class TestListObjects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not hasattr(sys.stdout, 'getvalue'):
            raise unittest.SkipTest('Test must be in buffered mode to run.')

    def test_main(self):
        auth.main('bigquery-devrel-samples')
        output = sys.stdout.getvalue().strip()
        self.assertRegexpMatches(
            output, re.compile(r'Timeseries.list raw response:\s*'
                               r'{\s*"kind": "[^"]+",'
                               r'\s*"oldest": *"[0-9]+', re.S))


if __name__ == '__main__':
    unittest.main()
