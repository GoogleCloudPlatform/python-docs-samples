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
import unittest

import list_logs
import testing


class TestListLogs(testing.CloudTest):

    def test_main(self):
        with testing.capture_stdout() as stdout:
            list_logs.main(self.config.GCLOUD_PROJECT)

        output = stdout.getvalue().strip()

        self.assertRegexpMatches(
            output, re.compile(r'.*', re.S))


if __name__ == '__main__':
    unittest.main()
