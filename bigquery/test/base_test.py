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
import json
import os
import unittest

from bigquery.test import RESOURCE_PATH


class BaseBigqueryTest(unittest.TestCase):

    def setUp(self):
        # A hack to prevent get_application_default to choose App Engine route.
        self._server_software_org = os.environ.get('SERVER_SOFTWARE')
        os.environ['SERVER_SOFTWARE'] = ''

        with open(
                os.path.join(RESOURCE_PATH, 'constants.json'),
                'r') as constants_file:

            self.constants = json.load(constants_file)

    def tearDown(self):
        os.environ['SERVER_SOFTWARE'] = self._server_software_org
