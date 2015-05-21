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
#
"""
Common testing utilities between samples
"""

import json
import os
import unittest


BUCKET_NAME_ENV = 'TEST_BUCKET_NAME'
PROJECT_ID_ENV = 'TEST_PROJECT_ID'
RESOURCE_PATH = os.path.join(os.getcwd(), 'resources')


class CloudBaseTest(unittest.TestCase):

    def setUp(self):
        # A hack to prevent get_application_default from going GAE route.
        self._server_software_org = os.environ.get('SERVER_SOFTWARE')
        os.environ['SERVER_SOFTWARE'] = ''

        # Constants from environment
        test_bucket_name = os.environ.get(BUCKET_NAME_ENV, '')
        test_project_id = os.environ.get(PROJECT_ID_ENV, '')
        if not test_project_id or not test_bucket_name:
            raise Exception('You need to define an env var "%s" and "%s" to '
                            'run the test.'
                            % (PROJECT_ID_ENV, BUCKET_NAME_ENV))

        # Constants from resources/constants.json
        with open(
                os.path.join(RESOURCE_PATH, 'constants.json'),
                'r') as constants_file:

            self.constants = json.load(constants_file)
        self.constants['projectId'] = test_project_id
        self.constants['bucketName'] = test_bucket_name
        self.constants['cloudStorageInputURI'] = (
            self.constants['cloudStorageInputURI'] % test_bucket_name)
        self.constants['cloudStorageOutputURI'] = (
            self.constants['cloudStorageOutputURI'] % test_bucket_name)

    def tearDown(self):
        os.environ['SERVER_SOFTWARE'] = self._server_software_org
