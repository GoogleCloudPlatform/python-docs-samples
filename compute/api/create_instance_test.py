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

from nose.plugins.attrib import attr
import tests

from .create_instance import main


@attr('slow')
class TestComputeGettingStarted(tests.CloudBaseTest):

    def test_main(self):
        with tests.capture_stdout() as mock_stdout:
            main(
                self.project_id,
                self.bucket_name,
                'us-central1-f',
                'test-instance',
                wait=False)

        stdout = mock_stdout.getvalue()

        expected_output = re.compile(
            (r'Instances in project %s and zone us-central1-.* - test-instance'
             r'.*Deleting instance.*done..$') % self.project_id,
            re.DOTALL)
        self.assertRegexpMatches(
            stdout,
            expected_output)
